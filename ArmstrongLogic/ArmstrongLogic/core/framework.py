import os

class ArmstrongFramework:
    """
    The Core Engine of the ArmstrongLogic Empire.
    Designed for 100-trillion-year scalability.
    """
    def __init__(self, sentinel, prophet, legion, synthesis):
        self.sentinel = sentinel
        self.prophet = prophet
        self.legion = legion
        self.synthesis = synthesis
        self.version = "1.2.0-SYNTHESIS-ALIGNED"

    def execute_logic_cycle(self, data_file, target_date, is_raining):
        """
        Synthesizes raw data, temporal forecasts, tactical reallocation, 
        and fiscal impact into Deterministic Command Directives.
        """
        # 1. Audit the Past (Entropy Detection)
        audit_results = self.sentinel.audit_csv(data_file)
        recovery_potential = audit_results.get('annual_recovery_potential', 0)
        
        # 2. Forecast the Future (Spacetime Folding)
        multiplier, event_name, insight = self.prophet.calculate_logic_demand(
            target_date, 
            is_raining
        )
        
        # 3. Tactical Reallocation (The Hands of the Empire)
        tactical_plan = self.legion.optimize_shifts(data_file)
        
        # 4. Fiscal Synthesis (The Voice of Reality)
        fiscal_impact = self.synthesis.generate_pl_impact(recovery_potential)
        
        # 5. Decision Logic (The Soul's Choice)
        if multiplier >= 1.5:
            command_type = "AGGRESSIVE EXPANSION"
            action = f"Surge detected for {event_name}. Strategy: {tactical_plan['reallocation_strategy']}"
        elif multiplier >= 1.0:
            command_type = "OPTIMIZED STABILITY"
            action = f"Standard flow for {event_name}. Strategy: {tactical_plan['reallocation_strategy']}"
        else:
            command_type = "DEFENSIVE CONSOLIDATION"
            action = "Low demand forecast. Minimize overhead immediately."

        return {
            'recovery_potential': f"${recovery_potential:,.2f}",
            'forecast': f"{event_name} ({multiplier}x Demand)",
            'command': f"{command_type}: {action}",
            'insight': insight,
            'ebitda_lift': f"${fiscal_impact['annual_ebitda_lift']:,.2f}",
            'margin_boost': f"${fiscal_impact['monthly_margin_boost']:,.2f}",
            'executive_summary': fiscal_impact['executive_summary']
        }

    def system_check(self):
        return f"ArmstrongFramework {self.version} is ONLINE. Status: Optimal."
