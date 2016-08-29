#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tkinter as tk
import sys
import DatabaseInteraction as DBinter
import tkinter.ttk as ttk
import datetime
import decimal

class InterfaceBill:
	def __init__(self, root):


		self.categories_management = DBinter.CategoriesManagement()
		self.bill_management = DBinter.BillsManagement()

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

		self.button_style = ttk.Style()
		self.button_style.configure("TButton", padding=2, relief="flat")
		self.frame_main = tk.Frame(self.root, width = self.width_root*0.9, height = self.height_root*0.85)
		self.button_add_bill = ttk.Button(self.root, text = "Ajouter", command = self.command_button_add)
		self.button_modify_bill = ttk.Button(self.root, text = "Modifier", command = self.command_button_mod)
		self.button_del_bill = ttk.Button(self.root, text = "Supprimer", command = self.command_button_del)

		self.treeview_main = ttk.Treeview(self.frame_main)
		self.width_column = int((self.width_root*0.9)/20)
		self.treeview_main["columns"] = ("bill_name", "category", "init_date", "due_date", "price", "paid", "notes")
		self.treeview_main["show"] = "headings"
		self.treeview_main.column("bill_name", width = self.width_column*2)
		self.treeview_main.column("category", width = self.width_column*2)
		self.treeview_main.column("init_date", width = self.width_column)
		self.treeview_main.column("due_date", width =self.width_column)
		self.treeview_main.column("price", width = self.width_column)
		self.treeview_main.column("paid", width = self.width_column)
		self.treeview_main.column("notes", width =self.width_column*3)

		self.treeview_main.heading("bill_name", text = "Nom", command = lambda : self.sort_tree("bill_name", "DESC"))
		self.treeview_main.heading("category", text  = "Categorie", command = lambda : self.sort_tree("category", "DESC"))
		self.treeview_main.heading("init_date", text = "Date d'émission", command = lambda : self.sort_tree("init_date", "DESC"))
		self.treeview_main.heading("due_date", text = "Date d'échéance", command = lambda : self.sort_tree("due_date", "DESC"))
		self.treeview_main.heading("price", text = "Montant", command = lambda : self.sort_tree("price", "DESC"))
		self.treeview_main.heading("paid", text = "Statut", command = lambda : self.sort_tree("paid", "DESC"))
		self.treeview_main.heading("notes", text = "Notes", command = lambda : self.sort_tree("notes", "DESC"))
		self.columns = {"bill_name" : "DESC", "category" : "DESC", "init_date" : "DESC",
						"due_date" : "DESC", "price" : "DESC", "paid" : "DESC", "notes" : "DESC"}


		self.menu_bar = tk.Menu(self.root)
		self.file_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.file_menu.add_command(label = "Catégories", command = self.command_menu_categories)
		self.file_menu.add_command(label = "À propos", command = self.command_menu_about)
		self.file_menu.add_separator()
		self.file_menu.add_command(label = "Quitter", command = sys.exit)
		self.menu_bar.add_cascade(label = "Fichier", menu = self.file_menu)

		self.filtering = tk.Menu(self.menu_bar, tearoff = 0)
		self.filtering.add_command(label = "Toutes", command = lambda : self.update_bills(0))
		self.filtering.add_command(label = "Prochaine semaine", command = lambda : self.update_bills(1))
		self.filtering.add_command(label = "Prochain mois", command = lambda : self.update_bills(2))
		self.filtering.add_command(label = "À payer", command = lambda : self.update_bills(3))
		self.filtering.add_command(label = "Payées", command = lambda : self.update_bills(4))
		self.menu_bar.add_cascade(label = "Filtres", menu = self.filtering)

		self.root.config(menu = self.menu_bar)


		self.bill_main_init()

	def bill_main_init(self):

		self.frame_main.place(anchor = "nw", relx = 0.05, rely = 0.05)
		self.frame_main.pack_propagate(0)
		self.treeview_main.pack(fill = "both", expand = 1)			
		self.button_add_bill.place(anchor = "se", relx = 0.95, rely = 0.95)
		self.button_modify_bill.place(anchor = "se", relx = 0.85, rely = 0.95)
		self.button_del_bill.place(anchor = "se", relx = 0.75, rely = 0.95)

		self.update_bills()

	def select_item_tree(self):
	
		for item in self.treeview_main.selection():
			self.item_text = self.treeview_main.item(item)
			self.values = self.item_text["values"]
			return self.values

	def sort_tree(self, data, sort):

		self.update_bills(sorting = (data, sort))
		
		if sort == "DESC":
			self.columns[data] = "ASC"
		else:
			self.columns[data] = "DESC"

		self.treeview_main.heading(data, command = lambda : self.sort_tree(data, self.columns[data]))

	def command_menu_about(self):

		self.top_about = tk.Toplevel(self.root)
		self.top_about.title("À propos")

		self.msg_about = tk.Message(self.top_about, text = "Application créee par\nCédric Guyaz")
		self.button_top_about = ttk.Button(self.top_about, text = "Fermer", command = self.top_about.destroy)
		self.msg_about.pack(side = "top")
		self.button_top_about.pack(side = "top")






	def command_button_del(self):
		
		self.bill_to_del = self.bill_management.get_bill_id(self.select_item_tree())
		self.bill_management.delete_bill(self.bill_to_del)
		self.update_bills()
	
	def command_button_mod(self):

		self.bill_to_mod = self.select_item_tree()
		self.command_button_add()
		self.id_bill_mod = self.bill_management.get_bill_id(self.bill_to_mod)

		for i in range(len(self.non_labels_top_add)):
			if type(self.non_labels_top_add[i]) is type(ttk.Entry()):
				self.non_labels_top_add[i].insert("end", self.bill_to_mod[i])
			elif type(self.non_labels_top_add[i]) is type(ttk.Combobox()):
				self.non_labels_top_add[i].set(self.bill_to_mod[i])
			elif type(self.non_labels_top_add[i]) is type(tk.Text()):
				self.non_labels_top_add[i].insert(1.0, self.bill_to_mod[i])
		
		self.button_top_add_confirm.config(command = lambda: self.command_confirm_add(mod = True))


	def command_button_add(self):
		
		self.top_add_bill = tk.Toplevel(self.root)
		self.top_add_bill.title("Ajouter une facture")

		self.paid = 0
		self.label_top_add_name = tk.Label(self.top_add_bill, text = "Nom :")
		self.entry_top_add_name = ttk.Entry(self.top_add_bill)
		self.label_top_add_category = tk.Label(self.top_add_bill, text = "Catégorie :")
		self.combobox_categories = ttk.Combobox(self.top_add_bill, height = 4, state = "readonly", values = self.categories_management.get_all_categories())
		self.label_top_add_init_date = tk.Label(self.top_add_bill, text = "Date d'émission :")
		self.entry_top_add_init_date = ttk.Entry(self.top_add_bill)
		self.label_top_add_due_date = tk.Label(self.top_add_bill, text = "Daté d'échéance :")
		self.entry_top_add_due_date = ttk.Entry(self.top_add_bill)
		self.label_top_add_price = tk.Label(self.top_add_bill, text = "Prix :")
		self.entry_top_add_price = ttk.Entry(self.top_add_bill)
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

		self.button_top_add_confirm = ttk.Button(self.top_add_bill, text = "Confirmer", command = self.command_confirm_add)
		self.button_top_add_cancel = ttk.Button(self.top_add_bill, text = "Annuler", command = self.top_add_bill.destroy)
		self.button_top_add_confirm.grid(row = 8, column = 4)
		self.button_top_add_cancel.grid(row = 8, column = 3)

	def command_confirm_add(self, mod = False):


		self.info_bill_to_add = []
		for element in self.non_labels_top_add:
			if element == self.checkbutton_paid:
				self.info_bill_to_add.append(self.paid)
			elif element == self.text_top_add_note:
				self.info_bill_to_add.append(self.text_top_add_note.get(1.0, "end"))
			else:	
				self.info_bill_to_add.append(element.get())
		if mod is True:
			self.bill_management.modify_bill(self.id_bill_mod, self.info_bill_to_add)
			self.button_top_add_confirm.config(command = lambda: self.command_confirm_add(mod = False))
		else:
			self.bill_management.add_bill(self.info_bill_to_add)

		self.update_bills()

		self.top_add_bill.destroy()

	def update_bills(self, filter_type = 0, sorting = ("due_date", "DESC")):

		self.treeview_main.delete(*self.treeview_main.get_children())
		self.all_bills = self.bill_management.get_all_bills(filter_applied = filter_type, sort = sorting)
		for element in self.all_bills:
			val = (element["bill_name"],
				element["category"],
				element["init_date"],
				element["due_date"],
				element["price"],
				element["paid"],
				element["notes"])
			self.treeview_main.insert("", 0, values = val)











	def command_menu_categories(self):

		self.top_menu_categories = tk.Toplevel(self.root, height = self.height_root*0.75, width = self.width_root*0.75)
		self.frame_top_listbox = tk.Frame(self.top_menu_categories, height = self.height_root*0.6, width = self.width_root*0.70)
		self.frame_top_listbox.propagate(0)
		self.frame_top_listbox.place(relx = 0.025, rely = 0.05, anchor = "nw")
		self.top_categories_listbox = tk.Listbox(self.frame_top_listbox, selectmode = "extended", bg = "#82916F", highlightthickness = 0, borderwidth = 1, font = ("Arial", 11), selectbackground = "#284145")
		self.top_categories_listbox.pack(expand = 1, fill = "both")

		self.frame_top_buttons_categories = tk.Frame(self.top_menu_categories, width = self.width_root*0.70)
		self.button_categories_add = ttk.Button(self.frame_top_buttons_categories, text = "Ajouter", command = self.command_add_category)
		self.button_categories_delete = ttk.Button(self.frame_top_buttons_categories, text = "Supprimer", command = self.command_delete_category)
		self.entry_top_categories = ttk.Entry(self.frame_top_buttons_categories)

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



if __name__ == "__main__":

	root = tk.Tk()
	app = InterfaceBill(root)
	root.mainloop()


	#def command_button_modify(self):
		#toplevel window
		#modier dans listbox
		#modifier dans databse

	#def resize:
		#resize
		#get new parametres
		#actualise
