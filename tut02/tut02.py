def octant_transition_count(mod=5000):
    import pandas as pd
    try:
        mod=mod+5                    #to check if entered mod value is an integer or not
        mod=mod-5
        data=pd.read_excel("input_octant_transition_identify.xlsx")
        a=mod+abs(mod)
        a=mod/a
    except FileNotFoundError:
        print("Incorrect file name")
    except TypeError:
        print("Incorrect value of mod entered. Please enter an integer value.")
    except ZeroDivisionError:
        print("Please enter a positive integral value of mod")    
    else:

        ##############################
        #Creating the columns in the excel sheet
        data["Octant"]="" 
        data[""]=""
        data.at[1,""]="User Input"
        data["Octant ID"]=""
        data.at[0,"Octant ID"]="Overall Count"
        data.at[1,"Octant ID"]="Mod "+str(mod)
        data["+1"]=""
        data["-1"]=""
        data["+2"]=""
        data["-2"]=""
        data["+3"]=""
        data["-3"]=""
        data["+4"]=""
        data["-4"]=""
        ##############################


        lastval=data.index[-1]  #To calculate the last index, when index starts from 0
        multiply=lastval//mod   #To calculate quotient when the last index is divided by mod 



        #################################
        #This is the overall transition count
        data.at[1+(multiply+1)+4,"Octant ID"]="Overall Transition Count"
        data.at[1+(multiply+1)+4+2,"Octant ID"]="Count"
        data.at[1+(multiply+1)+4+1,"+1"]="To"
        data.at[1+(multiply+1)+4+3,""]="From"
        listofvalues=["+1","-1","+2","-2","+3","-3","+4","-4"]
        for i in range(1+(multiply+1)+7,1+(multiply+1)+15,1):
            data.at[i,"Octant ID"]=listofvalues[i-(1+(multiply+1)+7)]
        for j in range(0,8,1):
            data.at[1+(multiply+1)+6,listofvalues[j]]=listofvalues[j]              
        ##################################




        #creating variables with inital value zero for doing the octant counts
        count1=0
        countm1=0
        count2=0
        countm2=0
        count3=0
        countm3=0
        count4=0
        countm4=0
        ##########################



        #creating a separate set of variables
        #counterforeachoctant helps to iterate through the excel sheet cells column wise with a constant
        #value for each mod range
        #a,b,c,d,e,f,g,h help us store the value of the sum till the previous mod range. We subtract it from
        #the cumulative octant count to get the octant count of the current mod range 
        counterforeachoctant=2
        a=0
        b=0
        c=0
        d=0
        e=0
        f=0
        g=0
        h=0
        for j in range(1,multiply+2,1):
            if(j==1):
                data.at[j+1,"Octant ID"]="0000"+"-"+str(mod-1)
            else:
                if(j<=multiply):
                    num=str(mod*(j-1))+"-"+str(mod*j - 1)
                    data.at[j+1,"Octant ID"]=num
                else:
                    num=str(mod*(j-1))+"-"+str(lastval)
                    data.at[j+1,"Octant ID"]=num


        ##############################################
        #The following lines of code would check the numbers in the 3 columns and determine the octant values
        #based on the conditional statements provided
        #Calculating the octant value follows the same logic as described in the explanatory video
        for i in range(0,lastval+1,1):
            u=data['U-u_avg'][i]
            v=data['V-v_avg'][i]
            w=data['W-w_avg'][i]
            if u>0:
                if v>0:
                    if w>0:
                        
                        data.at[i,'Octant']="+1"
                    else:
                        
                        data.at[i,'Octant']="-1"
                else:
                    if w>0:
                        
                        data.at[i,'Octant']="+4"
                    else:
                        
                        data.at[i,'Octant']="-4"
            else:
                if v>0:
                    if w>0:
                        data.at[i,'Octant']="+2"
                    else:
                        data.at[i,'Octant']="-2"
                else:
                    if w>0:
                        data.at[i,'Octant']="+3"
                    else: 
                        data.at[i,'Octant']="-3" 

            #Once the octant values are written down in the sheet, we simultaneously count the octant values
            #The followin code describes counting the octant and also for counting in each mod range                                
            if((data["Octant"][i])=="+1"):
                count1+=1
            elif((data["Octant"][i])=="-1"):
                countm1+=1
            elif((data["Octant"][i])=="+2"):
                count2+=1
            elif((data["Octant"][i])=="-2"):
                countm2+=1   
            elif((data["Octant"][i])=="+3"):
                count3+=1
            elif((data["Octant"][i])=="-3"):
                countm3+=1
            elif((data["Octant"][i])=="+4"):
                count4+=1
            elif((data["Octant"][i])=="-4"):
                countm4+=1
            if(((i!=0)and((i+1)%mod==0))or(i==lastval)): #checks if mod range has ended or the last value has been reached
                #usage of the variables a,b,c....has been previously explained
                data.at[counterforeachoctant,"+1"]=count1-a
                data.at[counterforeachoctant,"-1"]=countm1-b
                data.at[counterforeachoctant,"+2"]=count2-c
                data.at[counterforeachoctant,"-2"]=countm2-d
                data.at[counterforeachoctant,"+3"]=count3-e
                data.at[counterforeachoctant,"-3"]=countm3-f
                data.at[counterforeachoctant,"+4"]=count4-g
                data.at[counterforeachoctant,"-4"]=countm4-h
                a,b,c,d,e,f,g,h=count1,countm1,count2,countm2,count3,countm3,count4,countm4
                counterforeachoctant+=1
            else:
                continue
        ##############################################33
        





        #####################################
        #To count the total octant transitions
        #We iterate through all the values in the dataframe in the "octant" column
        #if there is a change in the value from ith to (i+1)th octant value then the position of writing 
        #in the excel sheet is stored in the two variables "toposition" and "fromposition" to uniquely
        #write to a particular cell in the excel sheet
        for i in range(0,lastval,1):
            values=["+1","-1","+2","-2","+3","-3","+4","-4"]
            for j in range(0,8,1):
                if(values[j]==data["Octant"][i]):
                    fromposition=(multiply+1)+1+7+j
                if(values[j]==data["Octant"][i+1]):
                    toposition=values[j]
            if(not(data[toposition][fromposition])):
                data.at[fromposition,toposition]=1 
            else:    
                data.at[fromposition,toposition]=data[toposition][fromposition]+1
        ######################################
            

        #We initialize all the octant transitions in each mod range by filling the matrix with zeroes
        #the variable k helps to get to the beginning of a new table of writing cells
        #the exact position of the writing cells is determined by two variables "toposition" and "fromposition"
        for k in range(1,multiply+2,1):
            values=["+1","-1","+2","-2","+3","-3","+4","-4"]
            for i in range(0,8,1):
                for j in range(0,8,1):
                    fromposition=1+multiply+1+8+(13*k)+i
                    toposition=values[j]
                    data.at[fromposition,toposition]=0 



        ##########################################3
        #Writing down the table headers and other values before writing the transition counts
        for k in range(1,multiply+2,1):
            data.at[1+(multiply+1)+5+(13*k),"Octant ID"]="Mod Transition Count"
            data.at[1+(multiply+1)+6+(13*k),"+1"]="To"
            data.at[1+(multiply+1)+7+(13*k),"Octant ID"]="Count"
            data.at[1+(multiply+1)+8+(13*k),""]="From"
            if(k==1):
                data.at[1+(multiply+1)+6+(13*k),"Octant ID"]="0000"+"-"+str(mod-1)
            else:
                if(k<=multiply):
                    num=str(mod*(k-1))+"-"+str(mod*(k) - 1)
                    data.at[1+(multiply+1)+6+(13*k),"Octant ID"]=num
                else:
                    num=str(mod*(k))+"-"+str(lastval)
                    data.at[1+(multiply+1)+6+(13*k),"Octant ID"]=num    
            listofvalues=["+1","-1","+2","-2","+3","-3","+4","-4"]
            for i in range(1+(multiply+1)+8+(13*k),1+(multiply+1)+16+(13*k),1):
                data.at[i,"Octant ID"]=listofvalues[i-(1+(multiply+1)+8+(13*k))]
            for j in range(0,8,1):
                data.at[1+(multiply+1)+7+(13*k),listofvalues[j]]=listofvalues[j]
            #######################################


            
            for i in range(mod*(k-1),mod*(k),1):
                if(i==lastval):
                    break
                values=["+1","-1","+2","-2","+3","-3","+4","-4"]
                for j in range(0,8,1):
                    if(values[j]==data["Octant"][i]):
                        fromposition=1+multiply+1+8+(13*k)+j
                    if(values[j]==data["Octant"][i+1]):
                        toposition=values[j]
                if(not(data[toposition][fromposition])):
                    data.at[fromposition,toposition]=1 #inserts 1 if value is empty
                else:    
                    data.at[fromposition,toposition]=data[toposition][fromposition]+1   #adds 1 if value is not empty          

        data.at[0,"+1"]=count1
        data.at[0,"-1"]=countm1
        data.at[0,"+2"]=count2
        data.at[0,"-2"]=countm2
        data.at[0,"+3"]=count3
        data.at[0,"-3"]=countm3
        data.at[0,"+4"]=count4
        data.at[0,"-4"]=countm4

        #For the final verification of overall counts after individually adding the  counts in each mod range
        data.at[1+multiply+2,"Octant ID"]="Verified"
        verificationcountlist=[0,0,0,0,0,0,0,0]
        for j in range(0,8,1):
            values=["+1","-1","+2","-2","+3","-3","+4","-4"]
            for i in range(2,(1+multiply+2),1):
                verificationcountlist[j]=verificationcountlist[j]+data[(values[j])][i]
            data.at[1+multiply+2,values[j]]=verificationcountlist[j]


        data.to_excel("output_octant_transition_identify.xlsx",index=False)


from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod=5000
octant_transition_count(mod)