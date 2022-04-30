import hashlib
p = 419
q = 541
N = p * q
e = 2737
d = 46513


def set_dictionary():
    dict_letters = {'': '000'}
    code = 1
    for symbol in """ ,.:;!?@§#$%&*"'`^_-+±=~()[]{}<>|/\\1234567890\t""":
        if code <= 9:
            letter_code = '00' + str(code)
        elif code <= 99:
            letter_code = '0' + str(code)
        else:
            letter_code = str(code)
        dict_letters[symbol] = letter_code
        code += 1

    for letters in [('A', 'Z'), ('a', 'z'), ('А', 'Я'), ('а', 'я')]:
        for index in range(ord(letters[0]), ord(letters[1])+1):
            if code <= 99:
                letter_code = '0' + str(code)
            else:
                letter_code = str(code)
            dict_letters[chr(index)] = letter_code
            code += 1
    return dict_letters


def text_into_blocks(message, block_size):
    blocks = []
    dict_symbols = set_dictionary()
    message = ''.join([dict_symbols[letter] for letter in message])

    for index in range(0, len(message), block_size):
        blocks.append(message[index:index+block_size])
    blocks[-1] = blocks[-1].ljust(block_size, '0')
    return blocks


def blocks_into_text(blocks, block_size):
    dictionary_keys = list(set_dictionary().keys())
    message = []
    for block in blocks:
        block = str(block).rjust(block_size, '0')
        for index in range(0, block_size, 3):
            message.append(dictionary_keys[int(block[index:index+3])])
    return ''.join(message)


def encrypt_rsa(message, public_key):
    n, e = public_key
    block_size = 3*(len(str(n))//3)
    encrypted_blocks = []
    for item in text_into_blocks(message, block_size):
        encrypted_blocks.append((int(item)**e) % n)
    return encrypted_blocks


def decrypt_rsa(encrypted_blocks, private_key):
    n, d = private_key
    block_size = 3*(len(str(n))//3)
    decrypted_blocks = []
    for item in encrypted_blocks:
        decrypted_blocks.append((item**d) % n)
    print('decrypted blocks: ', decrypted_blocks)
    return blocks_into_text(decrypted_blocks, block_size)


def hash_message(data):
    data = data.encode('utf-8')
    sha3_512 = hashlib.sha3_512(data).digest()
    return sha3_512


# message = 'ZzЯя .fkhvbkjl;ds;osejis'
message = input('message: ')
print('message: ', message)

e_blocks = encrypt_rsa(message, (N, e))
print('encrypted: ', e_blocks)

de_blocks = decrypt_rsa(e_blocks, (N, d))
print('decrypted: ', de_blocks)

print('hash1 == hash2: ', hash_message(message) == hash_message(de_blocks))

