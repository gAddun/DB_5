import csv

class GenreS: 
    readfrom=""

    def __init__(self,toRead):
        readfrom=toRead

    def splitter(self):
        mark=0
        toWrite="q2fix.csv"
        with open(self.readfrom, 'r') as file:
            with open(toWrite, 'w', newline='') as csvfile:
                csv_reader = csv.reader(file, delimiter=",")
                fieldnames = ['Genres']
                writer = csv.writer(csvfile)
                #writer.writeheader()

                #csv_reader = reader(file,delimiter=' ')

                for row in csv_reader:
                    i=0
                    #print(row)
                    #if "|" in str(row)
                    if "|" in row[0]:
                        i=row[0].index("|")
                        genre=row[0][0:i]
                        row2=row
                        row2[0]=genre
                        #print("reached")
                        #print(genre)
                        writer.writerow(row2)
                        
                    else:
                        #print(row[0])
                        writer.writerow(row)
        return toWrite
                    
                
    