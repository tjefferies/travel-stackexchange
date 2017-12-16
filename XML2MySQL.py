
# coding: utf-8

# Title: .xml to MySQL transformation
# Author: Travis Jefferies
# Date: 11/12/17
# Code Version: 1.0
# Availability: 

import xml.etree.ElementTree as ET
from sqlalchemy import create_engine
import sys
import pandas as pd
from mysql.connector import MySQLConnection, Error
from glob import glob
from os import path

def get_xml_files(path):
    """ Takes a path as input and globs all .xml files in path 
        Returns a list of .xml file paths """
    file_paths = list()
    for file in glob(path+'*'):
        file_paths.append(str(path)+str(file.split('\\')[1]))
    return file_paths

def connect(localhost,database,user,password):
    """ Connect to MySQL database
        Connection remains open 
        Returns MySQL db connection """
    try:
        conn = create_engine("mysql+mysqlconnector://"+user+':'+password+"@"+localhost+"/"+database)
    except:
        conn = False
    if conn:
        print('Connected to MySQL database')
    return conn

# def update_max_allowed_packet(db_connection):
#     """ Used to allow mass row entry into SQL table """
#     try:
#         with db_connection as cursor:
#             cursor.execute('SET GLOBAL max_allowed_packet=1073741824')
#         print('Table ready for input.')
#     except Error as e:
#         print(e)

class xml_to_mysql:
    
    def __init__(self, path_to_xml_file,db_connection,table_name):
        try:
            self.path = path_to_xml_file
        except IOError:
            input('Please enter valid .xml file path. Press any key to close program.')
            sys.exit()
        try:
            self.conn = db_connection
        except:
            input('Please enter valid MySQL database connection object. Press any key to close program.')
            sys.exit()
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()
        self.table = table_name
        self.df = pd.DataFrame()
        
    def xml2mysql(self):
        """ Finds root.children.attributes {tag: text}
            loops through grabbing data in row structure
            creates new table in database
            with records that use row inherited schema 
            or
            replaces existing table records
            depending on table exists status """
        root = self.root
        all_dummies = []
        for i, child in enumerate(root):
            dummy = {}
            for attr,value in child.attrib.items():
                dummy[attr] = value
            all_dummies.append(dummy)
        self.df = pd.DataFrame(all_dummies).drop_duplicates()
        self.df.to_sql(con=self.conn,name=self.table,if_exists='replace')
        df = self.df
        return df
        
# def main():
    # """ Takes a directory containing .xml files as input
        # parses .xml
        # creates new tables in existing MySQL database
        # using parsed .xml data """

    # """ connect() :params:   localhost := host_server Ex: 'localhost'
                             # database := target_database Ex: 'dvdrentals'
                             # user := username  Ex: 'root'
                             # password := password 'mypassworddadada'
                             
                  # :return:   MySQL DB connection """
    
    # """ update_max_allowed_packet() :params:   db_connection := connection object Ex: 'localhost'
                                    # :return: """
    
    # """ get_xml_files() :params:   path := directory of .xml files to be pushed to MySQL                             
                        # :return:   list of .xml file paths """
    
    # """ get_xml_files() :params:   path := directory of .xml files to be pushed to MySQL                             
                        # :return:   list of .xml file paths """
    
    # xml_file_path = "C:/Users/jeffe/Downloads/travel.stackexchange.com/"
    # try:
        # connection = connect('localhost','stackexchange_travel','root','F0xyrules30')
# #     update_max_allowed_packet(connection)
        # dfs = list()
        # split_paths = [path.split(p) for p in get_xml_files(xml_file_path)]
        # for xml, table in zip(get_xml_files(xml_file_path),split_paths):
            # x = xml_to_mysql(xml,connection,table[1].split('.')[0].lower())
            # dfs.append(x.xml2mysql())
        # print('.xml files successfully entered into database.')
        # return dfs
    # except BaseException as e:
        # print('Failed to do something: ' + str(e))
        # input('Press any key to end program.')
# if __name__ == '__main__':
    # main()
