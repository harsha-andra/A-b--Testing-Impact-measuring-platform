import pandas as pd
from .statistical_tests import perform_chi_squared

def detect_simpsons_paradox(df, segment_col='device', metric='converted'):
    """
    Check if the direction of the effect reverses when looking at subgroups vs aggregate.
    """
    # Aggregate effect
    _, p_agg = perform_chi_squared(df, metric)
    agg_lift = df[df['group']=='Treatment'][metric].mean() - df[df['group']=='Control'][metric].mean()
    
    # Subgroup effects
    subgroup_results = {}
    adjust_needed = False
    
    for segment in df[segment_col].unique():
        sub_df = df[df[segment_col] == segment]
        try:
           _, p_sub = perform_chi_squared(sub_df, metric)
           sub_lift = sub_df[sub_df['group']=='Treatment'][metric].mean() - sub_df[sub_df['group']=='Control'][metric].mean()
           
           # Check for sign flip
           if np.sign(agg_lift) != np.sign(sub_lift) and abs(sub_lift) > 0.001:
               adjust_needed = True
               
           subgroup_results[segment] = {
               'p_value': p_sub,
               'lift': sub_lift
           }
        except:
            pass
            
    return adjust_needed, agg_lift, subgroup_results
