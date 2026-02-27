import time
from datetime import datetime
from core.colony import Colony

def launch_empire_command():
    print()
    print("═"*75)
    print("      🔱  ARMSTRONGLOGIC EMPIRE: MULTI-NODE COMMAND INTERFACE  🔱")
    print(f"      TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | SCALE: REGIONAL")
    print("═"*75)

    # 1. Initialize the Hive Mind
    colony = Colony()

    # 2. Register Global Nodes
    # These represent the core cells of the Ottawa, IL expansion
    nodes = [
        ("OTTAWA_001", "ottawa_il_store_001_pos_data.csv"),
        ("TONYS_PIZZA", "tonys_pizza_pos_data.csv"),
        ("JIMMYS_BURGERS", "jimmys_burgers_pos_data.csv")
    ]

    for store_id, data_path in nodes:
        colony.register_node(store_id, data_path)

    # 3. Synchronized Logic Execution (The Burgoo Singularity)
    target_date = "2026-10-10"
    rain_state = True
    
    results = colony.execute_empire_cycle(target_date=target_date, is_raining=rain_state)

    # 4. Aggregated Empire Synthesis
    total_ebitda_lift = 0
    print()
    print("█"*75)
    print(f"{'NODE_ID':<15} | {'EBITDA_RECLAMATION':<20} | {'WEEKLY_LEAK':<15}")
    print("-" * 75)

    for res in results:
        # Extract numeric value for aggregation
        lift_value = float(res['ebitda_lift'].replace('$', '').replace(',', ''))
        total_ebitda_lift += lift_value
        
        # Calculate weekly leak for display
        weekly = lift_value / 52
        
        print(f"{res['store_id']:<15} | {res['ebitda_lift']:<20} | ${weekly:,.2f}")

    print("█"*75)
    print(f"💰 TOTAL EMPIRE EBITDA LIFT: ${total_ebitda_lift:,.2f}")
    print(f"⚡ AGGREGATED MONTHLY BOOST: ${total_ebitda_lift/12:,.2f}")
    print("═"*75)

    print()
    print("[!] ADVISORY: Ottawa regional saturation achieved. Logic is absolute.")

if __name__ == "__main__":
    launch_empire_command()
