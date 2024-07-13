import pandas as pd
import numpy as np
from math import sqrt
import pickle
import requests
from pandas import json_normalize
import json
import time
from datetime import date
from datetime import datetime
import datetime

# Define a function to safely calculate the ratio
def calculate_ratio(s):
    try:
        parts = s.split('-')
        if len(parts) == 2 and parts[0] and parts[1]:
            numerator = int(parts[0])
            denominator = int(parts[1])
            if denominator != 0:
                return numerator / denominator
            else:
                return float('inf')  # or use 1e-5 or np.nan
        else:
            return np.nan
    except ValueError:
        return np.nan

def calculate_ratio_opposite(s):
    try:
        parts = s.split('-')
        if len(parts) == 2 and parts[0] and parts[1]:
            numerator = int(parts[0])
            denominator = int(parts[1])
            if numerator != 0:
                return denominator / numerator
            else:
                return float('inf')  # or use 1e-5 or np.nan
        else:
            return np.nan
    except ValueError:
        return np.nan