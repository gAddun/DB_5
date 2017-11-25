import mysql
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
                # create next entry from returned data and add to array to be written
                next_entry = np.array([gross, num_voted_users, imdb_score])
                ret_data = np.vstack((ret_data, next_entry))
            else:
                i += 1
        ret_data = np.delete(ret_data, (0), axis=0) #remove initial null entry of array
        np.savetxt("q1.csv", ret_data, delimiter=',') #save the result of the query as a csv file
        print("\nOmitted {} entries from question 1 due to missing values")
        cursor.close()

    """
    Executes query related to question 3:
    'Can we predict genre based on number of facebook likes and number of faces in posters?'
    """
    def question_3(self):
        i = 0  # counter for number of omitted entries due to null values
        # initializes an n-dimensional array to store result of query
        ret_data = np.array([None, None, None])  # array initally filled with null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT movie_facebook_likes, facenumber_in_poster, genres FROM table")  # query to perform on database
        cursor.execute(query)
        # for each of the values returned from query, add those values to the n-dim array
        for(likes, faces, genres) in cursor:
            #make sure that no null values are loaded
            if (likes is not None) and (faces is not None) and (genres is not None):
                genres = genres.split('|')
                #make a speparate entry for each genre for each dataset
                for each in genres:
                    #create next entry from returned data and add to array to be written
                    next_entry = np.array([likes, faces, each])
                    ret_data = np.vstack((ret_data, next_entry))
            else:
                i+=1
        ret_data = np.delete(ret_data, (0), axis=0)  # remove initial null entry of array
        np.savetxt("q3.csv", ret_data, delimiter=',')  # save the result of the query as a csv file
        print("\nOmitted {} entries from question 1 due to missing values")
        cursor.close()

    """
    Executes query related to question 4:
    Can we predict the content rating of a film based on plot keywords?
    """

    def question_4(self):
        i = 0  # counter for number of omitted entries due to null values
        # initializes an n-dimensional array to store result of query
        ret_data = np.array([None, None, None])  # array initally filled with null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT plot_keywords, content_rating, genres FROM table")  # query to perform on database
        cursor.execute(query)
        ret_data = np.array([None, None])
        for(keywords, rating) in cursor:
            if(keywords is not None) and (rating is not None):
                keywords = keywords.replace("|", " ") #remove the '|' separator from the data
                next_entry = [keywords, rating]
                ret_data = np.vstack((ret_data, next_entry))
            else:
                i+=1

        ret_data = np.delete(ret_data, (0), axis=0)  # remove initial null entry of array
        np.savetxt("q4.csv", ret_data, delimiter=',')  # save the result of the query as a csv file
        print("\nOmitted {} entries from question 1 due to missing values")
        cursor.close()
