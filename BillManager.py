#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Cédric Guyaz"
__date__ = "01 septembre 2016"

"""
**********PROJET PENDU**********
BillManager.py : Fichier principal, responsable de toute l'interface graphique
						(InterfaceManager)
DatabaseInteraction.py : Responsable de la gestion des éléments et des catégories dans la
						base de données (BillsManagement, CategoriesManagement)
Background.png : Fond d'écran
Utilisé avec une base de données MySQL
"""

import tkinter as tk
import sys
import DatabaseInteraction as DBinter
import tkinter.ttk as ttk
import datetime
import decimal

class InterfaceManager:
	"""Main : relative to the Graphic User interface of the app"""

	def __init__(self, root):

		self.categories_management = DBinter.CategoriesManagement()
		self.bill_management = DBinter.BillsManagement()

		self.root = root
		self.width_root, self.height_root = 1000, 650
		self.root.resizable(width = False, height = False)
		self.width_screen = self.root.winfo_screenwidth()
		self.height_screen = self.root.winfo_screenheight()
		self.x = (self.width_screen/2) - (self.width_root/1.92)
		self.y = (self.height_screen/2) - (self.height_root/1.8)
		self.root.geometry("%dx%d+%d+%d" % (self.width_root, self.height_root, self.x, self.y))
		self.root.title("Organisateur personnel")
		self.root.config(bg = "#121212")
		self.canvas_background_main = tk.Canvas(self.root, width = self.width_root, height = self.height_root)
		self.image_background = tk.PhotoImage(file = "C:\\Users\\Cédric\\Documents\\Projets python - Documents autres\\Gestion de factures\\Background.png")
		self.canvas_background_main.pack(expand = 1, fill = "both")
		self.canvas_background_main.create_image(0, 0, image = self.image_background, anchor = "nw")

		self.button_style = ttk.Style()
		self.button_style.configure("TButton", padding=2, relief="flat")
		self.frame_main = tk.Frame(self.root, width = self.width_root*0.9, height = self.height_root*0.85)
		self.button_add_bill = ttk.Button(self.root, text = "Ajouter (Ctrl-A)", command = self.command_button_add)
		self.button_modify_bill = ttk.Button(self.root, text = "Modifier", command = self.command_button_mod)
		self.button_del_bill = ttk.Button(self.root, text = "Supprimer (Ctrl-S)", command = self.command_button_del)

		self.treeview_main = ttk.Treeview(self.frame_main, selectmode = "browse")
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
		self.treeview_main.heading("category", text  = "Categorie",
									command = lambda : self.sort_tree("category", "DESC"))
		self.treeview_main.heading("init_date", text = "Date d'émission",
									command = lambda : self.sort_tree("init_date", "DESC"))
		self.treeview_main.heading("due_date", text = "Date d'échéance",
									command = lambda : self.sort_tree("due_date", "DESC"))
		self.treeview_main.heading("price", text = "Montant", command = lambda : self.sort_tree("price", "DESC"))
		self.treeview_main.heading("paid", text = "Statut", command = lambda : self.sort_tree("paid", "DESC"))
		self.treeview_main.heading("notes", text = "Notes", command = lambda : self.sort_tree("notes", "DESC"))
		self.columns = {"bill_name" : "DESC", "category" : "DESC", "init_date" : "DESC",
						"due_date" : "DESC", "price" : "DESC", "paid" : "DESC", "notes" : "DESC"}

		self.menu_bar = tk.Menu(self.root)
		self.file_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.file_menu.add_command(label = "Catégories", command = self.command_menu_categories)
		self.file_menu.add_command(label = "À propos", command = lambda : self.toplevel_message(self.root,
									 "Application créee par\nCédric Guyaz", "À propos"))
		self.file_menu.add_separator()
		self.file_menu.add_command(label = "Quitter", command = sys.exit)
		self.menu_bar.add_cascade(label = "Fichier", menu = self.file_menu)
		self.filtering = tk.Menu(self.menu_bar, tearoff = 0)
		self.filtering.add_command(label = "Toutes", command = lambda : self.update_bills(0))
		self.filtering.add_command(label = "Prochaine semaine", command = lambda : self.update_bills(1))
		self.filtering.add_command(label = "Prochain mois", command = lambda : self.update_bills(2))
		self.filtering.add_command(label = "À compléter", command = lambda : self.update_bills(3))
		self.filtering.add_command(label = "Complétées", command = lambda : self.update_bills(4))
		self.menu_bar.add_cascade(label = "Filtres", menu = self.filtering)
		self.options = tk.Menu(self.root, tearoff = 0)
		self.options.add_command(label = "Archiver la sélection", command = self.command_archive)
		self.menu_bar.add_cascade(label = "Options", menu = self.options)
		self.root.config(menu = self.menu_bar)

		self.treeview_main.bind("<Double-Button-1>", self.double_click_tree)
		self.root.bind("<Control-a>", self.command_button_add)
		self.root.bind("<Control-s>", self.control_S)

		self.top_msg = None
		self.top_add_bill = None
		self.top_menu_categories = None

		self.bill_main_init()


	def bill_main_init(self):
		"""Place all widgets needed to build the main window"""

		self.frame_main.place(anchor = "nw", relx = 0.05, rely = 0.05)
		self.frame_main.pack_propagate(0)
		self.treeview_main.pack(fill = "both", expand = 1)			
		self.button_add_bill.place(anchor = "se", relx = 0.95, rely = 0.95)
		self.button_modify_bill.place(anchor = "se", relx = 0.84, rely = 0.95)
		self.button_del_bill.place(anchor = "se", relx = 0.75, rely = 0.95)

		self.update_bills()


	def select_item_tree(self, tree):
		"""Get item selected in a ttk.Treeview"""

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
		"""Sort column of a the main Treeview"""

		self.update_bills(sorting = (data, sort))
		if sort == "DESC":
			self.columns[data] = "ASC"
		else:
			self.columns[data] = "DESC"

		self.treeview_main.heading(data, command = lambda : self.sort_tree(data, self.columns[data]))


	def update_bills(self, filter_type = 0, sorting = ("due_date", "DESC")):
		"""Sync the bills in the Treeview with the bills in the database"""

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


	def toplevel_message(self, root, msg, title):
		"""Build a Toplevel to tell a message to the user (error, about)"""

		self.remove_toplevel(self.top_msg)
		self.top_msg = tk.Toplevel(root)
		self.top_msg.focus()
		self.top_msg.resizable(width = False, height = False)
		self.x_msg = self.width_screen*0.35
		self.y_msg = self.height_screen*0.3
		self.top_msg.geometry("%dx%d+%d+%d" % (self.width_root*0.3, self.height_root*0.3, self.x_msg, self.y_msg))
		self.top_msg.title(title)
		self.canvas_background_msg = tk.Canvas(self.top_msg)
		self.canvas_background_msg.pack(expand = 1, fill = "both")
		self.canvas_background_msg.create_image(0, 0, image = self.image_background, anchor = "nw")
		self.canvas_background_msg.create_text(self.width_root*0.15, self.height_root*0.1, text = msg, 
												anchor = "center", fill = "white", justify = "center")
		self.button_top_msg = ttk.Button(self.top_msg, text = "Fermer", command = self.top_msg.destroy)
		self.button_top_msg.place(relx = 0.5, rely = 0.7, anchor = "center")
		self.top_msg.bind("<Return>", lambda _: self.button_top_msg.invoke())


	def remove_toplevel(self, toplevel):
		"""Destroy a Toplevel if we're trying to open it again (by not closing it when going into focus
		on the main window)"""

		if toplevel is not None:
			toplevel.destroy()
			toplevel = None


	def command_button_add(self, *event):
		"""Command of the add button, to add a bill (GUI/DB). Open a Toplevel to enter information in fields"""
		
		self.remove_toplevel(self.top_add_bill)
		self.top_add_bill = tk.Toplevel(self.root)
		self.top_add_bill.focus()
		self.x_add = self.width_screen*0.35
		self.y_add = self.height_screen*0.2
		self.top_add_bill.geometry("%dx%d+%d+%d" % (self.width_root*0.5, self.height_root*0.5, self.x_add, self.y_add))
		self.top_add_bill.title("Gestion des éléments")
		self.canvas_background_add = tk.Canvas(self.top_add_bill, width = self.width_root*0.5,
												height = self.height_root*0.5)
		self.canvas_background_add.create_image(0, 0, image = self.image_background)
		self.canvas_background_add.place(relx = 0.5, rely = 0.5, anchor = "center")
		self.color = "#EFEFEF"

		self.frame_widgets_add = tk.Frame(self.top_add_bill, width = self.width_root*0.3,
											height = self.height_root*0.4, pady = 2, bg = self.color)
		self.frame_widgets_add.place(relx = 0.5, rely = 0.5, anchor = "center")
		self.paid = tk.IntVar()
		self.label_top_add_name = tk.Label(self.frame_widgets_add, text = "Nom :", bg = self.color)
		self.entry_top_add_name = ttk.Entry(self.frame_widgets_add, width = 23)
		self.label_top_add_category = tk.Label(self.frame_widgets_add, text = "Catégorie :", bg = self.color)
		self.combobox_categories = ttk.Combobox(self.frame_widgets_add, height = 4, state = "readonly", 
												values = self.categories_management.get_all_categories())
		self.label_top_add_init_date = tk.Label(self.frame_widgets_add, text = "Date d'émission :", bg = self.color)
		self.entry_top_add_init_date = ttk.Entry(self.frame_widgets_add, width = 23)
		self.label_top_add_due_date = tk.Label(self.frame_widgets_add, text = "Daté d'échéance :", bg = self.color)
		self.entry_top_add_due_date = ttk.Entry(self.frame_widgets_add, width = 23)
		self.label_top_add_price = tk.Label(self.frame_widgets_add, text = "Prix :", bg = self.color)
		self.entry_top_add_price = ttk.Entry(self.frame_widgets_add, width = 23)
		self.label_top_add_paid = tk.Label(self.frame_widgets_add, text = "Complétée :", bg = self.color)
		self.checkbutton_paid = tk.Checkbutton(self.frame_widgets_add, variable = self.paid, 
												command = self.get_checkbutton, bg = self.color)
		self.label_top_add_note = tk.Label(self.frame_widgets_add, text = "Notes :", bg = self.color)
		self.text_top_add_note = tk.Text(self.frame_widgets_add, width = 20, height = 4, font = ("Arial", 10))

		self.labels_top_add = [self.label_top_add_name, self.label_top_add_category,
								self.label_top_add_init_date, self.label_top_add_due_date,
								self.label_top_add_price, self.label_top_add_paid, self.label_top_add_note]
		self.non_labels_top_add = [self.entry_top_add_name, self.combobox_categories, 
								self.entry_top_add_init_date, self.entry_top_add_due_date,
								self.entry_top_add_price, self.checkbutton_paid, self.text_top_add_note]
		for i in range(len(self.labels_top_add)):
			self.labels_top_add[i].grid(row = i, column = 0, ipadx = 5)
			self.non_labels_top_add[i].grid(row = i, column = 1)

		self.frame_buttons_top_add = tk.Frame(self.frame_widgets_add, bg = self.color)
		self.button_top_add_confirm = ttk.Button(self.frame_buttons_top_add, text = "Confirmer",
										command = self.command_confirm_add)
		self.button_top_add_cancel = ttk.Button(self.frame_buttons_top_add, text = "Annuler",
										command = self.top_add_bill.destroy)
		self.frame_buttons_top_add.grid(row = 8, column = 0, columnspan = 2)
		self.button_top_add_confirm.pack(side = "right", padx = 4, pady = 10)
		self.button_top_add_cancel.pack(side = "right", padx = 4, pady = 10)
		self.top_add_bill.bind("<Escape>", lambda _: self.button_top_add_cancel.invoke())
		self.top_add_bill.bind("<Return>", lambda _: self.button_top_add_confirm.invoke())			


	def command_confirm_add(self, mod = False, *event):
		"""Command of the Confirm button in the add Toplevel, Button to confirm changes to a bill or to
		confirm the addition of a bill"""

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
			self.toplevel_message(self.top_add_bill, "Données entrées invalides", "Erreur de saisie")


	def command_button_del(self):
		"""Command of the delete button, to delete a bill from the GUI and from the database"""
		
		self.bill_to_del = self.bill_management.get_bill_id(self.select_item_tree(self.treeview_main))
		self.bill_management.delete_bill(self.bill_to_del)
		self.update_bills()

	
	def command_button_mod(self):
		"""Command of the modify button, to modify a bill (GUI/DB). Open the Toplevel associated with adding
		a bill but with all fields filled"""

		self.bill_to_mod = self.select_item_tree(self.treeview_main)
		if self.bill_to_mod is not None:
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


	def get_checkbutton(self):
		"""Command to get the value of the checkbutton in the add Toplevel"""

		return self.paid.get()


	def command_archive(self):
		"""Command of the button (under Option) to archive the selected bill"""

		try:
			self.id_bill_to_archive = self.bill_management.get_bill_id(self.select_item_tree(self.treeview_main))
			self.bill_management.archive_bill(self.id_bill_to_archive)
		except TypeError:
			self.toplevel_message(self.root, "Aucune sélection effectuée", "Erreur de saisie")
		self.update_bills()


	def double_click_tree(self, event):
		"""Command bound to the double-click, To modify the selected bill""" 

		try:
			self.command_button_mod()
		except TypeError:
			self.top_add_bill.destroy()


	def control_S(self, event):
		"""Command for the Ctrl-S shortcut, delete the selected bill"""

		try:
			self.command_button_del()
		except TypeError:
			pass


	def command_menu_categories(self):
		"""Command of the Categories button (under File), Open the window to manage categories"""

		self.remove_toplevel(self.top_menu_categories)
		self.top_menu_categories = tk.Toplevel(self.root)
		self.top_menu_categories.title("Gestion des catégories")
		self.top_menu_categories.focus()
		self.x_categories, self.y_categories = self.width_screen*0.23, self.height_screen*0.15
		self.top_menu_categories.geometry("%dx%d+%d+%d" % (self.width_root*0.45, self.height_root*0.7,
															self.x_categories, self.y_categories))
		self.top_menu_categories.resizable(width = False, height = False)


		self.canvas_background_categories = tk.Canvas(self.top_menu_categories)
		self.canvas_background_categories.pack(expand = 1, fill = "both")		
		self.canvas_background_categories.create_image(0, 0, image = self.image_background, anchor = "nw")
		
		self.frame_top_treeview = tk.Frame(self.top_menu_categories, height = self.height_root*0.5,
											width = self.width_root*0.4)
		self.frame_top_treeview.propagate(0)
		self.frame_top_treeview.place(relx = 0.05, rely = 0.05, anchor = "nw")
		
		self.treeview_top_categories = ttk.Treeview(self.frame_top_treeview, selectmode = "browse")
		self.treeview_top_categories["columns"] = ("categories")
		self.treeview_top_categories["show"] = "headings"
		self.treeview_top_categories.column("categories")
		self.treeview_top_categories.heading("categories", text = "Catégories")
		self.treeview_top_categories.pack(fill = "both", expand = 1)

		self.button_categories_add = ttk.Button(self.top_menu_categories, text = "Ajouter",
												command = self.command_add_category)
		self.button_categories_delete = ttk.Button(self.top_menu_categories, text = "Supprimer",
												command = self.command_delete_category)
		self.entry_top_categories = ttk.Entry(self.top_menu_categories, width = 30)

		self.button_categories_add.place(relx = 0.1, rely = 0.8)
		self.button_categories_delete.place(relx = 0.29, rely = 0.8)
		self.entry_top_categories.place(relx = 0.5, rely = 0.8)

		self.top_menu_categories.bind("<Escape>", lambda _: self.top_menu_categories.destroy())
		self.top_menu_categories.bind("<Return>", lambda _: self.button_categories_add.invoke())
		self.update_categories_tree()


	def update_categories_tree(self):
		"""Sync the categories of the Treeview and the database"""

		self.treeview_top_categories.delete(*self.treeview_top_categories.get_children())
		self.all_categories = self.categories_management.get_all_categories()
		for element in self.all_categories:
			self.treeview_top_categories.insert("", "end", values = element)


	def command_add_category(self):
		"""Command of the add button, To add a category (GUI and DB)"""

		self.category_added = self.entry_top_categories.get()
		self.entry_top_categories.delete(0, "end")
		self.categories_management.add_category(self.category_added)
		self.update_categories_tree()


	def command_delete_category(self):
		"""Command of the delete button, to delete a category (GUI and DB)"""

		self.category_to_del = self.select_item_tree(self.treeview_top_categories)
		self.categories_management.delete_category(self.category_to_del)
		self.update_categories_tree()



if __name__ == "__main__":

	root = tk.Tk()
	app = InterfaceManager(root)
	root.mainloop()