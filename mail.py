import gmail

email=""#your mail id here
pwd="hhep kriz yglp geqn" #your gmail id app password needed(12 characters)

def send_acn_cred(uemail,usub,utext):
    con=gmail.GMail(email,pwd)
    msg=gmail.Message(to=uemail,subject=usub,text=utext)
    con.send(msg)

def send_close_otp(uemail,usub,utext):
    con=gmail.GMail(email,pwd)
    msg=gmail.Message(to=uemail,subject=usub,text=utext)
    con.send(msg)