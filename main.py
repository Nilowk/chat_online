import client
import server
import threading
from tkinter import *
from window_utils import WindowUtils


class App(Tk, WindowUtils):

    def __init__(self):
        super().__init__()
        self.title("chat")
        self.geometry("400x600")
        self.resizable(False, False)
        self.config(background="#343434")
        self.elements = []
        self.init_gui()
        self.mainloop()

    def launch_client(self, pseudo, host):
        if host != "":
            self.clear_window()
            threading.Thread(name="client", target=lambda: client.Client(pseudo, host, self)).start()


    def click(self, type, pseudo):
        if type != None:
            if pseudo != "":
                if type == "client":
                    self.clear_window()
                    can = Canvas(self, bg="#343434", highlightthickness=0, height=100, width=100)
                    can.place(relx=0.5, rely=0.5, anchor=CENTER)
                    self.elements.append(can)

                    host = Entry(can, font=30)
                    host.pack()
                    self.elements.append(host)

                    self.add(host, "host-name")
                    host.bind("<FocusIn>", lambda event=None: self.erase(host, "host-name"))
                    host.bind("<FocusOut>", lambda event=None: self.add(host, "host-name"))

                    connect_button = Button(can, bg="grey", fg="white", font=30, borderwidth=0, text="connect to server", command=lambda: self.launch_client(pseudo, self.is_default_message(host)))
                    connect_button.pack(pady=40)
                    self.elements.append(connect_button)

                elif type == "c+serv":
                    threading.Thread(name="host", target=lambda: server.Server("localhost")).start()
                    self.launch_client(pseudo, "localhost")

    def init_gui(self):
        can = Canvas(self, bg="#343434", highlightthickness=0, height=100, width=100)
        can.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.elements.append(can)

        pseudo = Entry(can, font=30)
        pseudo.pack()
        self.elements.append(pseudo)

        self.add(pseudo, "pseudo")
        pseudo.bind("<FocusIn>", lambda event=None: self.erase(pseudo, "pseudo"))
        pseudo.bind("<FocusOut>", lambda event=None: self.add(pseudo, "pseudo"))

        frame = Frame(can, bg="#343434")
        frame.pack(pady=40)
        self.elements.append(frame)

        connect_button = Button(frame, bg="grey", fg="white", font=30, borderwidth=0, text="connect to server", command=lambda: self.click("client", self.is_default_message(pseudo)))
        connect_button.pack()
        self.elements.append(connect_button)

        host_button = Button(frame, bg="grey", fg="white", font=30, borderwidth=0, text="host private server", command=lambda: self.click("c+serv", self.is_default_message(pseudo)))
        host_button.pack(pady=20)
        self.elements.append(host_button)


App()