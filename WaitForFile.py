# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:52:05 2017

@author: vigneshpandi marimuthu
"""
import datetime
format="%y_%m_%d"
TODAY=datetime.date.today()
add = datetime.timedelta(days = 1)
YESTERDAY = datetime.date.today() - add
dd=datetime.date.strftime(TODAY,format) 
import Tkinter as tk
root = tk.Tk()
import time   
import smtplib                       
import os.path
import os
def mail_fun():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("pythoncod10@gmail.com", "pythontest")
    msg = "File is not there in particular directory for the date - " + str(dd)
    server.sendmail("abc@gmail.com", "v.marimuthu@perficient.com", msg)
    server.quit()
    return ""
def mail_fun_data():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("pythoncod10@gmail.com", "pythontest")
    msg = "File is there in particular directory for the date - " + str(dd) +"\nBut file doesn't have Data"
    server.sendmail("abc@gmail.com", "v.marimuthu@perficient.com", msg)
    server.quit()
    return ""
for i in range(1,7) : 
    if i==5:    
        mail_fun()
        ll = tk.Label(root, text="File Doesn't exist")
        ll.pack(pady=5)
        root.mainloop()
        break
    else:
        if os.path.isfile("D:\\Python_Test\\input_files\\INC_FILE_" + str(dd) +".txt"):
            File_size=os.stat("D:\\Python_Test\\input_files\\INC_FILE_" + str(dd) +".txt" )
            if File_size.st_size == 0:
                mail_fun_data()
                ll = tk.Label(root, text="File exist without Data")
                ll.pack(pady=5)
                root.mainloop()
                break
            else:
                print "File Exist iwth Data"
                execfile("C:\\Users\\v.marimuthu\\Desktop\\SCD_TEST\\SCD_DESKTOP_EX.py")
                break
        else:
            print "file is not loaded"
            time.sleep(10)

