# Data-Matrix-Testing
LEGO Spike 3.0 python Test to practice Data 2-D data entry

Index,Name,Data Type (Suggested)
0,Num,Integer (Used for Sorting)
1,Name,String (Identifier)
2,X,Float (Coordinate)
3,Y,Float (Coordinate)
4,Dir,Integer (0-360 Heading)
5,F/R,"String (""F"" for Forward, ""R"" for Reverse)"

Method,Usage,Description
"append_row([a,b,c,d,e])",Add to end,Best for continuous logging.
"insert_row(0, [...])",Add at index,Useful if you need to put a header or priority data at the top.
"modify_cell(r, c, val)",Update value,"Best for updating a ""Status"" or ""Max Value"" column."
delete_row(index),Remove data,Keeps memory clean by removing old or irrelevant data.
clear_table(self), to clear the table
save_to_csv(self) , to save Hub's flash storage
load_from_csv, Reads data from Hub's Flash storage
display(self), Prints table to console
