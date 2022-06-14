# IntercoderReliability

This is code used for my bachelor thesis. The data used are rows with respondents and columns with questions. The cells represent a category. The goal is to compare the coding of different person calculating the intercoder reliability. Each df (DataFrame (matrix)) that is read in is the coding of one person. The repo. consists of three files:

* InterRater_reliability.py
* perc_agreement.py
* pearson_corr.py

## InterRater_reliability.py
This file descirbes all the methods used to calculate the intercoder reliability. It consists of 3 steps.

1. First the methods used to get the df in the right format are described. For perc_agreement this is putting all the question below each other in order to get a Serie and then add each Serie of each Coder next to each other. For perc_agreement it is getting a Serie with the total times each categorie is used. After that is done each possible combination of coders needs to be put together in a dataframe.
2. Second the method used to calculate the percentage agreement is described. For each row the method calculates how often the most give category overlaps. So if 2 have chosen category A5, 1 A3, and 1 A4 the percentage agreement is 2/4 = 0.5. Following this the average percentage agreement of each row has to be calculated.
3. Lastly the method used to calculate the pearson correlation has to be calculated. Since pearson correlation is difficult to interprate bland-altman graphs are plot and thee statistics are added to a table. The statistics show the mean difference and the confidence interval of the difference. Lastly the pearson correlation of each combination is added to the key stat df. 

## perc_agreement.py
This file is used to calculate the percentage agreement using the methods from InterRater_reliability.py. This is done in 2 steps.

1. First the data is read in from the excel files and converted to one df. 
2. Lastly the percentage_agreement of each row is added to the df and the average perc_agreement is calculated and printed.

## pearson_corr.py
This file is used to calculate the pearson correlation and add the key stats to a dataframe. This consists of three steps.

1. First the dataframes are read in, the total amount each category is chosen are added to a new df, and each possible combination of coders is combined and added to a list. To keep tap of which combination is chosen a seperate lsit is created with the name of each series. Because the index are the same the name of coders compared can be traced back.
2. Secondly, a df for the key stats is created using the serie classifier. To this df the mean difference, and the confidence interval is added. 
3. Thirdly, the pearson correlation is calculated and added to the key stat df. 
