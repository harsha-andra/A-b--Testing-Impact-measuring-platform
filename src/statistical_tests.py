import pandas as pd
import numpy as np
from scipy import stats

def perform_ttest(df, metric='revenue'):
    """Calculate t-statistic and p-value for continuous metrics"""
    control = df[df['group'] == 'Control'][metric]
    treatment = df[df['group'] == 'Treatment'][metric]
    
    t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)
    return t_stat, p_val

def perform_chi_squared(df, metric='converted'):
    """Calculate Chi-square statistic and p-value for binary metrics"""
    contingency_table = pd.crosstab(df['group'], df[metric])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return chi2, p

def bootstrap_ci(df, metric='revenue', n_boot=1000, ci=0.95):
    """Calculate bootstrap confidence intervals for the difference in means"""
    control = df[df['group'] == 'Control'][metric].values
    treatment = df[df['group'] == 'Treatment'][metric].values
    
    diffs = []
    for _ in range(n_boot):
        c_sample = np.random.choice(control, len(control), replace=True)
        t_sample = np.random.choice(treatment, len(treatment), replace=True)
        diffs.append(np.mean(t_sample) - np.mean(c_sample))
        
    lower = np.percentile(diffs, (1-ci)/2 * 100)
    upper = np.percentile(diffs, (1+ci)/2 * 100)
    
    return lower, upper, np.mean(diffs)
