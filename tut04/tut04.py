from threading import *
import queue
from time import *
from datetime import datetime

start_time = datetime.now()  # For calculating the program execution time

lock = Lock()  # Lock for maintaining proper printing by the threads
num_routers = 0  # number of routers

# Working:
# There is a 'shared queue' in every router, which the neighbouring routers can access and send their
# routing tables to. The router will then access this queue (after all the neighbours have sent their tables)
# and update its own routing table according to the Bellman Ford equation. Further, every router is running in
# parallel in a separate thread, hence replicating the real life scenario.


class router:  # Every router is an instance of this class

    # Defining and initializing all the data structures
    def __init__(self, router_name, initial_routing_table):

        # Name of the router
        self.name = router_name

        # Addresses of the queues of neighbouring routers
        self.neighbour_queues = dict()

        # Costs of the links connecting to the neighbours
        self.neighbour_cost = dict()

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
        self.via_table[self.name] = self.name

    # Function to add an edge (neighbour) to the router
    def add_neighbour(self, router_name, edge_cost, router_queue):

        # Adding the neighbour, the link's cost and the neighbour's queue to the respective data structures
        self.routing_table[router_name] = edge_cost
        self.via_table[router_name] = router_name
        self.neighbour_cost[router_name] = edge_cost
        self.neighbour_queues[router_name] = router_queue

    # Function to display the routing table in proper format
    def display_routing_table(self, iteration_no):

        lock.acquire()  # So, no other thread can interrupt and print in between, until the entire table has been printed

        if iteration_no == 0:
            print(f"Initial routing table of router {self.name}:")
        elif iteration_no < num_routers:
            print(f"From Router {self.name} | Iteration {iteration_no} :")
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

    # The function which runs in the thread, works as a running router instance
    def distance_vector_routing(self):

        # Iterating (number of routers - 1) times (Bellman Ford)
        for ii in range(num_routers - 1):

            # For printing only the tables which got updated in previous iteration (also the initial tables) -
            # Uncomment the following line and indent the line below it
            # if ii == 0 or (True in list(self.changed_entry.values())):
            self.display_routing_table(ii)  # Printing the routing table

            sleep(2)  # Wait for 2 seconds (assumed to be the network delay, etc)

            # For each neighbour, put the routing table in its queue
            for router_name in self.neighbour_queues:
                nm = self.name

                # Creating a copy of the routing table
                tble = dict(self.routing_table)

                # Put in the neighbouring router's shared queue.
                # Neighbour router will then access it and update its own table
                self.neighbour_queues[router_name].put({nm: tble, })

            # Wait until all the neighbours have put their routing tables in the shared queue
            while len(list(self.shared_queue.queue)) != len(self.neighbour_queues):
                pass

            # For every routing table available in the shared queue (put by the neighbours)
            for i in range(len(list(self.shared_queue.queue))):

                router_dict = self.shared_queue.get()
                router_name = list(router_dict.keys())[0]
                router_table = router_dict[router_name]

                for r1_name in router_table:

                    # The shortest path from current router to r1
                    a = self.routing_table[r1_name]

                    # The shortest path from neighbour to r1
                    b = router_table[r1_name]

                    # The cost (distance) from current router to the neighbour
                    c = self.neighbour_cost[router_name]

                    # Bellman Ford equation
                    self.routing_table[r1_name] = min(b + c, a)

                    # Checking if the shortest path was updated. If yes, update the concerned data structures
                    if self.routing_table[r1_name] < a:
                        self.via_table[r1_name] = router_name
                        self.changed_entry[r1_name] = True

        # For printing only the tables which got updated in previous iteration -
        # Uncomment the following line and indent the line below it
        # if ii == 0 or (True in list(self.changed_entry.values())):
        self.display_routing_table(num_routers - 1)


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
    thread = Thread(target=routers[router_name].distance_vector_routing)
    thread.start()
    router_threads.append(thread)

# Wait for all the threads to finish executing (join with the main thread)
for router_thread in router_threads:
    router_thread.join()

print("Final routing tables of each router:\n")
for router_name in routers:
    routers[router_name].display_routing_table(num_routers)

# Displaying the total program execution time
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
