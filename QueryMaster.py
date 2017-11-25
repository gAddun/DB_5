import mysql
import DataHandler
from mysql.connector import errorcode
import numpy as np

"""
The QueryMaster class is responsible for holding connection objects for the SQL database
and for performing queries through the connection objects
"""

class QueryMaster:
    def __init__(self):
        self.connection = None

    def create_cnxn(self, user=None, password='', database=None, port=3306):
        if(self.connection is not None):
            self.connection.close()
        try:
            self.connection = mysql.connector.connect(user=user, password=password, host="127.0.0.1", database=database)
        except mysql.connector.errorcode as err:
            if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
                print("ACCESS DENIED")
            elif (err.errno ==errorcode.ER_BAD_DB_ERROR):
                print("DB DNE")
            else:
                print("error")

    """
    The below methods named question_1 - question_5 perform the queries into our database
    These methods wrote the results of these queries to csv file for the data
    """


    '''
    Executes the query for question 1:
    'Can we predict imdb score based on, votes and revenue?'
    '''
    def question_1(self):
        i = 0 #counter for number of omitted entries due to null values
        #initializes an n-dimensional array to store result of query
        ret_data = np.array([None, None, None])#array initally filled with null values
        cursor = self.connection.cursor() # cursor object to perform queries
        query = ("SELECT gross, num_voted_users, imdb_score FROM table") # query to perform on database
        cursor.execute(query)
        #for each of the values returned from query, add those values to the n-dim array
        for (gross, num_voted_users, imdb_score) in cursor:
            # check for null values
            if (gross is not None) and (num_voted_users is not None) and (imdb_score is not None):
                next_entry = np.array([gross, num_voted_users, imdb_score])
                np.vstack((ret_data, next_entry))
            else:
                i += 1
        ret_data = np.delete(ret_data, (0), axis=0) #remove initial null entry of array
        np.savetxt("q1.csv", ret_data, delimiter=',') #save the result of the query as a csv file
        print("\nOmitted {} entries from question 1 due to missing values")
        cursor.close()

    """
    Executes query related to question 3:
    'Can we predict genre based on number of facebook likes and number of faces in posters?
    """

    def question_3(self):
        i = 0
        ret_data = []