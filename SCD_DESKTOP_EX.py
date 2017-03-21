"""
Created on Mon Mar 13 15:52:05 2017

@author: vigneshpandi marimuthu
"""
import cx_Oracle
import datetime
format="%y_%m_%d"
TODAY=datetime.date.today()
add = datetime.timedelta(days = 1)
YESTERDAY = datetime.date.today() - add
dd=datetime.date.strftime(TODAY,format)
value_list_match=[]   
value_list_nochange=[] 
value_list=[]
#import pandas
List_record_with_columns=[]
List_record=[]
List_Sep=[]
List_Seq_UPD=[]
conn = cx_Oracle.connect('hr/admin@xe') #Oracle Connection
cursor = conn.cursor()
file = open("D:\\Python_Test\\input_files\\INC_FILE_" + str(dd) +".txt")
Lines=file.readlines()
for a in Lines:
    Line=a.split('\n')
    List_Test=list(Line)
    List_record_with_columns.append(List_Test)
#print List_record_with_columns
num_of_records=len(List_record_with_columns)-1
#print num_of_records
for i in range(1,num_of_records+1,1):
    a=List_record_with_columns[i]
    List_record.append(List_record_with_columns[i])
file.close()
#print Dict1
Q_Fetch="Select SEQ,ID,NAME,DESIGNATION,START_DATE,END_DATE FROM SCD_TEST_EX WHERE FLAG='Y'"
Initial_Check="select count(*) from SCD_TEST_EX"
cursor.execute(Initial_Check)
ora_row_count = cursor.fetchone()
#print ora_row_count[0]
#For initial Load
if ora_row_count[0] == 0:
    for j in range (0,len(List_record),1):
        value_list.append(j)
        c=List_record[j]
        d=c[0]
        e=d.split(',')
        Insert_Q="Insert into SCD_TEST_EX(SEQ,ID,NAME,DESIGNATION,START_DATE,END_DATE,FLAG) values (SEQ_SCD_EX.NEXTVAL,"+ str(e[0]) + "," + "'"+str(e[1])+"'" + "," +"'"+ str(e[2])+"'" + ","+"sysdate,NULL,'Y' )"
        cursor.execute(Insert_Q)
        conn.commit() 
else:
    cursor.execute(Q_Fetch)
    #print len(List_record)
    for k in cursor:
        for j in range (0,len(List_record),1):
            value_list.append(j)
            c=List_record[j]
            d=c[0]
            e=d.split(',')
            if int(e[0]) == int(k[1]):
                value_list_match.append(j)
                if (str(e[1]) == str(k[2])) & (str(e[2]) == str(k[3])):
                    value_list_nochange.append(j)
#To capture insert, update, no_change indexes                               
over_all_value=set(value_list)
Match_values=set(value_list_match)
No_change_values=set(value_list_nochange)
UPDATE_INDEX=list(set(value_list_match).difference(set(value_list_nochange)))
INSERT_INDEX=list(set(value_list).difference(set(value_list_nochange)))
#print "over_all_index " + str(set(value_list))
#print "Matched_index " + str(set(value_list_match))
#print "No_Change_index " + str(set(value_list_nochange))
#print "UPDATE_INDEX " + str(UPDATE_INDEX)
#print "INSERT_INDEX " + str(INSERT_INDEX)

#To Update records 
if ora_row_count[0] <> 0: 
    for ii in UPDATE_INDEX:
        c=List_record[ii]
        d=c[0]
        e=d.split(',') 
        #print e[0],e[1],e[2]
        Q_Fetch_SEQ="Select SEQ FROM SCD_TEST_EX WHERE ID =" + str(e[0]) + " and FLAG='Y' and end_date is null"
        cursor.execute(Q_Fetch_SEQ)
        ora_seq_fetch = cursor.fetchone()
        Q_update="Update SCD_TEST_EX set Flag='N', end_date=sysdate-1 where SEQ=" + str(ora_seq_fetch[0])  
        #print Q_update
        cursor.execute(Q_update)
        conn.commit()
#New record and update record to be inserted
if ora_row_count[0] <> 0:     
    for j in INSERT_INDEX:
        c=List_record[j]
        d=c[0]
        e=d.split(',')
        Insert_Q = "insert into SCD_TEST_EX(SEQ,ID,NAME,DESIGNATION,START_DATE,END_DATE,FLAG) values (SEQ_SCD_EX.nextval,"+ str(e[0]) + "," + "'"+str(e[1])+"'" + "," +"'"+ str(e[2])+"'" + ","+"sysdate,NULL,'Y' )"
        cursor.execute(Insert_Q)
        conn.commit()

#To Show Popup
import Tkinter
root = Tkinter.Tk()
ll = Tkinter.Label(root, text="The RESULT")
l1 = Tkinter.Label(root, text="Total Records From the file - " + str(len(over_all_value)))
l2=Tkinter.Label(root, text="Number of Records Inserted - " + str(len(INSERT_INDEX)))
l3=Tkinter.Label(root, text="Number of Records Updated - " + str(len(UPDATE_INDEX)))
b = Tkinter.Button(root, text='OK', command=root.destroy)
ll.pack(pady=5)
l1.pack(pady=5)
l2.pack(pady=5)
l3.pack(pady=5)
b.pack(pady=5)
root.mainloop() 
#To send mail with status
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("FromMail@gmail.com", "password")
msg = "Finished successfully"
server.sendmail("FromMail@gmail.com", "ToMailAddress@domain.com", msg)
server.quit()

print "FINISHED SUCCESSFULLY"
