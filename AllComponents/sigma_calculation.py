import statistics
import pandas as pd

data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})



def calculate_range(data, crit, deci=None):
	subscores = data[crit]
	# print(subscores)
	# print(subscores, "s")
	scores = [x for x in subscores if str(x)!= 'nan']
	# data[crit].to_list()
#print(severe_scores)
	sigma= statistics.stdev(scores)
	#print(sigma)
	mean_val = sum(scores)/len(scores)
	if crit == 'covid_cases': 
		return (1, round(mean_val + sigma, deci))
	return (round(mean_val - sigma, deci), round(mean_val + sigma, deci))

# calculate_range(data, )
#print(calculate_range(data, '% Adults with Diabetes', 1))

