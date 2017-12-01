import mysql
from mysql.connector import errorcode
import numpy as np
import csv

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

    def close(self):
        self.connection.close()

    '''
    Executes the query for question 1:
    'Can we predict imdb score based on votes and revenue?'
    '''
    def question_1(self):
        i = 0 #counter for number of omitted entries due to null values
        cursor = self.connection.cursor() # cursor object to perform queries
        query = ("SELECT Gross, UserReviews, ImdbScore FROM imdb5000") # query to perform on database
        cursor.execute(query)
        # CSV file to write
        with open('q1.csv', 'w', newline ='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (gross, num_voted_users, imdb_score) in cursor:
                # check for null values
                if (gross is not None and gross is not 0) and (num_voted_users is not None and num_voted_users is not 0) and (imdb_score is not None and imdb_score is not 0):
                    # write next entry into file
                    writer.writerow([gross, num_voted_users, imdb_score])
                else:
                    i += 1
        csvfile.close()
        print("\nOmitted {} entries from question 1 due to missing values".format(i))
        cursor.close()

    """
    The below methods executes query related to question 3:
    'How do relationships between gross, number user reviews and duration affect content rating?'
    3 queries are executed to create three tables to answer this question
    """
    def question_3a(self):
        #We only examine the most prevelant content ratings
        rating_list = ["G", "PG", "PG-13", "R", "NC-17", "X", "note rated"]
        i = 0  # counter for number of omitted entries due to null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT Duration, Gross, ContentRating FROM imdb5000")  # query to perform on database
        cursor.execute(query)
        # CSV file to write
        with open('q3a.csv', 'w', newline ='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for(dur, gross, rating) in cursor:
                #make sure that no null values are loaded
                if (dur is not None and dur is not 0) and (gross is not None and gross is not 0) and (rating is not None and rating is not ""):
                    if(rating_list.count(rating)<1):
                        i+=1
                    else:
                        #write each entry into the table
                        writer.writerow([dur, gross, rating])
                else:
                    i+=1
        print("\nOmitted {} entries from question 3 due to missing values".format(i))
        cursor.close()
    def question_3b(self):
        # We only examine the most prevelant content ratings
        rating_list = ["G", "PG", "PG-13", "R", "NC-17", "X", "note rated"]
        i = 0  # counter for number of omitted entries due to null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT Duration, Gross, ContentRating FROM imdb5000")  # query to perform on database
        cursor.execute(query)
        # CSV file to write
        with open('q3b.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (dur, gross, rating) in cursor:
                # make sure that no null values are loaded
                if (dur is not None and dur is not 0) and (gross is not None and gross is not 0) and (
                        rating is not None and rating is not ""):
                    if (rating_list.count(rating) < 1):
                        i += 1
                    else:
                        # write each entry into the table
                        writer.writerow([dur, gross, rating])
                else:
                    i += 1
        print("\nOmitted {} entries from question 3 due to missing values".format(i))
        cursor.close()
    def question_3c(self):
        # We only examine the most prevelant content ratings
        rating_list = ["G", "PG", "PG-13", "R", "NC-17", "X", "note rated"]
        i = 0  # counter for number of omitted entries due to null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT Duration, Gross, ContentRating FROM imdb5000")  # query to perform on database
        cursor.execute(query)
        # CSV file to write
        with open('q3c.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (dur, gross, rating) in cursor:
                # make sure that no null values are loaded
                if (dur is not None and dur is not 0) and (gross is not None and gross is not 0) and (
                        rating is not None and rating is not ""):
                    if (rating_list.count(rating) < 1):
                        i += 1
                    else:
                        # write each entry into the table
                        writer.writerow([dur, gross, rating])
                else:
                    i += 1
        print("\nOmitted {} entries from question 3 due to missing values".format(i))
        cursor.close()

    """
    Executes query related to question 4:
    Can we predict the content rating of a film based on plot keywords?
    """
    def question_4(self):
        i = 0  # counter for number of omitted entries due to null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT Keywords, ContentRating FROM imdb5000")  # query to perform on database
        cursor.execute(query)
        # CSV file to write
        with open('q4.csv', 'w', newline ='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for(keywords, rating) in cursor:
                if(keywords is not None and keywords is not "") and (rating is not None and rating is not ""):
                    keywords = keywords.replace("|", " ") #remove the '|' separator from the data
                    writer.writerow([keywords, rating])
                else:
                    i+=1
        print("\nOmitted {} entries from question 4 due to missing values".format(i))
        cursor.close()

    """
        Executes query related to question 5:
        Can we predict revenue based on budget, and imdb score?
    """
    def question_5(self):
        i = 0  # counter for number of omitted entries due to null values
        cursor = self.connection.cursor()  # cursor object to perform queries
        query = ("SELECT Budget, ImdbScore, CastFB, Gross FROM imdb5000")  # query to perform on database
        cursor.execute(query)
        #CSV file to write
        with open('q5.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for (budget, score, likes, gross) in cursor:
                # make sure that no null values are loaded
                if (budget is not None) and (score is not None and score is not "")\
                        and (likes is not None and likes is not "") and (gross is not None and gross!=0):
                    writer.writerow([budget, score, likes, gross])
                else:
                    i += 1
        print("\nOmitted {} entries from question 5 due to missing values".format(i))
        cursor.close()

    '''
    Single callable method to runn all queries
    '''
    def queries_to_tables(self):
        self.question_1()
        self.question_2()
        self.question_3()
        self.question_4()
        self.question_5()


