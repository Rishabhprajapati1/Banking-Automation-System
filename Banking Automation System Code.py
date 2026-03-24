from tkinter import Tk,Label,Frame,Entry,Button,Canvas,messagebox,Toplevel,simpledialog,Scrollbar,BOTTOM,X,Y,RIGHT,LEFT,BOTH,filedialog
from tkinter.ttk import Combobox,Treeview,Style
from tkcalendar import Calendar
from datetime import date
import time
from PIL import Image,ImageTk,ImageFilter #pip install pillow on cmd or terminal
import random
import generator
import sqlite3
import mail
import os,shutil

generator.generate_tables()

#to create root window
root=Tk()
root.state("zoomed")
root.resizable(width=False,height=False)
root.configure(bg="#A9A0AC")

#making header title
Title=Label(root,text="BANKING AUTOMATION SYSTEM",font=('georgia bold',58,'bold'),bg="black",fg="#F0F2F7",highlightbackground="white",highlightthickness=3)
Title.pack()



list_logos=['default.jpg','logo.jpg','logo1.jpg','logo2.png','logo3.jpg','logo4.jpg','logo5.png']#importing all image

def update_time():#to update time every time code run
    dt=time.strftime("%A,%d-%b-%Y ⌚%r")
    lbl_date.config(text=dt)
    root.after(1000,update_time)

def update_logo():#to update img every sec 
    logo=random.choice(list_logos)
    img1=Image.open(logo).resize((250,150))
    img_pil=ImageTk.PhotoImage(img1,master=root)
    lbl_logo1.configure(image=img_pil)
    lbl_logo1.image=img_pil
    lbl_logo2.configure(image=img_pil)
    lbl_logo2.image=img_pil
    root.after(1000,update_logo)

#making date and time
lbl_date=Label(root,text='',font=('arial',25,'bold'),bg="#F5F4F7",highlightbackground="black",highlightthickness=3)
lbl_date.pack()
update_time()

#to make logo and it's place(left corner)
img1=Image.open('logo.jpg').resize((250,150))
img_pil=ImageTk.PhotoImage(img1,master=root)
lbl_logo1=Label(root,image=img_pil)
lbl_logo2=Label(root,image=img_pil)
lbl_logo1.place(relx=0,rely=0)
lbl_logo2.place(relx=0.867,rely=0)
update_logo()

def main_frame():#to make a frame on middle of root window
    # 1. Get screen dimensions to calculate exact placement
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    fh = int(sh * 0.8) # Frame height is 80% of the screen height

    # 2. Update the refresh function to work with Canvas text
    def refresh_captcha():
        nonlocal gen_captcha
        gen_captcha=generator.generate_captcha()
        lbl_captcha.config(text=gen_captcha) # Updates the drawn text

    # 3. Create a Canvas instead of a Frame
    frm = Canvas(root, highlightbackground="black", highlightthickness=3)
    frm.place(relx=0, rely=0.145, relwidth=1, relheight=0.8)

    # 4. Add the blurred background directly to the Canvas
    try:
        bg_img = Image.open('wallpaper2.avif') # ⚠️ CHANGE THIS to your image name
        bg_img = bg_img.resize((sw, fh))
        blurred_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        frm.bg_photo = ImageTk.PhotoImage(blurred_img) 
        frm.create_image(0, 0, image=frm.bg_photo, anchor="nw")
    except Exception as e:
        print(f"Image Error: {e}") # Just in case the image isn't found

    # 5. Draw Transparent Text and Place Interactive Widgets

    def call_fp_frame():
        frm.destroy()
        fp_frame()

    def reset():
            e_acn.delete(0,"end")
            e_pass.delete(0,"end")
            e_captchaa.delete(0,"end")
            e_acn.focus()

    def login():
        utype=cb_user.get()
        uacn=e_acn.get()
        upass=e_pass.get()
        ucaptcha=e_captchaa.get()
        
        if len(uacn)==0 or len(upass)==0 or len(ucaptcha)==0:
            messagebox.showerror("Account","Empty field not valid")
            return
        

        if ucaptcha!=gen_captcha.replace(' ',''):
            messagebox.showerror("Login","Invalid captcha")
            return
        


        if utype=="Admin" and uacn=="0" and upass=="0":
            frm.destroy()
            admin_frame()

        elif utype=="Customer":
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=? and password=? '
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Login","Invalid ACN/Pass")
            else:
                frm.destroy()
                customer_frame(tup)
        else:
            messagebox.showerror("Login","Invalid user type")

    lbl_acn=Label(frm,text="Account.No🔑:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_acn.place(relx=.32,rely=.18)

    e_acn=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black")
    e_acn.place(relx=.47,rely=.18)

    lbl_pass=Label(frm,text="Password⛔:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_pass.place(relx=.32,rely=.30)

    e_pass=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black",show=('*'))
    e_pass.place(relx=.47,rely=.30)
    
    lbl_user=Label(frm,text="User👤:", font=('Rockwell Condensed',30,'bold'),bg="white",fg='black')
    lbl_user.place(relx=.32,rely=.42)
    
    cb_user=Combobox(frm,values=['Customer','Admin'],font=('Rockwell Condensed',28,'bold'),background='blue',)
    cb_user.current(0)
    cb_user.place(relx=.47,rely=.42)

    gen_captcha=generator.generate_captcha()
    lbl_captcha=Label(frm,text=gen_captcha, font=('Rockwell Condensed',28,'bold'),bg='grey',width=15,fg='white')
    lbl_captcha.place(relx=.47,rely=.52)

    btn_refresh=Button(frm,text='🔃',font=('Rockwell Condensed',17,'bold'),bd=5,command=refresh_captcha)
    btn_refresh.place(relx=.62,rely=.52)

    lbl_captchaa=Label(frm,text="Captcha:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_captchaa.place(relx=.32,rely=.60)

    e_captchaa=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black")
    e_captchaa.place(relx=.47,rely=.60)

    btn_login=Button(frm,text='Login',font=('Rockwell Condensed',17,'bold'),bd=5,command=login)
    btn_login.place(relx=.50,rely=.72)

    btn_reset=Button(frm,text='Reset',font=('Rockwell Condensed',17,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.56,rely=.72)

    btn_fp=Button(frm,text='Forget Password',font=('Rockwell Condensed',18,'bold'),bd=5,command=call_fp_frame)
    btn_fp.place(relx=.502,rely=.80)

def customer_frame(cust_tup):
     # 1. Get screen dimensions to calculate exact placement
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    fh = int(sh * 0.8) # Frame height is 80% of the screen height

    # 2. Update the refresh function to work with Canvas text

    # 3. Create a Canvas instead of a Frame
    frm = Canvas(root, highlightbackground="black", highlightthickness=3)
    frm.place(relx=0, rely=0.145, relwidth=1, relheight=0.8)

    # 4. Add the blurred background directly to the Canvas
    try:
        bg_img = Image.open('wallpaper.jpg') # ⚠️ CHANGE THIS to your image name
        bg_img = bg_img.resize((sw, fh))
        blurred_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        frm.bg_photo = ImageTk.PhotoImage(blurred_img) 
        frm.create_image(0, 0, image=frm.bg_photo, anchor="nw")
    except Exception as e:
        print(f"Image Error: {e}") # Just in case the image isn't found

    # 5. Draw Transparent Text and Place Interactive Widgets

    def logout():
        frm.destroy()
        main_frame()

    def upload_pic():
        filepath=filedialog.askopenfilename()
        shutil.copy(filepath,f"{cust_tup[0]}.jpg")
        img_profile=Image.open(f"{cust_tup[0]}.jpg").resize((195,150))
        img_profilepil=ImageTk.PhotoImage(img_profile,master=root)
        lbl_profilepic=Label(frm,image=img_profilepil)
        lbl_profilepic.image=img_profilepil
        lbl_profilepic.place(relx=0,rely=.06)


    lbl_wel=Label(frm,text=f"Welcome {cust_tup[1]}...", font=('Rockwell Condensed',28,'bold'),bg='black',fg='white')
    lbl_wel.place(relx=.0,rely=.0)

    btn_logout=Button(frm,text='Logout',font=('Rockwell Condensed',18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.952,rely=.0)


    if os.path.exists(f'{cust_tup[0]}.jpg'):
        img_profile=Image.open(f"{cust_tup[0]}.jpg").resize((195,150))
    else:                   
        img_profile=Image.open("default.jpg").resize((195,150))

    img_profilepil=ImageTk.PhotoImage(img_profile,master=root)
    lbl_profilepic=Label(frm,image=img_profilepil)
    lbl_profilepic.image=img_profilepil
    lbl_profilepic.place(relx=0,rely=.06)

    btn_update=Button(frm,text='🔃',font=('Rockwell Condensed',16,'bold'),bd=5,command=upload_pic)
    btn_update.place(relx=.1068,rely=.181)


    def details():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        Title=Label(ifrm,text="This Is View Detail Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from account where acno=?'
        curobj.execute(query,(cust_tup[0],))
        tup=curobj.fetchone()
        conobj.close()

        details=f"""
Account no         ==> {tup[0]}
Customer Name      ==> {tup[1]}
Customer Email     ==> {tup[5]}
Customer Mobile no ==> {tup[6]}
Available Balance  ==> {tup[7]}
Customer Address   ==> {tup[8]}
Account open date  ==> {tup[10]}
Customer Aadhar no ==> {tup[3]}
"""
        lbl_details=Label(ifrm,text=details,
                          font=('Courier', 25, 'bold'),bg='white',fg="#030303",border=4,highlightbackground="black",highlightthickness=5,justify='left')
        lbl_details.place(relx=.14,rely=.25)


    def edit():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        Title=Label(ifrm,text="This Is Edit Detail Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from account where acno=?'
        curobj.execute(query,(cust_tup[0],))
        tup=curobj.fetchone()
        conobj.close()

        def edit_db():
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadhar=e_adhar.get()
            upan=e_pan.get()
            uadr=e_adr.get()
            udob=e_dob.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update account set name=?,email=?,mob=?,aadhar=?,adr=?,pan=?,dob=? where acno=?'
            curobj.execute(query,(uname,uemail,umob,uadhar,upan,uadr,udob,cust_tup[0]))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Edit Details","Account details updated succesfully")

        def reset():
            e_name.delete(0,"end")
            e_pan.delete(0,"end")
            e_adhar.delete(0,"end")
            e_mob.delete(0,"end")
            e_email.delete(0,"end")
            e_adr.delete(0,"end")
            e_dob.delete(0,"end")
            return
        


        lbl_name=Label(ifrm,text="NAME:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_name.place(relx=.1,rely=.24)

        e_name=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_name.place(relx=.1,rely=.28)

        lbl_mob=Label(ifrm,text="MOBILE NO:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_mob.place(relx=.1,rely=.35)

        e_mob=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_mob.place(relx=.1,rely=.39)

        lbl_add=Label(ifrm,text="ADDRESS:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_add.place(relx=.1,rely=.46)

        e_adr=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_adr.place(relx=.1,rely=.50)

        lbl_email=Label(ifrm,text="EMAIL ID:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_email.place(relx=.1,rely=.59)

        e_email=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_email.place(relx=.1,rely=.63)

        lbl_adhar=Label(ifrm,text="AADHAR NO:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_adhar.place(relx=.55,rely=.24)

        e_adhar=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_adhar.place(relx=.55,rely=.28)
        
        lbl_pan=Label(ifrm,text="PAN No:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_pan.place(relx=.55,rely=.35)

        e_pan=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_pan.place(relx=.55,rely=.39)

        lbl_dob=Label(ifrm,text="Date Of Birth:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_dob.place(relx=.55,rely=.46)

        e_dob=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=32)
        e_dob.place(relx=.55,rely=.50)

        e_name.insert(0,tup[1])
        e_email.insert(0,tup[5])
        e_mob.insert(0,tup[6])
        e_adhar.insert(0,tup[3])
        e_adr.insert(0,tup[8])
        e_pan.insert(0,tup[4])
        e_dob.insert(0,tup[9])
        
        btn_update=Button(ifrm,text='Update',font=('Rockwell Condensed',20,'bold'),bd=5,width=10,command=edit_db)
        btn_update.place(relx=.58,rely=.62)

        btn_reset=Button(ifrm,text='Reset',font=('Rockwell Condensed',20,'bold'),bd=5,width=10,command=reset)
        btn_reset.place(relx=.70,rely=.62)

    def deposite():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        def deposite_db():
            uamt=float(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query1='update account set bal=bal+? where acno=?'
            query2='insert into txn_history values(?,?,?,?,?,?)'
            
            curobj.execute(query1,(uamt,cust_tup[0]))
            curobj.execute(query2,(None,cust_tup[0],uamt,'CR.',ubal+uamt,time.strftime("%d-%m-%Y %r")))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposited",f"""Amount {uamt} deposited ,
                                Updated Bal:{ubal+uamt}""")


        Title=Label(ifrm,text="This Is Deposite Amount Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        lbl_amt=Label(ifrm,text='Amount:',font=('Rockwell Condensed',30,'bold'),bg="black",fg="white")
        lbl_amt.place(relx=.28,rely=.19)

        e_amt=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=25)
        e_amt.place(relx=.38,rely=.2)

        btn_deposite=Button(ifrm,text='Deposite',font=('Rockwell Condensed',20,'bold'),bd=5,command=deposite_db)
        btn_deposite.place(relx=.4,rely=.35)


    def withdraw():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        Title=Label(ifrm,text="This Is Withdraw Amount Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        def withdraw_db():
            uamt=float(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='update account set bal=bal-? where acno=?'
                query2='insert into txn_history values(?,?,?,?,?,?)'
                
                curobj.execute(query1,(uamt,cust_tup[0]))
                curobj.execute(query2,(None,cust_tup[0],uamt,'DB.',ubal-uamt,time.strftime("%d-%m-%Y %r")))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"""Amount {uamt} Withdrawed ,
                                    Updated Bal:{ubal-uamt}""")
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")


        lbl_amt=Label(ifrm,text='Amount:',font=('Rockwell Condensed',30,'bold'),bg="black",fg="white")
        lbl_amt.place(relx=.28,rely=.19)

        e_amt=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=25)
        e_amt.place(relx=.38,rely=.2)

        btn_withdraw=Button(ifrm,text='Withdraw',font=('Rockwell Condensed',20,'bold'),bd=5,command=withdraw_db)
        btn_withdraw.place(relx=.4,rely=.35)


    def transfer():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        Title=Label(ifrm,text="This Is Transfer Amount Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        def transfer_db():
            toacn=e_to.get()
            uamt=float(e_amt.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            to_details=curobj.fetchone()[0]
            conobj.close()
            if to_details==None:
                messagebox.showerror("Transfer",f"Receivers account does not exist:{toacn}")
                return

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='update account set bal=bal-? where acno=?'
                query2='update account set bal=bal+? where acno=?'
                query3='insert into txn_history values(?,?,?,?,?,?)'
                query4='insert into txn_history values(?,?,?,?,?,?)'
                
                curobj.execute(query1,(uamt,cust_tup[0]))
                curobj.execute(query2,(uamt,toacn))
                curobj.execute(query3,(None,cust_tup[0],uamt,'DB.',ubal-uamt,time.strftime("%d-%m-%Y %r")))
                curobj.execute(query4,(None,toacn,uamt,'CR.',ubal+uamt,time.strftime("%d-%m-%Y %r")))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"""Amount {uamt} transfered ,
                                    Updated Bal:{ubal-uamt}""")
            else:
                messagebox.showerror("Transfer",f"Insufficient Balance:{ubal}")

        lbl_to=Label(ifrm,text="""Receiver's Account no:""",font=('Rockwell Condensed',20,'bold'),bg="black",fg="white")
        lbl_to.place(relx=.20,rely=.20)

        e_to=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=25)
        e_to.place(relx=.38,rely=.2)


        lbl_amt=Label(ifrm,text='Amount:',font=('Rockwell Condensed',20,'bold'),bg="black",fg="white")
        lbl_amt.place(relx=.28,rely=.41)

        e_amt=Entry(ifrm,font=('Courier',24,'bold'),bd=5,background='white',fg="black",width=25)
        e_amt.place(relx=.38,rely=.40)

        btn_transfer=Button(ifrm,text='Transfer',font=('Rockwell Condensed',20,'bold'),bd=5,command=transfer_db)
        btn_transfer.place(relx=.45,rely=.50)

    def history():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.14,rely=0.13,relwidth=.84,relheight=0.82)

        Title=Label(ifrm,text="This Is View History Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        # 1. Styling the Table
        style = Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        rowheight=35,
                        fieldbackground="white",
                        font=('Courier', 13, 'bold'))
        style.configure("Treeview.Heading", font=('Rockwell Condensed', 18, 'bold'), background="black", foreground="white")
        style.map('Treeview', background=[('selected', 'pink')])

        # 2. Creating a Frame for the Table and Scrollbar
        tv_frame = Frame(ifrm)
        tv_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        # 3. Setting up the Scrollbar
        tv_scroll = Scrollbar(tv_frame)
        tv_scroll.pack(side=RIGHT, fill=Y)

        # 4. Defining the Treeview Table
        tv = Treeview(tv_frame, yscrollcommand=tv_scroll.set, selectmode="extended")
        tv.pack(side=LEFT, fill=BOTH, expand=True)
        tv_scroll.config(command=tv.yview)

        # 5. Defining Table Columns
        tv['columns'] = ('Txn ID', 'Amount', 'Type', 'Updated Balance', 'Date & Time')
        tv.column('#0', width=0, stretch=False) # Hiding the default empty first column
        tv.column('Txn ID', anchor='center', width=100)
        tv.column('Amount', anchor='center', width=150)
        tv.column('Type', anchor='center', width=100)
        tv.column('Updated Balance', anchor='center', width=200)
        tv.column('Date & Time', anchor='center', width=250)

        # 6. Setting Table Headings
        tv.heading('#0', text='', anchor='center')
        tv.heading('Txn ID', text='Txn ID', anchor='center')
        tv.heading('Amount', text='Amount', anchor='center')
        tv.heading('Type', text='Type', anchor='center')
        tv.heading('Updated Balance', text='Updated Balance', anchor='center')
        tv.heading('Date & Time', text='Date & Time', anchor='center')

        # 7. Fetching Data from the Database
        try:
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'SELECT * FROM txn_history WHERE acno=?'
            curobj.execute(query, (cust_tup[0],))
            rows = curobj.fetchall()
            conobj.close()

            # 8. Inserting Data into the Table
            # Assuming row = (id, acno, amount, type, balance, date)
            count = 0
            for row in rows:
                if count % 2 == 0:
                    tv.insert(parent='', index='end', iid=count, text='', values=(row[0], row[2], row[3], row[4], row[5]), tags=('evenrow',))
                else:
                    tv.insert(parent='', index='end', iid=count, text='', values=(row[0], row[2], row[3], row[4], row[5]), tags=('oddrow',))
                count += 1
                
            # Add alternating row colors for better readability
            tv.tag_configure('evenrow', background="#f2f2f2")
            tv.tag_configure('oddrow', background="white")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch history: {e}")
    
    btn_detail=Button(frm,text='View Details',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=details)
    btn_detail.place(relx=.0,rely=.3)

    btn_edit=Button(frm,text='Edit Details',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=edit)
    btn_edit.place(relx=.0,rely=.4)

    btn_deposite=Button(frm,text='Deposite Amount',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=deposite)
    btn_deposite.place(relx=.0,rely=.5)

    btn_withdraw=Button(frm,text='Withdraw Amount',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=withdraw)
    btn_withdraw.place(relx=.0,rely=.6)

    btn_transfer=Button(frm,text='Transfer Amount',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=transfer)
    btn_transfer.place(relx=.0,rely=.7)

    btn_history=Button(frm,text='View History',font=('Rockwell Condensed',16,'bold'),bd=5,width=18,command=history)
    btn_history.place(relx=.0,rely=.8)

def admin_frame():
     # 1. Get screen dimensions to calculate exact placement
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    fh = int(sh * 0.8) # Frame height is 80% of the screen height

    # 2. Update the refresh function to work with Canvas text

    # 3. Create a Canvas instead of a Frame
    frm = Canvas(root, highlightbackground="black", highlightthickness=3)
    frm.place(relx=0, rely=0.145, relwidth=1, relheight=0.8)

    # 4. Add the blurred background directly to the Canvas
    try:
        bg_img = Image.open('wallpaper7.jpg') # ⚠️ CHANGE THIS to your image name
        bg_img = bg_img.resize((sw, fh))
        blurred_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        frm.bg_photo = ImageTk.PhotoImage(blurred_img) 
        frm.create_image(0, 0, image=frm.bg_photo, anchor="nw")
    except Exception as e:
        print(f"Image Error: {e}") # Just in case the image isn't found

    # 5. Draw Transparent Text and Place Interactive Widgets

    def logout():
        frm.destroy()
        main_frame()

    def open():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.08,rely=0.25,relwidth=.85,relheight=0.68)

        def save():
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadhar=e_adhar.get()
            upan=e_pan.get()
            uadr=e_add.get()
            udob=e_dob.get()
            ubal=0
            upass=generator.generate_password()
            uopendate=time.strftime("%d-%b-%Y %r")

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into account values(?,?,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(None,uname,upass,uadhar,upan,uemail,umob,ubal,uadr,udob,uopendate))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Account","Account opened succesfully")
            e_name.delete(0,"end")
            e_email.delete(0,"end")
            e_mob.delete(0,"end")
            e_adhar.delete(0,"end")
            e_pan.delete(0,"end")
            e_add.delete(0,"end")
            e_dob.delete(0,"end")

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query="select max(acno) from account"
            curobj.execute(query)
            uacn=curobj.fetchone()[0]

            usub="Account Opened in Dhink-Chika Bank"
            utext=f'''Dear {uname},
            We have successfully opened your account in Rishabh ji ke bank mein.
            Your ACN={uacn}
            Your pass={upass}

            thanks,
            Dhink-Chika bank,from Mangal'''
            try:
                mail.send_acn_cred(uemail,usub,utext)
                messagebox.showinfo("Account","Creadantail will be sent on given mail id.")
            except:
                msg=""""Something went wrong,
                kindly check your internet connection or mail id"""
                messagebox.showerror("Account",msg)

        Title=Label(ifrm,text="This Is Open Account Window",font=('georgia bold',30,'bold'),bg="black",fg="#FBFBFC",highlightbackground="white",highlightthickness=3)
        Title.pack()

        lbl_name=Label(frm,text="NAME:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_name.place(relx=.1,rely=.34)

        e_name=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_name.place(relx=.1,rely=.38)

        lbl_mob=Label(frm,text="MOBILE NO:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_mob.place(relx=.1,rely=.45)

        e_mob=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_mob.place(relx=.1,rely=.49)

        lbl_add=Label(frm,text="ADDRESS:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_add.place(relx=.1,rely=.56)

        e_add=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_add.place(relx=.1,rely=.60)

        lbl_email=Label(frm,text="EMAIL ID:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_email.place(relx=.1,rely=.69)

        e_email=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_email.place(relx=.1,rely=.73)

        lbl_adhar=Label(frm,text="AADHAR NO:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_adhar.place(relx=.45,rely=.34)

        e_adhar=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_adhar.place(relx=.45,rely=.38)
        
        lbl_pan=Label(frm,text="PAN No:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_pan.place(relx=.45,rely=.45)

        e_pan=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_pan.place(relx=.45,rely=.49)

        lbl_dob=Label(frm,text="Date Of Birth:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_dob.place(relx=.45,rely=.56)

        e_dob=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_dob.place(relx=.45,rely=.60)

        def open_calendar():
            top=Toplevel(ifrm)
            top.title("Select Date")
            top.geometry("250x240+1490+410")
            top.grab_set()
            cal=Calendar(top,selectmode='day',year=date.today().year,month=date.today().month,day=date.today().day, date_pattern='dd-mm-yyyy')
            cal.pack(pady=10)

            def pick_date():
                selected=cal.get_date()
                e_dob.delete(0,"end")
                e_dob.insert(0,selected)
                top.destroy()

            Button(top,text="Select",command=pick_date).pack(pady=5)

        btn_cal=Button(ifrm,text="🗓️",font=('Rockwell Condensed',15,'bold'),command=open_calendar,width=4)
        btn_cal.place(relx=.79,rely=.53)
        
        btn_save=Button(frm,text='Save',font=('Rockwell Condensed',20,'bold'),bd=5,width=10,command=save)
        btn_save.place(relx=.48,rely=.72)

        btn_reset=Button(frm,text='Reset',font=('Rockwell Condensed',20,'bold'),bd=5,width=10)
        btn_reset.place(relx=.60,rely=.72)


    def view():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.08,rely=0.25,relwidth=.85,relheight=0.68)

        def view_customer():
            uacn=e_acc.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=?'
            curobj.execute(query,(uacn,))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("View","Record not found")
            else:
                msg=f'''
                Name=>{row[1]}
                Bal=>{row[7]}
                Mobile no.=>{row[6]}
                Email=>{row[5]}
                opendate=>{row[10]}
                Adhar=>{row[3]}'''
                messagebox.showinfo("Details",msg)
            conobj.close()

        Title=Label(ifrm,text="This Is View Account Window",font=('georgia bold',30,'bold'),bg="black",fg="#F0F2F7",highlightbackground="white",highlightthickness=3)
        Title.pack()

        lbl_acc=Label(frm,text="Account No:", font=('Rockwell Condensed',19,'bold'),bg='white',fg='black')
        lbl_acc.place(relx=.28,rely=.35)

        e_acc=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_acc.place(relx=.28,rely=.40)

        btn_view=Button(frm,text='View Detail',font=('Rockwell Condensed',18,'bold'),bd=5,width=10,command=view_customer)
        btn_view.place(relx=.60,rely=.39)

    def close():
        ifrm=Frame(frm,highlightbackground="pink",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.08,rely=0.25,relwidth=.85,relheight=0.68)

        def send_otp():
            uacn=e_acc.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select email,password from account where acno=?'
            curobj.execute(query,(uacn,))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("View","Record not found")
            else:
                otp=generator.generate_otp()
                utext=f'''Dear {row[0]},
            Kindly share otp {otp} with bank to close your account in our bank.            

            thanks,
            Dhink-Chika bank,from Mangal'''
            conobj.close()
            try:
                mail.send_close_otp(row[1],"otp tto close account",utext)
                messagebox.showinfo("Account","Creadantail will be sent on customer mail id.")
                attempt=1
                while attempt<=3:
                    uotp=simpledialog.askstring("OTP","Enter OTP")
                    if str(otp)==uotp:
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from account where acno=?'
                        curobj.execute(query,(uacn,))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("close","Account closed")
                        break
                    else:
                        messagebox.showerror("close","invalid otp")
                        attempt+=1
                        if attempt==4:
                            messagebox.showerror("close","Max attempt completed, you need to resend otp")
            except:
                msg=""""Something went wrong,
                kindly check your internet connection or mail id"""
                messagebox.showerror("Account",msg)

        Title=Label(ifrm,text="This Is Close Account Window",font=('georgia bold',30,'bold'),bg="black",fg="#F1F4FA",highlightbackground="white",highlightthickness=3)
        Title.pack()

        lbl_acc=Label(frm,text="Account No:", font=('Rockwell Condensed',15,'bold'),bg='white',fg='black')
        lbl_acc.place(relx=.28,rely=.45)

        e_acc=Entry(frm,font=('Rockwell Condensed',24,'bold'),bd=5,background='white',fg="black",width=40)
        e_acc.place(relx=.28,rely=.50)

        btn_otp=Button(frm,text='Send OTP',font=('Rockwell Condensed',20,'bold'),bd=5,width=10,command=send_otp)
        btn_otp.place(relx=.58,rely=.49)


    lbl_wel=Label(frm,text="Welcome Admin", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black',highlightbackground="black",highlightthickness=3)
    lbl_wel.place(relx=.0,rely=.0)

    btn_logout=Button(frm,text='Logout',font=('Rockwell Condensed',18,'bold'),bd=5,command=logout,highlightbackground="black",highlightthickness=3)
    btn_logout.place(relx=.94,rely=.0)

    btn_open=Button(frm,text='Open Account',font=('Rockwell Condensed',21,'bold'),bd=5,command=open)
    btn_open.place(relx=.15,rely=.12)

    btn_view=Button(frm,text='View Account',font=('Rockwell Condensed',21,'bold'),bd=5,command=view)
    btn_view.place(relx=.44,rely=.12)

    btn_close=Button(frm,text='Close Account',font=('Rockwell Condensed',21,'bold'),bd=5,command=close)
    btn_close.place(relx=.73,rely=.12)


def fp_frame():
    def call_main_frame():
        frm.destroy()
        main_frame()
    
    # 1. Get screen dimensions to calculate exact placement
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    fh = int(sh * 0.8) # Frame height is 80% of the screen height

    # 2. Update the refresh function to work with Canvas text
     # Updates the drawn text

    # 3. Create a Canvas instead of a Frame
    frm = Canvas(root, highlightbackground="black", highlightthickness=3)
    frm.place(relx=0, rely=0.145, relwidth=1, relheight=0.8)

    # 4. Add the blurred background directly to the Canvas
    try:
        bg_img = Image.open('wallpaper3.jpg') # ⚠️ CHANGE THIS to your image name
        bg_img = bg_img.resize((sw, fh))
        blurred_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        frm.bg_photo = ImageTk.PhotoImage(blurred_img) 
        frm.create_image(0, 0, image=frm.bg_photo, anchor="nw")
    except Exception as e:
        print(f"Image Error: {e}") # Just in case the image isn't found

    # 5. Draw Transparent Text and Place Interactive Widgets

    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_aadhar.delete(0,"end")
        e_acn.focus()

    def send_otp():
            uacn=e_acn.get()
            uemail=e_email.get()
            uadhar=e_aadhar.get()

            if len(uacn)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror("Account","Empty field not valid")
            return

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select email,password,aadhar from account where acno=? and email=? and aadhar=?'
            curobj.execute(query,(uacn,uemail,uadhar))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("Password Recovery","Record not found")
                return
            else:
                otp=generator.generate_otp()
                utext=f'''Dear {row[0]},
            Kindly share otp {otp} with bank to recover passward of your account{uacn} in our bank.            

            thanks,
            Dhink-Chika bank,from Mangal'''
            conobj.close()
            try:
                mail.send_close_otp(row[1],"otp tto close account",utext)
                messagebox.showinfo("Account","Creadantail will be sent on customer mail id.")
                attempt=1
                while attempt<=3:
                    uotp=simpledialog.askstring("OTP","Enter OTP")
                    if str(otp)==uotp:
                        messagebox.showinfo("Passward Recovery",row[2])
                        break
                    else:
                        messagebox.showerror("Passward Recovery","invalid otp")
                        attempt+=1
                        if attempt==4:
                            messagebox.showerror("Passward Recovery","Max attempt completed, you need to resend otp")
            except:
                msg=""""Something went wrong,
                kindly check your internet connection or mail id"""
                messagebox.showerror("Account",msg)

    btn_back=Button(frm,text='Back',font=('Rockwell Condensed',17,'bold'),bd=5,command=call_main_frame)
    btn_back.place(relx=.0,rely=.0)

    lbl_acn=Label(frm,text="Account.No🔑:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_acn.place(relx=.32,rely=.18)

    e_acn=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black")
    e_acn.place(relx=.47,rely=.18)

    lbl_email=Label(frm,text="Email:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_email.place(relx=.32,rely=.28)

    e_email=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black")
    e_email.place(relx=.47,rely=.28)

    lbl_aadhar=Label(frm,text="Aadhar.No🔑:", font=('Rockwell Condensed',28,'bold'),bg='white',fg='black')
    lbl_aadhar.place(relx=.32,rely=.38)

    e_aadhar=Entry(frm,font=('Rockwell Condensed',28,'bold'),bd=5,background='white',fg="black")
    e_aadhar.place(relx=.47,rely=.38)

    btn_otp=Button(frm,text='Send OTP',font=('Rockwell Condensed',17,'bold'),bd=5,command=send_otp)
    btn_otp.place(relx=.49,rely=.48)

    btn_reset=Button(frm,text='Reset',font=('Rockwell Condensed',17,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.57,rely=.48)



lbl_footer=Label(root,text="Developed by Rishabh Roxx👽\n📲+91 8766543342",
                 font=('arial',18,'bold'),bg="#9E92A5")
lbl_footer.pack(side='bottom')

main_frame()
root.mainloop()