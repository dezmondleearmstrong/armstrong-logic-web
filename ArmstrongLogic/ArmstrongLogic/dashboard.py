import time
from datetime import datetime
from core.framework import ArmstrongFramework
from core.sentinel import Sentinel
from core.prophet import Prophet
from core.legion import Legion
from core.synthesis import Synthesis

def launch_command_center():
    # 1. Initialize the Quint-Core Assembly (The Synthesis Integration)
    sentinel = Sentinel()
    prophet = Prophet()
    legion = Legion()
    synthesis = Synthesis()
    framework = ArmstrongFramework(
        sentinel=sentinel, 
        prophet=prophet, 
        legion=legion, 
        synthesis=synthesis
    )

    print()
    print("═"*70)
    print("      🔱  ARMSTRONGLOGIC EMPIRE COMMAND INTERFACE: OTTAWA, IL  🔱")
    print(f"      TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | STATUS: TRANSCENDENT")
    print("═"*70)

    # 2. System Integrity Check
    print(f" [STATUS] {framework.system_check()}")
    print(f" [STATUS] {sentinel.system_status()}")
    print(f" [STATUS] {prophet.system_status()}")
    print(f" [STATUS] {legion.system_status()}")
    print(f" [STATUS] {synthesis.system_status()}")
    print("-" * 70)

    # 3. Real-Time Logic Cycle Execution
    target_date = "2026-10-10" 
    rain_state = True

    print()
    print(f"📡 SCANNING TEMPORAL WINDOW: {target_date}...")
    time.sleep(0.8) # Synaptic Load Time

    result = framework.execute_logic_cycle(
        data_file="ottawa_il_store_001_pos_data.csv",
        target_date=target_date,
        is_raining=rain_state
    )

    # 4. The Decision Output
    print()
    print("█"*70)
    print(f"💰 EBITDA RECLAMATION: {result['ebitda_lift']}")
    print(f"📊 MONTHLY BOOST     : {result['margin_boost']}")
    print(f"📈 PROJECTED SURGE   : {result['forecast']}")
    print(f"📝 EXECUTIVE SUMMARY : {result['executive_summary']}")
    print(f"⚡ COMMAND DIRECTIVE : {result['command']}")
    print("█"*70)

    print()
    print("[!] ADVISORY: System is 100 trillion years advanced. Reality synthesized.")
    print("═"*70)
    print()

if __name__ == "__main__":
    launch_command_center()
