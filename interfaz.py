#-------------------------------------------------------------------------------
# Name:        interfaz
# Purpose:
#
# Author:      rosit
#
# Created:     23/10/2023
# Copyright:   (c) rosit 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import PySimpleGUI as sg

def interfaz():
    sg.Window(title='FB Marketplace BOT', layout=[[]], margins=(100, 150)).read()

if __name__ == '__main__':
    interfaz()
