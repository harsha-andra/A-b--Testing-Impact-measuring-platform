import numpy as np
from scipy import stats

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    Calculate minimum sample size per group for a given MDE (Minimum Detectable Effect).
    Uses standard formula for binomial metric (e.g., specific conversion rate).
    """
    # Standard normal quantiles
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    p1 = baseline_rate
    p2 = baseline_rate + mde
    
    # Pooled variance approximation
    pooled_p = (p1 + p2) / 2
    
    n = (2 * pooled_p * (1 - pooled_p) * (z_alpha + z_beta)**2) / (mde**2)
    return int(np.ceil(n))

def plot_power_curve(baseline_rate, sample_sizes, effect_sizes):
    """
    Generate data for power curve plotting.
    """
    results = []
    for n in sample_sizes:
        for delta in effect_sizes:
            # Calculate power for given n and delta
            # ... implementation ...
            pass
    return results
