from tables import (
    IP, FP, E, P, S_BOXES, PC1, PC2, SHIFTS
)

#Helper functions
def hex_to_bin(hex_string):
    decimal_value = int(hex_string, 16)
    binary_string = bin(decimal_value)[2:]  # Remove the '0b' prefix
    # Pad with leading zeros to ensure it's 64 bits
    padded_binary_string = binary_string.zfill(len(hex_string) * 4)
    return padded_binary_string

def int_to_bin(n):
    binary_string = bin(int(n))[2:]
    pad_len = (64 - len(binary_string) % 64) % 64
    binary_string = '0' * pad_len + binary_string
    return tuple(int(bit) for bit in binary_string)

def text_to_bin(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return tuple(int(bit) for bit in binary_string)


def permute(block, table):
    return tuple([block[i - 1] for i in table])

def left_shift(block, n):
    return block[n:] + block[:n]

def xor(block1, block2):
    comb = zip(block1, block2)
    return tuple(b1 ^ b2 for b1, b2 in comb)

def generate_sub_keys(key):
    key = permute(key, PC1)
    C = key[:28]
    D = key[28:]
    sub_keys = []
    for shift in SHIFTS:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        combined_key = C + D
        sub_key = permute(combined_key, PC2)
        sub_keys.append(sub_key)
    return sub_keys # all 16 subkeys

def s_box(input_bits):
    result = []
    for i in range(8):
        block = input_bits[i*6:(i+1)*6]
        row = block[0] * 2 + block[5]
        col = block[1] * 8 + block[2] * 4 + block[3] * 2 + block[4]
        value = S_BOXES[i][row * 16 + col]
        value = bin(value)[2:].zfill(4)
        result.extend(int(bit) for bit in value)
    return tuple(result)


def f(R, K):
    R_expanded = permute(R, E)
    xor_result = xor(R_expanded, K)
    sbox_result = s_box(xor_result)
    f_result = permute(sbox_result, P)
    return f_result


def round(L, R, K):
    new_R = xor(L, f(R, K))
    new_L = R
    return new_L, new_R

def break_into_64bit(text):
    blocks = []
    for i in range (0, (len(text) + 63) // 64):
        block = text[i * 64: (i + 1) * 64]
        blocks.append(block)
    return blocks



def encrypt(plain_text, key):
    cipher_text = ''
    sub_keys = generate_sub_keys(key)
    for block in break_into_64bit(plain_text):
        broken_text = permute(block, IP)
        L = broken_text[:32]
        R = broken_text[32:]
        for K in sub_keys:
            L, R = round(L, R, K)
        combined_text = R + L
        cipher_text += ''.join(str(bit) for bit in permute(combined_text, FP))
    return cipher_text

def decrypt(cipher_text, key):
    plain_text = ''
    sub_keys = generate_sub_keys(key)[::-1]
    for block in break_into_64bit(cipher_text):
        broken_text = permute(block, IP)
        L = broken_text[:32]
        R = broken_text[32:]
        for K in sub_keys:
            L, R = round(L, R, K)
        combined_text = R + L
        plain_text += ''.join(str(bit) for bit in permute(combined_text, FP))
    return plain_text


def format_text(text):
    text = hex_to_bin(text)
    return tuple(int(bit) for bit in text)

def main():

    m_choice = input("What format is  your text in? Enter 1-4\n1) Hex\n2) Int\n3) Bin\n4) ASCII\n   ")
    k_choice = input("What format is  your key in? Enter 1-4\n1) Hex\n2) Int\n3) Bin\n4) ASCII\n   ")
    user_message = input("Enter your text: ")
    user_key = input("Enter your key: ")
    if m_choice == '1':
        plain_text = format_text(user_message)
    elif m_choice == '2':
        plain_text = int_to_bin(user_message)
    elif m_choice == '3':
        plain_text = tuple(int(bit) for bit in user_message.zfill(64))
    elif m_choice == '4':
        plain_text = text_to_bin(user_message)
    else:
        print("Invalid choice for message format.")
        return

    if k_choice == '1':
        user_key = format_text(user_key)
    elif k_choice == '2':
        user_key = tuple(int(bit) for bit in bin(int(user_key))[2:].zfill(64))
    elif k_choice == '3':
        user_key = tuple(int(bit) for bit in user_key.zfill(64))
    elif k_choice == '4':
        user_key = text_to_bin(user_key)
    else:
        print("Invalid choice for key format.")
        return

    decryption_choice = input("Would you like to encrypt or decrypt?: ").lower()
    if decryption_choice == 'decrypt':
        plain_text = decrypt(plain_text, user_key)
        plain_text_hex = hex(int(plain_text, 2))[2:].upper().zfill(16)
        print(f"\nPlain Text (Hex): {plain_text_hex}")

    elif decryption_choice == 'encrypt':
        cipher_text = encrypt(plain_text, user_key)
        cipher_text_hex = hex(int(cipher_text, 2))[2:].upper().zfill(16)
        print(f"\nCipher Text (Hex): {cipher_text_hex}")

    elif decryption_choice != 'encrypt' or 'decrypt':
        print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")


    done_choice = input("\nWould you like to process another message? (yes/no): ").lower()
    if done_choice == 'yes':
        main()
    elif done_choice == 'no':
        print("\nExiting the program.\n")
        return
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        return








    ''' Example usage
    plain_text_hex = "0123456789ABCDEF"
    key_hex = "133457799BBCDFF1"
    plain_large_text_hex = "0123456789ABCDEF0123456789ABCDEF"

    plain_text = format_text(plain_text_hex)
    plain_large_text = format_text(plain_large_text_hex)
    key = format_text(key_hex)


    cipher_text = encrypt(plain_text, key)
    cipher_large_text = encrypt(plain_large_text, key)

    cipher_text_hex = hex(int(cipher_text, 2))[2:].upper().zfill(16)
    cipher_large_text_hex = hex(int(cipher_large_text, 2))[2:].upper().zfill(32)

    print(f"\nPlain Text: {plain_text_hex}")
    print(f"Key: {key_hex}")
    print(f"Cipher Text: {cipher_text_hex}")
    print(f"Plain Large Text: {plain_large_text_hex}")
    print(f"Cipher Large Text: {cipher_large_text_hex}")'''


if __name__ == "__main__":
    main()