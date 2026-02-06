import os
from src.main.util.common import secret_to_shift
from src.main.util.cipherType import CipherType
from src.main.util.route import Route


class CipherController:
    def __init__(self, decrypt=False):
        self.encrypt_type = decrypt  # True if decrypting

    def start(self):
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                choice = input("Do you want to use substitution (S) or transposition (T)?")
                if choice.lower() == "s" or choice.lower() == "t":
                    # get secret key
                    secret = input("Input the secret key:")
                    # get file name
                    file_name = input("Input the name of the file you want to process:")
                    return self._select_menu(choice.lower(), secret, file_name)
                else:
                    raise ValueError()  # invalid choice
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id, secret, file_name):
        match menu_id:
            case "s":
                # substitution cipher
                return self._encrypt(CipherType.SUBSTITUTION, secret, file_name)
            case "t":
                # transposition cipher
                return self._encrypt(CipherType.TRANSPOSITION, secret, file_name)

    def _encrypt(self, cipher_type, secret, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as infile:
                text = infile.read()  # read file

            if cipher_type == CipherType.SUBSTITUTION:
                # process substitution
                result = self.substitution_cipher(text, secret, self.encrypt_type)

            elif cipher_type == CipherType.TRANSPOSITION:
                # process transposition
                result = self._transposition_cipher(text, secret, self.encrypt_type)

            else:
                raise ValueError("Unknown cipher type")

            name, ext = os.path.splitext(file_name)
            # output file name
            output_filename = f"{name}_{cipher_type}_{'dec' if self.encrypt_type else 'enc'}{ext}"

            with open(output_filename, "w", encoding="utf-8") as outfile:
                outfile.write(result)  # write result

            print(f"The file has been {'decrypted' if self.encrypt_type else 'encrypted'} and saved as {output_filename}")
            return Route.EXIT
        except Exception as e:
            print(f"Error: {e}")
            return Route.EXIT

    def substitution_cipher(self, text, secret, decrypt=False):
        shift = secret_to_shift(secret) % 256

        if not decrypt:
            data = text.encode('utf-8')
        else:
            data = bytes.fromhex(text)  # ciphertext passed as hex

        result = bytearray()
        for b in data:
            result.append((b - shift if decrypt else b + shift) % 256)

        if decrypt:
            return result.decode('utf-8')
        else:
            return result.hex()

    def _transposition_cipher(self, text, secret, decrypt=False):
        key = str(secret)  # convert secret to string
        key_len = len(key)

        # get column order
        order = sorted(range(key_len), key=lambda i: key[i])

        # ENCRYPT
        if not decrypt:
            rows = []
            for i in range(0, len(text), key_len):
                row = text[i:i + key_len]
                if len(row) < key_len:
                    # pad last row
                    row += " " * (key_len - len(row))
                rows.append(row)

            result = ""
            for col in order:
                for row in rows:
                    # read columns
                    result += row[col]

            return result

        # DECRYPT
        else:
            rows = len(text) // key_len
            # prepare grid
            grid = [[""] * key_len for _ in range(rows)]

            index = 0
            for col in order:
                for row in range(rows):
                    # fill grid
                    grid[row][col] = text[index]
                    index += 1

            result = ""
            for row in grid:
                # read rows
                result += "".join(row)

            # remove padding
            return result.rstrip()
