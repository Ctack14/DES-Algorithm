import pytest
import main


def test_encrypt():
    plain_text_hex = "0123456789ABCDEF"
    large_plain_text_hex = "0123456789ABCDEF0123456789ABCDEF"
    key_hex = "133457799BBCDFF1"
    expected_cipher_text_hex = "85E813540F0AB405"
    expected_large_cipher_text_hex = "85E813540F0AB40585E813540F0AB405"


    plain_text = main.format_text(plain_text_hex)
    large_plain_text = main.format_text(large_plain_text_hex)
    key = main.format_text(key_hex)

    cipher_text = main.encrypt(plain_text, key)
    large_cipher_text = main.encrypt(large_plain_text, key)
    large_cipher_text_hex = hex(int(large_cipher_text, 2))[2:].upper().zfill(32)
    cipher_text_hex = hex(int(cipher_text, 2))[2:].upper().zfill(16)


    assert large_cipher_text_hex == expected_large_cipher_text_hex
    assert cipher_text_hex == expected_cipher_text_hex