from statsmodels.stats.multitest import multipletests

def apply_corrections(p_values, method='fdr_bh'):
    """
    Apply multiple testing correction.
    methods: 'bonferroni', 'holm', 'fdr_bh' (Benjamini-Hochberg)
    """
    reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method=method)
    return reject, pvals_corrected
