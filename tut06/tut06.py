

from __future__ import print_function
from datetime import datetime
from tracemalloc import start
start_time = datetime.now()

def attendance_report():
    import pandas as pd
    try:
        data=pd.read_csv("input_attendance.csv")
        students=pd.read_csv("input_registered_students.csv")

    except FileNotFoundError:
        print("Incorrect file name")  
    else:
        import datetime

        #reads the attendance record file
        data=pd.read_csv("input_attendance.csv")

        #for getting information about the students actually registered for the course                
        students=pd.read_csv("input_registered_students.csv")   
        
        #To find the index of the last entry in the attendance record file 
        lastval=data.index[-1]
        
        lis=[]      #creating an empty list to use later to store date and time of each record in the the attendance file
        l=[]        #creating an empty list to store each entry of lis as sublists inside l
        rollno=[]   #creating a list to store all the roll numbers of registered stidents in order
        
        #initializing the columns for the consolidated list. The individual dates will be appended later
        columnsforconsolidated=["Roll Number","Name"]
        
        #To find the index of the last entry in the registered students list
        studentslastval=students.index[-1]   
        
        #To include all the roll numbers in order in the rollno list
        for i in range(0,studentslastval+1,1): 
            rollno.append(students["Roll No"][i])
        
        #appending the timestamps from the attendance record to "lis[]"
        for i in range(0,lastval+1,1):
            lis.append(data["Timestamp"][i])
        
        #splitting the timestamps from each element in "lis[]" and appending to "l[]" as sublists 
        for i in lis:
            l.append((str(i).split(" ")))
        
        #appending only the dates (and not the time) from "l[]" to a list named "a[]"
        a=[i[0] for i in l]
        startdate=a[0]
        enddate=a[-1]
        
        #empty list that would later store all the unique mondays and thursdays
        allmonandthur=[]
        
        #changing the order of the start date (dd-mm-yyyy to yyyy-mm-dd) so that it can be converted to a timestamp using the datetime.date function
        d,m,y=startdate.split("-")
        d,m,y=int(d),int(m),int(y)
        startdate=datetime.date(y,m,d)
        
        #changing the order of the end date (dd-mm-yyyy to yyyy-mm-dd) so that it can be converted to a timestamp using the datetime.date function
        d,m,y=enddate.split("-")
        d,m,y=int(d),int(m),int(y)
        enddate=datetime.date(y,m,d)
        
        #setting the increment to 1 day so that we get a range of dates from the start date to end date 
        #We will be choosing the Mondays and Thursdays from this range of dates
        increment=datetime.timedelta(days=1)
        
        
        #-------------------------------------------------------------------------------------
        #This block would iterate from the start date to end date and append the date to the list named
        #allmonandthur[] if the day is a Monday or a Thursday
        while(startdate<=enddate):
            daycheck=startdate.strftime("%A")
            if (daycheck==("Monday") or daycheck==("Thursday")):
                
                #converting yyyy-mm-dd to dd-mm-yyyy
                y,m,d=str(startdate).split("-")
                nicedate=d+"-"+m+"-"+y
                
                allmonandthur.append(nicedate)
            startdate+=increment
        #-------------------------------------------------------------------------------------
        
        
        #We now append the dates to the column list for the consolidated attendance file
        #The column list is named as columnsforconsolidated
        for i in allmonandthur:
            columnsforconsolidated.append(i)
        
        
        #-----------------------------------------------------------------------
        #The last three columns are also appended as given in the sample output
        columnsforconsolidated.append("Actual Lectures Taken")
        columnsforconsolidated.append("Total Real")
        columnsforconsolidated.append("% Attendance")    
        #-----------------------------------------------------------------------
        
        
        #We create a master list that would contain each individual student's record for the consolidated file
        #We name it as consolidatedattendanceoutside 
        consolidatedattendanceoutside=[]    
        
        
        #--------------------------------------------------------------------------------------------
        #We have a set of three nested loops
        #The outermost loop iterates through the roll number
        #The middle loop iterates through the dates
        #The innermost loop iterates through each record of the "input_attendance" sheet
        for r in range(0,studentslastval+1,1):
            
            #creating an empty list that wouldd store date wise attendance record for each student (Total, real, duplicate, invalid)
            attendance=[]
            
            #sublist that would be later appended to consolidatedattendanceoutside
            consolidatedattendanceinside=[rollno[r],students["Name"][r]]
            
            dayspresent=0           #total number of days present       
            for i in allmonandthur:
                totalrealcount=0    #real+duplicate
                invalidcount=0      #invalid attendance

                for j in range(0,lastval+1,1):

                    #will check if date exists and increment the counts if the particular roll number has a valid attendance in that day
                    if((l[j][0]==i)and(((data["Attendance"][j]).split(" "))[0]==rollno[r])):
                        
                        #to convert the time to int
                        a=int((l[j][1].split(":"))[0]+(l[j][1].split(":"))[1])
                        if (a<=1500 and a>=1400):
                            totalrealcount+=1
                        else:
                            invalidcount+=1
                
                #If no record of the particular roll number is present on that date
                if(totalrealcount==0):
                    c1=[i,rollno[r],students["Name"][r],invalidcount,0,0,invalidcount,1]
                    #c1 and c2 are used in the sibsequent lines of code below
                    c2=[i,"","",invalidcount,0,0,invalidcount,1]
                    consolidatedattendanceinside.append("A")
                
                #If records for that roll number is present on that date
                else:
                    c1=[i,rollno[r],students["Name"][r],totalrealcount+invalidcount,1,totalrealcount-1,invalidcount,0]
                    c2=[i,"","",totalrealcount+invalidcount,1,totalrealcount-1,invalidcount,0]
                    #c1 and c2 are used in the sibsequent lines of code below
                    consolidatedattendanceinside.append("P")
                    dayspresent+=1
                
                if(i==allmonandthur[0]):
                    #To include the name and roll number in the first row
                    attendance.append(c1)
                else:
                    #To ignore adding the name and roll number in the subsequent rows
                    attendance.append(c2)     
            
            #creating the dataframe for each individual roll number file
            datewiserecord=pd.DataFrame(attendance,columns=["Date","Roll Number","Name","Total Attendance Count","Real","Duplicate","Invalid","Absent"])                         
            
            #creating the path as it is inside a folder named "output"
            path="output\\"+str(rollno[r])+".xlsx"
            
            #writing the dataframe to the path
            datewiserecord.to_excel(path,index=False)
            
            #writing the total number of lectures in the consolidated file for each individual
            consolidatedattendanceinside.append(len(allmonandthur))
            
            #writing the total number of days present in the consolidated file for each individual
            consolidatedattendanceinside.append(dayspresent)
            
            #writing down the attendance percentage
            consolidatedattendanceinside.append(round(((dayspresent/len(allmonandthur))*100),2))
            
            #appending the sublist of each individial into the master list of consolidated attendance
            consolidatedattendanceoutside.append(consolidatedattendanceinside)
        
        #--------------------------------------------------------------------------------------------
        
        #creating the master dataframe for the consolidated attendance 
        consolidateddatewiserecord=pd.DataFrame(consolidatedattendanceoutside,columns=columnsforconsolidated)
        #creating the path
        path2="output\\"+"attendance_report_consolidated"+".xlsx"
        #writing output to the file
        consolidateddatewiserecord.to_excel(path2,index=False)
        def mail():
            option=str(input("Do want to send a copy of the consolidated report via mail?: (Y/N)"))
            if (option=="Y"):
                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                from email.mime.base import MIMEBase
                from email import encoders
                import csv
                from random import randint
                from time import sleep
                def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body, file_path):
                    try:
                        msg = MIMEMultipart()
                        print("[+] Message Object Created")
                    except:
                        print("[-] Error in Creating Message Object")
                        return
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = msg_subject
                    body = msg_body
                    msg.attach(MIMEText(body, 'plain'))
                    filename = file_path
                    attachment = open(filename, "rb")
                    p = MIMEBase('application', 'octet-stream')
                    p.set_payload((attachment).read())
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    try:
                        msg.attach(p)
                        print("[+] File Attached")
                    except:
                        print("[-] Error in Attaching file")
                        return
                    try:
                        #s = smtplib.SMTP('smtp.gmail.com', 587)
                        s = smtplib.SMTP('stud.iitp.ac.in', 587)
                        print("[+] SMTP Session Created")
                    except:
                        print("[-] Error in creating SMTP session")
                        return
                    s.starttls()
                    try:
                        s.login(fromaddr, frompasswd)
                        print("[+] Login Successful")
                    except:
                        print("[-] Login Failed")
                    text = msg.as_string()
                    try:
                        s.sendmail(fromaddr, toaddr, text)
                        print("[+] Mail Sent successfully")
                    except:
                        print('[-] Mail not sent')

                    s.quit()
                def isEmail(x):
                    if ('@' in x) and ('.' in x):
                        return True
                    else:
                        return False


                FROM_ADDR = "CHANGE ME"
                FROM_PASSWD = "CHANGE ME"
                TO_ADDR="cs3842022@gmail.com"
                FILE_PATH='output\\attendance_report_consolidated.xlsx'
                Subject = "Consolidated attendance report"
                Body ='''
                Dear Sir

Please find the copy of the consolidated attendance report attached herewith.

Sincerely
Shaheer
                '''  
                send_mail(FROM_ADDR, FROM_PASSWD, TO_ADDR, Subject, Body, FILE_PATH)  

            elif(option=="N"):
                print("Okay, closing the program now...")
            else:
                print("Invalid option! \n")
                mail()  
        mail()          
    
from platform import python_version
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


attendance_report()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
