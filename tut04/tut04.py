
from datetime import datetime
start_time = datetime.now()

#Help https://youtu.be/H37f_x4wAC0
def octant_longest_subsequence_count_with_range():
    import pandas as pd
    try:
        data=pd.read_excel("input_octant_longest_subsequence_with_range.xlsx")
    except FileNotFoundError:
        print("Incorrect file name")  
    else:

        ##############################
        #Creating the columns in the excel sheet
        data["Octant"]="" 
        data[""]=""
        data["count"]=""
        data["Longest Subsequence Length"]=""
        data["Count"]=""
        data["  "]=""
        data["octant"]=""
        data["Length of longest subsequence"]=""
        data["Count of longest subsequence"]=""
        values=["+1","-1","+2","-2","+3","-3","+4","-4"]
        for i in range(0,8,1):
            data.at[i,"count"]=values[i]
        ##############################
        lastval=data.index[-1]  #To calculate the last index, when index starts from 0 
        ##############################################
        #The following lines of code would check the numbers in the 3 columns and determine the octant values
        #based on the conditional statements provided
        #Calculating the octant value follows the same logic as described in the explanatory video
        for i in range(0,lastval+1,1):
            u=data["U'=U-U Avg"][i]
            v=data["V'=V-V Avg"][i]
            w=data["W'=W-W Avg"][i]
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
        
        
        count=[0,0,0,0,0,0,0,0] #creating an empty array to store the counted values of consecutive occurrences
        large=[0,0,0,0,0,0,0,0] #creating another empty array to store the largest consecutively counted occurrences
        pos=0
        for i in range(0,lastval,1):
            #goes to a value at a particular time and checks if the next occurring element is same as the current one
            if(data['Octant'][i]==data['Octant'][i+1]):     
                for j in range(0,8,1):                      
                    if (data['Octant'][i]==values[j]):
                        #keeps counting till the next element is same as the previous one                              
                        count[j]+=1
                        pos=j
            else:
                #after one point the next element will not be same as the previous one
                #in that case we'll be checking if the counted value is largest value counted yet 
                #once the largest counted value of the octant is added to large, count is set to zero again  
                                                        
                if (count[pos]>large[pos]):                 
                    large[pos]=count[pos]                   
                    count[pos]=0      

                #in case the counted value is smaller than or equal to the previous largest counted value then 'large' remains the same as before
                
                else:
                    large[pos]=large[pos]                   
                    count[pos]=0          
                    
        
        #the previous blocks counted the largest consecutive occerrence of a particular octant value
        #but the counted value will be one less than the actual value because the initial value of 'count' was set to zero
        #hence every octant element that exists, is given an additional count value in the code given below
        for j in range(0,8,1):
            for i in range(0,lastval,1):
                if (data['Octant'][i]==values[j]):
                    large[j]+=1
                    break
        
        #code to count how many largest occurrences present for each octant value
        count2=[0,0,0,0,0,0,0,0]              
        for j in range(0,8,1):                   
            for i in range(0,lastval-large[j]+1,1):
                supercount=0
                for k in range(0,large[j],1):
                    if(data['Octant'][i+k]==values[j]):
                        supercount+=1
                if(supercount==large[j]):
                    count2[j]+=1
        #code to insert the final values to the excel sheet
        for i in range(0,8,1):
            data.at[i,"Longest Subsequence Length"]=large[i]
            data.at[i,"Count"]=count2[i]
        

        timefromtopos=1
        for i in range(0,8,1):

            #Here we write the octant values as headings for each block in the excel sheet
            #We also add the headings "Time", "To" and "From" to the blocks for each octant
            data.at[timefromtopos-1,"octant"]=values[i]
            data.at[timefromtopos,"octant"]="Time"
            data.at[timefromtopos-1,"Length of longest subsequence"]=large[i]
            data.at[timefromtopos,"Length of longest subsequence"]="From"
            data.at[timefromtopos,"Count of longest subsequence"]="To"
            data.at[timefromtopos-1,"Count of longest subsequence"]=count2[i]
            
            anotherpos=1
            for j in range(0,lastval,1):
                newcount=1
                if(values[i]==data["Octant"][j]):   #this code checks the initial and final timestamp of the largest consecutive occerrence of an octant value
                    for k in range(1,large[i],1):   #it goes to the octant value, checks if the next 'n' consecutive numbers are same as the current number
                        if(large[i]<=(lastval-j)):  #where 'n' is the largest consecutive occerrence calculated previously
                            if(data["Octant"][j]==data["Octant"][j+k]):
                                newcount+=1
                if(newcount==large[i]):
                          #writes the timestamp to the excel sheet
                          data.at[timefromtopos+anotherpos,"Length of longest subsequence"]=data["Time"][j]
                          data.at[timefromtopos+anotherpos,"Count of longest subsequence"]=data["Time"][j+large[i]-1]
                          anotherpos+=1  
            timefromtopos+=2+count2[i]
        data.to_excel("output_octant_longest_subsequence_with_range.xlsx",index=False)



from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count_with_range()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
