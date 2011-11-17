""" Uses trials and acc to simulate a behavioral experiment"""
import simBehave

def all_learn(N,k,loc,event=True,rand_learn=True):
	"""
	Returns a trialset matching N,k along with accuracy and probability 
	lists to match (generated w/ behave.learn()).  If event is True 	
	event_random is used in place of random to create the trialset.
	"""
	## For each condition name (n),
	## create acc_n,p_n then map those
	## into acc,p for each matching trial (t)
	## in the trialset	
	from copy import deepcopy

	if event:
		trialset = simBehave.trials.event_random(N,k,mult=1)
	else:
		trialset = simBehave.trials.random(N,k)
	
	N_c = deepcopy(N)
	if event: N_c += 1
	acc = [0]*(N_c*k)
	p = [0]*(N_c*k)

	names = list(set(trialset))
	for n in names:
		## Skip null trials
		if (n is 0) | (n is '0'):
			print('n was 0, skipping.')
			continue

		## How many trials/condition?
		acc_n = []; p_n = []
		if rand_learn:
			## random_learn(N,p,loc):
			acc_n, p_n = simBehave.acc.random_learn(k,1/N,loc)
		else:
			acc_n, p_n = simBehave.acc.learn(k,loc)
		
		for ii,t in enumerate(trialset):
			if t == n:
				acc[ii] = acc_n.pop(0)
				p[ii] = p_n.pop(0)

	return trialset, acc, p


def some_learn(N,k,N_learn,loc,event=True,rand_learn=True):
	"""
	Creates 'uneven' acc, and p value distributions for k trials in 
	N conditions in the returned trialset where N_learn is the number 
	of conditions that show learning (via sim_acc_learn()).  
	
	N minus N_learn condtions simulated data will be governed instead 
	by sim_acc_rand. If event is True an event-related trialset is 
	created.
	"""
	from copy import deepcopy

	if N == N_learn: raise ValueError, 'N_learn must be less than N.'
	if N_learn <= 0: raise ValueError, 'N_learn must be 1 or greater.'

	if event:
		trialset = simBehave.trials.event_random(N,k,mult=1)
	else:
		trialset = simBehave.trials.random(N,k)

	N_c = deepcopy(N)
	if event: N_c += 1
	acc = [0]*(N_c*k)
	p = [0]*(N_c*k)

	names = list(set(trialset))
	for ii,n in enumerate(names):
		## Skip null trials
		if (n is 0) | (n is '0'):
			print('n was 0, skipping.')
			continue

		## How many trials/condition?
		acc_n = []; p_n = []

		## How many trials/condition?
		if ii <= N_learn: 
			print('Learning in iteration {0}.'.format(ii))
			if rand_learn:
				acc_n, p_n = simBehave.acc.random_learn(k,1./N,loc)
			else:
				acc_n, p_n = simBehave.acc.learn(k,loc)
		else:
			acc_n, p_n = simBehave.acc.random(k,1./N)

		for jj,t in enumerate(trialset):
			if t == n:
				acc[jj] = acc_n.pop(0)
				p[jj] = p_n.pop(0)

	return trialset, acc, p
