from hub import port
import motor_pair
import runloop
# Assuming your class is in a file named DataMaster.py
from DataMaster import DataMaster 

async def main():
    # --- 1. SETUP ---
    # Initialize the controller with Motor Pair ID, Left Port, Right Port, and Filename
    db = DataMaster(motor_pair.PAIR_1, port.A, port.B, "MyFirstMission")

    # --- 2. DATA ENTRY ---
    # Structure: [Num, Name, X, Y, Dir, F/R]
    # F/R: 1 = Forward, -1 = Reverse
    points = [
        [0, "Origin",   0,  0,  0,   1],
        [1, "Point_A", 40,  0,  0,   1], # Move 40cm Forward
        [2, "Point_B", 40, 30, 90,   1], # Move 30cm "Up"
        [3, "Return",   0,  0,  0,  -1]  # Move back toward origin in Reverse
    ]

    for p in points:
        db.append_row(p)

    # --- 3. EXECUTION ---
    print("Starting Mission...")
    
    # Drive from Row 0 to Row 1
    await db.drive_to_target(target_idx=1, current_idx=0, base_speed=50)
    
    # Drive from Row 1 to Row 2
    await db.drive_to_target(target_idx=2, current_idx=1, base_speed=40)
    
    # Drive from Row 2 to Row 3
    await db.drive_to_target(target_idx=3, current_idx=2, base_speed=30)

    # --- 4. FINISH ---
    db.save_to_hub()
    print("Mission Complete. Data saved.")
    db.display()

# Run the program
runloop.run(main())
