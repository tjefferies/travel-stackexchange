
# coding: utf-8

import pandas as pd
import seaborn as sns
from mysql.connector import MySQLConnection, Error
from XML2MySQL import connect
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

class MySQL2PandasDF:
    '''
    Takes the string connection elements of a MySQL database as input
    Class should only be initialized once - container holds database connection upon init
        All database tables are stored as Pandas DataFrames when returning class instance
        Allows a user to query MySQL normally and return a dataframe of the search results
        Stores user query history and optionally allows user to give each query a unique identifier
    '''
    def __init__(self,host,db,user,password):
        
        self.host = host
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
            
        self.source = dict()
        self.history = dict()
        self.plots = dict()
    
    def db2df(self, db_connection=None):
        """
        Sets self.source, an entire database as a dictionary of pandas DataFrames accessible by table name keys
        Optionally takes a MySQLConnection object as input with the db_connection parameter
        :params: (MySQLConnection object)
        :return: {Table: pd.DataFrame}
        """
        if db_connection is None:
            pass
        else:
            self.db_connection = db_connection
        cursor = self.db_connection.cursor()
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
        self.source = dict()
        for dummy_table_name in rows:
            self.source[dummy_table_name[0]] = pd.read_sql_table(dummy_table_name[0],self.query_connection)
        cursor.close()

    
    def query_mysql(self, query, title):
        """
        Query a MySQL database and return a pandas DataFrame
        Class tracks user history using a dictionary
        User must provide question title as it is the key for the DataFrame returned
        :params: MySQL query, title
        :return: {Query Title: pd.DataFrame}, DataFrame
        """
        if str(type(title)) != "<class 'str'>":
            title = input('Title must be be a string: ')
        else:
            df = pd.read_sql(query,self.query_connection)
            self.history[title] = df
        return df
            
    def plotdf(self, plot, title):
        """
        Plot a pd.series as a given plot title
        Class tracks plot history
        User must provide plot title as it is key for DataFrame returned
        :params: Seaborn or Matplotlibe object, plot title
        :return: {Plot Title: plot}, plot
        """
        if str(type(title)) != "<class 'str'>":
            title = input('Title must be be a string: ')
        else:
            self.plots[title] = plot
        return plot



