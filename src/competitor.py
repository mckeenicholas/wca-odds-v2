from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import numpy as np


@dataclass
class Competitor:
    """
    Represents a competitor in a competition.

    Attributes
    ----------
    id : str
        Identifier of the competitor.
    name : str
        Name of the competitor.
    results : pandas.DataFrame
        DataFrame containing raw results of the competitor.
    weighted_results : pandas.Series
        Series containing weighted average results of the competitor.
    dnf_rate : float
        Rate of Did Not Finish (DNF) events for the competitor.
    generated_results : Optional[np.array], optional
        Array of generated results (default is None).

    Methods
    -------
    None
    """

    id: str
    name: str
    results: pd.DataFrame
    weighted_results: pd.Series
    dnf_rate: float
    generated_results: Optional[np.array] = field(default_factory=lambda: None)
