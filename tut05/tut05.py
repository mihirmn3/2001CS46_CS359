

from datetime import datetime
from hashlib import new
start_time = datetime.now()

#Help https://youtu.be/N6PBd4XdnEw
def octant_range_names(mod=5000):
    octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}
    import pandas as pd
    try:
        data=pd.read_excel("octant_input.xlsx")
    except FileNotFoundError:
        print("Incorrect file name")  
    else:

        ##############################
        #Creating the columns in the excel sheet
        data=pd.read_excel("octant_input.xlsx")
        data["Octant"]=""
        data[""]=""
        data.at[2,""]="User Input"
        data[" "]=""
        data.at[0," "]="Octant ID"
        data.at[1," "]="Overall Count"
        data.at[2," "]="Mod "+str(mod)
        data["  "]=""
        data["   "]=""
        data["    "]=""
        data["     "]=""
        data["      "]=""
        data["       "]=""
        data["        "]=""
        data["         "]=""
        data.at[0,"  "]="1"
        data.at[0,"   "]="-1"
        data.at[0,"    "]="2"
        data.at[0,"     "]="-2"
        data.at[0,"      "]="3"
        data.at[0,"       "]="-3"
        data.at[0,"        "]="4"
        data.at[0,"         "]="-4"
        data["1"]=""
        data["-1"]=""
        data["2"]=""
        data["-2"]=""
        data["3"]=""
        data["-3"]=""
        data["4"]=""
        data["-4"]=""
        data["          "]=""
        data.at[0,"          "]="Rank 1 Octant ID"
        data["           "]=""
        data.at[0,"           "]="Rank 1 Octant Name"
        values=[1,-1,2,-2,3,-3,4,-4]
        s=1
        for i in values:
            data.at[0,str(i)]="Rank"+" "+str(s)
            s+=1
        data.at[0,"1"]="Rank 1"
        lastval=data.index[-1]
        count1=0
        countm1=0
        count2=0
        countm2=0
        count3=0
        countm3=0
        count4=0
        countm4=0
        multiply=lastval//mod
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
                data.at[j+2," "]="0000"+"-"+str(mod-1)
            else:
                if(j<=multiply):
                    num=str(mod*(j-1))+"-"+str(mod*j - 1)
                    data.at[j+2," "]=num
                else:
                    num=str(mod*(j-1))+"-"+str(lastval)
                    data.at[j+2," "]=num
        rank1count=[0,0,0,0,0,0,0,0]
        for i in range(0,lastval+1,1):
            u=data["U'=U-U Avg"][i]
            v=data["V'=V-V Avg"][i]
            w=data["W'=W-W Avg"][i]
            if u>0:
                if v>0:
                    if w>0:
                        
                        data.at[i,'Octant']=1
                    else:
                        
                        data.at[i,'Octant']=-1
                else:
                    if w>0:
                        
                        data.at[i,'Octant']=4
                    else:
                        
                        data.at[i,'Octant']=-4
            else:
                if v>0:
                    if w>0:
                        data.at[i,'Octant']=2
                    else:
                        data.at[i,'Octant']=-2
                else:
                    if w>0:
                        data.at[i,'Octant']=3
                    else: 
                        data.at[i,'Octant']=-3                     
            if((data["Octant"][i])==1):
                count1+=1
            elif((data["Octant"][i])==-1):
                countm1+=1
            elif((data["Octant"][i])==2):
                count2+=1
            elif((data["Octant"][i])==-2):
                countm2+=1   
            elif((data["Octant"][i])==3):
                count3+=1
            elif((data["Octant"][i])==-3):
                countm3+=1
            elif((data["Octant"][i])==4):
                count4+=1
            elif((data["Octant"][i])==-4):
                countm4+=1
            if(((i!=0)and((i+1)%mod==0))or(i==lastval)):
                data.at[counterforeachoctant+1,"  "]=count1-a
                data.at[counterforeachoctant+1,"   "]=countm1-b
                data.at[counterforeachoctant+1,"    "]=count2-c
                data.at[counterforeachoctant+1,"     "]=countm2-d
                data.at[counterforeachoctant+1,"      "]=count3-e
                data.at[counterforeachoctant+1,"       "]=countm3-f
                data.at[counterforeachoctant+1,"        "]=count4-g
                data.at[counterforeachoctant+1,"         "]=countm4-h
                counts=[count1-a,countm1-b,count2-c,countm2-d,count3-e,countm3-f,count4-g,countm4-h]
                ncounts=sorted(counts)
                for i in range(0,8,1):
                    for j in range(0,8,1):
                        if (ncounts[i]==counts[j]):
                            data.at[counterforeachoctant+1,str(values[j])]=8-i
                            data.at[counterforeachoctant+1,"          "]=values[j]
                            data.at[counterforeachoctant+1,"           "]=octant_name_id_mapping[str(values[j])]
                            if (i==7):
                                rank1count[j]=rank1count[j]+1
                a,b,c,d,e,f,g,h=count1,countm1,count2,countm2,count3,countm3,count4,countm4
                counterforeachoctant+=1
            else:
                continue    
        data.at[1,"  "]=count1
        data.at[1,"   "]=countm1
        data.at[1,"    "]=count2
        data.at[1,"     "]=countm2
        data.at[1,"      "]=count3
        data.at[1,"       "]=countm3
        data.at[1,"        "]=count4
        data.at[1,"         "]=countm4
        ovcounts=[count1,countm1,count2,countm2,count3,countm3,count4,countm4]    
        novcounts=sorted(ovcounts)
        for i in range(0,8,1):
            for j in range(0,8,1):
                if (novcounts[i]==ovcounts[j]):
                    data.at[1,str(values[j])]=8-i
                    data.at[1,"          "]=values[j]
                    data.at[1,"           "]=octant_name_id_mapping[str(values[j])]
        newpos=7+(lastval//mod)
        data.at[newpos,"  "]="Octant ID"
        data.at[newpos,"   "]="Octant Name"
        data.at[newpos,"    "]="Count of Rank 1 Mod Values"
        for i in range(0,8,1):
            data.at[newpos+1+i,"  "]=values[i]
            data.at[newpos+1+i,"   "]=octant_name_id_mapping[str(values[i])]
            data.at[newpos+1+i,"    "]=rank1count[i]        
        data.to_excel('octant_output.xlsx',index=False)

from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod=5000 
octant_range_names(mod)



#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
