

import socket
import threading
import tkinter as tk




def start_chat(username):






    def on_closing():
        client.send("/disconnect".encode('utf-8'))
        root.destroy()


    def client_receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "USERNAME":
                    client.send(username.encode('utf-8'))
                elif message.startswith("History:") and not received_history:
                    chat_history = message.replace("History:", "")
                    chat_box.insert(tk.END, chat_history)  # Inserting chat history
                    received_history = True
                else:
                    chat_box.insert(tk.END, message + "\n")
            except :
                print("Error !")
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
        elif message == "/history":  # Check for the /history command
            client.send(message.encode('utf-8'))
        else:
            message = f"{username}:{message}"  


        client.send(message.encode('utf-8'))
        entry.delete(0, tk.END)


    host = "127.0.0.1"
    port = 55555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

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



start_chat("anas")




    

