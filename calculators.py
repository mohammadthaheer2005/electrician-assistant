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
    Calculates Full Load Amps for a motor.
    """
    watts = hp * 746
    if phase == 1:
        amps = watts / (voltage * eff * pf)
    elif phase == 3:
        amps = watts / (math.sqrt(3) * voltage * eff * pf)
    else:
        return None
    
    # Add safety factor 25% for starting current / breaker sizing
    breaker_size = amps * 1.25
    return round(amps, 2), round(breaker_size, 2)

def recommend_wire_size(current_amps: float):
    """
    Recommends minimum wire size in mm2 based on current.
    """
    for size, max_amps in sorted(WIRE_AMPACITY.items()):
        if max_amps >= (current_amps * 1.25): # 125% safety margin
            return size
    return "> 35.0 (Consult Code)"

def calculate_voltage_drop(current: float, distance_meters: float, wire_gauge_mm2: float, voltage: float = 230.0, phase: int = 1):
    """
    Calculates voltage drop for Copper wiring.
    Resistance of Copper approx 0.0175 ohm*mm2/m
    """
    if phase == 1:
        # 2-wire return path
        vd = (2 * 0.0175 * current * distance_meters) / wire_gauge_mm2
    else:
        # 3-phase
        vd = (1.732 * 0.0175 * current * distance_meters) / wire_gauge_mm2
        
    end_voltage = voltage - vd
    percent_drop = (vd / voltage) * 100
    
    safety_status = "Safe" if percent_drop <= 5.0 else "Unsafe (Too High)"
    
    return round(vd, 2), round(end_voltage, 2), round(percent_drop, 2), safety_status

