import time
out_name = ""
attr_header = ""

# Open source file
with open("principals.tsv", "r", 1, encoding='utf-8') as source_file:
    #Read the first row with names of attributes
    attr_header = source_file.readline()
    i = 1 # Controls how many entries are written to a file
    j = 1 # Output file index

    # Initial output file
    out_file = open("principals_1.txt", "w", encoding ="utf-8")
    # Write the first row
    #out_file.write(attr_header)
    print(attr_header)
    '''
    The loop below writes 100,000 entries from the source file to the current out_file
    When the current out_file has 100,000 entries, the if statement triggers
    and closes the current out_file and opens the next out_file in the sequence
    '''
    for line in source_file:

        if i >= 100000:
            j += 1 # Update file index
            i = 1 # Reset entry counter
            out_file.close()# Close the current file when reached 100,000 entries
            time.sleep(.1)
            out_name = "principals_{}.txt".format(j)# Updates file name for next new file to be written
            out_file = open(out_name, "w", encoding ="utf-8")
            #out_file.write(attr_header)
            out_file.write(line)

        else:
            out_file.write(line)
            i += 1
    out_file.close()
source_file.close()