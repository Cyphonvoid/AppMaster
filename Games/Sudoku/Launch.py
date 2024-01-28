from .SudokuGame import *

def launch(parent):
    sudoku = Sudoku(parent, row=0, column=1, columnspan=3, rowspan=3, sticky="nsew")
    sudoku.start()