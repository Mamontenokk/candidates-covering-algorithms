import numpy as np
import pandas as pd
import random
import io


def generate_input(num_of_candidates, subgroups):
    if max(subgroups) > num_of_candidates:
        return False
    else:
        test = True
        while test:
            candidates = []
            for _ in range(num_of_candidates):
                candidates.append(generate_candidate(subgroups))
            test = check_candidates(np.asarray(candidates))
        return np.asarray(candidates)


def generate_candidate(subgroups):
    candidate = np.zeros(sum(subgroups))
    for index in range(len(subgroups)):
        candidate[sum(subgroups[:index])+random.choice(list(range(subgroups[index])))] = 1
    return candidate


def check_candidates(candidates):
    maximums = np.amax(candidates, axis = 0)
    if min(maximums) == 0:
        return True
    return False


def read_file(file):
	if file:
		candidates = pd.read_csv(file).to_numpy()
		return candidates