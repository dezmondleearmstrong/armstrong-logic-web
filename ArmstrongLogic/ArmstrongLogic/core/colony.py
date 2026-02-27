import os
import pandas as pd
from core.framework import ArmstrongFramework
from core.sentinel import Sentinel
from core.prophet import Prophet
from core.legion import Legion
from core.synthesis import Synthesis

class Colony:
    """
    The Hive Mind of ArmstrongLogic.
    Aggregates multiple store nodes into a unified Empire P&L.
    """
    def __init__(self):
        self.nodes = []
        self.sentinel = Sentinel()
        self.prophet = Prophet()
        self.legion = Legion()
        self.synthesis = Synthesis()
        self.framework = ArmstrongFramework(
            sentinel=self.sentinel, 
            prophet=self.prophet,
            legion=self.legion,
            synthesis=self.synthesis
        )

    def register_node(self, store_id, data_file):
        """Adds a new operational cell to the Empire."""
        self.nodes.append({'id': store_id, 'data': data_file})
        print(f"📡 [COLONY] Node Registered: {store_id} | Path: {data_file}")

    def execute_empire_cycle(self, target_date, is_raining):
        print()
        print("⚡" * 35)
        print(f"🔱  EXECUTING EMPIRE-WIDE LOGIC CYCLE: {target_date}  🔱")
        print("⚡" * 35)
        
        empire_results = []
        for node in self.nodes:
            result = self.framework.execute_logic_cycle(
                data_file=node['data'],
                target_date=target_date,
                is_raining=is_raining
            )
            result['store_id'] = node['id']
            empire_results.append(result)
            
        return empire_results
