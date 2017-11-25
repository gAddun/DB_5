import QueryMaster
import DataHandler
import numpy as np


qm = QueryMaster.QueryMaster()
qm.create_cnxn(user='user', password='password', database='mydb')
qm.question_1()
qm.question_2()