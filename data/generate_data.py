import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_experiment_data(n_users=150000, start_date='2024-01-01', duration_days=45):
    np.random.seed(42)
    
    dates = [datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=x) for x in range(duration_days)]
    
    # User segments
    countries = ['US', 'UK', 'DE', 'FR', 'IN', 'CA', 'AU', 'BR', 'JP', 'KR']
    devices = ['Mobile', 'Desktop', 'Tablet']
    browsers = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Samsung Internet'] # New
    sources = ['Google Ads', 'Facebook', 'Direct', 'Email', 'Referral', 'TikTok', 'Organic Search'] # New
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'] # New
    loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum'] # New
    genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say'] # New

    
    # Pre-generate arrays for faster processing
    print(f"Generating {n_users} user profiles...")
    
    # Assign attributes randomly (vectorized where possible)
    user_ids = np.random.randint(1000000, 9999999, n_users)
    country_arr = np.random.choice(countries, n_users, p=[0.35, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05])
    device_arr = np.random.choice(devices, n_users, p=[0.6, 0.3, 0.1])
    browser_arr = np.random.choice(browsers, n_users, p=[0.5, 0.3, 0.1, 0.05, 0.05])
    source_arr = np.random.choice(sources, n_users, p=[0.25, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05])
    age_arr = np.random.choice(age_groups, n_users, p=[0.15, 0.3, 0.25, 0.15, 0.1, 0.05])
    loyalty_arr = np.random.choice(loyalty_tiers, n_users, p=[0.6, 0.25, 0.1, 0.05])
    gender_arr = np.random.choice(genders, n_users, p=[0.48, 0.48, 0.02, 0.02])
    
    # Assign assignment dates
    date_indices = np.random.choice(len(dates), n_users)
    date_arr = [dates[i] for i in date_indices]
    
    # Assign Groups (Simpson's Paradox Logic included)
    # Desktop users more likely to be Control but higher base conversion
    group_arr = []
    base_crs = []
    
    for device in device_arr:
        if device == 'Desktop':
            # 60% Control, 40% Treatment
            if np.random.random() < 0.6:
                group_arr.append('Control')
            else:
                group_arr.append('Treatment')
            base_crs.append(0.08)
        else:
            # 50/50 split
            if np.random.random() < 0.5:
                group_arr.append('Control')
            else:
                group_arr.append('Treatment')
            base_crs.append(0.04)
            
    group_arr = np.array(group_arr)
    base_crs = np.array(base_crs)
    
    # Calculate Uplift
    # Treatment Effect: +1.5% on Mobile, +0.2% on Desktop
    uplifts = np.zeros(n_users)
    treatment_mask = (group_arr == 'Treatment')
    mobile_mask = (device_arr == 'Mobile')
    desktop_mask = (device_arr == 'Desktop')
    
    uplifts[treatment_mask & mobile_mask] = 0.015
    uplifts[treatment_mask & desktop_mask] = 0.002
    
    # Simulate Conversion
    rand_vals = np.random.random(n_users)
    converted_arr = (rand_vals < (base_crs + uplifts)).astype(int)
    
    # Simulate Revenue
    revenue_arr = np.zeros(n_users)
    converted_indices = np.where(converted_arr == 1)[0]
    # Revenue depends on loyalty tier slightly
    for i in converted_indices:
        tier = loyalty_arr[i]
        mu = 3.0
        if tier == 'Silver': mu = 3.2
        elif tier == 'Gold': mu = 3.5
        elif tier == 'Platinum': mu = 4.0
        
        revenue_arr[i] = round(np.random.lognormal(mu, 0.5), 2)
        
    # Extra engagement metrics
    session_duration_arr = np.random.exponential(180, n_users).astype(int) # avg 3 mins
    pages_visited_arr = np.random.poisson(4, n_users)
    pages_visited_arr = np.where(pages_visited_arr < 1, 1, pages_visited_arr) # at least 1 page

    # Create DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'date': date_arr,
        'country': country_arr,
        'device': device_arr,
        'browser': browser_arr,
        'source': source_arr,
        'age_group': age_arr,
        'gender': gender_arr,
        'loyalty_tier': loyalty_arr,
        'group': group_arr,
        'converted': converted_arr,
        'revenue': revenue_arr,
        'session_duration_sec': session_duration_arr,
        'pages_visited': pages_visited_arr
    })
    
    return df

if __name__ == "__main__":
    print("Generating comprehensive synthetic experiment data...")
    df = generate_experiment_data(n_users=150000) # Increased scale
    df.to_csv('data/experiment_data.csv', index=False)
    print(f"Data generated: {len(df)} rows saved to data/experiment_data.csv")
    print("Columns:", df.columns.tolist())
