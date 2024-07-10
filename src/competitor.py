from dataclasses import dataclass
from typing import Optional
import pandas as pd
import numpy as np


@dataclass
class Competitor:
    id: str
    name: str
    results: pd.DataFrame
    weighted_results: pd.Series
    dnf_rate: int
    generated_results: Optional[np.array] = None
