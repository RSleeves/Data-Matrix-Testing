from hub import light_matrix
import runloop

class DataTable:
    def __init__(self):
        # Initialize an empty list to store our rows
        self.table = []
        self.cols = 5

    def append_row(self, data):
        """Adds a new row to the end. Data must be a list of 5 items."""
        if len(data) == self.cols:
            self.table.append(data)
        else:
            print("Error: Row must have exactly 5 columns.")

    def delete_row(self, index):
        """Removes a row at a specific index."""
        if 0 <= index < len(self.table):
            return self.table.pop(index)
        print("Error: Index out of range.")

    def insert_row(self, index, data):
        """Inserts a row at a specific index."""
        if len(data) == self.cols:
            self.table.insert(index, data)
        else:
            print("Error: Row must have exactly 5 columns.")

    def modify_cell(self, row, col, new_value):
        """Changes a single value at a specific row and column."""
        if 0 <= row < len(self.table) and 0 <= col < self.cols:
            self.table[row][col] = new_value
        else:
            print("Error: Invalid row or column index.")

    def display(self):
        """Prints the table formatted for the console."""
        print("\n--- Current Table Data ---")
        for i, row in enumerate(self.table):
            print(f"Row {i}: {row}")
        print("--------------------------\n")

async def main():
    # 1. Create the object
    my_data = DataTable()

    # 2. Append data (5 columns each)
    # Format: [Time, Sensor_A, Sensor_B, Motor_Pos, Status]
    my_data.append_row([0, 10, 20, 0, "OK"])
    my_data.append_row([1, 15, 25, 90, "OK"])
    my_data.append_row([2, 12, 22, 180, "WARN"])
    
    # 3. Modify a specific cell (Update Status of Row 2)
    my_data.modify_cell(2, 4, "OK")

    # 4. Insert a missed data point at Row 1
    my_data.insert_row(1, [0.5, 12, 22, 45, "OK"])

    # 5. Delete the last row (now index 3)
    my_data.delete_row(3)

    # Show results
    my_data.display()

runloop.run(main())
