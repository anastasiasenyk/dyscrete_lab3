## Usage example
![](usage_example.png)


## Module:
1. [client.py](#func3)
2. [server.py](#func2)
3. [rsa_algorithm.py](#func1)


<a id="func3"></a>
### 1. CLIENT - client.py

 functions:
 
  - key_generation
     Generates secret and open pair of keys and adds them
     as an attribute of a Client class object.
     (Uses generation of big prime numbers from big_prime_gen module)

  - init_connection
     Connects client to the server, and sends all neccessary information,
     including username and open key to keep it stored on server.
     Starts two threads, to read and to write.
     
  - read_handler
     Provides a possibility to read messages from other clients.
     Recieves server's open key and saves it.
     Decodes recieved message with own secret key and prints it.
     Contains hash check, which indicates whether message is transfered correctly.
     
  - write_handler
     Checks if message contains only symbols which can me encoded/decoded.
     Gets hash of the message and sends it to server.
     Encrypts the message with server's open key and sends it.


<a id="func2"></a>
### 2. SERVER - server.py

 functions:
 
  - key_generation
     Generates secret and open pair of keys and adds them
     as an attribute of a Client class object.
     (Uses generation of big prime numbers from big_prime_gen module)

  - start
     Starts a server, and get information about new clients (username and open key).
     Stores this information and sends new clients own open key for encrypting.
     Starts a thread to interract with clients.
     
  - broadcast
     Sends given message for all clients without encryption.
     
  - handle_client
     Gets a message from client and decrypts it with own secret key.
     Checks whether hash is correct.
     Send a message and hash to all other clients, encrypting it with their open keys.

<a id="func1"></a>
### 3. RSA - rsa_algorithm.py
functions:
 - set_dictionary

    ...
 - text_into_blocks

    ...
 - blocks_into_text

    ...
 - encrypt_rsa

    ...
 - decrypt_rsa

    ...


