import socket #lets me use TCP sockets in 
import tkinter #handles GUI
import base64
import blowfish #handles encryption
from threading import Thread # allows multi threading
from datetime import datetime # lets me get current time
cipher = blowfish.Cipher(b"thisIsATest")



# server's IP address
print("some ip here is the default server port will always be 5002")
SERVER_HOST = input("input server ip input: ")
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # seperates client name and message sent by client

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))# connect to server
print("[+] Connected.")
#ask for name
name = input("Enter your name: ")

def receive(): # run this on message recevived
    while True:
        message = s.recv(1024)# get message from server
        #decrypt message
        message = b"".join(cipher.decrypt_ecb_cts(message))
 
        message = base64.b64decode(message)
        message = message.decode('utf8')
        message = message.replace(separator_token, ": ")
        msg_list.insert(tkinter.END, message)# print message to GUI

def send(event=None): #run this when you send message
    date_now = datetime.now().strftime('%d/%m/%Y %H:%M') 
    sendNow = f"{date_now} {name} {separator_token} {to_send.get()}" # string to send to server 
#encrypt message
    sendNow = sendNow.encode('utf8')
    sendNow_b64 = base64.b64encode(sendNow)
    sendNow_b64 = b"".join(cipher.encrypt_ecb_cts(sendNow_b64))
    #  send the message
    print(sendNow_b64)
    s.send(sendNow_b64)# value must be byte to send
    to_send.set(" ")
    
# start gui

top = tkinter.Tk()
fluffChatName = tkinter.Label(text="Fluffchat", foreground="#FFFFFF", background="#36393F")# set label at top of window to say fluffchat

top.title("fluffchat") #set title of window
top.geometry("800x700")#set size of window
top.configure(bg='#36393F')
messages_frame = tkinter.Frame(top)# create message frame for recived messages
to_send = tkinter.StringVar() # create variable for the message you send
to_send.set("Type message here") #placeholder text for text box
scrollbar = tkinter.Scrollbar(messages_frame)# make scrollbar easy to access in rest of code



msg_list = tkinter.Listbox(messages_frame, height=30, width=115 , yscrollcommand=scrollbar.set) #create box for recived messages
# pack things for GUI
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
fluffChatName.pack()
scrollbar.config( command = msg_list.yview )# config to make scrollbar work
messages_frame.pack()
#create message field and send button
entry_field = tkinter.Entry(top, textvariable=to_send, width=70)
entry_field.bind("<Return>", send)
entry_field.pack(pady=7)
send_button = tkinter.Button(top, text="Send", command=send, width=30)# make send button
send_button.pack(pady=5)


#threding for reciving messages
receive_thread = Thread(target=receive)
receive_thread.start()
#keep gui running
tkinter.mainloop()




# close the socket
s.close()
