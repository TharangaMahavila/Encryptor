import os
from src.main.util.common import secret_to_shift
from src.main.util.cipherType import CipherType
from src.main.util.route import Route


class CipherController:
    def __init__(self, decrypt=False):
        self.encrypt_type = decrypt

    def start(self):
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                choice = input("Do you want to use substitution (S) or transposition (T)?")
                if choice.lower() == "s" or choice.lower() == "t":
                    secret = input("Input the secret key:")
                    file_name = input("Input the name of the file you want to process:")
                    return self._select_menu(choice.lower(), secret, file_name)
                else:
                    raise ValueError()
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id, secret, file_name):
        match menu_id:
            case "s":
                return self._encrypt(CipherType.SUBSTITUTION, secret, file_name)
            case "t":
                return self._encrypt(CipherType.TRANSPOSITION, secret, file_name)

    def _encrypt(self, cipher_type, secret, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as infile:
                text = infile.read()

            if cipher_type == CipherType.SUBSTITUTION:
                result = self.substitution_cipher(text, secret, self.encrypt_type)

            elif cipher_type == CipherType.TRANSPOSITION:
                result = self._transposition_cipher(text, secret, self.encrypt_type)

            else:
                raise ValueError("Unknown cipher type")

            name, ext = os.path.splitext(file_name)
            output_filename = f"{name}_{cipher_type}_{'dec' if self.encrypt_type else 'enc'}{ext}"

            with open(output_filename, "w", encoding="utf-8") as outfile:
                outfile.write(result)

            print(f"The file has been {'decrypted' if self.encrypt_type else 'encrypted'} and saved as {output_filename}")
            return Route.EXIT
        except Exception as e:
            print(f"Error: {e}")
            return Route.EXIT

    def substitution_cipher(self, text, secret, decrypt=False):
        shift = secret_to_shift(secret)
        if decrypt:
            shift = -shift

        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result

    def _transposition_cipher(self, text, secret, decrypt=False):
        key = str(secret)
        key_len = len(key)

        order = sorted(range(key_len), key=lambda i: key[i])

        # ENCRYPT
        if not decrypt:
            rows = []
            for i in range(0, len(text), key_len):
                row = text[i:i + key_len]
                if len(row) < key_len:
                    row += " " * (key_len - len(row))
                rows.append(row)

            result = ""
            for col in order:
                for row in rows:
                    result += row[col]

            return result

        # DECRYPT
        else:
            rows = len(text) // key_len
            grid = [[""] * key_len for _ in range(rows)]

            index = 0
            for col in order:
                for row in range(rows):
                    grid[row][col] = text[index]
                    index += 1

            result = ""
            for row in grid:
                result += "".join(row)

            return result.rstrip()
