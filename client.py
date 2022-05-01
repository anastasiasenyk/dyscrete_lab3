import socket
import threading
from math import gcd
from big_prime_gen import prime_generator
from rsa_algorithm import encrypt_rsa
from rsa_algorithm import decrypt_rsa
from rsa_algorithm import hash_message


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.open_key = None
        self.secret_key = None
        self.server_open_key = None

    def key_generation(self, bits_num=1024):
        """Generates keys for the client"""
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

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        self.key_generation()

        self.s.send((str(self.open_key[0]) + ' ' + str(self.open_key[1])).encode())

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        self.server_open_key = self.s.recv(1024).decode()
        self.server_open_key = self.server_open_key.split(' ')
        self.server_open_key = list(map(int, self.server_open_key))


        while True:
            hash = self.s.recv(1024)
            message = self.s.recv(1024).decode()

            message = decrypt_rsa(message, self.secret_key)
            if hash != hash_message(message):
                print('Hash of the message is not equal! Possible transfering error.')

            print(message)

    def write_handler(self):
        while True:
            message = input()
            hash = hash_message(message)

            message = encrypt_rsa(message, self.server_open_key)

            message += ' '
            message += str(hash)

            # self.s.send(hash)
            self.s.send(message.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
