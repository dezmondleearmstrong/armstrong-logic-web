import pandas as pd
import os

class Legion:
    """
    The Hands of ArmstrongLogic.
    Translates fiscal directives into Tactical Labor Reallocation.
    """
    def __init__(self):
        self.module_name = "LEGION_V1"

    def optimize_shifts(self, data_file):
        """
        Analyzes the top 20% of leak days to identify 
        immediate labor reallocation opportunities.
        """
        if not os.path.exists(data_file):
            return {
                'target_days': 0,
                'avg_daily_waste': 0.0,
                'reallocation_strategy': "NO DATA: MAINTAIN CURRENT STANDARDS."
            }
        
        df = pd.read_csv(data_file)
        
        # Logic: Isolate the "Entropy Zones" (Top 20% of waste days)
        threshold = df['leak_amount'].quantile(0.8)
        high_leak_days = df[df['leak_amount'] >= threshold]
        avg_leak = high_leak_days['leak_amount'].mean()
        
        return {
            'target_days': len(high_leak_days),
            'avg_daily_waste': round(avg_leak, 2),
            'reallocation_strategy': "CUT: Mid-day prep overlaps. SURGE: Peak Burgoo evening windows."
        }

    def system_status(self):
        return "LEGION: TACTICAL READY. SHIFTS CALCULATED."
