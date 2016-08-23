#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pypyodbc

#class BillDatabase:?


class CategoriesManagement:

	def __init__(self):

		self.connexion_string = "DRIVER = {Microsoft Access Driver (*.mdb, *.accdb)}; Dbq = CategoriesDatabase.accdb;"
		self.connexion = pypyodbc.connect(self.connexion_string)

	#def add_category(self):

		# add access

	#def delete_category(self):

		# del access



if __name__ == "__main__":

	test = CategoriesManagement()





















"""
class Bill:

	def __init__(self):

		self.name = "Hydro"
		self.price = 14.85
		self.category = "electricity"
		self.date = "14-06-2016"
		self.paid = False
		self.note = None


	def get_bill_info(self):

	def set_bill_info(self):
"""