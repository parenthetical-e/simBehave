"""Monte Carlo simulations of accuracy"""
import numpy as np
import scipy.stats as stats
from simBehave.misc import process_prng


def random(N, p, prng=None):
    """
    Generate and returns a random sequence of {1,0} impulses of length <N> 
    with p probability of drawing a 1.
    """
    
    prng = process_prng(prng)
    
    acc = prng.binomial(1, p, N)
    return acc.tolist(), [p, ] * N, prng


def learn(N, loc, prng=None):
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

    prng = process_prng(prng)
    
    # Pass random state from prng to np so that
    # stats.<> will inherit the irght state.
    # There does not seem to be a way to set random
    # state of stats.* functions directly.
    np.random.set_state(prng.get_state())
    
    ## Learn:
    ## Create a noisy range for the CDF,
    trials = np.arange(.01,10,10/float(N))
    trials = trials + stats.norm.rvs(size=trials.shape[0]) 
    p_values = stats.norm.cdf(trials,loc)            

    # And p_values becomes acc
    prng.set_state(np.random.get_state())
        ## Pass the seed stat from np back to
        ## prng, then we can use prng again...
    
    acc = [int(prng.binomial(1, p, 1)) for p in p_values] 

    return acc, list(p_values), prng


def random_learn(N, p_rand, loc, prng=None):
    """
    Generates and returns an binomial array of length N where the p(1) 
    (also returned) increases with the CDF of the normal distribution, 
    after random trial T (sampled from a uniform distribution).  Before
    T accuracy is random governed .
    """
    from simBehave.acc import random

    prng = process_prng(prng)
    
    T = int(prng.randint(0,N,1))

    acc_1, p_1, prng = random(T, p_rand, prng)
    
    # Learn:
    trials = np.arange(.01, 10, (10/float(N - T)))
    
    # Pass random state from prng to np so that
    # stats.<> will inherit the irght state.
    # There does not seem to be a way to set random
    # state of stats.* functions directly.
    np.random.set_state(prng.get_state())
    
    trials = trials + stats.norm.rvs(size=trials.shape[0]) 
    p_2 = stats.norm.cdf(trials,loc)
    p_2[p_2 < 0.5] = 0.5
        ## Rwmove p vals lees than 0.5 -- 
        ## we don't want below chance sampling
        
    prng.set_state(np.random.get_state())
        ## Pass the seed stat from np back to
        ## prng, then we can use prng again...
    
    acc_2 = [int(prng.binomial(1, p, 1)) for p in p_2]
    
    acc = acc_1 + acc_2
    p = list(p_1) + list(p_2)

    return acc, p, prng

