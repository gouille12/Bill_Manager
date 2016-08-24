#!/usr/bin/env python
#-*- coding: utf-8 -*-

#class BillDatabase:?
import pymysql.cursors

class CategoriesManagement:

	def __init__(self):

		self.connection = pymysql.connect(host='localhost',
                            			user='root',
                             			password='cedric',
                             			db='bill_manager',
                             			charset='utf8mb4',
                             			cursorclass=pymysql.cursors.DictCursor)


	def add_category(self, name_new_category):

		self.name_new_category = name_new_category

		with self.connection.cursor() as cursor:

			self.sql = "INSERT INTO `categories` VALUES (NULL, %s)"
			cursor.execute(self.sql, self.name_new_category)
		
		self.connection.commit()


	def delete_category(self, name_del_category):

		self.name_del_category = name_del_category

		with self.connection.cursor() as cursor:

			self.sql = "DELETE FROM `Categories` WHERE (`category` = %s)"
			cursor.execute(self.sql, self.name_del_category)

		self.connection.commit()

	def close_connection(self):

		self.connection.close()

	def get_all_categories(self):

		with self.connection.cursor() as cursor:

			self.sql = "SELECT `category` FROM `categories` ORDER BY `category`"
			cursor.execute(self.sql)
			self.list_of_dict = cursor.fetchall()

			self.ordered_categories = []
			for dicts in self.list_of_dict:
				self.ordered_categories.append(dicts["category"])

			return self.ordered_categories

			

if __name__ == "__main__":

	test = CategoriesManagement()
	#test.add_category('epicerie2')
	#test.delete_category('epicerie2')
	print(test.get_all_categories())
	test.close_connection()






















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