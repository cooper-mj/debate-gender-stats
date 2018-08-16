import pandas as pd
import numpy as np
import random
import sys
from tabulate import tabulate


'''
Reads the .csv file into a Pandas dataframe.
'''
def read_csv_into_dataframe(filename):
	return pd.read_csv(filename)

'''
Takes in a dictionary correlating first names with "M" (if the name is 
commonly a male name), and "F" (if the name is commonly a female name),
and the names of two debaters. For each name, it returns determines 
whether the team member is most likely male or female, then it returns
"MM" if the team consists of two males, "FF" if the team consists of
two females, "FM" if it is a mixed team, and "Undefined" if it cannot
classify one of the speakers (if the speaker's name does not appear
in the dictionary)
'''
def classify_team(name_dict, debater1, debater2):
	classification = ""
	if debater1.split(" ")[0] in name_dict.keys():
		classification += name_dict[debater1.split(" ")[0]]
	else:
		return "Undefined"

	if debater2.split(" ")[0] in name_dict.keys():
		classification += name_dict[debater2.split(" ")[0]]
	else:
		return "Undefined"

	return ''.join(sorted(classification)) # Make sure mixed teams are all FM, instead of MF or FM

'''
Reads the list of names in from the database of names, and returns a
dictionary mapping first names to "M" or "F" depending on whether the
name is predominantly a male or female name. If the name appears in the
database as both a male or female name, the name is categorized based on
the relative frequency of the name being a male or female name.
'''
def read_names(filename):
	names_df = pd.read_csv(filename)
	names_dict = {}
	for index, row in names_df.iterrows():
		if row['Name'] in names_dict.keys():
			# Add the gender which has the greatest frequency. For example, "Emily" corresponds to
			# both "F" and "M", but the frequency with which it correlates to "F" is far greater than
			# that at which it corresponds to "M". So we should classify "Emily" as "F".
			if names_dict[row['Name']][1] < row['Frequency']:
				names_dict[row['Name']] = (row['Gender'], row['Frequency'])
			continue

		names_dict[row['Name']] = (row['Gender'], row['Frequency'])
	
	for name in names_dict.keys():
		names_dict[name] = names_dict[name][0]
	
	return names_dict

'''
Takes in a dataframe of a team tab, adds a column to the dataframe
representing the gender composition of the team (either "MM", "FF", or "FM")
probabilistically determined based on the speaker's first name.
'''
def add_genders(dataframe):
	name_dict = read_names("namesgenders.csv")
	dataframe['Gender'] = dataframe.apply(lambda row: classify_team(name_dict, row['Debater 1'], row['Debater 2']), axis=1)
	print(tabulate(dataframe, headers='keys', tablefmt='psql'))

'''
Takes in a dataframe of a team tab, augmented by team gender makeup.
Prints out the number of MM, MF, and FM teams, respectively.
'''
def num_teams_by_gender(dataframe):
	mm_rows = dataframe[(dataframe['Gender'] == 'MM') & (dataframe['Speaks'] != 0)]
	print("Number of MM teams: " + str(len(mm_rows)))
	ff_rows = dataframe[(dataframe['Gender'] == 'FF') & (dataframe['Speaks'] != 0)]
	print("Number of FF teams: " + str(len(ff_rows)))
	fm_rows = dataframe[(dataframe['Gender'] == 'FM') & (dataframe['Speaks'] != 0)]
	print("Number of FM teams: " + str(len(fm_rows)))


'''
Takes in a dataframe of a team tab, augmented by team gender makeup.
Prints out the mean number of metric for MM, FF, and FM teams, respectively,
where metric is a member of the set {'Wins', 'Speaks', 'Ranks'}.
'''
def mean_metric_by_gender(dataframe, metric):
	mm_rows = dataframe[(dataframe['Gender'] == 'MM') & (dataframe['Speaks'] != 0)]
	print("Mean " + metric.lower() + " for MM team: " + str(round(mm_rows[metric].mean(), 2)))
	ff_rows = dataframe[(dataframe['Gender'] == 'FF') & (dataframe['Speaks'] != 0)]
	print("Mean " + metric.lower() + " for FF team: " + str(round(ff_rows[metric].mean(), 2)))
	fm_rows = dataframe[(dataframe['Gender'] == 'FM') & (dataframe['Speaks'] != 0)]
	print("Mean " + metric.lower() + " for FM team: " + str(round(fm_rows[metric].mean(), 2)))

'''
Takes in a dataframe of a team tab, augmented by team gender makeup.
Prints out the median number of metric for MM, FF, and FM teams, respectively,
where metric is a member of the set {'Wins', 'Speaks', 'Ranks'}.
'''
def median_metric_by_gender(dataframe, metric):
	mm_rows = dataframe[(dataframe['Gender'] == 'MM') & (dataframe['Speaks'] != 0)]
	print("Median " + metric.lower() + " for MM team: " + str(round(mm_rows[metric].median(), 2)))
	ff_rows = dataframe[(dataframe['Gender'] == 'FF') & (dataframe['Speaks'] != 0)]
	print("Median " + metric.lower() + " for FF team: " + str(round(ff_rows[metric].median(), 2)))
	fm_rows = dataframe[(dataframe['Gender'] == 'FM') & (dataframe['Speaks'] != 0)]
	print("Median " + metric.lower() + " for FM team: " + str(round(fm_rows[metric].median(), 2)))


def main(filename):
	df = read_csv_into_dataframe(filename)
	add_genders(df)
	num_teams_by_gender(df)
	print("")
	mean_metric_by_gender(df, "Wins")
	print("")
	mean_metric_by_gender(df, "Speaks")
	print("")
	mean_metric_by_gender(df, "Ranks")
	print("")
	median_metric_by_gender(df, "Wins")
	print("")
	median_metric_by_gender(df, "Speaks")
	print("")
	median_metric_by_gender(df, "Ranks")

if __name__ == "__main__":
	try:
		filename = sys.argv[1]
		main(filename)
	except IndexError:
		# Error description since the user didn't enter a filename for the tab
		print("")
		print("Error. Please enter the name of the tab file you wish to analyze. E.g.")
		print("    $ python3 apda_gender_stats.py [filename]")
		print("")

