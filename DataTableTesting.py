from hub import light_matrix
import runloop
import sys
import os

class DataTable:
    def __init__(self, filename="mission_data"):
        self.table = []
        self.cols = 5
        self.filename = filename if filename.endswith('.csv') else filename + ".csv"
        self.headers = ["Time", "Sensor_A", "Sensor_B", "Motor_Pos", "Status"]

    # --- ROW MANIPULATION ---
    def append_row(self, data):
        """Adds a new row to the end."""
        if len(data) == self.cols:
            self.table.append(data)
            print(f"Row added. Total rows: {len(self.table)}")
        else:
            print(f"Error: Row must have {self.cols} columns.")

    def insert_row(self, index, data):
        """Inserts a row at a specific index."""
        if 0 <= index <= len(self.table) and len(data) == self.cols:
            self.table.insert(index, data)
        else:
            print("Error: Invalid index or column count.")

    def delete_row(self, index):
        """Removes a row by index."""
        if 0 <= index < len(self.table):
            return self.table.pop(index)
        print("Error: Index out of range.")

    def modify_cell(self, row, col, new_value):
        """Changes a single value in the table."""
        if 0 <= row < len(self.table) and 0 <= col < self.cols:
            self.table[row][col] = new_value
        else:
            print("Error: Invalid coordinates.")

    # --- FILE STORAGE (HUB INTERNAL MEMORY) ---
    def save_to_hub(self):
        """Saves current table to the Hub's internal flash storage."""
        try:
            with open(self.filename, 'w') as f:
                f.write(",".join(self.headers) + "\n")
                for row in self.table:
                    f.write(",".join(map(str, row)) + "\n")
            print(f"File '{self.filename}' saved to Hub memory.")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_from_hub(self):
        """Reads data from the Hub's storage back into the table list."""
        if self.filename in os.listdir():
            try:
                self.table = []
                with open(self.filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines[1:]: # Skip header
                        parts = line.strip().split(',')
                        if len(parts) == self.cols:
                            self.table.append([self._parse(x) for x in parts])
                print(f"Loaded {len(self.table)} rows from Hub.")
            except Exception as e:
                print(f"Load failed: {e}")
        else:
            print("No file found on Hub.")

    # --- CONSOLE I/O (BRIDGE TO COMPUTER) ---
    def export_to_console(self):
        """Prints formatted CSV for you to copy-paste into Excel."""
        print("\n--- COPY DATA BELOW ---")
        print(",".join(self.headers))
        for row in self.table:
            print(",".join(map(str, row)))
        print("--- END OF DATA ---\n")

    async def import_from_console(self):
        """Waits for user to paste CSV data into the terminal. Type 'END' to finish."""
        print("\n[PASTE CSV DATA BELOW]")
        print("[TYPE 'END' AND PRESS ENTER TO FINISH]")
        self.table = []
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
        """Helper to convert strings to numbers where possible."""
        try:
            num = float(val)
            return int(num) if num.is_integer() else num
        except ValueError:
            return val

    def display(self):
        """Prints a clean view of the table to the Hub console."""
        print(f"\nTable: {self.filename}")
        print(" | ".join(self.headers))
        for i, row in enumerate(self.table):
            print(f"{i}: {row}")

# --- MAIN EXECUTION ---
async def main():
    db = DataTable("RobotLog")

    # 1. Capture some sample data
    db.append_row([0.0, 100, 50, 0, "START"])
    db.append_row([1.2, 110, 55, 90, "DRIVING"])
    db.append_row([2.5, 105, 52, 180, "STOP"])

    # 2. Demonstrate modification
    db.modify_cell(1, 4, "TURNING")
    
    # 3. Save to Hub storage (Internal)
    db.save_to_hub()

    # 4. Export to Console (For you to copy to Excel)
    db.export_to_console()

    # 5. Wait for user to paste data back in (Interactive)
    # Note: You can paste the data that was just exported!
    await db.import_from_console()

    # 6. Final display
    db.display()

runloop.run(main())
