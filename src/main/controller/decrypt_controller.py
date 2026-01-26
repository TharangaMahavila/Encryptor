from src.main.util.route import Route


class DecryptController:
    def __init__(self):
        self.login_service = None

    def start(self):
        attempts = 0
        while True:
            if attempts == 5:
                print("Five invalid attempts. Come back again later!")
                break
            try:
                choice = input("Do you want to encrypt (E) or decrypt (D)?")
                if choice.lower() == "e" or choice.lower() == "d":
                    return self._select_menu(choice.lower())
                else:
                    raise ValueError()
            except ValueError:
                attempts += 1
                print("Invalid choice. Please try again\n")

    def _select_menu(self, menu_id):
        match menu_id:
            case "e":
                return self._user_login()
            case "d":
                self._member_registration()
