
# coding: utf-8

# In[ ]:




# In[63]:

import pandas as pd
# this part needed for mac
# import pymysql
# pymysql.install_as_MySQLdb()
############################
import seaborn as sns
from mysql.connector import MySQLConnection, Error
from XML2MySQL import connect
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from collections import defaultdict

class set_table_data_types:

	def __init__(self,host,db,user,password):
		
		self.host = host
		self.db = db
		connection_string = 'mysql+mysqldb://'+user+':'+password+'@'+host+'/'+db
		self.query_connection = create_engine(connection_string)
		try:
			self.db_connection = MySQLConnection(
										host = host,
										database = db,
										user = user,
										password = password)
			if self.db_connection.is_connected():
				print('Connection to MySQL database ' + db + ' successful.')
		except Error:
			print('Error connecting to database ' + db)
			print(Error)
			
		self.columns = defaultdict(list)

	def change_column_datatype(self, column_data_type_mapping=None):
		alter_tbl_query = list()
		alter_tbl_query.append('USE '+self.db+';')
		alter_query_template = "ALTER TABLE {} MODIFY {} {}"
		try:
			cursor_alter_tables = self.db_connection.cursor()
			cursor_table_name = self.db_connection.cursor()
			cursor_table_name.execute("SHOW TABLES")
			table_names = cursor_table_name.fetchall()
			for table_name in table_names:
				tbl_name = table_name[0]
				cursor_column_names = self.db_connection.cursor()
				query = "SELECT * FROM information_schema.columns WHERE table_name= " + "'" + tbl_name + "'"
				cursor_column_names.execute(query)
				col_names = cursor_column_names.fetchall()
				for c_name in col_names:
					self.columns[tbl_name].append(c_name[3])
				cursor_column_names.close()
			alter_query_template = "ALTER TABLE {} MODIFY {} {} ;"
			for tbl, cols in session.columns.items():
				for col in cols:
					if col.lower() == 'date':
						sql_syntax_col_name = '`'+col+'`'
						column_type = 'DATETIME'
					elif col.lower() == 'count':
						sql_syntax_col_name = '`'+col+'`'
						column_type = 'INT'
					elif col.lower() == 'index':
						sql_syntax_col_name = '`'+col+'`'
						column_type = 'INT'
					else:
						sql_syntax_col_name = col
						if 'date' in col.lower():
							column_type = 'DATETIME'
						elif 'id' in col.lower() and not column_type_mapping.get(col.lower()):
							column_type = 'INT'
						elif 'vote' in col.lower():
							column_type = 'INT'
						elif 'count' in col.lower():
							column_type = 'INT'
						elif col.lower() in column_type_mapping.keys():
							column_type = column_type_mapping.get(col.lower())
						else:
							column_type = 'TEXT'
					alter_tbl_query.append(alter_query_template.format(tbl.lower(),sql_syntax_col_name,column_type))
			print('SQL: \n')
			print('\n'.join(alter_tbl_query))
		finally:
			cursor_table_name.close()
			self.db_connection.close()
			self.db_connection.disconnect()


# In[64]:

session = set_table_data_types(host = 'localhost', db = 'stackexchange_cooking', user = 'root', password = password)


# In[65]:

column_type_mapping = {'age':'INT', 'reputation':'INT', 'index': 'INT', 'class': 'INT',  'score': 'INT','bountyamount': 'FLOAT','revisionguid': 'TEXT'}
session.change_column_datatype(column_type_mapping)

# In[ ]:



