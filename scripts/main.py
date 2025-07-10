import pip
pip.main(['install', 'ttkthemes'])
import os
import csv
import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
items_dir = os.path.join(base_dir, "ITEMS")
def csv_to_nested_list(file_path):
    if not os.path.exists(file_path):
        return [["PARTY NAME", "DATE", "QUANTITY", "PRICE", "VALUE"]]
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        return list(csv.reader(csv_file))
def display_table(nested_list):
    table_window = tk.Toplevel(root)
    table_window.title("CURRENT RECORDS")

    tree = ttk.Treeview(table_window, show="headings")
    tree["columns"] = tuple(nested_list[0])

    for idx, col in enumerate(nested_list[0]):
        tree.heading(col, text=col)
        width = 200 if idx in [0, 1] else 100 if idx == 2 else 50
        tree.column(col, anchor="center", width=width)

    for row in nested_list[1:]:
        tree.insert("", tk.END, values=tuple(row))

    tree.pack(expand=True, fill=tk.BOTH)

# ----------------------------------------
# Format records and push to display
# ----------------------------------------
def using_data(data):
    nested_list = [["ITEM NAME", "PARTY NAME", "DATE", "QUANTITY", "PRICE", "VALUE"]]
    for i in data:
        row_data = i[2]
        segments = (len(row_data) - 1) // 4
        for j in range(segments):
            entry = [
                i[1].replace(".csv", "") if j == 0 else "",
                row_data[0] if j == 0 else "",
                row_data[1 + j * 4],
                row_data[2 + j * 4],
                row_data[3 + j * 4],
                row_data[4 + j * 4]
            ]
            nested_list.append(entry)
            nested_list.append(["", "", "", "", "", ""])
        nested_list.append(["-" * 40] * 6)
    display_table(nested_list)

# ----------------------------------------
# Search matching records
# ----------------------------------------
def search_records():
    party_name = party_name_entry.get().strip().lower()
    item_name = item_name_entry.get().strip().lower()

    if party_name == "exit":
        root.destroy()
        return
    if item_name == "exit":
        return

    matching_items = []
    for file_name in os.listdir(items_dir):
        if file_name.endswith(".csv") and all(part in file_name.lower() for part in item_name.split()):
            full_path = os.path.join(items_dir, file_name)
            nested_list = csv_to_nested_list(full_path)
            matching_items.extend([(item_name, file_name, row) for row in nested_list[1:]])

    matching_records = [rec for rec in matching_items if party_name in rec[2][0].lower()]

    if matching_records:
        using_data(matching_records)
    else:
        messagebox.showinfo("No Records", "No matching records found for the given criteria.")

# ----------------------------------------
# GUI Setup
# ----------------------------------------
root = ThemedTk(theme="black")
root.title("Search Records")
root.attributes("-fullscreen", True)

# Labels and inputs
tk.Label(root, text="Please Enter party name:").pack(pady=10)
party_name_entry = tk.Entry(root)
party_name_entry.pack(pady=10)

tk.Label(root, text="Please Enter item name:").pack(pady=10)
item_name_entry = tk.Entry(root)
item_name_entry.pack(pady=10)

# Buttons
tk.Button(root, text="Search Records", command=search_records).pack(pady=20)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=20)

root.eval('tk::PlaceWindow . center')
root.mainloop()
