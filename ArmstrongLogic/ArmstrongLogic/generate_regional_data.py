import pandas as pd
import numpy as np
import os

def manifest_colony_data():
    nodes = {
        "tonys_pizza_pos_data.csv": {"base_sales": 3500, "leak_pct": (0.08, 0.18)},
        "jimmys_burgers_pos_data.csv": {"base_sales": 2800, "leak_pct": (0.12, 0.22)}
    }

    for file_name, config in nodes.items():
        print(f"⚡ MANIFESTING NODE DATA: {file_name}...")
        data = []
        for d in range(365):
            sales = np.random.uniform(config['base_sales'] * 0.7, config['base_sales'] * 1.3)
            # Simulate human management entropy
            leak = sales * np.random.uniform(*config['leak_pct'])
            data.append({'leak_amount': round(leak, 2), 'daily_sales': round(sales, 2)})
        
        pd.DataFrame(data).to_csv(file_name, index=False)
    
    print("✅ REGIONAL DATA BOUND. COLONY NODES SYNCHRONIZED.")

if __name__ == "__main__":
    manifest_colony_data()
