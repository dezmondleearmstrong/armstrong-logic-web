import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_empire_data():
    print("⚡ GENERATING ARCHITECTURAL DATA FOR OTTAWA, IL...")
    
    # 1. Setup Timeframe (Last 365 Days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    
    for current_date in date_range:
        # 2. Logic: Define Base Sales (Simulating a mid-market restaurant)
        base_sales = np.random.uniform(2000, 5000)
        
        # 3. Inject Entropy (Inefficient Labor)
        # Humans usually over-schedule labor by 10-15% during slow times
        labor_cost = base_sales * np.random.uniform(0.30, 0.45) 
        
        # 4. Calculate the Leak (The "Entropy" ArmstrongLogic captures)
        # Target labor is 25%, anything above that is a leak
        target_labor = base_sales * 0.25
        leak_amount = max(0, labor_cost - target_labor)
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'daily_sales': round(base_sales, 2),
            'actual_labor': round(labor_cost, 2),
            'target_labor': round(target_labor, 2),
            'leak_amount': round(leak_amount, 2)
        })

    # 5. Manifest the CSV
    df = pd.DataFrame(data)
    file_path = "ottawa_il_store_001_pos_data.csv"
    df.to_csv(file_path, index=False)
    
    print(f"✅ DATA MANIFESTED: {file_path}")
    print(f"📊 TOTAL ANNUAL LEAK DETECTED: ${df['leak_amount'].sum():,.2f}")

if __name__ == "__main__":
    generate_empire_data()
