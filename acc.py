"""Monte Carlo simulations of accuracy"""
import numpy as np
import scipy.stats as stats

def random(N,p):
	"""
	Generate and returns a random sequence of {1,0} impulses of length N 
	with p probability of drawing a 1.
	"""

	acc = np.random.binomial(1,p,(N))
	return list(acc), [p]*N


def learn(N,loc):
	"""
	Generates and returns an binomial array of length N where the p(1) 
	(also returned) increases with the CDF of the normal distribution, 
	integrated from 0.01 to 10, plus white noise.
	
	The learning rate is determined by sampling of a normal distribution 
	centered on loc.  
	
	Note: A loc of 3 gives curves qualitatively similar to learning 
	patterns often observed in the abstract categorization tasks 
	common to the Seger Lab.
	"""

	## Learn:
	## Create a noisy range for the CDF,
	trials = np.arange(.01,10,10/float(N))
	trials = trials + stats.norm.rvs(size=trials.shape[0]) 
	p_values = stats.norm.cdf(trials,loc)			

	## And p_values becomes acc
	acc = []
	[acc.append(int(np.random.binomial(1,p,(1)))) for p in p_values] 

	return acc, list(p_values)


def random_learn(N,p_rand,loc):
	"""
	Generates and returns an binomial array of length N where the p(1) 
	(also returned) increases with the CDF of the normal distribution, 
	after random trial T (sampled from a uniform distribution).  Before
	T accuracy is random governed .
	"""
	from simBehave.acc import random

	T = int(np.random.randint(0,N,1))
	
	acc_1, p_1 = random(T,p_rand)
	
	# Learn:
	trials = np.arange(.01,10,10/float(N-T))
	trials = trials + stats.norm.rvs(size=trials.shape[0]) 
	p_2 = stats.norm.cdf(trials,loc)			
	p_2[p_2 < 0.5] = 0.5
		## Rwmove p vals lees than 0.5 -- 
		## we don't want below chance sampling
		
	acc_2 = []
	[acc_2.append(int(np.random.binomial(1,p,(1)))) for p in p_2]
	
	acc = acc_1 + acc_2
	p = list(p_1) + list(p_2)

	return acc, p

