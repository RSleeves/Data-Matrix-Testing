from hub import light_matrix
import runloop
import sys
import os

class DataTable:
    def __init__(self, filename="robot_data"):
        # 6 Columns: Num, Name, X, Y, Dir, F/R
        self.table = []
        self.cols = 6
        self.filename = filename if filename.endswith('.csv') else filename + ".csv"
        self.headers = ["Num", "Name", "X", "Y", "Dir", "F/R"]

    # --- CORE MANIPULATION ---
    def append_row(self, data):
        """Adds a new row [Num, Name, X, Y, Dir, F/R]."""
        if len(data) == self.cols:
            self.table.append(data)
        else:
            print(f"Error: Row must have {self.cols} columns.")

    def insert_row(self, index, data):
        """Inserts a row at a specific position."""
        if 0 <= index <= len(self.table) and len(data) == self.cols:
            self.table.insert(index, data)
        else:
            print("Error: Invalid index or column count.")

    def delete_row(self, index):
        """Removes a row at index."""
        if 0 <= index < len(self.table):
            return self.table.pop(index)
        print("Error: Index out of range.")

    def modify_cell(self, row, col, new_value):
        """Updates a specific value (e.g., modify_cell(0, 1, 'NewName'))."""
        if 0 <= row < len(self.table) and 0 <= col < self.cols:
            self.table[row][col] = new_value
        else:
            print("Error: Invalid row/col index.")

    def clear(self):
        """Wipes table from memory."""
        self.table = []

    # --- SEARCH & SORT ---
    def sort_by_num(self, reverse=False):
        """Sorts the table based on the 'Num' column (Index 0)."""
        try:
            self.table.sort(key=lambda x: x[0], reverse=reverse)
            print("Sorted by 'Num'.")
        except Exception as e:
            print(f"Sort Error: {e}")

    # --- FILE I/O (HUB STORAGE) ---
    def save_to_hub(self):
        """Saves table to Hub flash memory."""
        try:
            with open(self.filename, 'w') as f:
                f.write(",".join(self.headers) + "\n")
                for row in self.table:
                    f.write(",".join(map(str, row)) + "\n")
            print(f"Successfully saved to {self.filename}")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_from_hub(self):
        """Loads table from Hub flash memory."""
        if self.filename in os.listdir():
            try:
                self.table = []
                with open(self.filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines[1:]: # Skip header
                        parts = line.strip().split(',')
                        if len(parts) == self.cols:
                            self.table.append([self._parse(x) for x in parts])
                print(f"Loaded {len(self.table)} rows.")
            except Exception as e:
                print(f"Load failed: {e}")
        else:
            print("No file found.")

    # --- CONSOLE I/O (PC INTERFACE) ---
    def export_to_console(self):
        """Prints CSV text to copy-paste into Excel."""
        print("\n--- START CSV ---")
        print(",".join(self.headers))
        for row in self.table:
            print(",".join(map(str, row)))
        print("--- END CSV ---\n")

    async def import_from_console(self):
        """Waits for user to paste CSV data. Type 'END' to finish."""
        print("\n[PASTE CSV DATA BELOW]")
        print("[TYPE 'END' TO FINISH]")
        while True:
            line = sys.stdin.readline().strip()
            if line.upper() == "END": break
            if line and "," in line:
                if any(h in line for h in self.headers): continue
                parts = line.split(",")
                if len(parts) == self.cols:
                    self.table.append([self._parse(x) for x in parts])
        print(f"Imported {len(self.table)} rows.")

    def _parse(self, val):
        """Converts strings to int/float if possible."""
        try:
            num = float(val)
            return int(num) if num.is_integer() else num
        except ValueError:
            return val

    def display(self):
        """Displays data in a readable format."""
        print("\n" + " | ".join(self.headers))
        print("-" * 45)
        for i, row in enumerate(self.table):
            print(f"{i}: {row}")

# --- EXAMPLE WORKFLOW ---
async def main():
    db = DataTable("MissionLog")

    # 1. Add Data (Out of order)
    db.append_row([3, "Target_C", 120, 40, 180, "F"])
    db.append_row([1, "Home", 0, 0, 0, "F"])
    db.append_row([2, "Gate_B", 50, 10, 90, "R"])

    # 2. Sort it
    db.sort_by_num()
    
    # 3. Modify a value
    db.modify_cell(1, 1, "Checkpoint_Alpha")

    # 4. Save and Show
    db.save_to_hub()
    db.display()

    # 5. Export for Excel
    db.export_to_console()

    # 6. Interactive Import (Uncomment to use during run)
    # await db.import_from_console()

runloop.run(main())
