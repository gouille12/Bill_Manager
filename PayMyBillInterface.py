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


		self.treeview_main.bind("<Double-Button-1>", self.double_click_tree)
		self.root.bind("<Control-a>", self.command_button_add)
		self.root.bind("<Control-s>", self.control_S)

		self.bill_main_init()

	def bill_main_init(self):

		self.frame_main.place(anchor = "nw", relx = 0.05, rely = 0.05)
		self.frame_main.pack_propagate(0)
		self.treeview_main.pack(fill = "both", expand = 1)			
		self.button_add_bill.place(anchor = "se", relx = 0.95, rely = 0.95)
		self.button_modify_bill.place(anchor = "se", relx = 0.85, rely = 0.95)
		self.button_del_bill.place(anchor = "se", relx = 0.75, rely = 0.95)

		self.update_bills()

	def select_item_tree(self, tree):
	
		for item in tree.selection():
			self.item_text = tree.item(item)
			self.values = self.item_text["values"]

			if len(self.values) > 1:
				if self.values[5] == "Ok":
					self.values[5] = 1
				else:
					self.values[5] = 0
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
		self.top_about.bind("<Escape>", lambda _: self.button_top_about.invoke())






	def command_button_del(self):
		
		self.bill_to_del = self.bill_management.get_bill_id(self.select_item_tree(self.treeview_main))
		self.bill_management.delete_bill(self.bill_to_del)
		self.update_bills()
	
	def command_button_mod(self):

		self.bill_to_mod = self.select_item_tree(self.treeview_main)
		self.command_button_add()
		self.id_bill_mod = self.bill_management.get_bill_id(self.bill_to_mod)

		self.entry_top_add_name.insert("end", self.bill_to_mod[0])
		self.combobox_categories.set(self.bill_to_mod[1])
		self.entry_top_add_init_date.insert("end", datetime.datetime.strftime(self.bill_to_mod[2], "%d-%m-%Y"))
		self.entry_top_add_due_date.insert("end", datetime.datetime.strftime(self.bill_to_mod[3], "%d-%m-%Y"))
		self.entry_top_add_price.insert("end", self.bill_to_mod[4])
		if self.bill_to_mod[5] == 1: self.checkbutton_paid.select()
		self.text_top_add_note.insert(1.0, self.bill_to_mod[6])
		
		self.button_top_add_confirm.config(command = lambda: self.command_confirm_add(mod = True))


	def command_button_add(self, *event):
		

		self.top_add_bill = tk.Toplevel(self.root)
		self.top_add_bill.title("Ajouter une facture")


		self.paid = tk.IntVar()
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
		self.checkbutton_paid = tk.Checkbutton(self.top_add_bill, variable = self.paid, command = self.get_checkbutton)
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
		self.top_add_bill.bind("<Escape>", lambda _: self.button_top_add_cancel.invoke())
		self.top_add_bill.bind("<Return>", lambda _: self.button_top_add_confirm.invoke())

	def command_confirm_add(self, mod = False, *event):


		self.info_bill_to_add = []
		for element in self.non_labels_top_add:
			if element == self.checkbutton_paid:
				self.info_bill_to_add.append(self.paid.get())
			elif element == self.text_top_add_note:
				self.info_bill_to_add.append(self.text_top_add_note.get(1.0, "end"))
			else:	
				self.info_bill_to_add.append(element.get())
		try:
			if mod is True:
				self.bill_management.modify_bill(self.id_bill_mod, self.info_bill_to_add)
				self.button_top_add_confirm.config(command = lambda: self.command_confirm_add(mod = False))
			else:
				self.bill_management.add_bill(self.info_bill_to_add)

			self.update_bills()
			self.top_add_bill.destroy()
		except ValueError:
			self.top_error = tk.Toplevel(self.top_add_bill)
			self.top_error.title("Erreur de saisie")
			self.msg_error = tk.Message(self.top_error, text = "Données entrées invalides")
			self.button_top_error = ttk.Button(self.top_error, text = "Fermer", command = self.top_error.destroy)
			self.msg_error.pack(side = "top")
			self.button_top_error.pack(side = "top")
			
	def update_bills(self, filter_type = 0, sorting = ("due_date", "DESC")):

		self.treeview_main.delete(*self.treeview_main.get_children())
		self.all_bills = self.bill_management.get_all_bills(filter_applied = filter_type, sort = sorting)
		for element in self.all_bills:
			if element["paid"] == 1:
				self.paid_tree = "Ok"
			elif element["paid"] == 0:
				self.paid_tree = " "

			self.init_date_tree = datetime.datetime.strftime(element["init_date"], "%d-%m-%Y")
			self.due_date_tree = datetime.datetime.strftime(element["due_date"], "%d-%m-%Y")

			val = (element["bill_name"],
				element["category"],
				self.init_date_tree,
				self.due_date_tree,
				element["price"],
				self.paid_tree,
				element["notes"])
			self.treeview_main.insert("", 0, values = val)

	def get_checkbutton(self):

		return self.paid.get()


	def double_click_tree(self, event):

		try:
			self.command_button_mod()
		except TypeError:
			self.top_add_bill.destroy()

	def control_S(self, event):

		try:
			self.command_button_del()
		except TypeError:
			pass




	def command_menu_categories(self):

		self.top_menu_categories = tk.Toplevel(self.root, height = self.height_root*0.75, width = self.width_root*0.75)
		self.frame_top_treeview = tk.Frame(self.top_menu_categories, height = self.height_root*0.6, width = self.width_root*0.70)
		self.frame_top_treeview.propagate(0)
		self.frame_top_treeview.place(relx = 0.025, rely = 0.05, anchor = "nw")
		
		self.treeview_top_categories = ttk.Treeview(self.frame_top_treeview)
		self.treeview_top_categories["columns"] = ("categories")
		self.treeview_top_categories["show"] = "headings"
		self.treeview_top_categories.column("categories")
		self.treeview_top_categories.heading("categories", text = "Catégories")
		self.treeview_top_categories.pack(fill = "both", expand = 1)

		self.frame_top_buttons_categories = tk.Frame(self.top_menu_categories, width = self.width_root*0.70)
		self.button_categories_add = ttk.Button(self.frame_top_buttons_categories, text = "Ajouter", command = self.command_add_category)
		self.button_categories_delete = ttk.Button(self.frame_top_buttons_categories, text = "Supprimer", command = self.command_delete_category)
		self.entry_top_categories = ttk.Entry(self.frame_top_buttons_categories)

		self.frame_top_buttons_categories.place(anchor = "se", relx = 0.75/2, rely = 0.95)
		self.button_categories_add.pack(side = "right")
		self.button_categories_delete.pack(side = "right")
		self.entry_top_categories.pack(side = "right", expand = 1, fill = "both")

		self.top_menu_categories.bind("<Escape>", lambda _: self.top_menu_categories.destroy())
		self.top_menu_categories.bind("<Return>", lambda _: self.button_categories_add.invoke())
		self.update_categories_tree()

	def command_add_category(self):

		self.category_added = self.entry_top_categories.get()
		self.entry_top_categories.delete(0, "end")

		self.categories_management.add_category(self.category_added)
		self.update_categories_tree()

	def update_categories_tree(self):

		self.treeview_top_categories.delete(*self.treeview_top_categories.get_children())

		self.all_categories = self.categories_management.get_all_categories()
		for element in self.all_categories:
			self.treeview_top_categories.insert("", "end", values = element)

	def command_delete_category(self):

		self.category_to_del = self.select_item_tree(self.treeview_top_categories)
		self.categories_management.delete_category(self.category_to_del)
		self.update_categories_tree()



if __name__ == "__main__":

	root = tk.Tk()
	app = InterfaceBill(root)
	root.mainloop()


	#def resize:
		#resize
		#get new parametres
		#actualise
