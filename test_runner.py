import QueryMaster
import DataHandler
import numpy as np
import Analyzer

qm = QueryMaster.QueryMaster()
qm.create_cnxn(user='root', password='', database='mydb')
#qm.question_1()
#qm.question_3()
qm.question_4()
qm.close()
'''lyzer = Analyzer.Analyzer()
lyzer.question_1()'''