# AI Lab 4 #

This is the final lab for the course of Aritificial Intelligence 

Work done by Varun Deliwala vd2298 

There are 3 seperate folders for KNN, Naive Bayes and KMeans which contain the respective data with the python file.

Please make sure to change directories while running the code or please put in the relative path of the python file and the respective train and test csv files. 

## Requirements ##
Python 3 or above
I have used the csv library for parsing the csv. 
"pip install csv"


## For KNN ##
The folder with the same name contains knn.py 

to run the program:
    python3 knn.py -train 'train_file.csv' -test 'test_file.csv' -k (int)

example: 
' python3 knn.py -train knn1_train.csv -test knn1_test.csv -k 3 '

' python3 knn.py -train knn2_train.csv -test knn2_test.csv -k 3 '

' python3 knn.py -train knn3_train.csv -test knn3_test.csv -k 5 '


## For Naive Bayes ##
The folder (NaiveBayes) contains the file 'NaiveBayes.py' and the respecitve train and test files 


to run the program:
    python3 NaiveBayes.py -train 'train_file.csv' -test 'test_file.csv' -c (int)

example: 

' python3 NaiveBayes.py -train bayes1_train.csv -test bayes1_test.csv -c 1 '

' python3 NaiveBayes.py -train bayes2_train.csv -test bayes2_test.csv -c 2 '


## KMeans ##
The folder (KMeans) contains the file 'KMeans.py' and the respecitve  files; 
Note the clusters might be interchanged so please do check the output clearly.


to run the program:
    'python3 kMeans.py -train 'KMeans_file.csv' c1x,c1y c2x,c2y, c3x,c3y -d (e2/manh)'

example: 
' python kmeans.py -train KMeans1.csv 0,0 200,200 500,500 -d e2
'

' python kmeans.py -train KMeans2.csv 0,0,0 200,200,200 500,500,500 -d manh
'