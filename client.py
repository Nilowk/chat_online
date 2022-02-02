import socket as s
import threading
from tkinter import *
from window_utils import WindowUtils


class Chat(WindowUtils):

    def __init__(self, client):
        self.root = client.root
        self.client = client
        self.elements = []
        self.messages = []

        self.chat = Canvas(self.root, bg="#343434", highlightthickness=0, height=500, width=300)
        self.chat.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.elements.append(self.chat)

        interaction = Canvas(self.root, bg="#343434", highlightthickness=1, height=100, width=100)
        interaction.place(relx=0.5, rely=0.95, anchor=CENTER)
        self.elements.append(interaction)

        image = PhotoImage(file="./img/microphone.png").subsample(25)
        lbl = Label(image=image)
        lbl.image = image
        voc_button = Button(interaction, bg="#2d8dfd", fg="white", borderwidth=0, image=image, command=lambda: threading.Thread(name="record", target=self.stream_audio()))
        voc_button.grid(row=0, column=0, ipadx=2, padx=5)
        self.elements.append(voc_button)

        message = Entry(interaction, font=30)
        message.grid(row=0, column=1, padx=5)
        self.elements.append(message)

        self.add(message, "message")
        message.bind("<FocusIn>", lambda event=None: self.erase(message, "message"))
        message.bind("<FocusOut>", lambda event=None: self.add(message, "message"))

        send_button = Button(interaction, bg="#2d8dfd", fg="white", borderwidth=0, text="send", command=lambda: self.send_message(self.is_default_message(message)))
        send_button.grid(row=0, column=2, ipadx=2, padx=5)
        self.elements.append(send_button)

    def send_message(self, msg):
        if msg != "":
            msg = f"[{self.client.pseudo}]: {msg}"
            self.client.send_message(msg)
            self.add_message(msg)

    def stream_audio(self):
        pass

    def add_message(self, msg):
        if msg != "":
            message = Label(self.chat, text=msg)
            self.messages.append(message)
            if len(self.messages) >= 22:
                self.messages[0].destroy()
                self.messages.pop(0)
            message.pack(side=TOP)


class Client:

    def __init__(self, pseudo, ip, root):
        self.ip = ip
        self.root = root
        self.pseudo = pseudo
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.connect((self.ip, 64599))
        chat = Chat(self)

        while True:
            data = self.socket.recv(1024).decode("utf-8")
            if data:
                chat.add_message(data)

    def send_message(self, msg):
        if msg != "":
            self.socket.send(msg.encode("utf-8"))
