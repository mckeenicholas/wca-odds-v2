import numpy as np
from formats import event_formats


def multi_simulation_thread(results, dnf_rate, event, count):
    """
    Perform a multi-threaded simulation of competition results.

    This function simulates competition results based on a gamma distribution,
    optionally introducing Did Not Finish (DNF) rates.

    Parameters
    ----------
    results : numpy.ndarray
        An array of historical results to derive simulation parameters.
    dnf_rate : float
        The rate of Did Not Finish (DNF) occurrences in the simulation.
    event : str
        The identifier of the event being simulated.
    count : int
        The number of simulations to perform.

    Returns
    -------
    numpy.ndarray
        An array of simulated competition results based on the specified event format.

    Notes
    -----
    The simulation uses the gamma distribution to model the variability in competition results.
    If `format` is 'a', the WCA Ao5 calculation is used.
    If `format` is 'm', the mean is taken across all attempts.
    Otherwise, the best result of the attempts is returned.

    See Also
    --------
    event_formats : A dictionary defining event-specific formats and rules.
    """
    use_dnf = True

    mean = results.mean().iloc[-1]
    stdev = results.std().iloc[-1]

    if np.isnan(stdev):
        stdev = 0.01

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
