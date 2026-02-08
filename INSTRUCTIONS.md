# 🤖 DataMaster Master Controller Guide

The **DataMaster** class is an all-in-one system for LEGO SPIKE Prime 3.0. It allows you to manage robot paths using a 2D table, store coordinates permanently on the Hub, and execute autonomous driving missions.

---

## 📋 1. The 6-Column Data Protocol
The navigation and motor engines require every row to have exactly 6 columns in this order:

| Index | Header | Type | Description |
| :--- | :--- | :--- | :--- |
| **0** | **Num** | `int` | **Sequence ID:** Used for sorting mission steps. |
| **1** | **Name** | `str` | **Label:** A name for the waypoint (e.g., "Dock_A"). |
| **2** | **X** | `float` | **X-Coordinate:** Position on the horizontal axis (cm). |
| **3** | **Y** | `float` | **Y-Coordinate:** Position on the vertical axis (cm). |
| **4** | **Dir** | `int` | **Target Angle:** The compass heading (0-359°). |
| **5** | **F/R** | `int` | **Drive Mode:** `1` = Forward, `-1` = Reverse. |

---

## 🛠️ 2. Key Functions

### Data Management
* `append_row([data])`: Adds a new 6-column list to the end of the table.
* `modify_cell(row, col, value)`: Updates a specific piece of information.
* `delete_row(index)`: Removes a waypoint and shifts others up.
* `sort_by_num()`: Re-orders the table numerically based on Column 0.

### Navigation & Driving
* `get_navigation(start_idx, end_idx)`: Calculates the **Distance** (Pythagoras) and **Heading** (Atan2) between two points.
* `await drive_to_target(target_idx, base_speed, current_idx)`:
    * Automatically calculates the path.
    * Sets motor direction using the **F/R** column.
    * Commands the `MotorPair` to move the calculated distance.

### Storage & Transfer
* `save_to_hub()`: Saves the table to the Hub's flash memory as a `.csv`. Data persists after power-off.
* `load_from_hub()`: Restores your saved path into the robot's memory.
* `export_to_console()`: Prints the table for copy-pasting into **Excel/Google Sheets**.
* `import_from_console()`: (Async) Waits for you to paste CSV rows from your computer into the terminal. Type `END` to finish.

---

## 🚀 3. Quick Start Example

```python
# 1. Setup the Controller
db = DataMaster(motor_pair.PAIR_1, port.A, port.B, "MissionOne")

# 2. Define your Path
db.append_row([1, "Start", 0, 0, 0, 1])
db.append_row([2, "Target_A", 50, 0, 0, 1])  # 50cm Forward
db.append_row([3, "Return", 20, 0, 0, -1])  # Reverse to the 20cm mark

# 3. Run the Mission
await db.drive_to_target(target_idx=1, current_idx=0)
await db.drive_to_target(target_idx=2, current_idx=1)

# 4. Save to Hub
db.save_to_hub()
