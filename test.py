import tkinter as tk

root = tk.Tk()
entry1 = tk.Entry(root)

print(type(entry1))
if type(entry1) is type(tk.Entry()):
	print("allo")