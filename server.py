import socket
import threading
import json
import mysql.connector

host = "127.0.0.1"
port = 55555
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()



clients = []
usernames = []
chat_history = []









def handle_password_reset(client, message):
    try:
        username, new_password = message.split(":")[1:]
        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NBVmysqlCXW@24",
            database="userdata"
        )

        cursor = db.cursor()
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            update_query = "UPDATE user SET password = %s WHERE username = %s"
            cursor.execute(update_query, (new_password, username))
            db.commit()

            client.send("PASSWORD_RESET_SUCCESS".encode('utf-8'))
        else:
            client.send("PASSWORD_RESET_FAILURE: Username not found".encode('utf-8'))

        cursor.close()
        db.close()

    except Exception as e:
        client.send(f"Password reset failed: {e}".encode('utf-8'))



def handle_login(client, message):
    try:
        login_data = message.split(":")
        if len(login_data) >= 3:
            username = login_data[1]
            password = login_data[2]

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="NBVmysqlCXW@24",
                database="userdata"
            )

            cursor = db.cursor()

            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            print(f"Username: {username}, Password: {password}, User from DB: {user}")  # Debug line
            
            if user:
                client.send("LOGIN_SUCCESS".encode('utf-8'))
            else:
                client.send("LOGIN_FAILURE".encode('utf-8'))

            cursor.close()
            db.close()

        else:
            client.send("LOGIN_FAILURE".encode('utf-8')) 

    except mysql.connector.Error as err:
        client.send(f"Database Error: {err}".encode('utf-8'))
    except Exception as e:
        client.send(f"An unexpected error occurred: {e}".encode('utf-8'))
def history(client) :

    history_message = "History: " + str(chat_history)
    client.send(history_message.encode('utf-8'))



def broadcast(message):
    encoded_message = message if isinstance(message, bytes) else message.encode('utf-8')
    chat_history.append(encoded_message)
    for client in clients:
        client.send(encoded_message)


def send_private_message(sender_username, recipient_username, message):
    try:
        recipient_index = usernames.index(recipient_username)
        recipient_client = clients[recipient_index]
        recipient_client.send(f"(Private) {sender_username}: {message}".encode('utf-8'))
        sender_index = usernames.index(sender_username)
        sender_client = clients[sender_index]
        sender_client.send(f"(Private) {sender_username}: {message}".encode('utf-8'))
    except ValueError:
        sender_index = usernames.index(sender_username)
        sender_client = clients[sender_index]
        sender_client.send(f"username [ {recipient_username} ] not found.".encode('utf-8'))

def handle_signup(data):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NBVmysqlCXW@24",
            database="userdata"
        )

        cursor = db.cursor()

        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already exists, Try another one !"
        else :
            insert_query = "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (email, username, password))
            db.commit()

            cursor.close()
            db.close()

            return "Signup successful!"
    

    except mysql.connector.Error as err:
        return f"Database Error: {err}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"




def handle_client(client):
    sender_username = usernames[clients.index(client)]

    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message.startswith('@') :
                recipient, content = message.split(':', 1)
                recipient_username = recipient[1:].strip()
                send_private_message(sender_username, recipient_username, content.strip())
            elif message == "/disconnect": 
                broadcast(f"{sender_username} has left the chat room.".encode('utf-8'))
                index = clients.index(client)
                clients.remove(client)
                client.close()
                usernames.remove(sender_username)
                break
            elif message == "/history" :
                history(client)
            else:
                broadcast(message)

        except ConnectionResetError:
            print(f"{sender_username} has left the chat room!")
            cleanup_client(client, sender_username)
            break
        except Exception as e:
            print(f"Error: {e}")
            cleanup_client(client, sender_username)
            break

def cleanup_client(client, username):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    usernames.remove(username)
    broadcast(f"{username} has left the chat room!".encode('utf-8'))
def handle_signup_request(client, message):
    signup_data = json.loads(message.split(':', 1)[1])
    signup_response = handle_signup(signup_data)
    client.send(signup_response.encode('utf-8'))


def handle_chat_connection(client, address):

        
            
    client.send("USER:".encode('utf-8'))
            
    username = client.recv(1024).decode('utf-8')
    usernames.append(username)
    clients.append(client)
    print(f"The username of this client is {username}")
                
    broadcast(f"{username} has joined the chat room.".encode('utf-8'))
                
    client.send("You are now connected.".encode('utf-8'))
                
                
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()



def receive():
    while True:
        client, address = server.accept()
        message = client.recv(1024).decode('utf-8')

        if message.startswith("SIGNUP"):
            handle_signup_request(client, message)
        elif message =="USER:":
            handle_chat_connection(client, address)
        elif message.startswith("LOGIN:"):
                    handle_login(client, message)
                    print(f"Connection established with {str(address)}")
        elif message.startswith("FORGOT_PASSWORD:"):
            handle_password_reset(client, message)


print("Server is running and listening...")
receive()




