from os import error
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
                    self.__index(cmd)
                elif instruction == 'buscar':
                    self.__search(cmd)
                elif instruction == 'mostrar':
                    self.__inspect(cmd)
                elif instruction == 'terminar':
                    running = False
                else:
                    print('Instrucción no válida')
            else:
                print('Debe ingresar una instrucción')
            print('--- --- --- --- ---')
            print()
    
    def __index(self, cmd):
        cmdMatches = re.search('indizar \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\"', cmd)
        if cmdMatches != None:
            try:
                print('Ejecutandose...')
                self.index.doIndexing(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3))
                print('Completado con exito')
            except error:
                print("ERROR - Ingresar direcciones que existan")
    
    def __search(self, cmd):
        cmdMatches = re.search('buscar \"([^\"]*)\" (.+) \"([^\"]*)\" ([0-9]+) \"([^\"]*)\"', cmd)
        if cmdMatches != None:
            try:
                print('Ejecutandose...')
                self.search.search(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3), int(cmdMatches.group(4)), cmdMatches.group(5))
                print('Completado con exito')
            except error:
                print("ERROR - Ingresar direcciones que existan")

    def __inspect(self, cmd):
        cmdMatches = re.search('mostrar \"([^\"]*)\" (.+) \"([^\"]*)\"', cmd)
        if cmdMatches != None:
            try:
                print('Ejecutandose...')
                self.inspection.inspect(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3))
                print('Completado con exito')
            except error:
                print("ERROR - Ingresar direcciones que existan")
        
menu = MainMenu()
menu.startMenu()