import sqlite3      #sqlite3 module of python to use SQL statements
import cv2          #to import open cv for image processing
import numpy as np      # for processing image data
pic=input(str("Enter the name of image to be simulated:")) # taking image input from user

MyData = sqlite3.connect('ImageSet.db') #connection object to connect to database
curImg = MyData.cursor()            #cursor method as an event handler

def data():
    global dataset
    dataset= curImg.execute('''SELECT * FROM image''') #comparing with data from database

def func():
    global dict1
    dict1 ={}
    for x in dataset:   #to retrieve values from dataset
        image= x[2]     #Images Column
        name= x[1]      #Name Column
        var=x[3]        #Values Column
        unit=x[4]       #Units Column
        with open('{}.jpg'.format(name),'wb') as f:
            f.write(image)   #transforming images back to .jpg to be prcessed using open cv

        img = cv2.imread("{}".format(pic))   #storing user provided image in a variable
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #for image processing

        template=cv2.imread("{}.jpg".format(name), cv2.IMREAD_GRAYSCALE)   #using the templates retrieved above from respective column
        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED) #storing the result of comparison in a variable
        if np.any(result >= 0.9) == True:    #using numpy library to use if statement
            print("{} found. Value= {} {}".format(name,var,unit))   #printing the data as per template matched
            dict1['{}'.format(name)]=var                            #storing the values of circuit elements in dictionary for later use 
        else: print("No Other Element found")

data()
func()

val= input("Do you wish to compute results? Y/N ")
if val=='Y':
    Current=(dict1['Voltage Source']/dict1['Resistor'])         #for a simple circuit as this, we directly find current 
    print("Current={} amperes".format(Current))                 #displaying the result
else: print("Terminated") 
MyData.commit()             
MyData.close()          #closing the connection to database


