"""Create lists of randomized trials."""
## TESTED
import os
import numpy as np

def random(N,k):
	"""
	Creates a trialset of N randomized conditions of total length N+1*k, 
	where k is the number of trials/condition. Returns a list of conditions.
	Conditions are indexed from 1; 0 implies terminal condtions, somthing 
	this function can't handle.
	"""

	conditions = []
	[conditions.extend([n]*k) for n in range(1,N+1)]	
	np.random.shuffle(conditions) 
		# in place

	return conditions


def event_random(N,k,mult=1):
	"""
	Simulates (by Monte Carlo methods) a event-related trialset of 
	N + 1 randomized conditions (adding one to N for the jittered 
	baseline, which is always 0) of total length N+1*k, where k is 
	the number of trials/condition.
	
	It is assumed that trial and baseline events are of the same length 
	and that both are interger multilples of the TR.  

	For example, if mult is 1 (default) then each condition event takes 
	exactly one TR.  If it is 2 then that there are 2 TRs per 
	condition event, and so on.

	Note: 0 (or null) conditions have a special meaning in the fitRL 
	functions.

	Returns a list of the conditions; '0' always indicates baseline,
	the terminal state.
	"""

	## Create N conditions, randomize their order
	conditions = []
	[conditions.extend([int(cond)]*k) for cond in range(0,N+1)]
	np.random.shuffle(conditions)
		# shuffle is inplace, ysy.
	
	if mult == 1:
		return conditions
	else:
		conditions_mult = []
		[conditions_mult.extend([c]*int(mult)) for c in conditions]
		return conditions_mult

