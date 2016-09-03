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

import pymysql.cursors
import datetime

class BillsManagement:
	"""Management of the database tables relative to bills and archives bills"""

	def __init__(self):

		self.connection = pymysql.connect(host="localhost",
                            			user="root",
                             			password="cedric",
                             			db="bill_manager",
                             			charset="utf8mb4",
                             			cursorclass=pymysql.cursors.DictCursor)

	
	def get_all_bills(self, filter_applied = 0, sort = ("due_date", "ASC")):
		"""Get all the bills that are in the database
		 NB. 0 = "Toutes" 1 = "7 prochains jours" 2 = "30 prochains jours" 3 = "Payées" 4 = "Impayées" """

		with self.connection.cursor() as cursor:

			self.sql = """SELECT `bill_name`, `category`, `init_date`, `due_date`, `price`, `paid`, `notes`
						FROM `bills`"""
			if filter_applied == 1:
				self.sql += "WHERE (`due_date` < ADDDATE(CURDATE(), 7))"
			elif filter_applied == 2:
				self.sql += "WHERE (`due_date` < ADDDATE(CURDATE(), 31))"
			elif filter_applied == 3:
				self.sql += "WHERE (`paid` = 0)"
			elif filter_applied == 4:
				self.sql += "WHERE (`paid` = 1)"
			self.sql += "ORDER BY `{}`".format(sort[0])
			self.sql += sort[1]
			cursor.execute(self.sql)
			
			return cursor.fetchall()

	
	def get_bill_id(self, bill_info):
		"""Get a specific bill's id to identify it"""

		self.bill_info = bill_info
		self.bill_info[2] = datetime.datetime.strptime(self.bill_info[2], "%d-%m-%Y").date()
		self.bill_info[3] = datetime.datetime.strptime(self.bill_info[3], "%d-%m-%Y").date()

		with self.connection.cursor() as cursor:

			self.sql = """SELECT `id`
						FROM `bills`
						WHERE (`bill_name` = %s)
						AND (`category` = %s)
						AND (`init_date` = %s)
						AND (`due_date` = %s)
						AND (`price` = %s)
						AND (`paid` = %s)
						AND (`notes` = %s)"""
			cursor.execute(self.sql, (tuple(self.bill_info)))

			return cursor.fetchone()["id"]			

	
	def add_bill(self, bill_info):
		"""Add a bill into the database"""

		self.bill_info = bill_info
		self.verify_info(self.bill_info)
		self.bill_info[2] = datetime.datetime.strptime(self.bill_info[2], "%d-%m-%Y").date()
		self.bill_info[3] = datetime.datetime.strptime(self.bill_info[3], "%d-%m-%Y").date()

		with self.connection.cursor() as cursor:

			self.sql = "INSERT INTO `bills` VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(self.sql, tuple(self.bill_info))

		self.connection.commit()


	def delete_bill(self, bill_to_del_id):
		"""Delete a bill from the database"""

		self.bill_to_del_id = bill_to_del_id

		with self.connection.cursor() as cursor:

			self.sql = """DELETE FROM `bills` 
						WHERE (`id` = %s)"""
			cursor.execute(self.sql, self.bill_to_del_id)

		self.connection.commit()


	def modify_bill(self, bill_to_mod_id, new_info):
		"""Modify a bill in the database"""

		self.bill_to_mod_id = bill_to_mod_id
		self.new_info = new_info
		self.verify_info(self.new_info)
		self.new_info[2] = datetime.datetime.strptime(self.new_info[2], "%d-%m-%Y").date()
		self.new_info[3] = datetime.datetime.strptime(self.new_info[3], "%d-%m-%Y").date()
		self.new_info.append(self.bill_to_mod_id)
		with self.connection.cursor() as cursor:

			self.sql = """UPDATE `bills` 
						SET `bill_name`= %s, `category` = %s, `init_date` = %s,
						`due_date` = %s, `price` = %s, `paid` = %s, `notes` = %s 
						WHERE (`id` = %s)"""
			cursor.execute(self.sql, (tuple(self.new_info)))

		self.connection.commit()


	def archive_bill(self, bill_to_archive):
		"""Put important bills into another DB to be able to access it later if needed"""

		self.bill_to_archive = bill_to_archive
		with self.connection.cursor() as cursor:

			self.sql = """INSERT INTO `archives`
						SELECT *
						FROM `bills`
						WHERE (`id` = %s)
						"""
			cursor.execute(self.sql, self.bill_to_archive)

		self.delete_bill(self.bill_to_archive)
		self.connection.commit()		


	def verify_info(self, bill_info_verify):
		"""Verify info of the bill that we're trying to add (Error Manager)"""

		self.bill_info_verify = bill_info_verify
		try:
			self.init_date_verify = datetime.datetime.strptime(self.bill_info_verify[2], "%d-%m-%Y").date()
		except ValueError:
			raise ValueError("Date d'émission invalide")
		
		try:
			self.due_date_verify = datetime.datetime.strptime(self.bill_info_verify[3], "%d-%m-%Y").date()
		except ValueError:
			raise ValueError("Date d'échéance invalide")

		try:
			if not (99999 > float(self.bill_info_verify[4]) >= 0):
				raise ValueError("Montant invalide")
		except TypeError:
			raise ValueError("Montant invalide")

		

class CategoriesManagement:
	"""Management of the database table relative to categories"""

	def __init__(self):

		self.connection = pymysql.connect(host="localhost",
                            			user="root",
                             			password="cedric",
                             			db="bill_manager",
                             			charset="utf8mb4",
                             			cursorclass=pymysql.cursors.DictCursor)


	def get_all_categories(self):
		"""Get all categories that are in the database"""

		with self.connection.cursor() as cursor:

			self.sql = "SELECT `category` FROM `categories` ORDER BY `category`"
			cursor.execute(self.sql)
			self.list_of_dict = cursor.fetchall()

			self.ordered_categories = [" "]
			for dicts in self.list_of_dict:
				self.ordered_categories.append(dicts["category"])

			return self.ordered_categories


	def add_category(self, name_new_category):
		"""Add a category to the database"""
		
		self.name_new_category = name_new_category

		with self.connection.cursor() as cursor:

			self.sql = "INSERT INTO `categories` VALUES (NULL, %s)"
			cursor.execute(self.sql, self.name_new_category)
		
		self.connection.commit()


	def delete_category(self, name_del_category):
		"""Delete a category from the database"""

		self.name_del_category = name_del_category

		with self.connection.cursor() as cursor:

			self.sql = "DELETE FROM `Categories` WHERE (`category` = %s)"
			cursor.execute(self.sql, self.name_del_category)

		self.connection.commit()



if __name__ == "__main__":

	test = CategoriesManagement()
	#test.add_category('epicerie2')
	#test.delete_category("epicerie2")
	#print(test.get_all_categories())

	bill_test = BillsManagement()
	#bill_test.add_bill(["toto", "lolo", "14-06-2016", "11-11-2016", "253.20", 1, "test_4"])
	#x = bill_test.get_bill_id(["toto", "lolo", "14-06-2016", "11-11-2016", "253.20", 1, "test_4"])	
	#print(x)
	#bill_test.delete_bill(x)
	#bill_test.modify_bill(x, ["popo", "doolo", "20-01-2016", "09-09-2016", "110.20", 1, "test_12"])
	#print(bill_test.get_all_bills())
	#print(bill_test.get_all_bills(sort = ("price", "ASC")))
	#bill_test.verify_info(["toto", "lolo", "14-12-2016", "11-11-2016", "253.20", 1, "test_4"])
	#bill_test.archive(x)
