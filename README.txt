I. FILE LIST
------------
gender_stats.py         Statistical analysis functions for speaker and team performance based on gender.
namesgenders.csv        1996 US Census Data (https://www.ssa.gov/oact/babynames/limits.html) mapping first names to genders.
cambridgeiv2017s.csv    Tab from Cambridge IV 2017.
oxfordiv2017s.csv       Tab from Oxford IV 2017.
wudc2017s.csv           Tab from WUDC 2017.
yaleiv2016s.csv         Tab from Yale IV 2016.
README.txt              This file.
LICENSE                 License information (MIT License).

II. TAB FORMAT
--------------
This program takes in .csv files of a specific format (below). The column categories are as follows:
ENL,ESL,Gender,Speaker,Team,Team Points,Speaker Points,AVG,#1,#2,#3,#4,#5,#6,#7,#8,#9

And an example of a row in the .csv file would be:
11,,Undefined,Harry Elliott,Stanford LE,11,405,81,81,77,86,82,79,0,0,0,0This example is for a five-round tournament; in this case, rounds 6-9 are entered into the .csv as speaker scores of zero.