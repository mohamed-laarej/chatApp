
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import socket
import json



def send_signup_data():
    user_data = {
        "email": emailEntary.get(),
        "username": userentary.get(),
        "password": passwordentary.get()
    }
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 55555))


        signup_message = f"SIGNUP:{json.dumps(user_data)}"
        client.send(signup_message.encode('utf-8'))
        
        response = client.recv(1024).decode('utf-8') 
        print(response) 
        
        client.close()
        if response == "Username already exists, Try another one !" :
            messagebox.showerror("Error", response)
            clear()
        else:
           messagebox.showinfo("successe","Signup successful!")
           signup_window.destroy()
           import Login
    
    except socket.error as e:
        messagebox.showerror("Error", f"Socket error: {e}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


def clear() :
    emailEntary.delete(0,END)
    userentary.delete(0,END)
    passwordentary.delete(0,END)
    confpasswordentary.delete(0,END)
    check.set(0)


def connect_database() :
    if emailEntary.get() == "" or userentary.get() == "" or passwordentary.get() == "" or confpasswordentary == "" :
        messagebox.showerror("Error" , "All Fields Are Required !")
    elif passwordentary.get() != confpasswordentary.get() :
        messagebox.showerror("Error" , "Password mismatch!")
    elif check.get() == 0 :
        messagebox.showerror("Error" , "Please Acepte Terms & Conditions !")

    else :
            send_signup_data()


def login_page() :
    signup_window.destroy()
    import Login

signup_window = Tk()

signup_window.resizable(0,0)
signup_window.title('signup Page')
signup_window.geometry('990x660+50+50')
background = ImageTk.PhotoImage(file="bg.jpg")
bglabel = Label(signup_window,image= background)
bglabel.place(x=0 , y=0)

frame = Frame(signup_window , bg='white')
frame.place(x=554 , y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 16 , 'bold') 
                ,bg='white', fg='#4c66cb')
heading.grid(row=0 ,column=0,padx=10 ,pady=10)


emaillabel = Label(frame , text='Email' , font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white', fg='#4c66cb')
emaillabel.grid(row=1 , column=0 , sticky='w' ,padx=25 ,pady=(10,0))
emailEntary = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white')
emailEntary.grid(row=2 ,column=0 ,sticky='w' ,padx=25 )

userlabel = Label(frame , text='User name' , font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white', fg='#4c66cb')
userlabel.grid(row=3 , column=0 , sticky='w' ,padx=25 ,pady=(10,0))
userentary = Entry(frame,width=30, font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white')
userentary.grid(row=4 ,column=0 ,sticky='w' ,padx=25 )

passwordlabel = Label(frame , text='Password' , font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white', fg='#4c66cb')
passwordlabel.grid(row=5 , column=0 , sticky='w' ,padx=25 ,pady=(10,0))
passwordentary = Entry(frame,width=30, font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white')
passwordentary.grid(row=6 ,column=0 ,sticky='w' ,padx=25 )

confpasswordlabel = Label(frame , text='Confirm Password' , font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white', fg='#4c66cb')
confpasswordlabel.grid(row=7 , column=0 , sticky='w' ,padx=25 ,pady=(10,0))
confpasswordentary = Entry(frame,width=30, font=('Microsoft Yahei UI Light', 10 , 'bold'), bg='white')
confpasswordentary.grid(row=8 ,column=0 ,sticky='w' ,padx=25 )


check = IntVar()
termsandconditions = Checkbutton(frame, text='I agree to the Terms & Conditions', 
                                 font=('Open Sans', 8 , 'bold'),bg='white'
                                 ,cursor='hand2',activebackground='white' , variable=check)
termsandconditions.grid(row=9 , column=0 ,pady=10 , padx=15 )

signupbutton =Button(frame, text='SIGN UP',font=('Open sans' , 16 , 'bold')
                     ,fg='white', bg='#4c66cb',activebackground='#4c66cb'
                     ,activeforeground='white', cursor='hand2' , bd=0 ,width=17 , command=connect_database)
signupbutton.grid(row=10 , column=0 , pady=10 , padx=30)

login_lebal = Label(frame, text='You have an account ?', font=('Microsoft Yahei UI Light' ,9, 'bold')
                ,bg='white')
login_lebal.grid(row=11 , column=0 ,sticky='w',padx=25,pady=10)

loginbutton = Button(frame, text= 'Login',font=('Open sans' , 10 , 'bold underline')
                     ,fg='blue', bg='white',activebackground='white'
                     ,activeforeground='blue', cursor='hand2' , bd=0 , command= login_page)
loginbutton.place(x=180 , y=397)









signup_window.mainloop()