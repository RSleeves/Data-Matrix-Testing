from hub import light_matrix
import runloop
import os

class DataTable:
    def __init__(self, filename="robot_data.csv"):
        self.table = []
        self.cols = 5
        self.filename = filename if filename.endswith('.csv') else filename + ".csv"
        # Optional: Define your column headers
        self.headers = ["Time", "Sensor_A", "Sensor_B", "Motor_Pos", "Status"]

    # --- ROW MANIPULATION ---
    def append_row(self, data):
        """Adds a new row to the end."""
        if len(data) == self.cols:
            self.table.append(data)
        else:
            print(f"Error: Expected {self.cols} columns, got {len(data)}.")

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

    def clear_table(self):
        """Wipes the current table from memory."""
        self.table = []
        print("Table cleared.")

    # --- FILE I/O OPERATIONS ---
    def save_to_csv(self):
        """Saves current table to the Hub's flash storage."""
        try:
            with open(self.filename, 'w') as f:
                # Write the headers first
                f.write(",".join(self.headers) + "\n")
                # Write the data
                for row in self.table:
                    line = ",".join(map(str, row))
                    f.write(line + "\n")
            print(f"Saved: {self.filename}")
        except Exception as e:
            print(f"Save failed: {e}")

    def load_from_csv(self):
        """Reads data from the Hub's storage back into the table."""
        if self.filename in os.listdir():
            try:
                self.table = []
                with open(self.filename, 'r') as f:
                    lines = f.readlines()
                    # Skip the first line (headers)
                    for line in lines[1:]:
                        # Strip whitespace and split by comma
                        clean_row = line.strip().split(',')
                        # Convert back to numbers if possible, else keep as string
                        processed_row = []
                        for item in clean_row:
                            try:
                                # Try to convert to float/int
                                num = float(item)
                                processed_row.append(int(num) if num.is_integer() else num)
                            except ValueError:
                                processed_row.append(item)
                        self.table.append(processed_row)
                print(f"Loaded {len(self.table)} rows from {self.filename}")
            except Exception as e:
                print(f"Load failed: {e}")
        else:
            print("No existing file found.")

    def display(self):
        """Prints table to console."""
        print(f"\n--- {self.filename} ---")
        print(" | ".join(self.headers))
        for i, row in enumerate(self.table):
            print(f"{i}: {row}")
        print("----------------------------\n")

async def main():
    # Initialize
    db = DataTable("MissionLog")

    # 1. Add some initial data
    db.append_row([0.0, 10, 20, 0, "START"])
    db.append_row([1.5, 45, 22, 90, "ACTIVE"])
    db.append_row([3.0, 12, 19, 180, "STOP"])

    # 2. Modify and Insert
    db.modify_cell(1, 4, "BOOST") # Change "ACTIVE" to "BOOST"
    db.insert_row(1, [0.7, 20, 21, 45, "MID"])

    # 3. Save to Hub
    db.save_to_csv()

    # 4. Prove it works: Clear memory and then Load it back
    db.clear_table()
    db.display() # Should be empty
    
    db.load_from_csv()
    db.display() # Should be restored

runloop.run(main())
