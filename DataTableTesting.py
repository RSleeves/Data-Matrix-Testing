from hub import light_matrix
import runloop
import sys
import os
import math

class DataMaster:
    def __init__(self, filename="mission_data"):
        # Table Structure: [Num, Name, X, Y, Dir, F/R]
        # F/R is now: 1 for FWD, -1 for REV
        self.table = []
        self.cols = 6
        self.filename = filename if filename.endswith('.csv') else filename + ".csv"
        self.headers = ["Num", "Name", "X", "Y", "Dir", "F/R"]

    # --- ROW MANIPULATION ---
    def append_row(self, data):
        """Adds a new row. F/R (index 5) should be 1 or -1."""
        if len(data) == self.cols:
            self.table.append(data)
        else:
            print(f"Error: Expected {self.cols} columns.")

    def insert_row(self, index, data):
        if 0 <= index <= len(self.table) and len(data) == self.cols:
            self.table.insert(index, data)

    def delete_row(self, index):
        if 0 <= index < len(self.table):
            return self.table.pop(index)

    def modify_cell(self, row, col, new_value):
        if 0 <= row < len(self.table) and 0 <= col < self.cols:
            self.table[row][col] = new_value

    # --- TOOLS: SORTING & NAVIGATION ---
    def sort_by_num(self, reverse=False):
        try:
            self.table.sort(key=lambda x: x[0], reverse=reverse)
        except Exception as e:
            print(f"Sort error: {e}")

    def get_navigation(self, start_idx, end_idx):
        """Calculates distance and heading between two points."""
        try:
            r1, r2 = self.table[start_idx], self.table[end_idx]
            dx, dy = r2[2] - r1[2], r2[3] - r1[3]
            
            distance = math.sqrt(dx**2 + dy**2)
            angle_deg = math.degrees(math.atan2(dy, dx))
            heading = angle_deg if angle_deg >= 0 else angle_deg + 360
            
            return {"dist": round(distance, 2), "head": round(heading, 2)}
        except IndexError:
            return None

    # --- FILE & CONSOLE I/O ---
    def save_to_hub(self):
        try:
            with open(self.filename, 'w') as f:
                f.write(",".join(self.headers) + "\n")
                for row in self.table:
                    f.write(",".join(map(str, row)) + "\n")
            print(f"Saved to {self.filename}")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_from_hub(self):
        if self.filename in os.listdir():
            try:
                self.table = []
                with open(self.filename, 'r') as f:
                    lines = f.readlines()
                    for line in lines[1:]:
                        parts = line.strip().split(',')
                        if len(parts) == self.cols:
                            self.table.append([self._parse(x) for x in parts])
                print(f"Loaded {len(self.table)} rows.")
            except Exception as e:
                print(f"Load failed: {e}")

    def export_to_console(self):
        print("\n--- CSV DATA START ---")
        print(",".join(self.headers))
        for row in self.table:
            print(",".join(map(str, row)))
        print("--- CSV DATA END ---\n")

    async def import_from_console(self):
        print("\n[PASTE DATA AND TYPE 'END' TO FINISH]")
        while True:
            line = sys.stdin.readline().strip()
            if line.upper() == "END": break
            if line and "," in line:
                if any(h in line for h in self.headers): continue
                parts = line.split(",")
                if len(parts) == self.cols:
                    self.table.append([self._parse(x) for x in parts])

    def _parse(self, val):
        """Helper to convert input. Now handles 1/-1 for F/R."""
        val = val.strip()
        # Handle specific string to int conversion for F/R if needed
        if val.upper() == "FWD" or val.upper() == "F": return 1
        if val.upper() == "REV" or val.upper() == "R": return -1
        
        try:
            num = float(val)
            return int(num) if num.is_integer() else num
        except ValueError:
            return val

    def display(self):
        print("\n" + " | ".join(self.headers))
        print("-" * 55)
        for i, row in enumerate(self.table):
            # Display helpful labels for the F/R column
            status = "FWD" if row[5] == 1 else "REV" if row[5] == -1 else row[5]
            print(f"{i}: {row[:-1]} [{status}]")

# --- EXAMPLE WORKFLOW ---
async def main():
    db = DataMaster("MissionLog")

    # 1. Add rows using 1 for Forward and -1 for Reverse
    # [Num, Name, X, Y, Dir, F/R]
    db.append_row([1, "Start", 0, 0, 0, 1])
    db.append_row([2, "BackUp", 10, 0, 0, -1]) 
    db.append_row([3, "Goal", 100, 50, 90, 1])

    db.sort_by_num()
    db.display()

    # Example of using the F/R integer for motor logic:
    current_row = db.table[1]
    speed = 50 * current_row[5] # If F/R is -1, speed becomes -50
    print(f"\nMotor Logic Check: Direction {current_row[5]} results in Speed {speed}")

runloop.run(main())
