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

	def add_bill(self, bill_info):

		self.bill_info = bill_info

		with self.connection.cursor() as cursor:

			self.sql = "INSERT INTO `bills` VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(self.sql, tuple(self.bill_info))

		self.connection.commit()

	def get_all_bills(self, filter_applied = 0, sort = ("due_date", "ASC")):

		# 0 = "Toutes" 1 = "7 prochains jours" 2 = "30 prochains jours" 3 = "Payées" 4 = "Impayées"

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



	def delete_bill(self, bill_to_del_id):

		self.bill_to_del_id = bill_to_del_id

		with self.connection.cursor() as cursor:

			self.sql = """DELETE FROM `bills` 
						WHERE (`id` = %s)"""
			cursor.execute(self.sql, self.bill_to_del_id)

		self.connection.commit()

	def modify_bill(self, bill_to_mod_id, new_info):

		self.bill_to_mod_id = bill_to_mod_id
		self.new_info = new_info
		self.new_info.append(self.bill_to_mod_id)
		with self.connection.cursor() as cursor:

			self.sql = """UPDATE `bills` 
						SET `bill_name`= %s, `category` = %s, `init_date` = %s, `due_date` = %s, `price` = %s, `paid` = %s, `notes` = %s 
						WHERE (`id` = %s)"""
			cursor.execute(self.sql, (tuple(self.new_info)))

		self.connection.commit()

		
	def get_bill_id(self, bill_info):

		self.bill_info = bill_info

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

			return cursor.fetchone()['id']

		
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
	#bill_test.add_bill(['momo', 'lolo', 20160514, 20161205, 253.20, 0, 'test_4'])
	#x = bill_test.get_bill_id(['rororo', 'lolo', 20160514, 20161020, 253.20, 0, 'test_4'])	
	#print(x)
	#bill_test.delete_bill(x)
	#bill_test.modify_bill(x, ['bobobo', 'nonodo', 20160414, 20160920, 243.20, 1, 'tes_4'])
	#print(bill_test.get_all_bills())

	#print(bill_test.get_all_bills())
	#print(bill_test.get_all_bills(sort = ("price", "ASC")))


	bill_test.close_connection()
