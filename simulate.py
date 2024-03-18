from competitor import competitor
from query import *
import passwords
from threading import Thread
import numpy as np
import time

def calc_results(competitor: competitor, num_results: int, num_attempts=5, use_dnf=False):
    mean = competitor.weighted_results.mean().iloc[-1]
    stdev = competitor.weighted_results.std().iloc[-1]

    shape = (mean ** 2) / (stdev ** 2)
    scale = (stdev ** 2) / mean

    random_values = np.random.gamma(shape, scale, (num_results, num_attempts)).astype(int)
    
    if use_dnf:
        mask = np.random.rand(*random_values.shape)
        replace_indices = np.where(mask < competitor.dnf_rate) 

        random_values[replace_indices] = np.iinfo(np.int32).max

    sorted_by_instance = np.sort(random_values, axis=1)
    trimmed = sorted_by_instance[:, 1:4]
    means = np.mean(trimmed, axis=1)

    competitor.generated_results = means
    
def run_simulations(names: list[str], num_simulations=100000):
    num_competitors = len(names)
    start = time.time()

    conn = connect(passwords.HOST, passwords.PSQL_USERNAME, passwords.PSQL_PASSWORD)
    competitors = extract_results(conn, names, event='555', halflife='30 days')

    threads = [Thread(target=calc_results, args=(result, num_simulations, 5, True)) for result in competitors]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    all_results = np.stack([competitor.generated_results for competitor in competitors])
    sorted_indicies = np.argsort(all_results, axis=0)

    win_indicies = sorted_indicies[0, :]
    podium_indicies = sorted_indicies[: min(num_competitors, 3), :].flat

    win_by_person = np.bincount(win_indicies, minlength=num_competitors)
    podium_by_person = np.bincount(podium_indicies, minlength=num_competitors)

    end = time.time()

    print(f"wcaid     |    win% | podium% ")
    print(f"----------+---------+----------")

    for idx, competitor in enumerate(competitors):
        print(f"{competitor.id}| {win_by_person[idx] * 100 / num_simulations:.3f}% | {podium_by_person[idx] * 100 / num_simulations:.3f}%") 

    print(f"ran {num_simulations} simulations in {end - start:.3f} seconds")