#!/usr/bin/env python
#-*- coding: utf-8 -*-

#class BillDatabase:?
import pymysql.cursors

class BillsManagement:

	def __init__(self):

		self.connection = pymysql.connect(host='localhost',
                            			user='root',
                             			password='cedric',
                             			db='bill_manager',
                             			charset='utf8mb4',
                             			cursorclass=pymysql.cursors.DictCursor)		
	def close_connection(self):

		self.connection.close()

	def add_bill(self, bill_name, category, bill_date, due_date, price, paid, notes):

		self.bill_name = bill_name
		self.category = category
		self.bill_date = bill_date
		self.due_date = due_date
		self.price = price
		self.paid = paid
		self.notes = notes

		with self.connection.cursor() as cursor:

			self.sql = "INSERT INTO `bills` VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(self.sql, (self.bill_name, self.category, self.bill_date, self.due_date, self.price, self.paid, self.notes))

		self.connection.commit()

	def get_all_bills(self):

		with self.connection.cursor() as cursor:

			self.sql = """SELECT `bill_name`, `category`, `init_date`, `due_date`, `price`, `paid`, `notes`
						FROM `bills`
						ORDER BY `due_date`"""
			cursor.execute(self.sql)
			return cursor.fetchall()

	def delete_bill(self, bill_name, init_date, due_date, price):

		self.bill_name = bill_name
		self.init_date = init_date
		self.due_date = due_date
		self.price = price

		with self.connection.cursor() as cursor:

			self.sql = """DELETE FROM `bills` 
						WHERE (`bill_name`= %s)
						AND (`init_date` = %s)
						AND (`due_date` = %s)
						AND (`price` = %s)"""
			cursor.execute(self.sql, (self.bill_name, self.init_date, self.due_date, self.price))


		self.connection.commit()

		
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
	#print(test.get_all_categories())
	test.close_connection()

	bill_test = BillsManagement()
	#bill_test.add_bill('bitchezz', 'homo', 20160514, 20161020, 253.20, 0, 'test_4')
	#bill_test.delete_bill('bitchezz', 20160514, 20161020, 253.20)
	#print(bill_test.get_all_bills())
	bill_test.close_connection()






















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