import csv

class GenreS: #this is for breaking genres down into single genres for use with classification
    readfrom=""

    def __init__(self,toRead):  
        readfrom=toRead

    def splitter(self): #the actual method to split
        mark=0
        toWrite="q2fix.csv" #file results are saved to
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
                        genre=row[0][0:i]   #edit one column of the row
                        row2=row
                        row2[0]=genre
                        #print("reached")
                        #print(genre)
                        writer.writerow(row2) #write the editted row into the toWrite file
                        
                    else:
                        #print(row[0])
                        writer.writerow(row)    #if only one genre in genres, no need to fix
        return toWrite
                    
                
    
