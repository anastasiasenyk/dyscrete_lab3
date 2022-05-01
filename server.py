import socket
import threading
from math import gcd
from big_prime_gen import prime_generator
from rsa_algorithm import encrypt_rsa
from rsa_algorithm import decrypt_rsa
from rsa_algorithm import hash_message


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def key_generation(self, bits_num=1024):
        """Generates keys for the server"""
        while True:
            e = 65537
            p = prime_generator(bits_num)
            q = prime_generator(bits_num)
            n = p * q
            if gcd((p-1) * (q-1), e) == 1:
                d = pow(e, -1, (p-1) * (q-1))
                break
        self.open_key = (n, e)
        self.secret_key = (n, d)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        self.key_generation()

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            client_key = c.recv(1024).decode()
            client_key = client_key.split(' ')
            client_key = list(map(int, client_key))
            print(f"{username} tries to connect")
            # self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append((c, client_key))

            c.send((str(self.open_key[0]) + ' ' + str(self.open_key[1])).encode())

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            client[0].send(msg.encode())

    def handle_client(self, c: socket, add): 
        while True:
            msg = c.recv(1024).decode()
            msg = msg.split()
            # print(msg)
            hash = msg[1]
            msg = msg[0]
            msg = decrypt_rsa(msg, self.secret_key)
            print('Hash:')
            print(hash == str(hash_message(msg)))
            for client in self.clients:
                cl_key = client[1]
                if client[0] != c:
                    client[0].send(hash_message(msg))
                    msg = encrypt_rsa(msg, cl_key)
                    client[0].send(msg.encode())

if __name__ == "__main__":
    s = Server(9001)
    s.start()
