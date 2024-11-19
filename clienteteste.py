import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClient:
    def __init__(self, host="localhost", port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        
        self.root = tk.Tk()
        self.root.title("Chat do Cliente")

        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', wrap='word', width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Enviar", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.connect_to_server()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_server(self):
        """conecta ao servidor."""
        try:
            self.client_socket.connect(self.server_address)
            self.display_message("Conectado ao servidor! ;)")
        except Exception as e:
            self.display_message(f"Erro ao conectar ao servidor: {e} :(")

    def send_message(self, event=None):
        """envia mensagem para o servidor."""
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode())
                self.display_message(f"Você: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message(f"Erro ao enviar: {e} :(")

    def receive_messages(self):
        """recebe mensagens do servidor."""
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.display_message(f"Servidor: {message}")
            except Exception as e:
                self.display_message(f"Erro ao receber: {e} :(")
                break

    def display_message(self, message):
        """exibe uma mensagem na área de texto."""
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def run(self):
        """inicia a interface gráfica."""
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()