"""Monte Carlo simulations of accuracy"""
## TESTED
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

	trial_idx = range(N)
	T = int(np.random.randint(0,N,1))
	
	## Random:
	acc_1 = list(np.random.binomial(1,p_rand,(N))[:T+1])
		# +1 so it actually goes to T
	p_1 = ([p_rand]*N)[:T]

	## Learn:
	## Create a noisy range for the CDF,
	## and add noise to its center too
	trials = np.arange(.01,10,10/float(N-T))
	trials = trials + stats.norm.rvs(size=trials.shape[0]) 
	p_2 = list(stats.norm.cdf(trials,loc))

	## And p_2 becomes acc_2
	acc_2 = []
	[acc_2.append(int(np.random.binomial(1,p_i,(1)))) for p_i in p_2]

	## Concat _1 and _2 (all are lists)
	acc = acc_1 + acc_2 
	p = p_1 + p_2

	return acc, p

