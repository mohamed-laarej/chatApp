from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import tkinter as tk
import socket
import threading
from tkinter import messagebox

def start_chat(username):





    def on_closing():
        client.send("/disconnect".encode('utf-8'))
        root.destroy()


    def client_receive():
        chat_box.tag_config("my_tag", foreground="red")
        received_history = False
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                

                if message == "USER:":
                    client.send(username.encode('utf-8'))
                elif message.startswith("History:") and not received_history:
                    chat_history = message.replace("History:", "")
                    chat_history = chat_history.strip("[]")
                    chat_box.insert(tk.END, "<<<< BEGIN OF HISTORY :>>>>", "my_tag")
                    chat_box.insert(tk.END, "\n")
                    chat_history = chat_history.replace(", ", "\n")
                    chat_history = chat_history.replace("b'", "")
                    chat_history = chat_history.replace("'", "")
                    chat_history = chat_history.replace("[", "")
                    chat_box.insert(tk.END, chat_history , "my_tag")
                    chat_box.insert(tk.END, "\n") 
                    chat_box.insert(tk.END, "<<<< END OF HISTORY ;>>>>", "my_tag")
                    chat_box.insert(tk.END, "\n")
                    received_history = True
                else:
                    if not message.startswith("History:"):
                        chat_box.insert(tk.END, message + "\n")
            except Exception as e:
                print(f"Error: {e}")
                client.close()
                break


    def client_send(event=None):
        message = entry.get()
        if message == "/disconnect":
            client.send(message.encode('utf-8'))
            root.destroy()
        elif message.startswith('@'):
            recipient, content = message.split(':', 1)
            message = f"{recipient}:{content}"
        elif message == "/history":  
            client.send(message.encode('utf-8'))
        else:
            message = f"{username}:{message}"  

        client.send(message.encode('utf-8'))
        entry.delete(0, tk.END)


    host = "127.0.0.1"
    port = 55555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(f"USER:".encode('utf-8'))

    root = tk.Tk()
    root.title("Chat Client")
    root.protocol("WM_DELETE_WINDOW" , on_closing)

    chat_frame = tk.Frame(root)
    chat_frame.pack(padx=10, pady=10)

    chat_scrollbar = tk.Scrollbar(chat_frame)
    chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_box = tk.Text(chat_frame, height=20, width=50, yscrollcommand=chat_scrollbar.set)
    chat_box.pack()
    

    chat_scrollbar.config(command=chat_box.yview)

    entry = tk.Entry(root, width=30)
    entry.pack(padx=10, pady=10)
    entry.bind("<Return>", client_send)

    send_button = tk.Button(root, text="Send", command=client_send)
    send_button.pack()
    


    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()
    
    

    root.mainloop()







def forget_password() :

    def handle_password_reset():
        if user_entry.get() == "" or pass_entry.get() == "" or confpass_entry.get() == "":
            messagebox.showerror("Error", "All Fields Are Required!",parent=window)
        elif pass_entry.get() != confpass_entry.get():
            messagebox.showerror("Error", "Password mismatch!",parent=window)
        else:
            host = "127.0.0.1"
            port = 55555

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            username = user_entry.get()
            new_password = pass_entry.get()


            try:
                message = f"FORGOT_PASSWORD:{username}:{new_password}"
                client.send(message.encode('utf-8'))
                
                response = client.recv(1024).decode('utf-8')
                if response.startswith("PASSWORD_RESET_SUCCESS"):
                    messagebox.showinfo("Success", "Password is reset. Please log in with the new password!",parent=window)
                    window.destroy()
                elif response.startswith("PASSWORD_RESET_FAILURE"):

                    messagebox.showerror("Error", "Password reset failed: Username not found",parent=window)
                else:

                    messagebox.showerror("Error", "Unexpected response from server.",parent=window)

            except ConnectionAbortedError:
                client.close()
                messagebox.showerror("Error", "Connection was aborted.")
            except Exception as e:
                client.close()
                messagebox.showerror("Error", f"Password reset failed: {e}")


    window = Toplevel()
    window.resizable(0,0)
    window.title("Forget password")
    window.geometry("790x512")

    bgpic = ImageTk.PhotoImage(file="background.jpg")
    bglabel = Label(window , image= bgpic)
    bglabel.grid()
    heading_label = Label(window , text="RESET PASSWORD" , font=("arial" , "18" ,"bold")
                          ,bg="white" , fg="#4c64cb")
    heading_label.place(x=480 , y=60)

    usename_label = Label(window , text="Username", font=("arial",12,"bold"),bg="white",fg="#4c64cb")
    usename_label.place(x=470 , y=130)
    user_entry = Entry(window , width=25,font=("arial", 11 ,"bold"),bd=0)
    user_entry.place(x=470 , y=160)
    Frame(window , width=250 , height=2 , bg="#4c64cb").place(x=470 , y=180)

    password_label = Label(window , text="New Password", font=("arial",12,"bold"),bg="white",fg="#4c64cb")
    password_label.place(x=470 , y=210)
    pass_entry = Entry(window , width=25,font=("arial", 11 ,"bold"),bd=0)
    pass_entry.place(x=470 , y=240)
    Frame(window , width=250 , height=2 , bg="#4c64cb").place(x=470 , y=260)

    confpassword_label = Label(window , text="Confirm New Password", font=("arial",12,"bold"),bg="white",fg="#4c64cb")
    confpassword_label.place(x=470 , y=290)
    confpass_entry = Entry(window , width=25,font=("arial", 11 ,"bold"),bd=0)
    confpass_entry.place(x=470 , y=310)
    Frame(window , width=250 , height=2 , bg="#4c64cb").place(x=470 , y=330)

    submitButton = Button(window , text="Submit" , bd=0 ,font=("Open Sans", 16 ,"bold")
                          , width=19 ,)
    submitButton = Button(window, text='Submit', bd=0, bg='#4c64cb', fg="white",font=("Open Sans", 16, "bold"),
                         width=19, cursor='hand2', activebackground='#4c64cb', activeforeground="white", command=handle_password_reset)
    submitButton.place(x=470, y=390)




    window.mainloop()

def info() :
    messagebox.showinfo("announcement", "This option is not currently available!")

def login_user():
    username = usernameEntary.get()
    password = passwordEntary.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required!")
        return

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("127.0.0.1", 55555))

        login_data = f"LOGIN:{username}:{password}" 
        server.send(login_data.encode('utf-8')) 

        response = server.recv(1024).decode('utf-8') 

        if response == "LOGIN_SUCCESS":
            messagebox.showinfo("Welcome", "Login is successful.")
            login_window.destroy()
            start_chat(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

        server.close()

    except ConnectionRefusedError:
        messagebox.showerror("Error", "Server is not available.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")





def hide() :
    openeeye.config(file='closeye.png')
    if passwordEntary.get()!= "Password":
        passwordEntary.config(show='*')
    eyebutton.config(command=show)
def show() :
    openeeye.config(file='openeye.png')
    passwordEntary.config(show='')
    eyebutton.config(command=hide)
def user_entry(event) :
    if usernameEntary.get() == 'user name' :
        usernameEntary.delete(0,END)

def pass_entry(event) :
    if passwordEntary.get() == 'Password' :
        passwordEntary.delete(0,END)



def signup_page() :
    login_window.destroy()
    import signup


login_window = Tk()

login_window.resizable(0,0)
login_window.title('Login Page')
login_window.geometry('990x660+50+50')
bgImage = ImageTk.PhotoImage(file="bg.jpg")
bglabel = Label(login_window,image= bgImage)
bglabel.place(x=0 , y=0)
heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23 , 'bold') 
                ,bg='white', fg='#4c66cb')
heading.place(x=605 , y= 120)


usernameEntary = Entry(login_window,width=25 , font=('Microsoft Yahei UI Light', 11 , 'bold' ), bd=0)
usernameEntary.place(x=580 , y= 200)
usernameEntary.insert(0,'user name')
usernameEntary.bind('<FocusIn>', user_entry)
frame1 = Frame(login_window,width=250,height=2)
frame1.place(x=580 , y=222)

passwordEntary = Entry(login_window,width=25 , font=('Microsoft Yahei UI Light', 11 , 'bold' ), bd=0)
passwordEntary.place(x=580 , y= 260)
passwordEntary.insert(0,'Password')
passwordEntary.bind('<FocusIn>', pass_entry)
frame2 = Frame(login_window,width=250,height=2)
frame2.place(x=580 , y=282)

openeeye = PhotoImage(file="openeye.png")
eyebutton = Button(login_window , image= openeeye , bd=0 , bg='white' , activebackground='white'
                   ,cursor='hand2' , command=hide)
eyebutton.place(x=800 , y=255)

forgetbutton = Button(login_window , text='Forget your Password ?' , bd=0 ,fg='blue',activeforeground='blue'
                      , bg='white' , activebackground='white'
                   ,cursor='hand2' , font=('Microsoft Yahei UI Light' , 8 , 'bold' ),command=forget_password)
forgetbutton.place(x=703 , y=295)

loginbutton = Button(login_window, text= 'Login',font=('Open sans' , 16 , 'bold')
                     ,fg='white', bg='#4c66cb',activebackground='#4c66cb'
                     ,activeforeground='white', cursor='hand2' , bd=0 , width=19 , command= login_user)
loginbutton.place(x=578 , y=350)

orlebal = Label(login_window , text='--------------- OR ---------------', font=('Open Sans' , 16)
                ,fg='#4c66cb',bg='white')
orlebal.place(x=583 , y=400)

facebook_logo = PhotoImage(file='facebook.png')
fb_button = Button(login_window , image= facebook_logo , bg='white', bd=0 , activebackground="white"
                   ,cursor="hand2", command=info)
fb_button.place(x=640 , y=440)

google_logo = PhotoImage(file='google.png')
gg_button = Button(login_window , image= google_logo , bg='white', bd=0 , activebackground="white"
                   ,cursor="hand2", command=info)
gg_button.place(x=690 , y=440)

twitter_logo = PhotoImage(file='twitter.png')
tt_button = Button(login_window , image= twitter_logo , bg='white', bd=0 , activebackground="white"
                   ,cursor="hand2", command=info)
tt_button.place(x=740 , y=440)

signup_lebal = Label(login_window , text='don\'t have an account ?', font=('Open Sans' ,9, 'bold')
                ,bg='white')
signup_lebal.place(x=590 , y=500)

createaccountbutton = Button(login_window, text= 'create a new one',font=('Open sans' , 9 , 'bold underline')
                     ,fg='blue', bg='white',activebackground='white'
                     ,activeforeground='blue', cursor='hand2' , bd=0 , command= signup_page)
createaccountbutton.place(x=727 , y=500)

login_window.mainloop()