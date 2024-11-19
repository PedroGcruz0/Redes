import socket
import threading

class ChatServer:
    def __init__(self, host="localhost", port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Servidor iniciado em {host}:{port}")
        self.clients = {}

    def broadcast(self, message, sender_socket=None):
        """envia mensagem para todos os clientes, só não para o remetente."""
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except Exception as e:
                    print(f"Erro ao enviar mensagem: {e}")
                    self.disconnect_client(client_socket)

    def handle_client(self, client_socket):
        """gerencia comunicação com um cliente específico."""
        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break  
                print(f"Mensagem recebida: {message.decode()}")
                self.broadcast(message, sender_socket=client_socket)
        except Exception as e:
            print(f"Erro no cliente: {e} :(")
        finally:
            self.disconnect_client(client_socket)

    def disconnect_client(self, client_socket):
        """desconecta e remove o cliente do servidor."""
        print(f"Cliente {self.clients.get(client_socket)} desconectado.")
        if client_socket in self.clients:
            del self.clients[client_socket]
        client_socket.close()

    def accept_connections(self):
        """aceita conexões de novos clientes."""
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Nova conexão de {client_address}")
            self.clients[client_socket] = client_address
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def run(self):
        """roda o servidor."""
        print("Servidor em execução...")
        try:
            self.accept_connections()
        except KeyboardInterrupt:
            print("Servidor encerrando...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.run()

