import random
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as m


# DATABASE CONNECTION

mydatabase=m.connect(host="localhost",user="root",password="RasamYash@176",database="pythondb1")
query="insert into passmng(website,username,password) values(%s,%s,%s)"
cursor=mydatabase.cursor()


# MAIN WINDOW

window= Tk()
window.title("Password Manager")
window.config(padx=10,pady=10,bg='papaya whip')

# ADDING LOGO

canvas=Canvas(height=500,width=600)
logo= PhotoImage(file="logo.png")
canvas.create_image(300,300,image=logo)
canvas.configure(bg='papaya whip')
canvas.grid(row=0,column=1,columnspan=1,pady=20)

# ADDING LABELS AND ENTRIES

# for website
web= Label(window,text="Website: ")
web.configure(font=('Segoe UI Light',12,'bold'),fg='olive',bg='papaya whip')
webE= Entry(window,width=40,font=('Segoe UI Light',12,'bold'),bg="papaya whip",border=3)
webE.focus()
web.grid(row=1,column=0,pady=5)
webE.grid(row=1,column=1,pady=5)

# for username
uname= Label(window,text="Username/Email: ")
uname.configure(font=('Segoe UI Light',12,'bold'),fg='olive',bg='papaya whip')
unameE= Entry(window,width=40,font=('Segoe UI Light',12,'bold'),bg="papaya whip",border=3)
uname.grid(row=2,column=0,pady=5)
unameE.grid(row=2,column=1,pady=5)

# for password
pswd= Label(window,text="Password: ")
pswd.configure(font=('Segoe UI Light',12,'bold'),fg='olive',bg='papaya whip')
pswdE= Entry(window,width=40,font=('Segoe UI Light',12,'bold'),bg="papaya whip",border=3)
pswd.grid(row=3,column=0,pady=5)
pswdE.grid(row=3,column=1,pady=5)

# SAVING DATA INTO DATABASE
def Register():
    if (len(webE.get())==0 or len(unameE.get())==0 or len(pswdE.get())==0):
        messagebox.showinfo(title="Oops",message="All the fields are *Required")
    else:
        ok= messagebox.askokcancel(title=webE.get(),message=f"Username:{unameE.get()}\nPassword:{pswdE.get()}\nAre this details ok??")

        if (ok):
            cursor.execute(query,[webE.get(),unameE.get(),pswdE.get()])
            mydatabase.commit()
            webE.delete(0,END)
            unameE.delete(0, END)
            pswdE.delete(0, END)

# PASSWORD GENERATOR LOGIC
def generatePass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pswdE.delete(0, END)
    newpass = random.sample(letters, 8) + random.sample(numbers, 3) + random.sample(symbols, 3)
    random.shuffle(newpass)
    npass = "".join(newpass)
    pswdE.insert(0,npass)

# SHOWING ALL THE  SAVED PASSWORDS
def showRecords():
    # LOGIN WINDOW

    login=Tk()
    login.title("Login")
    login.config(padx=20,pady=20)

    #username
    id=Label(login,text="Username: ",font=('Segoe UI Light',10,'bold'))
    id.grid(row=0,column=0)
    idE=Entry(login,width=30,font=('Segoe UI Light',10,'bold'),border=2)
    idE.grid(row=0,column=1,pady=5)

    #password
    pd = Label(login, text="Password: ", font=('Segoe UI Light', 10, 'bold'))
    pd.grid(row=1, column=0)
    pdE = Entry(login, width=30, font=('Segoe UI Light', 10, 'bold'), border=2)
    pdE.config(show="*")
    pdE.grid(row=1, column=1,pady=5)

    # AUTHORIZATION LOGIC

    def Authorization():
        if(idE.get()=='yashrasam54' and pdE.get()=='yaSh@4121$'):
            # SHOWING THE RECORDS FROM DATABASE USING TTK.TREEVIEW

            r = Tk()
            r.title("Password Records")

            cursor = mydatabase.cursor()
            cursor.execute("select * from passmng")

            tree = ttk.Treeview(r)
            tree['show'] = "headings"

            s = ttk.Style(r)
            s.theme_use("clam")

            s.configure(".", font=('Helvetica', 12))
            s.configure("Treeview.Heading", foreground='dodger blue', font=('Helvetica', 12, 'bold'))

            tree["columns"] = ("website", "username", "password")

            tree.column("website", width=150, minwidth=150, anchor=tkinter.CENTER)
            tree.column("username", width=200, minwidth=200, anchor=tkinter.CENTER)
            tree.column("password", width=150, minwidth=150, anchor=tkinter.CENTER)

            tree.heading("website", text="Website Name", anchor=tkinter.CENTER)
            tree.heading("username", text="Username/Email", anchor=tkinter.CENTER)
            tree.heading("password", text="Password", anchor=tkinter.CENTER)

            i = 0
            for ro in cursor:
                tree.insert('', i, text="", values=(ro[0], ro[1], ro[2]))
                i += 1

            tree.pack()

            # DELETING DATA FROM DATABASE AND THE RECORDS WINDOW

            def DeleteData(tree):
                ok = messagebox.askokcancel(message="Are you sure you want to delete this record")
                if (ok):
                    sitem = tree.selection()[0]
                    web = tree.item(sitem)['values'][0]
                    cursor.execute("delete from passmng where website=%s", (web,))
                    mydatabase.commit()
                    tree.delete(sitem)
                    messagebox.showinfo(title="Done",message="Record Deleted Successfully")

            # delete button
            delete = Button(r, text="Delete Record", width=20, command=lambda: DeleteData(tree), bg='dodger blue',font=('Segoe UI Light', 10, 'bold'), fg='white')
            delete.pack(side='bottom')

            r.mainloop()
        else:
            messagebox.showinfo(title="Invalid User",message="Sorry you dont have access to the Records")

    # login button
    log = Button(login, text="Login", width=20,command=Authorization, bg='dodger blue', font=('Segoe UI Light', 10, 'bold'), fg='white')
    log.grid(row=3, column=1, pady=10)

    login.mainloop()

# ADDING BUTTONS

# generate password
genpswd= Button(window,text="Generate Password",width=20,command=generatePass,bg='dodger blue',font=('Segoe UI Light',10,'bold'),fg='white')
genpswd.grid(row=3,column=2)

# save
add= Button(window,text="Save",width=40,command=Register,bg='dodger blue',font=('Segoe UI Light',10,'bold'),fg='white')
add.grid(row=4,column=1,pady=10)

# show  saved password
records=Button(window,text="Show Saved Passwords",width=40,command=showRecords,bg='dodger blue',font=('Segoe UI Light',10,'bold'),fg='white')
records.grid(row=5,column=1,padx=10)

window.mainloop()