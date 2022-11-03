#!/usr/bin/env python3
"""
Simple sudoku solver

This codes presents a straightforward application of recursion to
implement a simple yet reasonably effective sudoku solver.  A sudoku is
represented as a string of 81 characters from the set "123456789.",
where the dot (".") represents an unknown cell.  Other characters can
be given as well, but will be ignored.

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
    block_start = 27 * (row//3) + 3 * (col//3)
    result -= {sudoku[block_start + 9*i + j] for
               i in range(3) for j in range(3)}  # Remove block digits
    return result


def recurse(sudoku, solutions):
    if "." not in sudoku:
        solutions.append(sudoku)
    else:
        # To minimize branching factor, find cell with fewest possible digits:
        best_set = set("0123456789")  # Large-enough dummy starting set
        for cell, digit in enumerate(sudoku):
            if digit == ".":
                digit_set = possible_digits(sudoku, cell)
                if len(digit_set) < len(best_set):
                    best_cell = cell
                    best_set = digit_set
        # Now we perform recursion using that cell:
        for digit in best_set:
            new_sudoku = sudoku[:best_cell] + digit + sudoku[best_cell+1:]
            recurse(new_sudoku, solutions)


def all_solutions(sudoku):
    solutions = []
    sudoku = "".join(c for c in sudoku if c in "123456789.")
    recurse(sudoku, solutions)
    return solutions
