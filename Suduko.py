import tkinter as tk
from tkinter import messagebox
import random

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        
        # Create the grid
        self.grid = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]

        self.create_widgets()
        self.generate_puzzle()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18), borderwidth=1, relief='solid', justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry

        check_button = tk.Button(self.root, text="Check", command=self.check_solution)
        check_button.grid(row=10, columnspan=9, pady=5)

    def generate_puzzle(self):
        # Fill the grid with a valid Sudoku solution
        self.solve(self.grid)
        
        # Randomly remove elements to create the puzzle
        for _ in range(50):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.grid[row][col] = 0

        self.update_grid_display()

    def update_grid_display(self):
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j]
                self.entries[i][j].delete(0, tk.END)
                if value != 0:
                    self.entries[i][j].insert(0, str(value))
                    self.entries[i][j].config(state='disabled')

    def check_solution(self):
        user_grid = [[0] * 9 for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value:
                    try:
                        value = int(value)
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter only numbers.")
                        return
                    user_grid[i][j] = value
                else:
                    messagebox.showinfo("Incomplete", "Please complete the Sudoku.")
                    return

        if self.is_complete(user_grid) and self.is_valid_sudoku(user_grid):
            messagebox.showinfo("Congratulations", "You successfully completed the Sudoku!")
        else:
            messagebox.showinfo("Incorrect", "The Sudoku is incorrect. Try again.")

    def is_complete(self, grid):
        for row in grid:
            if 0 in row:
                return False
        return True

    def is_valid_sudoku(self, grid):
        def is_valid_row(row):
            return len(set(row)) == 9

        def is_valid_col(col):
            return len(set(col)) == 9

        def is_valid_box(box):
            return len(set(box)) == 9

        for i in range(9):
            if not is_valid_row([grid[i][j] for j in range(9)]):
                return False
            if not is_valid_col([grid[j][i] for j in range(9)]):
                return False

        for box_x in range(3):
            for box_y in range(3):
                if not is_valid_box([grid[i][j] for i in range(box_x * 3, (box_x + 1) * 3) for j in range(box_y * 3, (box_y + 1) * 3)]):
                    return False

        return True

    def find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def valid(self, grid, num, pos):
        row, col = pos

        # Check row
        for i in range(9):
            if grid[row][i] == num and i != col:
                return False

        # Check column
        for i in range(9):
            if grid[i][col] == num and i != row:
                return False

        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self, grid):
        find = self.find_empty(grid)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(grid, i, (row, col)):
                grid[row][col] = i

                if self.solve(grid):
                    return True

                grid[row][col] = 0

        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
