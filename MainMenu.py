from Index import Index
from Search import Search
from Inspection import Inspection
import re

class MainMenu:
    index = Index()
    search = Search()
    inspection = Inspection()

    def startMenu(self):
        running = True

        while(running):
            print('Ingresar instrucción:')
            cmd = input()
            print('--- --- --- --- ---')
            if cmd != '':
                instruction = cmd.split()[0]
                if instruction == 'indizar':
                    pass
                elif instruction == 'buscar':
                    pass
                elif instruction == 'mostar':
                    pass
                elif instruction == 'terminar':
                    running = False
                else:
                    print('Instrucción no válida')
            else:
                print('Debe ingresar una instrucción')
            print('--- --- --- --- ---')


menu = MainMenu()
menu.startMenu()