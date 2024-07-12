# flag{GJVWUSSL[[QOESXVZVULWY^WQL[W^XO}

from pwn import *
from typing import List

p = process("./sudoku")

def parse_grid(output):
    grid = []
    lines = output.strip().split("\n")
    for line in lines[1:-1]:
        line = line.strip()
        if line.startswith("|"):
            row = []
            for char in line:
                if char.isdigit():
                    row.append(int(char))
                elif char == '.':
                    row.append(None)
            if len(row) == 9:
                grid.append(row)
    return grid

def is_valid_move(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    box_row_start = row - row % 3
    box_col_start = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[box_row_start + i][box_col_start + j] == num:
                return False
    return True

def solve(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] is None: 
                for num in range(1, 10): 
                    if is_valid_move(grid, row, col, num):  
                        grid[row][col] = num 
                        if solve(grid):  
                            return True
                        grid[row][col] = None 
                return False
    return True

def send_solved_grid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] is not None:
                # print(f"Sending: {row} {col} {grid[row][col]}")  # Debugging line
                p.sendline(f"{row} {col} {grid[row][col]} ".encode())
                p.recvuntil("Enter row (0-8), column (0-8), and number (1-9) to fill (space-separated):").decode()

def solve_sudoku():
    for _ in range(420):
        p.sendline(f"0 0 #".encode())
        output = p.recvuntil("Enter row (0-8), column (0-8), and number (1-9) to fill (space-separated):").decode()
        # print(output)
        grid = parse_grid(output)
        solve(grid)    # Solved the complete grid (when first time a sudoku appears)
        # print(grid)
        send_solved_grid(grid)  # this will send the input one by one after receiving updated sudoku from last step


solve_sudoku()
currline = p.recvall().decode()
print(currline)
p.close()

