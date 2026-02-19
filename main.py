import os
import pandas as pd
from data.generate_data import generate_experiment_data
from src.statistical_tests import perform_ttest, perform_chi_squared
from src.simpsons_paradox import detect_simpsons_paradox

def main():
    print("🚀 Starting A/B Testing Analysis Project...")
    
    # 1. Data Generation
    data_path = 'data/experiment_data.csv'
    if not os.path.exists(data_path):
        print("Generating synthetic data...")
        df = generate_experiment_data()
        os.makedirs('data', exist_ok=True)
        df.to_csv(data_path, index=False)
    else:
        print("Loading existing data...")
        df = pd.read_csv(data_path)
        
    print(f"Loaded {len(df)} records.")
    
    # 2. Basic Analysis
    print("\n--- Overall Results ---")
    t_stat, p_rev = perform_ttest(df, 'revenue')
    chi2, p_conv = perform_chi_squared(df, 'converted')
    
    print(f"Revenue T-Test p-value: {p_rev:.5f}")
    print(f"Conversion Chi-Square p-value: {p_conv:.5f}")
    
    if p_conv < 0.05:
        print("Result: Statistically Significant Difference in Conversion!")
    else:
        print("Result: No Statistically Significant Difference.")
        
    # 3. Simpson's Paradox Check
    print("\n--- Simpson's Paradox Check ---")
    adjust_needed, agg_lift, subgroups = detect_simpsons_paradox(df, 'device')
    if adjust_needed:
        print("⚠️ Simpson's Paradox Detected! The trend reverses in subgroups.")
        # Logic to show subgroup results
    else:
        print("No Simpson's Paradox detected.")
        
    print("\n✅ Analysis Complete. Run 'python dashboard/app.py' to view the interactive dashboard.")

if __name__ == "__main__":
    main()
