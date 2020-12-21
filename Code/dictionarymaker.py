import csv

def clean(word):
    """
    Method to only keep alphabetical characters
    """
    return ''.join(filter(str.isalpha, word.lower()))

if __name__ == "__main__":
    """
    Main Function to write dictionary and a reference for a text file.
    """
    file1 = open("dictionary.txt","w") 
    with open('final_dataset_imdb.csv',encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0 
        for row in csv_reader:
            if row_number==0:
                row_number=1
                continue

            for i in list(row[2].split(" ")):

                file1.write(clean(i)+"\n")
            for i in list(row[9].split(" ")):
                file1.write(clean(i)+"\n")
            for i in list(row[10].split(" ")):
                file1.write(clean(i)+"\n")
            for i in list(row[12].split(", ")):
                for j in i.split(" "):
                    file1.write(clean(j)+"\n")


    file1.close()