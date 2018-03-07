import numpy as np
import math
from urllib import urlopen
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import beta
from scipy.stats import chisquare
import scipy.stats
import random
import csv

'''
Function: read_data(filename)

Description: reads data from a .csv file into a double array, from which
values can be accessed by  arr[row][col]. If the file does not exist,
it raises an appropriate error and ceases execution.

Returns: a numpy recarray, containing lists, each containing data from a row
of the original .csv file.
'''
rounds = 0

def read_data(filename):
	# Reads data from csv into double list

	try: 
		tab = np.recfromcsv(filename, delimiter=',', filling_values=0, case_sensitive=True, deletechars='', replace_space=' ', usecols=np.arange(0,9))
		# get the number of rounds
		f = open(filename,'rU')
		reader = csv.reader(f)
		global rounds
		for row in reader:
			if len(row)-8 > rounds:
				rounds = len(row)-8
		return tab


	except IOError:
		raise IOError("The file you have named does not exist - please check the filename, and try again.")

'''
Function: open_names(filename)

Description: reads data from a US Census Names Datafile (in program folder)
into a dictionary, mapping first names to the character 'M' if it is a male name,
and 'F' if it is a female name.

Returns: dictionary, mapping names to respective gender.
'''
def open_names(filename):
	dic = {}
	names_arr = np.recfromcsv(filename, delimiter=',', filling_values=0, case_sensitive=True, deletechars='', replace_space=' ', usecols=np.arange(0,3))
	for i in range(len(names_arr)):
		dic[names_arr[i][0]] = names_arr[i][1]
	return dic

def update_gender(tab, namelist):
	for i in range(len(tab)):
		f_name = tab[i][3].split(' ')[0]
		if f_name in namelist.keys():
			tab[i][2] = namelist[f_name]
		#else : we don't care as our thing can't identify them.
	newtab = []
	for i in range(len(tab)):
		if tab[i][2] in ['M', 'F']:
			newtab.append(tab[i])
	return newtab

'''
This returns a list of speaker scores of the speakers of the gender "gender".
'''
def scores_list(tab, gender):
	ret_list = []
	for i in range(len(tab)):
		# Some people don't show up, so we shouldn't count people whose average is a 60
		if tab[i][2] == gender and tab[i][7] > 60:
			ret_list.append(round(tab[i][7], 3))
	return ret_list

'''
Creates a scatter plot of scores:frequency, then applies a curve of best fit
to the scores.
'''
def plot_performance(tab, m_list, f_list, t_name=""):
	## t_name is a string with the name of the tournament
	#print(m_list)
	#print(f_list)
	
	m_freq_dic = defaultdict(float) #Male speaker scores - score:frequency
	f_freq_dic = defaultdict(float)
	m_list = [round(item, 0) for item in m_list]
	f_list = [round(item, 0) for item in f_list]
	
	for elem in m_list:
		m_freq_dic[elem] += 1
	for elem in f_list:
		f_freq_dic[elem] += 1
	
	m_scores = np.array(m_freq_dic.keys())
	m_freq = [item /(float(len(m_list))/len(f_list)) for item in m_freq_dic.values()]

	f_scores = f_freq_dic.keys()
	f_freq = f_freq_dic.values()
	# ----- DONE CALCULATING THE NUMBERS NOW PLOT IT
	ax = plt.subplot(111)
	# We can look at bar charts
	#b_m = ax.bar(m_scores-0.4, m_freq,width=0.4,color='b',align='center', label="Male Speakers")
	#b_f = ax.bar(f_scores, f_freq,width=0.4,color='g',align='center', label="Female Speakers")
	plt.xlabel('Speaker Score, Rounded to Nearest Point')
	plt.ylabel('Normalized Frequency of Score')
	plt.title(t_name + " - Speaker Scores Distributed by Sex")
	ax.legend()

	# Now make a curve fitting for MEN
	z_men = np.polyfit(m_scores, m_freq, 4)
	f_men = np.poly1d(z_men)
	x_new_m = np.linspace(60, 90, 100)
	y_new_m = f_men(x_new_m)

	# Now many a curve fitting for WOMEN
	z_fem = np.polyfit(f_scores, f_freq, 4)
	f_fem = np.poly1d(z_fem)
	x_new_f = np.linspace(60, 90, 100) #linspace(min_score, max_score, num_splits)
	y_new_f = f_fem(x_new_f)

	# Set axes - change these if they don't play well with the plot
	plt.axis((60,90,0,max(max(m_freq), max(f_freq))))

	plt.plot(m_scores, m_freq,'o', x_new_m, y_new_m, color="blue")

	plt.plot(f_scores, f_freq,'o', x_new_f, y_new_f, color="red")

	plt.show()
	
'''
Assumes that the scores of debaters are normally distributed. Then, plots
the distributions of male and female scores.
'''
def plot_normal_dist(tab, m_list, f_list, t_name=""):
	# plots a normal distribution of the speaker scores on the tab.
	import matplotlib.mlab as mlab #not good convention to put it here

	m_mean = np.mean(m_list)
	m_var = np.var(m_list)
	m_sigma = math.sqrt(m_var)

	f_mean = np.mean(f_list)
	f_var = np.var(f_list)
	f_sigma = math.sqrt(f_var)

	x = np.linspace(60, 90, 100)

	plt.plot(x,mlab.normpdf(x, m_mean, m_sigma), label="Male Speakers")
	plt.plot(x, mlab.normpdf(x, f_mean, f_sigma), label="Female Speakers")
	plt.legend()


	plt.xlabel('Speaker Score')
	plt.ylabel('Probability of Obtaining Score')
	plt.title(t_name + " - Speaker Scores Distributed by Sex")

	plt.show()

def bootstrap_p_value(m_list, f_list):
	mean_diff = abs(np.mean(m_list)-np.mean(f_list))
	N = len(m_list)
	M = len(f_list)
	universal = m_list+f_list
	count = 0
	for i in range(10000):
		m_list_resample = random.sample(universal, N)
		f_list_resample = random.sample(universal, M)
		m_list_mu = np.mean(m_list_resample)
		f_list_mu = np.mean(f_list_resample)
		meandifference = abs(m_list_mu-f_list_mu)
		if meandifference > mean_diff:
			count += 1
	return count / float(10000)

def beta_dist(tab, m_list, f_list, t_name=""):
	## t_name is a string with the name of the tournament
	# Make a beta distribution for a man scoring above an 80; woman scoring above an 80
	# List of all scores in the tournament > 80
	high_scores = []
	for i in range(len(tab)):
		if tab[i][7] >= 80:
			high_scores.append(round(tab[i][7], 3))

	prior_high = float(len(high_scores))/len(tab)
	# print("Prior Probability of Scoring above an 80: " + str(prior_high))
	# Use this probability to create priors for male and female debaters - normalized
	# for the size of m_list and f_list
	# print(float(len(m_list))/(len(m_list)+len(f_list)))
	# print(float(len(f_list))/(len(m_list)+len(f_list)))

	prior_men_a = int(len(m_list)*prior_high)
	prior_men_b = len(m_list)-(prior_men_a)

	prior_women_a = int(len(f_list)*prior_high)
	prior_women_b = len(f_list)-(prior_women_a)
	'''
	print("Prior men a: " + str(prior_men_a))
	print("Prior men b: " + str(prior_men_b))
	print("Prior women a: " + str(prior_women_a))
	print("Prior women b: " + str(prior_women_b))
	print("Len men: " + str(len(m_list)))
	print("Len women: " + str(len(f_list)))
	'''
	posterior_women_a = len([x for x in f_list if x > 80])
	posterior_women_b = len(f_list) - (posterior_women_a)

	posterior_men_a = len([x for x in m_list if x > 80])
	posterior_men_b = len(m_list) - (posterior_men_a)

	# Now plot a beta for mens' performances
	m_a = prior_men_a+posterior_men_a
	m_b = prior_men_b+posterior_men_b
	x = np.arange(0.01, 1, 0.01)
	m_y = beta.pdf(x, m_a, m_b)
	plt.plot(x, m_y, label="Male Speakers")

	f_a = prior_women_a+posterior_women_a
	f_b = prior_women_b+posterior_women_b
	f_y = beta.pdf(x, f_a, f_b)
	plt.plot(x, f_y, label="Female Speakers")
	#Add vertical line showing the prior probability of scoring above an 80
	plt.axvline(x=prior_high, label="Prior Probability of Average Score > 80", color="black")

	plt.xlabel('X~P(overall average score > 80 | gender)')
	plt.ylabel('dbeta(X, m_a/f_a, m_b/f_b')
	plt.title(t_name + " - Speaker Scores Distributed by Sex")


	plt.legend()
	plt.show()

'''
Function: tournament_team_list(tab)

Description: This function takes in the tournament tab, and returns a dictionary
mapping the team name to a list of team members. This function only returns the teams
for which the update_gender function was able to identify the gender of both speakers.

Returns: a dictionary, where the key is the name of a given team at the tournament,
and the value is a list of speakers on that team.
'''
def tournament_team_list(tab):
	# returns a dictionary - key is team name, value is a list of the speakers on the team.
	teams_list = {}
	for i in range(len(tab)):
		if tab[i][4] not in teams_list.keys():
			teams_list[tab[i][4]] = []

	end_teams_list = []
	for i in teams_list.keys():
		tmp_team = []
		for j in range(len(tab)):
			if (tab[j][4]) == i:
				tmp_team.append(tab[j][3])
		if len(tmp_team) > 1:
			teams_list[i] = tmp_team
		else:
			del teams_list[i]
	return teams_list

def gender_split(teams_list, namelist):
	# Returns a tuple of lists. ([MM_teams], [FF_teams], [MF_teams])
	MM_teams = []
	FF_teams = []
	MF_teams = []

	for elem in teams_list.keys():
		partner_one = teams_list[elem][0].split(' ')[0]
		partner_two = teams_list[elem][1].split(' ')[0]

		if namelist[partner_one] == 'M' and namelist[partner_two] == 'M':
			MM_teams.append(elem)
		elif namelist[partner_one] == 'F' and namelist[partner_two] == 'F':
			FF_teams.append(elem)
		else:
			MF_teams.append(elem) #For error purposes, note that there is the most bias against MF teams
								  # in this system
	return (MM_teams, MF_teams, FF_teams)

def mean_points_genders(tab, gender_list):
	MM_team_points = []
	FF_team_points = []
	MF_team_points = []

	for elem in gender_list[0]: #The MM ones
		for i in range(len(tab)):
			if tab[i][4] == elem:
				MM_team_points.append(int(tab[i][5]))

	for elem in gender_list[1]: #The MF ones
		for i in range(len(tab)):
			if tab[i][4] == elem:
				MF_team_points.append(int(tab[i][5]))

	for elem in gender_list[2]: #The FF ones
		for i in range(len(tab)):
			if tab[i][4] == elem:
				FF_team_points.append(int(tab[i][5]))
	return (MM_team_points, MF_team_points, FF_team_points)

'''
Assumes that the team points of debaters are normally distributed. Then, plots
the distributions of MM, MF, and FF teams.
'''
def gender_teams_normal(gender_tup, t_name):
	import matplotlib.mlab as mlab #not good convention to put it here
	global rounds

	mm_mean = np.mean(gender_tup[0]) #MM
	mm_var = np.var(gender_tup[0])
	mm_sigma = math.sqrt(mm_var)

	print("\tP(MM Team Score > 2*rounds) = " + str(1-scipy.stats.norm(mm_mean, mm_sigma).cdf(2*rounds)))

	mf_mean = np.mean(gender_tup[1]) #MF
	mf_var = np.var(gender_tup[1])
	mf_sigma = math.sqrt(mf_var)

	print("\tP(MF Team Score > 2*rounds) = " + str(1-scipy.stats.norm(mf_mean, mf_sigma).cdf(2*rounds)))


	ff_mean = np.mean(gender_tup[2]) #FF
	ff_var = np.var(gender_tup[2])
	ff_sigma = math.sqrt(ff_var)

	print("\tP(FF Team Score > 2*rounds) = " + str(1-scipy.stats.norm(ff_mean, ff_sigma).cdf(2*rounds)))

	x = np.linspace(0, 27)

	try:
		plt.plot(x,mlab.normpdf(x, mm_mean, mm_sigma), label="Male-Male Teams")
	except ZeroDivisionError:
		print("No Male-Male teams found at the tournament.")
	try:
		plt.plot(x,mlab.normpdf(x, mf_mean, mf_sigma), label="Male-Female Teams")
	except ZeroDivisionError:
		print("No Male-Female teams found at the tournament.")
	try:
		plt.plot(x, mlab.normpdf(x, ff_mean, ff_sigma), label="Female-Female Teams")
	except ZeroDivisionError:
		print("No Female-Female teams found at the tournament.")
	plt.legend()


	plt.xlabel('Team Points')
	plt.ylabel('Probability of Obtaining X Points')
	plt.title(t_name + " - Team Points by Gender Composition of Team")

	plt.show()

def basic_info(tab, m_list, f_list, t_name, names, team_gender_points, orig_tablen):
	print("===== Basic Information - " + t_name + " =====\n")
	print("Speaker Points Statistics:\n")
	print("\tMean Male Speaker Score: " + str(round(np.mean(m_list), 1)))
	print("\tMean Female Speaker Score: " + str(round(np.mean(f_list), 1)) + "\n")
	print("\tMedian Male Speaker Score: " + str(np.median(m_list)))
	print("\tMedian Female Speaker Score: " + str(np.median(f_list)) + "\n")
	print("\tNumber of Male Competitors: " + str(len(m_list)))
	print("\tNumber of Female Competitors: " + str(len(f_list)) + "\n")
	print("\tRatio of Men to Women: " + str(round(float(len(m_list))/len(f_list), 2)) + "\n")

	# Assuming p < 0.05 is statistical significance, is there a statistically significant
	# difference in performance of men vs. women?
	p = bootstrap_p_value(m_list, f_list)
	if p < 0.05:
		print("\tStatsitically Significant Difference in Speaker Performance Conditioned on Gender: p = " + str(p) + "\n")
	else:
		print("\tStatistically Insignificant Difference in Speaker Performance Conditioned on Gender: p = " + str(p) + "\n")
	
	print("Team Points Statistics:\n")
	print("\tMean of MM Teams: " + str(round(np.mean(team_gender_points[0]), 2)))
	print("\tMean of MF Teams: " + str(round(np.mean(team_gender_points[1]), 2)))
	print("\tMean of FF Teams: " + str(round(np.mean(team_gender_points[2]), 2)) + "\n")

	print("\tMedian of MM Teams: " + str(np.median(team_gender_points[0])))
	print("\tMedian of MF Teams: " + str(np.median(team_gender_points[1])))
	print("\tMedian of FF Teams: " + str(np.median(team_gender_points[2])) + "\n")

	MF_speaks_tup = MF_speaks(tab, gender_split(tournament_team_list(tab), names)[1], names)
	print("\tNumber of Identified MF Teams: " + str(len(gender_split(tournament_team_list(tab), names)[1])))
	print("\tMean Male Speaks within MF Teams: " + str(round(np.mean(MF_speaks_tup[0]), 1)))
	print("\tMean Female Speaks within MF Teams: " + str(round(np.mean(MF_speaks_tup[1]), 1)) + "\n")

def MF_speaks(tab, MF_teams, namelist):
	# Returns a tuple containing a list of male speaks from MF teams, and female speaks from MF teams
	M_speaks_list = []
	F_speaks_list = []
	##THESE LISTS TURN UP EMPTY AND I DONT KNOW WHY
	for team in MF_teams:
		for i in range(len(tab)):			
			if tab[i][4] == team and namelist[tab[i][3].split(' ')[0]] == 'M':
				M_speaks_list.append(tab[i][7])
			if tab[i][4] == team and namelist[tab[i][3].split(' ')[0]] == 'F':
				F_speaks_list.append(tab[i][7])
	return (M_speaks_list, F_speaks_list)


def main():
	global rounds
	names = open_names("namesgenders.csv")
	#t_file = raw_input("Enter the name of the tournament file to read from: ")
	tab = read_data("wudc2017s.csv")
	orig_tablen = len(tab)
	t_name = "EUDC 2017" #raw_input("Enter the name of the tournament (optional): ")
	tab = update_gender(tab, names)

	m_list = (scores_list(tab, 'M'))
	f_list = (scores_list(tab, 'F'))

	team_gender_points = mean_points_genders(tab, gender_split(tournament_team_list(tab), names))
	basic_info(tab, m_list, f_list, t_name, names, team_gender_points, orig_tablen)

	# plot_performance(tab, m_list, f_list, t_name)

	# ------ PLOTS ------
	plot_normal_dist(tab, m_list, f_list, t_name)

	gender_teams_normal(team_gender_points, t_name)

	# Accuracy of sex identity algorithm - see what proportion of the tournament could be classified
	print("\n")
	print("Sex Identity Algorithm Accuracy: " + str((len(m_list)+len(f_list))/float(orig_tablen)))

	beta_dist(tab, m_list, f_list, t_name)

if __name__ == '__main__':
	main();

'''
Use normals to find: 1) Probability speakers score above an 80, 2) Probability that teams break (straights) - 
for this bit I'll need to calculate how many rounds the tournament is.
'''
