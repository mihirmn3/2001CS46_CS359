from threading import *
import queue
from time import *
from datetime import datetime

start_time = datetime.now()  # For calculating the program execution time

lock = Lock()  # Lock for maintaining proper printing by the threads
num_routers = 0  # number of routers

# Working:
# There is a 'shared queue' in every router, which the neighbouring routers can access and send their
# neighbouring information to. The router will then access this queue, send this connectivity information to its neighbours,
# and use it to update its graph. Finally, apply Dijkstra's algorithm to find the shortest paths in this graph, from
# this router to every other router. This is repeated everytime a new connectivity information is received.
# Thus, every router constructs the entire graph of the network and finds the shortest paths using Dijsktra's algorithm


class router:  # Every router is an instance of this class

    # Defining and initializing all the data structures
    def __init__(self, router_name, initial_routing_table):

        # Name of the router
        self.name = router_name

        # Addresses of the queues of neighbouring routers
        self.neighbour_queues = dict()

        # Graph (Adjacency matrix) maintained in the router
        self.graph = dict()

        # A list of routers whose connectivity information we know
        self.routers_visited = [self.name]

        # Current router's shared queue, in which, the neighbouring routers will put their tables
        self.shared_queue = queue.Queue()

        # Current router's routing table
        self.routing_table = dict(initial_routing_table)
        self.routing_table[self.name] = 0

        self.iteration_num = 0  # Iteration number

        # Keeps a record of entries (shortest paths) which were changed in previous iteration
        self.changed_entry = dict()

        # The neighbouring routers in the direction of the shortest path from the current router
        # to all the routers are maintained in this dictionary
        self.via_table = dict()

        # Initializing the above data structures
        for router_name in self.routing_table:
            self.via_table[router_name] = "-"
            self.changed_entry[router_name] = False
            self.graph[router_name] = dict()

        self.via_table[self.name] = self.name

    # Function to add an edge (neighbour) to the router
    def add_neighbour(self, router_name, edge_cost, router_queue):

        # Adding the neighbour, the link's cost and the neighbour's queue to the respective data structures
        self.routing_table[router_name] = edge_cost
        self.via_table[router_name] = router_name
        self.neighbour_queues[router_name] = router_queue

        self.graph[self.name][router_name] = edge_cost
        self.graph[router_name][self.name] = edge_cost

    # Function to display the routing table in proper format
    def display_routing_table(self, iteration_no, neighbour_router):

        lock.acquire()  # So, no other thread can interrupt and print in between, until the entire table has been printed

        if iteration_no == 1:
            print(f"Initial routing table of router {self.name}:")
        elif iteration_no <= num_routers:
            print(
                f"From Router {self.name} | Iteration {iteration_no-1} | Connectivity info received from Router {neighbour_router} :")
        else:
            print(f"From Router {self.name}:")

        to = "To Router"
        cst = "Cost"
        v = "Via Router"
        tmpstr = ""
        for i in range(36):
            tmpstr += "-"  # Used to add horizontal lines

        print(tmpstr)
        print(f"|{to:^11}|{cst:^9}|{v:^12}|")
        print(tmpstr)

        for router_name in self.routing_table:

            router_nm = router_name

            # Checking if the entry for this router has changed in the previous iteration.
            if self.changed_entry[router_name] == True:
                router_nm = "*"  # If yes, add a '*' at the start
                router_nm += router_name
                self.changed_entry[router_name] = False

            router_cst = self.routing_table[router_name]
            if router_cst == float("inf"):
                router_cst = "-"

            print(
                f"|{router_nm:^11}|{router_cst:^9}|{self.via_table[router_name]:^12}|")
            print(tmpstr)

        print()
        lock.release()

    # Function to add edges to the priority queue containing all the edges not yet considered
    def add_edges(self, edge_list, router_name):
        for router_nm in self.graph[router_name]:
            edge_list.put(
                [self.graph[router_name][router_nm], router_name, router_nm])

    # Dijkstra's shortest path algorithm
    def dijkstra(self):

        # Maintaining a priority queue for finding the shortest edge at every step
        edge_list = queue.PriorityQueue()

        # Keeping a track of visited routers
        visited_routers = [self.name]

        # Starting with the source node (the current router)
        self.add_edges(edge_list, self.name)

        # While loop runs until all the edges in the graph are considered
        # This is the main part of the algorithm. Finding the shortest edge among the currently considered edges,
        # and expanding to consider the edges connected to that router (if not already considered)
        while not edge_list.empty():
            smallest_edge = edge_list.get()

            edge_cost = smallest_edge[0]
            from_router = smallest_edge[1]
            to_router = smallest_edge[2]

            if to_router not in visited_routers:
                visited_routers.append(to_router)
                self.add_edges(edge_list, to_router)

            # Updating the distance in the routing table and other data structures
            tmp = self.routing_table[from_router] + edge_cost
            if self.routing_table[to_router] > tmp:
                self.routing_table[to_router] = tmp
                self.via_table[to_router] = self.via_table[from_router]
                self.changed_entry[to_router] = True

    # The function which runs in the thread, works as a running router instance
    def link_state_routing(self):

        # Fetching the name of the router
        nm = self.name

        # Creating the neighbours table (connectivity information) to send to other routers
        neighbours_table = dict()
        for router_nm in self.neighbour_queues:
            neighbours_table[router_nm] = self.routing_table[router_nm]

        # For each neighbour, put the neighbours table in its queue
        # Neighbour router will then access it and update its graph, and forward the table to its neighbours
        for router_name in self.neighbour_queues:
            self.neighbour_queues[router_name].put(
                {nm: neighbours_table, })

        # A variable to maintain which router sent its connectivity information in the last update
        prev_router = "-"

        # Iterating until the neighbouring information from all the routers have been received
        while len(self.routers_visited) < num_routers:

            # For printing only the tables which got updated in previous iteration (also the initial tables) -
            # uncomment the following line and indent the line below it
            # if routers_visited == 1 or (True in list(self.changed_entry.values())):
            self.display_routing_table(len(self.routers_visited), prev_router)

            sleep(2)  # Wait for 2 seconds (assumed to be the network delay, etc)

            # Data structures to process the received information
            router_dict = dict()
            router_name = str()
            router_neighbour_table = dict()

            # Loop until we receive new information in the queue
            while True:
                if self.shared_queue.empty():
                    continue

                # For the neighbour's info table available in the shared queue
                router_dict = self.shared_queue.get()
                router_name = list(router_dict.keys())[0]
                router_neighbour_table = router_dict[router_name]

                # If the information is not from an already considered router, break out and process it
                if router_name not in self.routers_visited:
                    break

            prev_router = router_name

            # Add the router to the visited list
            self.routers_visited.append(router_name)

            # Updating the graph using this information
            for router_nm in router_neighbour_table:
                if router_nm == router_name:
                    continue
                self.graph[router_name][router_nm] = router_neighbour_table[router_nm]
                self.graph[router_nm][router_name] = router_neighbour_table[router_nm]

            # Forwarding to the neighbouring routers
            for router_nm in self.neighbour_queues:
                self.neighbour_queues[router_nm].put(
                    {router_name: router_neighbour_table, })

            # Calling the function to update the routing table using the newly constructed graph
            self.dijkstra()

        # For printing only the tables which got updated in previous iteration -
        # uncomment the following line and indent the line below it
        # if (True in list(self.changed_entry.values())):
        self.display_routing_table(num_routers, prev_router)


cnt = 0  # Number of lines of input
routers = {}  # Addresses of all the router instances

# Opening the input file - located in the same folder as the code, and creating a list of its lines
f = open("topology.txt", "r")
lines = f.readlines()

for line in lines:

    # First line contains the number of routers
    if cnt == 0:
        num_routers = int(line)

    # Second line contains the names of the routers
    elif cnt == 1:
        names = line.split(sep=" ")
        names[-1] = names[-1][:-1]  # Ignoring the escape character at last

        tmp_table = dict()
        for name in names:
            tmp_table[name] = float('inf')

        # Creating router objects for every router, and sending a temporary initial routing table
        for name in names:
            routers[name] = router(name, tmp_table)

    # If it is not the second or first line, and also not EOF, then the line contains the information of an edge
    elif line != "EOF":

        # Splitting the line to get the information of the edge - router1 name, router2 name, the edge cost
        edge = line.split(sep=" ")
        edge[-1] = int(edge[-1])
        r1 = edge[0]
        r2 = edge[1]
        cst = edge[2]

        # Adding the edge (neighbour) information to the router objects
        routers[r1].add_neighbour(r2, cst, routers[r2].shared_queue)
        routers[r2].add_neighbour(r1, cst, routers[r1].shared_queue)

    # If End Of Line encountered, break
    elif line == "EOF":
        break

    cnt += 1

# A list containing the threads of routers
router_threads = list()

# Creating a thread for every router instance and starting it
for router_name in routers:
    thread = Thread(target=routers[router_name].link_state_routing)
    thread.start()
    router_threads.append(thread)

# Wait for all the threads to finish executing (join with the main thread)
for router_thread in router_threads:
    router_thread.join()

print("Final routing tables of each router:\n")
for router_name in routers:
    routers[router_name].display_routing_table(num_routers + 1, "")

# Displaying the total program execution time
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
