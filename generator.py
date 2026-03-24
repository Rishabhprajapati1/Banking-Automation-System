#to generate otp,captcha
import random
import sqlite3

def generate_captcha():
    li=[]
    for i in range(2):
        digit=random.randint(0,9)
        li.append(str(digit))

    for j in range(2):
        digit=random.randint(97,122)
        ch=chr(digit)
        li.append(ch)

    random.shuffle(li)
    captcha=' '.join(li)
    return captcha

def generate_tables():
    conobj=sqlite3.connect(database='bank.sqlite') #cwd
    curobj=conobj.cursor()
    query1='''create table if not exists account(
    acno integer primary key autoincrement,
        name text,
        password text,
        aadhar text,
        pan text,
        email text,
        mob text,
        bal float,
        adr text,
        dob text,
        opendate text
    )
    '''
    query2='''create table if not exists txn_history(
    txnid integer primary key autoincrement,
    acno integer,
    amt float,
    type text,
    upbal float,
    txndate text
    )
    '''
    curobj.execute(query1)
    curobj.execute(query2)
    conobj.close()
    print('Table created')

def generate_password():
    li=[]
    for i in range(3):
        digit=random.randint(0,9)
        li.append(str(digit))

    for j in range(3):
        digit=random.randint(65,122)
        ch=chr(digit)
        li.append(ch)

    random.shuffle(li)
    password=''.join(li)
    return password

def generate_otp():
    otp=random.randint(1000,9999)
    return otp

if __name__=='__main__':
    print(generate_captcha())
    print(generate_password())