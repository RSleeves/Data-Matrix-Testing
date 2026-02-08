# 📘 DataMaster System Instructions

Welcome to the **DataMaster** documentation. This system is designed to provide LEGO SPIKE Prime 3.0 users with a professional-grade 2D data management and navigation engine.

---

## 🏗 The 6-Column Data Structure
To ensure compatibility with the navigation and sorting engines, every data row must follow this strict 6-column format:

| Index | Column Name | Type | Description |
| :--- | :--- | :--- | :--- |
| **0** | **Num** | `int` | **ID/Order:** Used for chronological sorting. |
| **1** | **Name** | `str` | **Label:** A unique name for the waypoint (e.g., "Gate_A"). |
| **2** | **X** | `float` | **X-Coord:** Horizontal position in your units (cm/in). |
| **3** | **Y** | `float` | **Y-Coord:** Vertical position in your units (cm/in). |
| **4** | **Dir** | `int` | **Target Heading:** Target angle (0-359°). |
| **5** | **F/R** | `int` | **Motor Modifier:** `1` for Forward, `-1` for Reverse. |

---

## 🛠 Function Guide

### 1. Data Entry & Modification
Use these methods to manage the table in the Hub's memory (RAM).
* **`append_row([list])`**: Adds a new row. *Usage:* `db.append_row([1, "Start", 0, 0, 0, 1])`
* **`modify_cell(row, col, value)`**: Updates a specific value.
* **`delete_row(index)`**: Removes a row by its position in the list.
* **`sort_by_num()`**: Automatically re-orders the table so Point #1 comes before Point #2.

### 2. File & Console Operations (The "Bridge")
These functions move data between the **Robot**, the **Hub's Memory**, and your **Computer**.

* **`save_to_hub()`**: Writes the table to the Hub's flash storage. **Data stays saved even if the battery is removed.**
* **`load_from_hub()`**: Loads the previously saved `.csv` file back into the program.
* **`export_to_console()`**: Prints the table as raw CSV text. You can copy this text and paste it into **Excel** or **Google Sheets**.
* **`import_from_console()`**: (Async) Pauses the program and waits for you to paste data from a spreadsheet into the SPIKE App console. Type `END` to finish.

### 3. Navigation Logic
* **`get_navigation(start_idx, end_idx)`**:
    Calculates the straight-line distance and the required heading (angle) to travel between two rows.
    * **Distance:** Calculated via Pythagorean Theorem ($a^2 + b^2 = c^2$).
    * **Heading:** Calculated via `atan2` to provide a 0-360° compass bearing.

---

## 🚀 How to Add New Data via Computer
If you have a list of coordinates in Excel and want to put them on your robot:
1.  **Format** your Excel sheet to have these 6 columns.
2.  **Copy** the data rows.
3.  **Run** the robot script and call `await db.import_from_console()`.
4.  **Paste** the data into the SPIKE App terminal.
5.  Type `END` and press Enter.
6.  Call `db.save_to_hub()` to lock the data into the robot's memory.

---

## 💡 Code Snippet: Using F/R for Driving
The **F/R** column (Index 5) is designed to simplify your driving code. Use it as a multiplier for your speed:

```python
row = db.table[0]
base_speed = 50
# If F/R is -1, move_speed becomes -50 (Reverse)
move_speed = base_speed * row[5] 
motor_pair.move_for_distance(PAIR, dist, 'cm', velocity=move_speed)
