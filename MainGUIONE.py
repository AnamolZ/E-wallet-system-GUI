import customtkinter
from tkinter import *
import tkinter as tk
import csv
import random
import datetime
import sys
import socket
import socket
import tqdm
import os
import time
from threading import Thread
import threading

DATA_BASE_FILE_PATH = "/home/exteronous/Code/E-wallet-System/data_base.csv"
TRANSACTION_HISTORY_FILE_PATH= "/home/exteronous/Code/E-wallet-System/transaction_history.csv"
ADMIN_FILE_PATH="/home/exteronous/Code/E-wallet-System/admin_data.csv"

date_time,user_transaction_info_list=datetime.datetime.now(),[]
store_user_credentials,admin_info=[],[]

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("E-WALLET SYSTEM")
app.geometry("420x250")
app.minsize(420, 250)
app.maxsize(420, 250)

acc_num,acc_pass=tk.StringVar(),tk.StringVar()
load_amt,pass_w=tk.StringVar(),tk.StringVar()
phno,trans_amt=tk.StringVar(),tk.StringVar()
rece_accnum,sndr_accpass=tk.StringVar(),tk.StringVar()
fname,lname=tk.StringVar(),tk.StringVar()
phno,email=tk.StringVar(),tk.StringVar()
pas,amnt=tk.StringVar(),tk.StringVar()
srch_vlu=tk.StringVar()

def listening():
    SERVER_HOST,SERVER_PORT,BUFFER_SIZE= "192.168.2.183",5001,4096
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(0)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept() 
    print(f"[+] {address} is connected.")
    received = client_socket.recv(BUFFER_SIZE).decode().split()
    filename = "/home/exteronous/Code/redata.csv"
    with open(filename, "w") as f:
        for i in received:f.write(i + "\n")
    client_socket.close()
    s.close()
    time.sleep(10)

def receiving():
    BUFFER_SIZE = 4096
    s = socket.socket()
    host,port= "192.168.2.183",5002
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    filename = DATA_BASE_FILE_PATH
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:break
            s.sendall(bytes_read)
    s.close()

def clear():
    list = app.grid_slaves()
    for l in list:l.destroy()

def frame_text(t):frame_label=customtkinter.CTkLabel(master=app, text=t).grid(row=4,column=2)

def retrieve_data():
    def cal_mny(arg):
        passw,phonenumber= pass_w.get(),phno.get()
        transfering_amount=load_amt.get()
        if(arg=="+"):fun(int(sender_total_amount)+int(transfering_amount))
        elif(arg=="-"):fun(int(sender_total_amount)-int(transfering_amount))
    def fun(calculated_sender_amount):
        with open(DATA_BASE_FILE_PATH) as read_file:
            read_sender_file = read_file.read()
            if account_number in read_sender_file:read_sender_file = read_sender_file.replace(str(sender_total_amount),str(calculated_sender_amount))
        with open(DATA_BASE_FILE_PATH,"w") as write_file:write_file.write(read_sender_file)
    def l_m(confirm_button):
        user_info_label=customtkinter.CTkLabel(master=app,text="\n"+data_value).grid(row=0, column=2)
        loadamt_entry=customtkinter.CTkEntry(master=app,textvariable=load_amt,placeholder_text="Amount",width=170,height=30).grid(row=0, column=1, padx=15, pady=5)
        phno_entry=customtkinter.CTkEntry(master=app,textvariable=phno,placeholder_text="Phone Number",width=170,height=30).grid(row=1, column=1, padx=15, pady=0)
        passacc_entry=customtkinter.CTkEntry(master=app,textvariable=pass_w,placeholder_text="Password",width=170,height=30).grid(row=2, column=1, padx=15, pady=10)
        confirm_button
        back_button=customtkinter.CTkButton(master=app, text="Back", command=lambda:[clear(),app.title("E-WALLET SYSTEM"),retrieve_data()],width=170,height=30).grid(row=4,column=1,padx=15,pady=10)
    def load_money():l_m(customtkinter.CTkButton(master=app, text="Confirm",command=lambda:[frame_text("Transaction Done Sucessfully"),cal_mny("+")],width=170,height=30).grid(row=3, column=1, padx=15, pady=0))
    def withdraw_money():l_m(customtkinter.CTkButton(master=app, text="Confirm",command=lambda:[frame_text("Transaction Done Sucessfully"),cal_mny("-")],width=170,height=30).grid(row=3, column=1, padx=15, pady=0))

    def transaction():
        def transaction_handler():
            sender_account_number = acc_num.get()
            sender_key_pass = sndr_accpass.get()
            transferring_amount = trans_amt.get()
            receiver_account_number = rece_accnum.get()
            with open(DATA_BASE_FILE_PATH) as read_file:
                transaction_data = csv.reader(read_file)
                header = next(transaction_data)
                for per_transaction_data in transaction_data:
                    user_transaction_info_list.append(per_transaction_data)
            for row in user_transaction_info_list:
                if sender_account_number in row:
                    sender_total_amount = row[-1]
                if receiver_account_number in row:
                    receiver_total_amount = row[-1]
            calculated_sender_amount = int(sender_total_amount)-int(transferring_amount)
            calculated_receiver_amount = int(receiver_total_amount)+int(transferring_amount)
            if  calculated_sender_amount > 500:
                with open(DATA_BASE_FILE_PATH) as read_file:
                    read_sender_file = read_file.read()
                    if sender_account_number in read_sender_file:
                        read_sender_file = read_sender_file.replace(str(sender_total_amount),str(calculated_sender_amount))
                with open(DATA_BASE_FILE_PATH,"w") as write_file:
                    write_file.write(read_sender_file)
                with open(DATA_BASE_FILE_PATH) as read_file:
                    read_file_receiver=read_file.read()
                    if receiver_account_number in read_file_receiver:
                        read_file_receiver=read_file_receiver.replace(str(receiver_total_amount),str(calculated_receiver_amount))
                with open(DATA_BASE_FILE_PATH,"w") as write_file:
                    write_file.write(read_file_receiver)
                with open(TRANSACTION_HISTORY_FILE_PATH,"w") as write_file:
                    write_file.write("\n"+str(transferring_amount) + " Transfered From " + str(sender_account_number) + " To "+str(receiver_account_number)+str(date_time))

        user_info_label = customtkinter.CTkLabel(master=app, text="\n"+data_value).grid(row=0, column=2, padx=0, pady=0)
        transferring_amt_entry = customtkinter.CTkEntry(master=app,textvariable=trans_amt,placeholder_text="Amount",width=170,height=30).grid(row=0, column=1, padx=0, pady=15)
        receiver_acc_num_entry = customtkinter.CTkEntry(master=app,textvariable=rece_accnum,placeholder_text="Receiver Account Number",width=170,height=30).grid(row=1, column=1, padx=0, pady=0)
        sender_acc_pass_entry = customtkinter.CTkEntry(master=app,textvariable=sndr_accpass,placeholder_text="Sender Account Password",width=170,height=30).grid(row=2, column=1, padx=0, pady=15)
        send_button = customtkinter.CTkButton(master=app,text="Send",command=lambda:[frame_text("Money Transferred Sucessfully"),transaction_handler()],width=170,height=30).grid(row=3, column=1, padx=0, pady=0)
        back_button = customtkinter.CTkButton(master=app,text="Back",command=lambda:[clear(),app.title("E-WALLET SYSTEM"),retrieve_data()],width=170,height=30).grid(row=4, column=1, padx=0, pady=15)

    account_number,key_pass=acc_num.get(),acc_pass.get()
    try:
        with open(DATA_BASE_FILE_PATH) as read_file:
            bouncer_data = csv.reader(read_file)
            header = next(bouncer_data)
            for user_credentials in bouncer_data:store_user_credentials.append(user_credentials)
            app.geometry("420x250")
            app.minsize(420, 250)
            app.maxsize(420, 250)
        for i in range(len(store_user_credentials)):
            if account_number in store_user_credentials[i][5] and key_pass in store_user_credentials[i][4]:
                sender_total_amount = store_user_credentials[i][6]
                user_data_label_first = customtkinter.CTkLabel(master=app,text="Account Number "+store_user_credentials[i][5]+"\nEmail "+store_user_credentials[i][3]+"\nPhone Number "+store_user_credentials[i][2]).grid(row=0, column=1, padx=80, pady=20)
                user_data_label_second = customtkinter.CTkLabel(master=app,text="Amount "+store_user_credentials[i][6]).grid(row=0, column=0, padx=0, pady=0)
                data_value = "Amount "+store_user_credentials[i][6]+"\n"+"Account Number "+store_user_credentials[i][5]+"\nEmail "+store_user_credentials[i][3]+"\nPhone Number "+store_user_credentials[i][2]
                LoadMoney_button = customtkinter.CTkButton(master=app, text="Load Money",command=lambda:[clear(),app.title("Load Money"),load_money()]).grid(row=1, column=0, padx=0, pady=10)
                WithDrawMoney_button = customtkinter.CTkButton(master=app, text="WithDraw Money",command=lambda:[clear(),app.title("WithDraw Money"),withdraw_money()]).grid(row=2, column=0, padx=0, pady=10)
                Transaction_button = customtkinter.CTkButton(master=app, text="Transaction",command=lambda:[clear(),app.title("Transaction"),transaction()]).grid(row=3, column=0, padx=0, pady=10)
                Refresh_button = customtkinter.CTkButton(master=app, text="Refresh",command=lambda:[clear(),retrieve_data()]).grid(row=1, column=1, padx=0, pady=0)                
                Logout_button = customtkinter.CTkButton(master=app, text="LogOut",command=lambda:[clear(),main_login()]).grid(row=2, column=1, padx=0, pady=0)
                Quit_button = customtkinter.CTkButton(master=app, text="Quit", command=quit).grid(row=3, column=1, padx=0, pady=0)
                break
        else:main_login()
    except Exception as Error:print(Error)

def entry():
    acc_num_entry = customtkinter.CTkEntry(master=app,textvariable=acc_num,placeholder_text="ID Number").grid(row=0, column=1, padx=130, pady=30)
    acc_pass_entry = customtkinter.CTkEntry(master=app,textvariable=acc_pass,placeholder_text="ID Password").grid(row=1, column=1, padx=0, pady=0)
    back_button = customtkinter.CTkButton(master=app, text="Back", command=main_login).grid(row=3, column=1, padx=0, pady=0)

def user_login_section():
    app.title("User Login")
    entry()
    login_button = customtkinter.CTkButton(master=app, text="Login", command=lambda:[clear(),app.title("E-WALLET SYSTEM"),retrieve_data()]).grid(row=2, column=1, padx=0, pady=30)

def admin_login_section():
    def value_get():
        app.title("User Account Detail")
        app.geometry("500x250")
        app.minsize(500, 250)
        app.maxsize(500, 250)
        search_result = srch_vlu.get()
        word = search_result
        with open(DATA_BASE_FILE_PATH,'r') as f:
            lines = f.read().split("\n")
        for i,line in enumerate(lines):
            if word in line:
                a = i+1
        with open(DATA_BASE_FILE_PATH,'r') as f:
            if word == "":
                user_data()
            elif word not in line:
                user_data()
            else:
                frame_label= customtkinter.CTkLabel(master=app, text=f.readlines()[a-1]).grid(padx=0,pady=30)
                back_button = customtkinter.CTkButton(master=app, text="Back",command=lambda:[clear(),user_data()]).grid(padx=0,pady=100)

    def account_creation():
        app.title("Account Creation")
        app.geometry("400x320")
        app.minsize(400, 320)
        app.maxsize(400, 320)
        print(user_data)
        def save_file():
            acc_number=random.randint(152749224,965489336)
            f = fname.get()
            l = lname.get()
            p = phno.get()
            e = email.get()
            pa = pas.get()
            a = amnt.get()
            user_data=f+","+l+","+p+","+e+","+pa+","+acc_num+","+a
            with open(DATA_BASE_FILE_PATH,"a+") as append_file:append_file.write(user_data)
        firstname_entry = customtkinter.CTkEntry(master=app,textvariable=fname,placeholder_text="First Name").grid(row=1,padx=130,pady=10)
        lastname_entry = customtkinter.CTkEntry(master=app,textvariable=lname,placeholder_text ="Last Name").grid(row=2,padx=130,pady=0)
        phonenumber_entry = customtkinter.CTkEntry(master=app,textvariable=phno,placeholder_text="Phone Number").grid(row=3,padx=130,pady=10)
        email_entry = customtkinter.CTkEntry(master=app,textvariable=email,placeholder_text="Email").grid(row=4,padx=130,pady=0)
        password_entry = customtkinter.CTkEntry(master=app,textvariable=pas,placeholder_text="Password").grid(row=5,padx=130,pady=10)
        entry_amount = customtkinter.CTkEntry(master=app,textvariable=amnt,placeholder_text="Pre Amount").grid(row=6,padx=130,pady=0)
        submit_button = customtkinter.CTkButton(master=app,text="Submit",command=lambda:[clear(),save_file(),admin_widget()]).grid(row=7,pady=10)
        back_button = customtkinter.CTkButton(master=app,text="Back",command=lambda:[clear(),admin_widget()]).grid(row=8,pady=0)
    def transaction_history():
        try:
            app.title("Transaction History")
            with open(TRANSACTION_HISTORY_FILE_PATH) as read_file:
                transaction_data = read_file.read()
                frame_label= customtkinter.CTkLabel(master=app, text=transaction_data).grid(padx=0,pady=30)
                back_button = customtkinter.CTkButton(master=app, text="Back",command=lambda:[clear(),admin_widget()]).grid(padx=0,pady=10)
        except Exception as Error:
            print("ok")

    def user_data():
        def dl():
            search_result = srch_vlu.get()
            word = search_result
            if len(word) >=2:
                with open(DATA_BASE_FILE_PATH,"r+") as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        if word not in line:
                            f.write(line)
                    f.truncate()
            else:
                user_data()
        app.geometry("800x350")
        app.title("User Data")
        app.minsize(800, 350)
        app.maxsize(800, 350)
        with open(DATA_BASE_FILE_PATH) as f1:
            f=f1.read()
        frame_label= customtkinter.CTkLabel(master=app, text=f).grid(padx=120,pady=30)
        search_entry = customtkinter.CTkEntry(master=app,textvariable=srch_vlu).grid(row=1,pady=0)
        search_button = customtkinter.CTkButton(master=app,text="Search",command=lambda:[clear(),value_get()]).grid(row=2,pady=10)
        back_button = customtkinter.CTkButton(master=app,text="Back",command=lambda:[clear(),admin_widget()]).grid(row=3,column=0)
        delete_button = customtkinter.CTkButton(master=app,text="Delete",command=lambda:[dl()]).grid(row=4,pady=10)
    def admin_widget():
        app.title("Admin Control Panel")
        app.geometry("400x250")
        app.minsize(400, 250)
        app.maxsize(400, 250)
        view_user = customtkinter.CTkButton(master=app,text="View Server Data",command=lambda:[clear(),user_data()]).grid(padx=120,pady=30)
        accreg_user = customtkinter.CTkButton(master=app,text="Create Account",command=lambda:[clear(),account_creation()]).grid(padx=120,pady=0)
        view_userhistory = customtkinter.CTkButton(master=app,text="View Transaction History",command=lambda:[clear(),transaction_history()]).grid(padx=120,pady=30)
        Back = customtkinter.CTkButton(master=app,text="Back",command=lambda:[clear(),main_login()]).grid(padx=120,pady=0)
    def redirect():
        account_number=acc_num.get()
        key_pass=acc_pass.get()
        if account_number == "Anamol" and key_pass in "anmol1379":
            clear()
            app.title("Admin")
            admin_widget()
        else:
            main_login()
    app.title("Admin Login")  
    entry()
    login_button = customtkinter.CTkButton(master=app, text="Login", command=lambda:[redirect()]).grid(row=2, column=1, padx=0, pady=30)

def info():
    app.title("ABOUT US")
    aboutusnote = customtkinter.CTkLabel(master=app, text="CloudX is designed to \nprovide the better \nE-WALLET MONETRY TRANSACTION \nwith better client support\n\n\n\n\nDeveloped by EXTERONOUS Head Team").grid(row=3, column=1, padx=80, pady=80)

def main_login():
    app.title("E-WALLET SYSTEM")
    userlogin_button = customtkinter.CTkButton(master=app, text="User Login", command=user_login_section).grid(row=0, column=1, padx=130, pady=30)
    adminlogin_button = customtkinter.CTkButton(master=app, text="Admin Login", command=admin_login_section).grid(row=1, column=1, padx=0, pady=0)
    aboutus_button = customtkinter.CTkButton(master=app, text="About Us", command=lambda: [clear(), info()]).grid(row=2, column=1, padx=0, pady=30)
    quit_button = customtkinter.CTkButton(master=app, text="Quit", command=quit).grid(row=3, column=1, padx=0, pady=0)

def fileupdating():
    while True:
        listening()
        receiving()
def maingui():
    main_login()

if __name__ == '__main__':
    Thread(target = maingui).start()
    Thread(target = fileupdating).start()

app.mainloop()