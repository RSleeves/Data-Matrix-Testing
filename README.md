# Data-Matrix-Testing
LEGO Spike 3.0 python Test to practice Data 2-D data entry

Index,Name,Type,Description
0,Num,int,The ID or Sequence number (used for sorting).
1,Name,str,"A label for the point (e.g., ""Home"", ""Base"")."
2,X,float,"X-coordinate in your chosen units (cm, inches, etc.)."
3,Y,float,Y-coordinate in your chosen units.
4,Dir,int,The target heading/compass angle (0–359).
5,F/R,int,"1 for Forward, -1 for Reverse."

Method,Usage,Description
"append_row([a,b,c,d,e])",Add to end,Best for continuous logging.
"insert_row(0, [...])",Add at index,Useful if you need to put a header or priority data at the top.
"modify_cell(r, c, val)",Update value,"Best for updating a ""Status"" or ""Max Value"" column."
delete_row(index),Remove data,Keeps memory clean by removing old or irrelevant data.
clear_table(self), to clear the table
save_to_csv(self) , to save Hub's flash storage
load_from_csv, Reads data from Hub's Flash storage
display(self), Prints table to console
