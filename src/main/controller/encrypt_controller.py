import os
from src.main.util.common import secret_to_shift
from src.main.util.route import Route


class EncryptController:
    def __init__(self):
        self.login_service = None

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
                return self._substitution_encrypt(secret, file_name)
            case "t":
                return None

    def _substitution_encrypt(self, secret, file_name):
        with open(file_name, "r", encoding="utf-8") as infile:
            plaintext = infile.read()

        shift = secret_to_shift(secret)
        result = ""

        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char  # keep spaces, numbers, symbols

        name, ext = os.path.splitext(file_name)
        output_filename = f"{name}_enc{ext}"
        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(result)

        print("The file has been encrypted and the results have been saved in the file ", output_filename)
        return Route.EXIT
