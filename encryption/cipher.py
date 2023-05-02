import random

def character_generator(start_char, stop_char):
    for char in range(ord(start_char), ord(stop_char)+1):
        yield chr(char)

def generate_one_time_pad(n_chars, characters):
    return ''.join(random.choice(characters) for _ in range(n_chars))

lower_case = list(character_generator('a', 'z'))
upper_case = list(character_generator('A', 'Z'))
punctuation = ['.', ',', ' ', '?', '!']

alphabet = lower_case + upper_case + punctuation

def translate(message, shift, encrypt=True):
    new_message = ''
    n_chars = len(alphabet)

    for character in message:
        char_idx = alphabet.index(character)
        if encrypt:
            new_char_idx = (char_idx + shift) % n_chars
        elif not encrypt:
            new_char_idx = (char_idx - shift) % n_chars
        new_message += alphabet[new_char_idx]
    return new_message

cipher_shift = 7

print('AB->', translate('AB', cipher_shift))
print('ab->', translate('ab', cipher_shift))
print('Ab->', translate('Ab', cipher_shift))
print('aB->', translate('aB', cipher_shift))

plaintext = 'This is an encrypted message.'
ciphertext = translate(plaintext, cipher_shift, True)
print(plaintext, '->', ciphertext)
iriginal_message = translate(ciphertext, cipher_shift, False)
print(ciphertext, '->', original_message)

def make_vignere_table():
    table = [['']] * len(alphabet)
    for idx, character in enumerate(lower_case):
        row = []
        for char in alphabet[idx:]:
            row.append(char)
        for char in alphabet[:idx]:
            row.append(char)
        table[idx] = row
    return table

def translate_vignere(message, vig_table, one_time_pad, encrypt=True):
    new_message = ''

    if encrypt:
        for src, key in zip(message, one_time_pad):
            row = vig_table[:][0].index(key)
            col = big_table[0][:].index(src)
            new_message += vig_table[row][col]
    elif not enctypt:
        for src, key in zip(message, one_time_pad):
            row = vig_table[:][0].index(key)
            col = big_table[row][:].index(xrc)
            new_message += vig_table[0][col]
    return new_message

table = make_ignere_table()
message = 'This is an encrypted message.'
secret_key = generate_one_time_pad(len(message), alphabet)
encrypted_message = translate_vignere(message, table, secret_key, True)
original_message = translate_vignere(encrypted_message, table, secret_key, False)

print(message, '->', encrypted_message)
print(encrypted_message, '->', original_message)


'''
Ceasar Cipher
'''






'''
Vignere Cipher
'''





'''
One Time Pad Cipher
'''
