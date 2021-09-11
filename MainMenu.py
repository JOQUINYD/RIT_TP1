from os import error
from Index import Index
from Search import Search
from Inspection import Inspection
import re
import os

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
                if self.__indexArgumentsValid(cmdMatches.group(1), cmdMatches.group(2)):
                    print('Ejecutandose...')
                    self.index.doIndexing(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3))
                    print('Completado con exito')
                else:
                    print("ERROR - Directorio o Archivo inválido")
            except error:
                print("ERROR - Ingresar direcciones válidas")
    
    def __search(self, cmd):
        cmdMatches = re.search('buscar \"([^\"]*)\" (.+) \"([^\"]*)\" ([0-9]+) \"([^\"]*)\"', cmd)
        if cmdMatches != None:
            try:
                if self.__searchArgumentsValid(cmdMatches.group(1), cmdMatches.group(2)):
                    print('Ejecutandose...')
                    self.search.search(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3), int(cmdMatches.group(4)), cmdMatches.group(5))
                    print('Completado con exito')
                else:
                    print("Error - Directorio o tipo inválido")
            except error:
                print("ERROR - Ingresar direcciones que existan")

    def __inspect(self, cmd):
        cmdMatches = re.search('mostrar \"([^\"]*)\" (.+) \"([^\"]*)\"', cmd)
        if cmdMatches != None:
            try:
                if self.__inspectArgumentsValid(cmdMatches.group(1), cmdMatches.group(2)):
                    print('Ejecutandose...')
                    self.inspection.inspect(cmdMatches.group(1), cmdMatches.group(2), cmdMatches.group(3))
                    print('Completado con exito')
                else:
                    print("Error - Directorio o tipo inválido")
            except error:
                print("ERROR - Ingresar direcciones que existan")
        
    def __isDirectoryValid(self, path):
        if os.path.exists(path):
            return len(os.listdir(path)) != 0
        return False

    def __fileExists(self, path):
        return os.path.isfile(path)

    def __indexArgumentsValid(self, filesPath, stopwordsPath):
        return self.__isDirectoryValid(filesPath) and self.__fileExists(stopwordsPath)

    def __searchArgumentsValid(self, indexPath, searchType):
        return self.__isDirectoryValid(indexPath) and (searchType == 'vec' or searchType == 'bm25')

    def __inspectArgumentsValid(self, indexPath, inspectType):
        return self.__isDirectoryValid(indexPath) and (inspectType == 'ter' or inspectType == 'doc')

menu = MainMenu()
menu.startMenu()