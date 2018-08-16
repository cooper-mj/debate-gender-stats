import pandas as pd
import numpy as np
import random
from tabulate import tabulate


'''
Reads the .csv file into a Pandas dataframe.
'''
def read_csv_into_dataframe(filename):
	return pd.read_csv(filename)

'''
Takes in a dictionary correlating first names with "M" (if the name is 
commonly a male name), and "F" (if the name is commonly a female name),
and a name. For the given name, it returns whether the first name of
the name is predominantly male or female, then returns "M" or "F" 
accordingly. Returns "Undefined" if the first name does not appear in
the dictionary.
'''
def classify_name(name_dict, name):
	if name.split(" ")[0] in name_dict.keys():
		return name_dict[name.split(" ")[0]]
	return "Undefined"

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
Takes in a dataframe of a speaker tab, adds a column to the dataframe
representing the gender of the speaker, probabilistically determined
based on the speaker's first name.
'''
def add_genders(dataframe):
	name_dict = read_names("namesgenders.csv")
	dataframe['Gender'] = dataframe['Name'].apply(lambda name: classify_name(name_dict, name))
	print(tabulate(dataframe, headers='keys', tablefmt='psql'))

'''
Takes in a dataframe of a speaker tab, augmented by gender classification.
Prints out the number of male and female competitors, respectively.
'''
def num_competitors_by_gender(dataframe):
	male_rows = dataframe[(dataframe['Gender'] == 'M') & (dataframe['Speaks'] != 0)]
	print("Number of male competitors: " + str(len(male_rows)))
	female_rows = dataframe[(dataframe['Gender'] == 'F') & (dataframe['Speaks'] != 0)]
	print("Number of female competitors: " + str(len(female_rows)))

'''
Takes in a dataframe of a speaker tab, augmented by gender classification.
Prints out the mean speaks of male and female speakers at the tournament.
'''
def mean_speaks_by_gender(dataframe):
	male_rows = dataframe[(dataframe['Gender'] == 'M') & (dataframe['Speaks'] != 0)]
	print("Mean speaker score for male competitors: " + str(round(male_rows['Speaks'].mean(), 2)))
	female_rows = dataframe[(dataframe['Gender'] == 'F') & (dataframe['Speaks'] != 0)]
	print("Mean speaker score for female competitors: " + str(round(female_rows['Speaks'].mean(), 2)))

'''
Takes in a dataframe of a speaker tab, augmented by gender classification.
Prints out the median speaks of male and female speakers at the tournament.
'''
def median_speaks_by_gender(dataframe):
	male_rows = dataframe[(dataframe['Gender'] == 'M') & (dataframe['Speaks'] != 0)]
	print("Median speaker score for male competitors: " + str(round(male_rows['Speaks'].median(), 2)))
	female_rows = dataframe[(dataframe['Gender'] == 'F') & (dataframe['Speaks'] != 0)]
	print("Median speaker score for female competitors: " + str(round(female_rows['Speaks'].median(), 2)))

'''
Takes in a dataframe of a speaker tab, augmented by gender classification.
Uses the bootstrap technique to calculate the probability that the differences
in speaker scores between male and female speakeres at this tournament was due
to chance (the p-value). If the p-value is less than 0.05, it indicates that there
is a statistically significant difference between the performance of men and women
at the tournament; if the p-value is greater than 0.05, it indicates that there is
not a statistically significant difference in the performances of men and women at
the tournament.
'''
def bootstrap_p_value_speaks(dataframe):
	male_scores = dataframe[(dataframe['Gender'] == 'M') & (dataframe['Speaks'] != 0)]['Speaks'].tolist()
	female_scores = dataframe[(dataframe['Gender'] == 'F') & (dataframe['Speaks'] != 0)]['Speaks'].tolist()

	mean_diff = abs(np.mean(male_scores) - np.mean(female_scores))

	num_males = len(male_scores)
	num_females = len(female_scores)

	universal = male_scores + female_scores

	counter = 0

	for i in range(10000):
		male_resample = random.sample(universal, num_males)
		female_resample = random.sample(universal, num_females)

		male_mu = np.mean(male_resample)
		female_mu = np.mean(female_resample)

		if abs(male_mu - female_mu) > mean_diff:
			counter += 1

	p = counter / float(10000)

	if p < 0.05:
		print("There is a statistically significant difference in speaker scores by gender. In this distribution, p = " + str(p))
	else:
		print("There is not a statistically significant difference in speaker scores by gender. In this distribution, p = " + str(p))


def main(filename):
	df = read_csv_into_dataframe(filename)
	add_genders(df)
	num_competitors_by_gender(df)
	mean_speaks_by_gender(df)
	median_speaks_by_gender(df)
	bootstrap_p_value_speaks(df)


if __name__ == "__main__":
	main("debaters.csv")
