"""
Electrical Calculators File
Provides standard logical calculations for Motor Load, Voltage Drop, and Wire Sizing.
"""
import math

# Reference dictionary for approximate Ampacity of copper wires (mm2) at 30°C
WIRE_AMPACITY = {
    1.0: 11,
    1.5: 15,
    2.5: 20,
    4.0: 27,
    6.0: 34,
    10.0: 46,
    16.0: 62,
    25.0: 80,
    35.0: 99
}

def calculate_motor_load(hp: float, phase: int = 1, voltage: float = 230.0, eff: float = 0.85, pf: float = 0.85):
    """
    Calculates Full Load Amps (FLA) for a motor.
    """
    watts = hp * 746
    if phase == 1:
        amps = watts / (voltage * eff * pf)
    elif phase == 3:
        amps = watts / (math.sqrt(3) * voltage * eff * pf)
    else:
        return 0, 0
    
    # Starting current (Approx 1.25x for Breaker, 6x for Peak)
    breaker_size = amps * 1.5
    return round(amps, 2), round(breaker_size, 2)

def get_starter_recommendation(hp: float):
    """
    Suggests the best motor starter based on industrial standards.
    """
    if hp < 5.0:
        return "DOL Starter (Direct Online)", "Standard protection for small motors."
    elif 5.0 <= hp <= 20.0:
        return "Star-Delta Starter", "Reduced voltage starting to protect windings."
    else:
        return "Soft Starter / VFD", "Advanced torque control and energy saving."

def calculate_efficiency_pf(volts: float, amps: float, real_power_kw: float, phase: int = 1):
    """
    Calculates Efficiency and Power Factor.
    """
    apparent_power_kva = (volts * amps) / 1000 if phase == 1 else (math.sqrt(3) * volts * amps) / 1000
    if apparent_power_kva == 0: return 0, 0
    
    pf = real_power_kw / apparent_power_kva
    input_power_kw = real_power_kw # Simplification: assume measured power is input
    # In practice: Efficiency = Output Power / Input Power
    # For this tool: we assume user provides Output (HP converted) and Input KW
    
    return round(pf, 2), round(apparent_power_kva, 2)

def calculate_voltage_drop(current: float, dist: float, wire_mm2: float, voltage: float = 230.0, phase: int = 1, material: str = "Copper"):
    """
    Advanced Voltage Drop for Copper and Aluminum.
    Resistivity (rho): Cu ~ 0.0175, Al ~ 0.028
    """
    rho = 0.0175 if material == "Copper" else 0.028
    
    if phase == 1:
        vd = (2 * rho * current * dist) / wire_mm2
    else:
        vd = (math.sqrt(3) * rho * current * dist) / wire_mm2
        
    percent_drop = (vd / voltage) * 100
    target_wire = wire_mm2
    
    # Suggest better wire if drop > 3%
    if percent_drop > 3.0:
        for size in [1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0]:
            if size > wire_mm2:
                new_vd = (2 * rho * current * dist) / size if phase == 1 else (math.sqrt(3) * rho * current * dist) / size
                if (new_vd / voltage) * 100 <= 3.0:
                    target_wire = size
                    break
    
    sf = "Safe" if percent_drop <= 3.0 else "Caution: High Drop"
    return round(vd, 2), round(percent_drop, 2), sf, target_wire

