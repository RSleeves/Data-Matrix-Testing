# Data-Matrix-Testing
LEGO Spike 3.0 python Test to practice Data 2-D data entry

Method,Usage,Description
"append_row([a,b,c,d,e])",Add to end,Best for continuous logging.
"insert_row(0, [...])",Add at index,Useful if you need to put a header or priority data at the top.
"modify_cell(r, c, val)",Update value,"Best for updating a ""Status"" or ""Max Value"" column."
delete_row(index),Remove data,Keeps memory clean by removing old or irrelevant data.
