import sys
from src.main.controller.menu_controller import MenuController
from src.main.controller.cipher_controller import CipherController
from src.main.util.route import Route


class RouterController:
    def __init__(self):
        self.controllers = {
            Route.MENU: MenuController(),
            Route.ENCRYPT: CipherController(False),
            Route.DECRYPT: CipherController(True),
        }

    def start(self):
        route = Route.MENU

        while route != Route.EXIT:
            controller = self.controllers[route]
            direction = controller.start()
            if direction:
                route = direction

        print("Thank you for using the application!")
        sys.exit(0)
