import socket #lets me use TCP sockets in 
import tkinter #handles GUI
from threading import Thread # allows multi threading
from datetime import datetime # lets me get current time




# server's IP address
SERVER_HOST = "127.0.0.1"
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
        message = s.recv(1024).decode("utf8")# decode message from server
        
        msg_list.insert(tkinter.END, message)# print message to GUI

def send(event=None): #run this when you send message
    date_now = datetime.now().strftime('%d/%m/%Y %H:%M') 
    sendNow = f"{date_now} {name} {separator_token} {to_send.get()}" # string to send to server 
    #  send the message
    s.send(bytes(sendNow, "utf8"))
    to_send.set(" ")
# start gui

top = tkinter.Tk()
top.title("fluffchat") #set title of window
top.geometry("400x400")#set size of window
messages_frame = tkinter.Frame(top)# create message frame for recived messages
to_send = tkinter.StringVar() # create variable for the message you send
to_send.set("Type message here") #placeholder text for text box
scrollbar = tkinter.Scrollbar(messages_frame)# make scrollbar easy to access in rest of code



msg_list = tkinter.Listbox(messages_frame, height=20, width=50, yscrollcommand=scrollbar.set) #create box for recived messages
# pack things for GUI
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
scrollbar.config( command = msg_list.yview )# config to make scrollbar work
messages_frame.pack()
#create message field and send button
entry_field = tkinter.Entry(top, textvariable=to_send)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)# make send button
send_button.pack()


#threding for reciving messages
receive_thread = Thread(target=receive)
receive_thread.start()
#keep gui running
tkinter.mainloop()




# close the socket
s.close()
