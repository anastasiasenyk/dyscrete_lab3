"""RSA: encoding, decoding; hash"""
import hashlib


def set_dictionary() -> dict:
    """
    create dictionary with unique symbols
    :return: dict
    """
    dict_letters = {'': '000'}
    code = 1
    for symbol in """ ,.:;!?@§#$%&*"'`^_-+±=~()[]{}<>|/\\1234567890\tІіЇїҐґЄє№₴""":
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


def text_into_blocks(message: str, block_size: int) -> list:
    """
    divide the text into blocks of numbers
    :param message: str
    :param block_size: int
    :return: list
    >>> text_into_blocks('Привіт? Hello!', 9)
    ['124157149', '143048159', '007001064', '087094094', '097006000']
    """
    blocks = []
    dict_symbols = set_dictionary()
    message = ''.join([dict_symbols[letter] for letter in message])

    for index in range(0, len(message), block_size):
        blocks.append(message[index:index+block_size])
    blocks[-1] = blocks[-1].ljust(block_size, '0')
    return blocks


def blocks_into_text(blocks: list, block_size: int) -> str:
    """
    combine a list of numeric blocks into text
    :param blocks: list
    :param block_size: int
    :return: str
    >>> blocks_into_text(['124157149', '143048159', '007001064', '087094094', '097006000'], 9)
    'Привіт? Hello!'
    """
    dictionary_keys = list(set_dictionary().keys())
    message = []
    for block in blocks:
        block = str(block).rjust(block_size, '0')
        for index in range(0, block_size, 3):
            message.append(dictionary_keys[int(block[index:index+3])])
    return ''.join(message)


def encrypt_rsa(message: str, public_key: tuple) -> list:
    """
    encoding the message according to the RCA algorithm
    :param message: str
    :param public_key: tuple(N, e)
    :return: list
    >>> encrypt_rsa('Привіт? Hello!', (226679, 2737))
    '32688 44161 193026 14987 58027 151658 219982 1 69011 44230 \
173593 173593 12513 161224'
    """
    n, e = public_key
    block_size = 3*(len(str(n))//3-1)
    encrypted_blocks = []
    for item in text_into_blocks(message, block_size):
        encrypted_blocks.append(str(pow(int(item), e, n)))

    return ' '.join(encrypted_blocks)


def decrypt_rsa(encrypted_blocks: str, private_key: tuple) -> str:
    """
    decoding the message according to the RCA algorithm
    :param encrypted_blocks: list
    :param private_key: tuple(N, d)
    :return: str
    >>> decrypt_rsa('32688 44161 193026 14987 58027 151658 219982 1 69011 \
44230 173593 173593 12513 161224', (226679, 46513))
    'Привіт? Hello!'
    """
    n, d = private_key
    block_size = 3*(len(str(n))//3-1)
    decrypted_blocks = []
    for item in encrypted_blocks.split(' '):
        decrypted_blocks.append(pow(int(item), d, n))
    return blocks_into_text(decrypted_blocks, block_size)


def hash_message(data: str) -> bytes:
    """
    return a message hash
    - sha3_512
    :param data: str
    :return: bytes
    >>> type(hash_message('a'))
    <class 'bytes'>
    """
    data = data.encode('utf-8')
    sha3_512 = hashlib.sha3_512(data).digest()
    return sha3_512