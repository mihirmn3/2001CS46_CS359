
from datetime import datetime
start_time = datetime.now()

#Help
def scorecard():
	try:
		#opening the teams file and retrieving the names of the players
		teams=open(r"teams.txt","r")
		indinnfile=open(r"india_inns2.txt","r")
		pakinnfile=open(r"pak_inns1.txt","r")
		indinn=indinnfile.readlines()
		pakinn=pakinnfile.readlines()
	
		#reading the innnings files of each team and splitting the names of batsman, bowlers, runs
		#overs, and everything using the comma delimitter
		#First done for India innings-----------------------------------------------------------------
		for i in range(0,len(indinn),1):
			indinn[i]=indinn[i].replace(" to ",",")
			temp=indinn[i].split(",")
			if (temp[0]!="\n"):
				temp2=temp[0].split(" ")
				temp3=temp2[0]+" "
				
				#We store the byes and legbyes separately so that we count them at the end when we print 
				#the extras
				
				if ((temp[2].strip()=="byes")): 
					temp[2]=temp[3]+" bye"
				if ((temp[2].strip()=="leg byes")):
					temp[2]=temp[3]+" leg bye"
				if((temp[2].strip().split(" "))[0].lower()=="out"):

					#if player is caught then the person who caught the ball is stored separately
					if((temp[2].strip().split(" "))[1].lower()=="caught"):
						add=temp[2].strip().split(" ")[3]
						if ("!" in add):

							#the type of wcket is also stored so that we check later whether the batsman
							#got out on a catch or simply got bowled or had an lbw
							#we frequently use comma delimitters to split and store information
							temp[2]="out,"+"caught,"+temp[2].strip().split(" ")[3].strip("!!")
						else:	
							temp[2]="out,"+"caught,"+temp[2].strip().split(" ")[3]+" "+temp[2].strip().split(" ")[4].strip("!!")
					elif((temp[2].strip().split(" "))[1].lower()=="bowled!!"):
						temp[2]="out,"+"bowled"
					elif((temp[2].strip().split(" "))[1].lower()=="lbw!!"):
						temp[2]="out,"+"lbw"	
						
				indinn[i]=[temp2[0],(temp[0].replace(temp3,"")).strip(),temp[1].strip(),temp[2].strip()]
		while "\n" in indinn:
			indinn.remove("\n")	
		
		#----------------------------------------------------------------------------------------------
		
		
		#same has been done for the Pakistan innings
		#-----------------------------------------------------------------------
		for i in range(0,len(pakinn),1):
			pakinn[i]=pakinn[i].replace(" to ",",")
			temp=pakinn[i].split(",")
			if (temp[0]!="\n"):
				temp2=temp[0].split(" ")
				temp3=temp2[0]+" "
				if ((temp[2].strip()=="byes")):
					temp[2]=temp[3]+" bye"
				if ((temp[2].strip()=="leg byes")):
					temp[2]=temp[3]+" leg bye"	
				if((temp[2].strip().split(" "))[0].lower()=="out"):
					if((temp[2].strip().split(" "))[1].lower()=="caught"):
						add=temp[2].strip().split(" ")[3]
						if ("!" in add):
							temp[2]="out,"+"caught,"+temp[2].strip().split(" ")[3].strip("!!")
						else:	
							temp[2]="out,"+"caught,"+temp[2].strip().split(" ")[3]+" "+temp[2].strip().split(" ")[4].strip("!!")
					elif((temp[2].strip().split(" "))[1].lower()=="bowled!!"):
						temp[2]="out,"+"bowled"
					elif((temp[2].strip().split(" "))[1].lower()=="lbw!!"):
						temp[2]="out,"+"lbw"	
					
				pakinn[i]=[temp2[0],(temp[0].replace(temp3,"")).strip(),temp[1].strip(),temp[2].strip()]		
		while "\n" in pakinn:
			pakinn.remove("\n")		
	#-------------------------------------------------------------------------------------------

		lines=teams.readlines()
		pak=[] #pak in this case
		ind=[] #india in this case
		a=""
		for i in lines:
			a=a+i
		a=a.split("\n")
		while '' in a:
			a.remove('')

		#we store the names of the players in ind[] and pak[]
		#we also remove the symbol : from the lines read from the file to avoid problems while appending the names	
		a[0]=a[0].replace(":",",")
		a[1]=a[1].replace(":",",")	
		pak=a[0].split(",")
		ind=a[1].split(",")
		del pak[0]
		del ind[0]
		for i in range(0,len(ind),1):
			ind[i]=ind[i].strip()
			pak[i]=pak[i].strip()
		#calculation of runs, balls played, fours, sixes, strike rate, extras, wickets, fall of wickets, 
		# overs and dot balls
		# we take a number of variables for all the tasks
		indruns=0
		pakruns=0
		indwickets=0
		pakwickets=0
		indbyes=0
		indlb=0
		indwides=0
		indnb=0
		indp=0
		pakbyes=0
		paklb=0
		pakwides=0
		paknb=0
		pakp=0
		indscorecard=[]
		pakscorecard=[]
		indscorecardbowlers=[]
		pakscorecardbowlers=[]
		indcumulativescore=[]
		pakcumulativescore=[]
		indlist=[]
		paklist=[]
		indbat=[]
		pakbat=[]

		# we now make a unique list of batsman who have played atleast a ball
		# we then remove recurrring names from the list
		# we do the same for both india and pakistan
		for i in range(0,len(indinn),1):
			indlist.append(indinn[i][2])
		for i in range(0,len(pakinn),1):
			paklist.append(pakinn[i][2])
		while len(indlist)!=0:
			indbat.append(indlist[0])
			yo=indlist[0]
			while yo in indlist:
				indlist.remove(yo)		
		while len(paklist)!=0:
			pakbat.append(paklist[0])
			yo=paklist[0]
			while yo in paklist:
				paklist.remove(yo)
	
		for i in range(0,len(indbat),1):
			#[runs, balls played, fours, sixes, strike rate,fall of wicket,taken by,(also append if caught)]
			indscorecard.append([0,0,0,0,0,0,0])
		for i in range(0,len(pakbat),1):
			#[runs, balls played, fours, sixes, strike rate,fall of wicket,taken by,(also append if caught)]
			pakscorecard.append([0,0,0,0,0,0,0])	
		#calculating pak batsmen scores
		#this is the normal algebraic addition of runs, with extras being counted separately
		# stats of each batsman s stores separately
		for i in pakinn:	
			for j in range(0,len(pakbat),1):
				if(i[2]==pakbat[j]):
					if	(i[3].lower() == "no run"):
						pakscorecard[j][1]+=1
					if	(i[3].lower()[0:3] == "out"):
						pakwickets+=1
						pakscorecard[j][5]=i[0]
						pakscorecard[j][6]="b "+i[1]
						if ("," in i[3]):
							if (i[3].lower().split(",")[1]=="caught"):
								pakscorecard[j].append("c "+(i[3].split(",")[2]))
								#if caught, the name of the catcher is stored separately
							elif (i[3].lower().split(",")[1]=="lbw"):
								pakscorecard[j].append("lbw")	
						pakcumulativescore.append([pakruns,pakwickets,pakbat[j],i[0]])
						pakscorecard[j][1]+=1	
					if	(i[3].lower() == "1 run"):
						pakscorecard[j][0]+=1
						pakscorecard[j][1]+=1
						pakruns+=1
					if	(i[3].lower() == "2 runs"):
						pakscorecard[j][0]+=2
						pakscorecard[j][1]+=1
						pakruns+=2
					if	(i[3].lower() == "3 runs"):
						pakscorecard[j][0]+=3
						pakscorecard[j][1]+=1
						pakruns+=3
					if	(i[3].lower() == "4 runs"):
						pakscorecard[j][0]+=4
						pakscorecard[j][1]+=1
						pakruns+=4
					if	(i[3].lower() == "1 run bye"):
						pakscorecard[j][1]+=1
						pakruns+=1
						pakbyes+=1
					if	(i[3].lower() == "2 runs bye"):
						pakscorecard[j][1]+=1
						pakruns+=2
						pakbyes+=2
					if	(i[3].lower() == "3 runs bye"):
						pakscorecard[j][1]+=1
						pakruns+=3
						pakbyes+=3
					if	(i[3].lower() == "4 runs bye"):
						pakscorecard[j][1]+=1
						pakruns+=4
						pakbyes+=4
					if	(i[3].lower() == "four bye"):
						pakscorecard[j][1]+=1
						pakruns+=4
						pakbyes+=4
					if	(i[3].lower() == "four"):
						pakscorecard[j][0]+=4
						pakscorecard[j][1]+=1
						pakscorecard[j][2]+=1
						pakruns+=4
					if	(i[3].lower() == "six"):
						pakscorecard[j][0]+=6
						pakscorecard[j][1]+=1
						pakscorecard[j][3]+=1
						pakruns+=6
					if	(i[3].lower() == "wide"):
						pakruns+=1
						pakwides+=1
					if	(i[3].lower() == "2 wides"):
						pakruns+=2
						pakwides+=2
					if	(i[3].lower() == "3 wides"):
						pakruns+=3
						pakwides+=3	
					if	(i[3].lower() == "no-ball"):
						pakruns+=1
						paknb+=1
					if(pakscorecard[j][1]==0):
						pakscorecard[j][4]=0
					else:
						hello=round(((pakscorecard[j][0]/pakscorecard[j][1])*100),2)
						pakscorecard[j][4]=hello	
			#this is the condition to get the amount of runs scored during the powerplay
			if(i[0]=="5.6"):
				pakpowerplay=pakruns			
		
		#we do the same for the indian team-------------------------------------------------------------
		for i in indinn:	
			for j in range(0,len(indbat),1):
				if(i[2]==indbat[j]):
					if	(i[3].lower() == "no run"):
						indscorecard[j][1]+=1
					if	(i[3].lower()[0:3] == "out"):
						indwickets+=1
						indscorecard[j][5]=i[0]
						indscorecard[j][6]="b "+i[1]
						if ("," in i[3]):
							if (i[3].lower().split(",")[1]=="caught"):
								indscorecard[j].append("c "+(i[3].split(",")[2]))
								#if caught, the name of the catcher is stored separately
							elif (i[3].lower().split(",")[1]=="lbw"):
								indscorecard[j].append("lbw")
						indcumulativescore.append([indruns,indwickets,indbat[j],i[0]])
						indscorecard[j][1]+=1	
					if	(i[3].lower() == "1 run"):
						indscorecard[j][0]+=1
						indscorecard[j][1]+=1
						indruns+=1
					if	(i[3].lower() == "2 runs"):
						indscorecard[j][0]+=2
						indscorecard[j][1]+=1
						indruns+=2
					if	(i[3].lower() == "3 runs"):
						indscorecard[j][0]+=3
						indscorecard[j][1]+=1
						indruns+=3
					if	(i[3].lower() == "4 runs"):
						indscorecard[j][0]+=4
						indscorecard[j][1]+=1
						indruns+=4
					if	(i[3].lower() == "1 run bye"):
						indscorecard[j][1]+=1
						indruns+=1
						indbyes+=1
					if	(i[3].lower() == "2 runs bye"):
						indscorecard[j][1]+=1
						indruns+=2
						indbyes+=2
					if	(i[3].lower() == "3 runs bye"):
						indscorecard[j][1]+=1
						indruns+=3
						indbyes+=3
					if	(i[3].lower() == "4 runs bye"):
						indscorecard[j][1]+=1
						indruns+=4
						indbyes+=4
					if	(i[3].lower() == "four bye"):
						indscorecard[j][1]+=1
						indruns+=4
						indbyes+=4
					if	(i[3].lower() == "1 run leg bye"):
						indscorecard[j][1]+=1
						indruns+=1
						indlb+=1
					if	(i[3].lower() == "2 runs leg bye"):
						indscorecard[j][1]+=1
						indruns+=2
						indlb+=2
					if	(i[3].lower() == "3 runs leg bye"):
						indscorecard[j][1]+=1
						indruns+=3
						indlb+=3
					if	(i[3].lower() == "4 runs leg bye"):
						indscorecard[j][1]+=1
						indruns+=4
						indlb+=4
					if	(i[3].lower() == "four leg bye"):
						indscorecard[j][1]+=1
						indruns+=4
						indlb+=4
					if	(i[3].lower() == "four"):
						indscorecard[j][0]+=4
						indscorecard[j][1]+=1
						indscorecard[j][2]+=1
						indruns+=4
					if	(i[3].lower() == "six"):
						indscorecard[j][0]+=6
						indscorecard[j][1]+=1
						indscorecard[j][3]+=1
						indruns+=6
					if	(i[3].lower() == "wide"):
						indruns+=1
						indwides+=1
					if	(i[3].lower() == "2 wides"):
						indruns+=2
						indwides+=2
					if	(i[3].lower() == "3 wides"):
						indruns+=3
						indwides+=3	
					if	(i[3].lower() == "no-ball"):
						indruns+=1
					if(indscorecard[j][1]==0):
						indscorecard[j][4]=0
					else:
						hello=round(((indscorecard[j][0]/indscorecard[j][1])*100),2)
						indscorecard[j][4]=hello	
			if(i[0]=="5.6"):
				indpowerplay=indruns							
		#---------------------------------------------------------------------------------------------
		indblist=[]
		pakblist=[]
		indb=[]
		pakb=[]

		#we make a similar unique list for bowlers.
		# we first extract the names of the bowlers who have delivered atleast one ball
		# then we arrange them in order of bowling
		# then we remove the recurring names
		for i in range(0,len(indinn),1):
			indblist.append(indinn[i][1])
		for i in range(0,len(pakinn),1):
			pakblist.append(pakinn[i][1])
		while len(indblist)!=0:
			indb.append(indblist[0])
			yo=indblist[0]
			while yo in indblist:
				indblist.remove(yo)	#recurring names removed
		while len(pakblist)!=0:
			pakb.append(pakblist[0])
			yo=pakblist[0]
			while yo in pakblist:
				pakblist.remove(yo) #recurring names removed
		for i in range(0,len(indb),1):
			#[overs, maidens, runs, wicket, no ball,wides,economy]
			indscorecardbowlers.append([0,0,0,0,0,0,0])
		for i in range(0,len(pakb),1):
			#[overs, maidens, runs, wicket, no ball,wides,economy]
			pakscorecardbowlers.append([0,0,0,0,0,0,0])
	
		#calculating bowler stats
		# we now calculate the bowler stats
		# legal deliveries are counted as balls
		# the extras are not counted in the bowlers' acccount
		#the comparison for the outcome of each delivery is made using the list which was used to store the
		# innings data in the beginning with specific added attributes such as legbyes, byes, and catches
		for i in pakinn:	
			for j in range(0,len(pakb),1):
				if(i[1]==pakb[j]):
					if	(i[3].lower() == "no run"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower()[0:3] == "out"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][3]+=1	
					if	(i[3].lower() == "1 run"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=1
					if	(i[3].lower() == "2 runs"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=2
					if	(i[3].lower() == "3 runs"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=3
					if	(i[3].lower() == "4 runs"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=4
					if	(i[3].lower() == "1 run bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "2 runs bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "3 runs bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "4 runs bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "four bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "1 run leg bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "2 runs leg bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "3 runs leg bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "4 runs leg bye"):
						pakscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "four leg bye"):
						pakscorecardbowlers[j][0]+=1	
					if	(i[3].lower() == "four"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=4
					if	(i[3].lower() == "six"):
						pakscorecardbowlers[j][0]+=1
						pakscorecardbowlers[j][2]+=6
					if	(i[3].lower() == "wide"):
						pakscorecardbowlers[j][5]+=1
					if	(i[3].lower() == "2 wides"):
						pakscorecardbowlers[j][5]+=2
					if	(i[3].lower() == "3 wides"):
						pakscorecardbowlers[j][5]+=3
					if	(i[3].lower() == "no-ball"):
						pakscorecardbowlers[j][4]+=1
		
		#[overs, maidens, runs, wicket, no ball,wides,economy]
		
		#calculating bowler stats
		#We do the same for the indian team
		#-----------------------------------------------------------------------------------------------
		for i in indinn:	
			for j in range(0,len(indb),1):
				if(i[1]==indb[j]):
					if	(i[3].lower() == "no run"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower()[0:3] == "out"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][3]+=1	
					if	(i[3].lower() == "1 run"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=1
					if	(i[3].lower() == "2 runs"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=2
					if	(i[3].lower() == "3 runs"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=3
					if	(i[3].lower() == "4 runs"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=4
					if	(i[3].lower() == "1 run bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "2 runs bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "3 runs bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "4 runs bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "four bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "1 run leg bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "2 runs leg bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "3 runs leg bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "4 runs leg bye"):
						indscorecardbowlers[j][0]+=1
					if	(i[3].lower() == "four leg bye"):
						indscorecardbowlers[j][0]+=1	
					if	(i[3].lower() == "four"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=4
					if	(i[3].lower() == "six"):
						indscorecardbowlers[j][0]+=1
						indscorecardbowlers[j][2]+=6
					if	(i[3].lower() == "wide"):
						indscorecardbowlers[j][5]+=1
					if	(i[3].lower() == "2 wides"):
						indscorecardbowlers[j][5]+=2
					if	(i[3].lower() == "3 wides"):
						indscorecardbowlers[j][5]+=3
					if	(i[3].lower() == "no-ball"):
						indscorecardbowlers[j][4]+=1
		#--------------------------------------------------------------------------------------------				
		
		indinnovers=0
		pakinnovers=0
		#we now calculate the strike rate of th bowlers
		#strike rate will be zero if no balls delivered
		for i in indscorecardbowlers:
			i[2]=i[2]+i[5]
			if(i[0]==0):
				i[6]=0
			else:
				hello=round(((i[2]/i[0])*6),1)
				i[6]=str(hello)+("0")
			i[0]=str(i[0]//6)+"."+str(i[0]%6)
			indinnovers+=float(i[0])
		for i in pakscorecardbowlers:
			i[2]=i[2]+i[5]
			if(i[0]==0):
				i[6]=0
			else:
				hello=round(((i[2]/i[0])*6),1)
				i[6]=str(hello)+("0")
			i[0]=str(i[0]//6)+"."+str(i[0]%6)
			pakinnovers+=float(i[0])

#------------------------------------------------------------------------------------------------------------
#-------------------------------Exporting to the file starts here----------------------------------------------------			
		winningmessage=0
		if(indruns>pakruns):
			winningmessage="India won by "+str(10-indwickets)+" wickets"
		elif(indruns<pakruns):
			winningmessage="Pakistan won by "+str(10-pakwickets)+" wickets"	
		else:
			winningmessage="Match tied"
		f = open("Scorecard.txt","w")
		title="India vs Pakistan, 2nd Match, Group A"
		print(f"{title:^100}",file=f)
		print("\n\n",file=f)
		print(f"{winningmessage:<40}",file=f)
		text1="Pakistan Innings"
		t2=str(pakruns)+"-"+str(pakwickets)+"("+str(pakinnovers)+" Ov)"		
		print(f"{text1:<79}{t2:<10}",file=f)
		batter="Batter"
		r="R"
		b="B"
		fours="4s"
		s="6s"
		sr="SR"
		gap=""
		print(f"{batter:<20}{gap:<35}{r:<6}{b:<6}{fours:<6}{s:<6}{sr:<6}",file=f)
		var=0
		for i in pakscorecard:
			name=pakbat[var]
			if(name=="Rizwan"):
				name="Rizwan(wk)"
			if(name=="Babar Azam"):
				name="Babar Azam(c)"	
			if (len(i)==8):
				result=i[7]+" "+i[6]
			else:
				if(i[6]==0):
					result="not out"
				else:
					result=i[6]
			runs=str(i[0])
			balls=str(i[1])
			fours=str(i[2])
			sixes=str(i[3])
			strike=str(i[4])
			print(f"{name:<20}{result:<35}{runs:<6}{balls:<6}{fours:<6}{sixes:<6}{strike:<6}",file=f)
			var+=1
		extras="Extras"
		t3=str(paklb+pakbyes+paknb+pakwides+pakp)
		t4="(b "+str(pakbyes)+",lb "+str(paklb)+",w "+str(pakwides)+",nb "+str(paknb)+",p "+str(pakp)+")"
		print(f"{extras:<55}{t3:<2}{t4:<20}",file=f)
		total="Total"
		t5=str(pakruns)
		t6="("+str(pakwickets)+"wkts,"+str(pakinnovers)+" Ov)"
		print(f"{total:<55}{t5:<3}{t6:<15}",file=f)
		if (pakwickets!=10):
			for i in range(pakwickets+2,11,1):
				didnotbat=didnotbat+", "+ind[i]
			didnotbat=didnotbat[2:]	
			didnot="Did not Bat"
			print(f"{didnot:20}{didnotbat:80}",file=f)
		fall="Fall of Wickets"
		print(f"{fall:<55}",file=f)
		fallofwick=''
		mul=1
		for i in pakcumulativescore:
			fallofwick=fallofwick+str(i[0])+"-"+str(i[1])+" ("+i[2]+","+i[3]+"), "
			if((len(fallofwick)//85)>=mul):
				fallofwick=fallofwick+"\n"
				mul+=1
		fallofwick=fallofwick[0:len(fallofwick)-2]		
		print(f"{fallofwick:<85}",file=f)
		print("\n",file=f)

		bowler="Bowler"
		o="O"
		m="M"
		r="R"
		w="W"
		nb="NB"
		wd="WD"
		eco="Eco"
		gap=""
		print(f"{bowler:<43}{o:<6}{m:<6}{r:<6}{w:<6}{nb:<6}{wd:<6}{eco:<6}",file=f)
		var=0
		for i in pakscorecardbowlers:
			name=pakb[var]
			overs=i[0]
			maidens=str(i[1])
			runs=str(i[2])
			wickets=str(i[3])
			noball=str(i[4])
			wide=str(i[5])
			econ=i[6]
			print(f"{name:<43}{overs:<6}{maidens:<6}{runs:<6}{wickets:<6}{noball:<6}{wide:<6}{econ:<6}",file=f)
			var+=1
			powerplays="Powerplays"
			overs="Overs"
			runs="Runs"
		print(f"{powerplays:<43}{overs:<30}{runs:<6}",file=f)
		mand="Mandatory"
		t7="0.1-6"
		pakpowerplay=str(pakpowerplay)
		print(f"{mand:<43}{t7:<30}{pakpowerplay:<6}",file=f)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------		
#------------------------------Same has been done for team India----------------------------------------------------					
		print("\n\n",file=f)
		text1="India Innings"
		t2=str(indruns)+"-"+str(indwickets)+"("+str(indinnovers)+" Ov)"		
		print(f"{text1:<79}{t2:<10}",file=f)
		batter="Batter"
		r="R"
		b="B"
		fours="4s"
		s="6s"
		sr="SR"
		gap=""
		print(f"{batter:<20}{gap:<35}{r:<6}{b:<6}{fours:<6}{s:<6}{sr:<6}",file=f)
		var=0
		for i in indscorecard:
			name=indbat[var]
			if(name=="Rohit"):
				name="Rohit(c)"
			if(name=="Karthik"):
				name="Karthik(wk)"
			if (len(i)==8):
				result=i[7]+" "+i[6]
			else:
				if(i[6]==0):
					result="not out"
				else:
					result=i[6]
			runs=str(i[0])
			balls=str(i[1])
			fours=str(i[2])
			sixes=str(i[3])
			strike=str(i[4])
			print(f"{name:<20}{result:<35}{runs:<6}{balls:<6}{fours:<6}{sixes:<6}{strike:<6}",file=f)
			var+=1
		extras="Extras"
		t3=str(indlb+indbyes+indnb+indwides+indp)
		t4="(b "+str(indbyes)+",lb "+str(indlb)+",w "+str(indwides)+",nb "+str(indnb)+",p "+str(indp)+")"
		#print("\n",file=f)
		print(f"{extras:<55}{t3:<2}{t4:<20}",file=f)
		total="Total"
		t5=str(indruns)
		t6="("+str(indwickets)+"wkts,"+str(indinnovers)+" Ov)"
		print(f"{total:<55}{t5:<3}{t6:<15}",file=f)
		didnotbat=''
		if (indwickets!=10):
			for i in range(indwickets+2,11,1):
				didnotbat=didnotbat+", "+ind[i]
			didnotbat=didnotbat[2:]	
			didnot="Did not Bat"
			print(f"{didnot:20}{didnotbat:80}",file=f)	
		fall="Fall of Wickets"
		print(f"{fall:<55}",file=f)
		fallofwick=''
		mul=1
		for i in indcumulativescore:
			fallofwick=fallofwick+str(i[0])+"-"+str(i[1])+" ("+i[2]+","+i[3]+"), "
			if((len(fallofwick)//85)>=mul):
				fallofwick=fallofwick+"\n"
				mul+=1
		fallofwick=fallofwick[0:len(fallofwick)-2]		
		print(f"{fallofwick:<85}",file=f)
		print("\n",file=f)

		bowler="Bowler"
		o="O"
		m="M"
		r="R"
		w="W"
		nb="NB"
		wd="WD"
		eco="Eco"
		gap=""
		print(f"{bowler:<43}{o:<6}{m:<6}{r:<6}{w:<6}{nb:<6}{wd:<6}{eco:<6}",file=f)
		var=0
		for i in indscorecardbowlers:
			name=indb[var]
			overs=i[0]
			maidens=str(i[1])
			runs=str(i[2])
			wickets=str(i[3])
			noball=str(i[4])
			wide=str(i[5])
			econ=i[6]
			print(f"{name:<43}{overs:<6}{maidens:<6}{runs:<6}{wickets:<6}{noball:<6}{wide:<6}{econ:<6}",file=f)
			var+=1
			powerplays="Powerplays"
			overs="Overs"
			runs="Runs"
		print(f"{powerplays:<43}{overs:<30}{runs:<6}",file=f)
		mand="Mandatory"
		t7="0.1-6"
		indpowerplay=str(indpowerplay)
		print(f"{mand:<43}{t7:<30}{indpowerplay:<6}",file=f)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
	
	
	except FileNotFoundError:
		print("Incorrect file name")
	except ZeroDivisionError:
		print("Can't divide by zero")
	else:	
		pass


###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


scorecard()






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
