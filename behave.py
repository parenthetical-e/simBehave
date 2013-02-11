""" Uses trials and acc to simulate a behavioral experiment"""
from simBehave.acc import random as randomacc, random_learn, learn
from simBehave.trials import event_random as event_randomtrial
from simBehave.trials import random as randomtrial
from simBehave.misc import process_prng


def random(N, k, event=True, prng=None):
    """
    Returns a trialset matching N,k along with matching accuracy and
    probability lists. If event is True event_random is used in place of 
    random to create the trialset.    
    """
    from copy import deepcopy

    prng = process_prng(prng)
    
    if event:
        trialset, prng = event_randomtrial(N, k, 1, prng)
    else:
        trialset, prng = randomtrial(N, k, prng)
    
    N_c = deepcopy(N)
    if event: 
        N_c += 1
    
    acc = [0, ] * (N_c*k)
    p = [0, ] * (N_c*k)

    names = list(set(trialset))
    for n in names:
        ## Skip null trials
        if (n == 0) | (n == '0'):
            continue

        ## How many trials/condition?
        acc_n = []
        p_n = []
        acc_n, p_n, prng = randomacc(k, 1/N, prng)
        
        for ii, t in enumerate(trialset):
            if t == n:
                acc[ii] = acc_n.pop(0)
                p[ii] = p_n.pop(0)

    return trialset, acc, p, prng


def learn(N, k, loc, event=True, prng=None):
    """
    Returns a trialset matching N,k along with matching accuracy and
    probability lists. If event is True event_random is used in place of 
    random to create the trialset.
    """
    from copy import deepcopy
    
    prng = process_prng(prng)
    
    ## For each condition name (n),
    ## create acc_n,p_n then map those
    ## into acc,p for each matching trial (t)
    ## in the trialset
    if event:
        trialset, prng = event_randomtrial(N, k, 1, prng)
    else:
        trialset, prng = randomtrial(N, k, prng)
    
    N_c = deepcopy(N)
    if event: 
        N_c += 1
    
    acc = [0, ] * (N_c*k)
    p = [0, ] * (N_c*k)

    names = list(set(trialset))
    for n in names:
        ## Skip null trials
        if (n is 0) | (n is '0'):
            continue

        ## How many trials/condition?
        acc_n = []
        p_n = []
        acc_n, p_n, prng = random_learn(k, 1/N, loc, prng)
        for ii, t in enumerate(trialset):
            if t == n:
                acc[ii] = acc_n.pop(0)
                p[ii] = p_n.pop(0)

    return trialset, acc, p, prng


def some_learn(N, k, N_learn, loc, event=True, rand_learn=True, prng=None):
    """
    Creates 'uneven' acc, and p value distributions for k trials in 
    N conditions in the returned trialset where N_learn is the number 
    of conditions that show learning (via sim_acc_learn()).  
    
    N minus N_learn condtions simulated data will be governed instead 
    by sim_acc_rand. If event is True an event-related trialset is 
    created.
    """
    from copy import deepcopy

    prng = process_prng(prng)    
    if N == N_learn:
        raise ValueError('N_learn must be less than N.')
    if N_learn <= 0:
        raise ValueError('N_learn must be 1 or greater.')

    if event:
        trialset, prng = event_randomtrial(N, k, mult=1, prng=prng)
    else:
        trialset, prng = randomtrial(N, k, prng)

    N_c = deepcopy(N)
    if event:
        N_c += 1
    
    acc = [0, ] * (N_c*k)
    p = [0, ] * (N_c*k)

    names = list(set(trialset))
    for ii,n in enumerate(names):
        ## Skip null trials
        if (n == 0) | (n == '0'):
            continue

        ## How many trials/condition?
        acc_n = []
        p_n = []

        ## How many trials/condition?
        if ii <= N_learn: 
            print('Learning in iteration {0}.'.format(ii))
            if rand_learn:
                acc_n, p_n, prng = random_learn(k, 1./N, loc, prng)
            else:
                acc_n, p_n, prng = learn(k, loc, prng)
        else:
            acc_n, p_n, prng = randomacc(k,1./N)

        for jj,t in enumerate(trialset):
            if t == n:
                acc[jj] = acc_n.pop(0)
                p[jj] = p_n.pop(0)

    return trialset, acc, p, prng
