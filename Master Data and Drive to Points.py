from hub import light_matrix, port
import runloop
import sys
import os
import math
import motor_pair

class DataMaster:
    def __init__(self, pair_id, motor_1, motor_2, filename="mission_data"):
        # Initialize Table
        self.table = []
        self.cols = 6
        self.filename = filename if filename.endswith('.csv') else filename + ".csv"
        self.headers = ["Num", "Name", "X", "Y", "Dir", "F/R"]
        
        # Initialize Motors
        self.pair = pair_id
        motor_pair.pair(self.pair, motor_1, motor_2)

    # --- MOVEMENT ENGINE ---
    async def drive_to_target(self, target_idx, base_speed=40, current_idx=0):
        """Calculates nav math and physically moves the robot."""
        nav = self.get_navigation(current_idx, target_idx)
        
        if nav:
            target_row = self.table[target_idx]
            print(f"Moving to {target_row[1]}...")

            # 1. Directional Multiplier (1 for Fwd, -1 for Rev)
            modifier = target_row[5]
            move_speed = base_speed * modifier
            
            # 2. Distance Calculation
            # Note: 1 unit in table = 1 cm. Adjust math here if using different scales.
            distance = int(nav['dist'])
            
            # 3. Execution
            # In a full setup, you would add a turn_to(nav['head']) here.
            await motor_pair.move_for_distance(self.pair, distance, 'cm', velocity=move_speed)
            print(f"Reached {target_row[1]}.")

    # --- NAVIGATION MATH ---
    def get_navigation(self, start_idx, end_idx):
        try:
            r1, r2 = self.table[start_idx], self.table[end_idx]
            dx, dy = r2[2] - r1[2], r2[3] - r1[3]
            distance = math.sqrt(dx**2 + dy**2)
            angle = math.degrees(math.atan2(dy, dx))
            heading = angle if angle >= 0 else angle + 360
            return {"dist": distance, "head": heading}
        except IndexError:
            print("Navigation Error: Index out of range.")
            return None

    # --- DATA MANIPULATION ---
    def append_row(self, data):
        if len(data) == self.cols: self.table.append(data)

    def sort_by_num(self):
        self.table.sort(key=lambda x: x[0])

    # --- FILE & CONSOLE I/O ---
    def save_to_hub(self):
        with open(self.filename, 'w') as f:
            f.write(",".join(self.headers) + "\n")
            for row in self.table:
                f.write(",".join(map(str, row)) + "\n")

    def load_from_hub(self):
        if self.filename in os.listdir():
            with open(self.filename, 'r') as f:
                lines = f.readlines()[1:]
                self.table = [[self._parse(x) for x in l.strip().split(',')] for l in lines]

    def export_to_console(self):
        print("\n" + ",".join(self.headers))
        for row in self.table: print(",".join(map(str, row)))

    async def import_from_console(self):
        print("Paste CSV (Type 'END' to finish):")
        while True:
            line = sys.stdin.readline().strip()
            if line.upper() == "END": break
            parts = line.split(",")
            if len(parts) == self.cols and "Num" not in line:
                self.table.append([self._parse(x) for x in parts])

    def _parse(self, val):
        try:
            num = float(val)
            return int(num) if num.is_integer() else num
        except: return val

# --- MAIN MISSION SCRIPT ---
async def main():
    # Setup: Use MotorPair 1 on Ports A and B
    db = DataMaster(motor_pair.PAIR_1, port.A, port.B)

    # 1. Load existing data or add new points
    db.append_row([1, "Origin", 0, 0, 0, 1])
    db.append_row([2, "Target_A", 50, 0, 0, 1])  # 50cm Forward
    db.append_row([3, "Target_B", 20, 0, 0, -1]) # 30cm Reverse (from A back to 20)

    # 2. Execute Mission
    # Drive from Row 0 (Origin) to Row 1 (Target_A)
    await db.drive_to_target(target_idx=1, current_idx=0)
    
    # Drive from Row 1 (Target_A) to Row 2 (Target_B)
    await db.drive_to_target(target_idx=2, current_idx=1)

    # 3. Save Final State
    db.save_to_hub()

runloop.run(main())
