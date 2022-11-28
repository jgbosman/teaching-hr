#!/usr/bin/env python3
"""
Simple sudoku solver

This codes presents a straightforward application of recursion to
implement a simple yet reasonably effective sudoku solver.

A sudoku is represented as a string of 81 characters from the set
"123456789.", where the dot (".") represents an unknown cell.  Other c
haracters can be given as well, but will be ignored.

Three easy-to-understand recursion implementations are given, in
increasing order of complexity and speed.

EXAMPLE (Wikipedia):
>>> sudoku = '''
...     53..7....
...     6..195...
...     .98....6.
...     8...6...3
...     4..8.3..1
...     7...2...6
...     .6....28.
...     ...419..5
...     ....8..79
...     '''
>>> solutions = all_solutions(sudoku)
>>> len(solutions)
1
>>> print_sudoku(solutions[0])
┌───┬───┬───┐
│534│678│912│
│672│195│348│
│198│342│567│
├───┼───┼───┤
│859│761│423│
│426│853│791│
│713│924│856│
├───┼───┼───┤
│961│537│284│
│287│419│635│
│345│286│179│
└───┴───┴───┘

EXAMPLE (Arto Inkala's "World's Hardest Sudoku"):
>>> sudoku = '''
...     8........
...     ..36.....
...     .7..9.2..
...     .5...7...
...     ....457..
...     ...1...3.
...     ..1....68
...     ..85...1.
...     .9....4..
...     '''
>>> print_sudoku(all_solutions(sudoku)[0])
┌───┬───┬───┐
│812│753│649│
│943│682│175│
│675│491│283│
├───┼───┼───┤
│154│237│896│
│369│845│721│
│287│169│534│
├───┼───┼───┤
│521│974│368│
│438│526│917│
│796│318│452│
└───┴───┴───┘
"""

def print_sudoku(sudoku):
    sudoku = "".join(c for c in sudoku if c in "123456789.")
    for i in range(3):
        print("┌───┬───┬───┐" if i == 0 else "├───┼───┼───┤")
        for row in range(3*i, 3*i + 3):
            sudorow = sudoku[9*row : 9*row + 9]
            print(f"│{sudorow[:3]}│{sudorow[3:6]}│{sudorow[6:]}│")
    print("└───┴───┴───┘")


def possible_digits(sudoku, cell):
    row, col = divmod(cell, 9)
    result = set("123456789")
    result -= set(sudoku[9*row : 9*row + 9])  # Remove row digits
    result -= set(sudoku[col::9])  # Remove column digits
    block_start = 27 * (row//3) + 3 * (col//3)  # Upper-left cell of block
    result -= {sudoku[block_start + 9*i + j] for
               i in range(3) for j in range(3)}  # Remove block digits
    return result


def recurse_1(sudoku):
    if "." not in sudoku:  # Base case: sudoku has been filled in completely
        return [sudoku]
    else:
        cell = sudoku.find(".")  # Select first unexplored cell for exploration
        result = []
        for digit in possible_digits(sudoku, cell):
            new_sudoku = sudoku[:cell] + digit + sudoku[cell+1:]
            result += recurse_1(new_sudoku)  # Recursive call
        return result


def recurse_2(sudoku):
    if "." not in sudoku:  # Base case: sudoku has been filled in completely
        return [sudoku]
    else:
        # To reduce the branching factor, pick cell with fewest possibilities:
        free_cells = [cell for cell in range(81) if sudoku[cell] == "."]
        best_cell = min(free_cells,
                        key=lambda cell: len(possible_digits(sudoku, cell)))
        result = []
        for digit in possible_digits(sudoku, best_cell):
            new_sudoku = sudoku[:best_cell] + digit + sudoku[best_cell+1:]
            result += recurse_2(new_sudoku)  # Recursive call
        return result


def recurse_3(sudoku):
    if "." not in sudoku:  # Base case: sudoku has been filled in completely
        return [sudoku]
    else:
        # To reduce the branching factor, pick cell with fewest possibilities:
        best_cell_digits = set("1234567890")  # Large-enough dummy starting set
        for cell in range(81):
            if sudoku[cell] == ".":
                digits = possible_digits(sudoku, cell)
                if len(digits) == 1:  # Place all naked singles immediately
                    digit, = digits  # Extract element from 1-element set
                    sudoku = sudoku[:cell] + digit + sudoku[cell+1:]
                if len(digits) < len(best_cell_digits):
                    if not digits:  # No solution exists
                        return []
                    best_cell = cell
                    best_cell_digits = digits

        result = []
        for digit in best_cell_digits:
            new_sudoku = sudoku[:best_cell] + digit + sudoku[best_cell+1:]
            result += recurse_3(new_sudoku)  # Recursive call
        return result


def all_solutions(sudoku, recurse=recurse_3):
    sudoku = "".join(c for c in sudoku if c in "123456789.")
    return recurse(sudoku)
