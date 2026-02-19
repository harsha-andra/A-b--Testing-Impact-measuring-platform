import pandas as pd
from sklearn.linear_model import LogisticRegression

def propensity_score_matching(df, covariates=['country', 'device'], treatment='group', outcome='converted'):
    """
    Perform PSM to adjust for confounding variables.
    """
    df_encoded = pd.get_dummies(df, columns=covariates, drop_first=True)
    
    # Logistic Regression for Propensity Scores
    treatment_col = (df[treatment] == 'Treatment').astype(int)
    features = [c for c in df_encoded.columns if c not in [treatment, outcome, 'user_id', 'date', 'revenue']]
    
    ps_model = LogisticRegression(solver='liblinear')
    ps_model.fit(df_encoded[features], treatment_col)
    
    df['propensity_score'] = ps_model.predict_proba(df_encoded[features])[:, 1]
    
    # Matching (Simple nearest neighbor within caliper)
    # This is a simplified implementation for demonstration
    control = df[df[treatment] == 'Control']
    treated = df[df[treatment] == 'Treatment']
    
    matched_control = []
    
    # For each treated unit, find closest control unit
    # (Note: In production, use specialized libraries like causalinference or PsmPy)
    
    return df
