from formats import event_formats
import numpy as np


# This is the actual simulation thread, it is seperate from the object
# as there are some class variables are not pickleable
def multi_simulation_thread(results, dnf_rate, event, count):
    use_dnf = True

    mean = results.mean().iloc[-1]
    stdev = results.std().iloc[-1]

    shape = (mean**2) / (stdev**2)
    scale = (stdev**2) / mean

    num_attempts = event_formats[event]["num_attempts"]
    format = event_formats[event]["default_format"]

    random_values = np.random.gamma(shape, scale, (count, num_attempts)).astype(int)

    if use_dnf:
        mask = np.random.rand(*random_values.shape)
        replace_indices = np.where(mask < dnf_rate)

        random_values[replace_indices] = np.iinfo(np.int32).max

    sorted_by_instance = np.sort(random_values, axis=1)

    if format == "a":
        trimmed = sorted_by_instance[:, 1:4]
        results = np.mean(trimmed, axis=1)
    elif format == "m":
        results = np.mean(sorted_by_instance, axis=1)
    else:
        results = sorted_by_instance[:, 0]

    return results
