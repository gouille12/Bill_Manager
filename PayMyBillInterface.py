#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tkinter as tk
import sys
import DatabaseInteraction as DBinter
import tkinter.ttk as ttk

class InterfaceBill:

	def __init__(self, root):

		self.categories_management = DBinter.CategoriesManagement()
		
		self.root = root
		self.width_root, self.height_root = 1000, 650
		self.root.geometry("{}x{}+183+20".format(self.width_root, self.height_root))
		self.root.maxsize(self.width_root, self.height_root)
		self.root.title("PayMyBill")
		self.root.config(bg = "#121212")
		self.color_grey = "#CDCDCD"

		self.canvas_background = tk.Canvas(self.root, width = self.width_root, height = self.height_root)
		self.image_background = tk.PhotoImage(file = "test.png")
		self.canvas_background.pack(expand = 1, fill = "both")
		self.canvas_background.create_image(0, 0, image = self.image_background, anchor = "nw")

		self.frame_main = tk.Frame(self.root, width = self.width_root*0.9, height = self.height_root*0.85)
		self.listbox_main = tk.Listbox(self.frame_main, selectmode = "extended", bg = "#82916F", highlightthickness = 0, borderwidth = 1, font = ("Arial", 11), selectbackground = "#284145")
		self.button_add_bill = tk.Button(self.root, text = "Ajouter", bg = "#284145", relief = "flat", padx = 6, pady = 2, font = ("Arial", 9, "bold"), command = self.command_button_add)
		self.button_modify_bill = tk.Button(self.root, text = "Modifier", bg = "#284145", relief = "flat", padx = 6, pady = 2, font = ("Arial", 9, "bold"))
		
		self.menu_bar = tk.Menu(self.root)
		self.file_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.file_menu.add_command(label = "Statistiques")
		self.file_menu.add_command(label = "Catégories", command = self.command_menu_categories)
		self.file_menu.add_command(label = "À propos", command = self.command_menu_about)
		self.file_menu.add_separator()
		self.file_menu.add_command(label = "Quitter", command = sys.exit)
		self.menu_bar.add_cascade(label = "Fichier", menu = self.file_menu)
		self.root.config(menu = self.menu_bar)


		self.bill_main_init()



	def bill_main_init(self):

		self.frame_main.place(anchor = "nw", relx = 0.05, rely = 0.05)
		self.frame_main.pack_propagate(0)
		self.listbox_main.insert("end", "allokjbdksjbck")
		self.listbox_main.insert("end", "bitchezzzz")
		self.listbox_main.pack(fill = "both", expand = 1)			
		self.button_add_bill.place(anchor = "se", relx = 0.95, rely = 0.95)
		self.button_modify_bill.place(anchor = "se", relx = 0.85, rely = 0.95)

	def command_menu_about(self):

		self.top_about = tk.Toplevel(self.root)
		self.top_about.title("À propos")

		self.msg_about = tk.Message(self.top_about, text = "Application créee par\nCédric Guyaz")
		self.button_top_about = tk.Button(self.top_about, text = "Fermer", font = ("Arial", 9, "bold"), command = self.top_about.destroy)
		self.msg_about.pack(side = "top")
		self.button_top_about.pack(side = "top")


	def command_button_add(self):
		
		self.top_add_bill = tk.Toplevel(self.root)
		self.top_add_bill.title("Ajouter une facture")

		self.paid = 0
		self.label_top_add_name = tk.Label(self.top_add_bill, text = "Nom :")
		self.entry_top_add_name = tk.Entry(self.top_add_bill)
		self.label_top_add_category = tk.Label(self.top_add_bill, text = "Catégorie :")
		self.combobox_categories = ttk.Combobox(self.top_add_bill, height = 4, state = "readonly", values = self.categories_management.get_all_categories())
		self.label_top_add_init_date = tk.Label(self.top_add_bill, text = "Date d'émission :")
		self.entry_top_add_init_date = tk.Entry(self.top_add_bill)
		self.label_top_add_due_date = tk.Label(self.top_add_bill, text = "Daté d'échéance :")
		self.entry_top_add_due_date = tk.Entry(self.top_add_bill)
		self.label_top_add_price = tk.Label(self.top_add_bill, text = "Prix :")
		self.entry_top_add_price = tk.Entry(self.top_add_bill)
		self.label_top_add_paid = tk.Label(self.top_add_bill, text = "Payée? :")
		self.checkbutton_paid = tk.Checkbutton(self.top_add_bill, variable = self.paid)
		self.label_top_add_note = tk.Label(self.top_add_bill, text = "Notes :")
		self.text_top_add_note = tk.Text(self.top_add_bill)

		self.labels_top_add = [self.label_top_add_name, self.label_top_add_category,
			self.label_top_add_init_date, self.label_top_add_due_date,
			self.label_top_add_price, self.label_top_add_paid, self.label_top_add_note]

		self.non_labels_top_add = [self.entry_top_add_name, self.combobox_categories, 
			self.entry_top_add_init_date, self.entry_top_add_due_date,
			self.entry_top_add_price, self.checkbutton_paid, self.text_top_add_note]

		for i in range(len(self.labels_top_add)):
			self.labels_top_add[i].grid(row = i, column = 0)
			self.non_labels_top_add[i].grid(row = i, column = 1)


		self.button_top_add_confirm = tk.Button(self.top_add_bill, text = "Confirmer")
		self.button_top_add_cancel = tk.Button(self.top_add_bill, text = "Annuler", command = self.top_add_bill.destroy)
		self.button_top_add_confirm.grid(row = 8, column = 4)
		self.button_top_add_cancel.grid(row = 8, column = 3)


		#add dans listbox
		#upload dans la database


	def command_menu_categories(self):

		#insert categories deja crees
		self.top_menu_categories = tk.Toplevel(self.root, height = self.height_root*0.75, width = self.width_root*0.75)
		self.frame_top_listbox = tk.Frame(self.top_menu_categories, height = self.height_root*0.6, width = self.width_root*0.70)
		self.frame_top_listbox.propagate(0)
		self.frame_top_listbox.place(relx = 0.025, rely = 0.05, anchor = "nw")
		self.top_categories_listbox = tk.Listbox(self.frame_top_listbox, selectmode = "extended", bg = "#82916F", highlightthickness = 0, borderwidth = 1, font = ("Arial", 11), selectbackground = "#284145")
		self.top_categories_listbox.pack(expand = 1, fill = "both")

		self.frame_top_buttons_categories = tk.Frame(self.top_menu_categories, width = self.width_root*0.70)
		self.button_categories_add = tk.Button(self.frame_top_buttons_categories, text = "Ajouter", padx = 6, pady = 2, command = self.command_add_category)
		self.button_categories_delete = tk.Button(self.frame_top_buttons_categories, text = "Supprimer", padx = 6, pady = 2, command = self.command_delete_category)
		self.entry_top_categories = tk.Entry(self.frame_top_buttons_categories)

		self.frame_top_buttons_categories.place(anchor = "se", relx = 0.75/2, rely = 0.95)
		self.button_categories_add.pack(side = "right")
		self.button_categories_delete.pack(side = "right")
		self.entry_top_categories.pack(side = "right", expand = 1, fill = "both")

		self.update_categories_listbox()

	def command_add_category(self):

		self.category_added = self.entry_top_categories.get()
		self.entry_top_categories.delete(0, "end")

		self.categories_management.add_category(self.category_added)
		self.update_categories_listbox()

	def update_categories_listbox(self):

		self.top_categories_listbox.delete(0, "end")

		self.all_categories = self.categories_management.get_all_categories()
		for element in self.all_categories:
			self.top_categories_listbox.insert("end", element)

	def command_delete_category(self):

		self.category_to_del = self.top_categories_listbox.get("active")

		self.categories_management.delete_category(self.category_to_del)

		self.update_categories_listbox()










	#def command_button_modify(self):
		#toplevel window
		#modier dans listbox
		#modifier dans databse

	#def resize:
		#resize
		#get new parametres
		#actualise



if __name__ == "__main__":

	root = tk.Tk()
	app = InterfaceBill(root)
	root.mainloop()
