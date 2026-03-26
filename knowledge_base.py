"""
Knowledge Base for standard motor winding data.
This acts as a lookup table/RAG augmentation for the AI.
"""

# --- INDUSTRIAL FAULT DATA ---
FAULT_SYMPTOMS = {
    "motor_humming_no_rotation": {
        "possible_faults": ["Faulty Capacitor", "Bearing Jam", "Single Phasing (if 3-ph)", "Winding Short"],
        "solution": "1. Check capacitor with multimeter. 2. Verify all phases present. 3. Check for mechanical jam in fan/pump."
    },
    "motor_overheating": {
        "possible_faults": ["Overload", "Low Voltage", "Poor Ventilation", "Bearing Friction"],
        "solution": "1. Measure current (Amps) vs Nameplate. 2. Increase wire size if voltage drop is high. 3. Clean cooling fins."
    },
    "sparking_at_brushes": {
        "possible_faults": ["Worn Carbon Brushes", "Dirty Commutator", "Overload"],
        "solution": "1. Replace brushes if < 5mm. 2. Clean commutator with fine sandpaper. 3. Check load."
    },
    "circuit_breaker_tripping": {
        "possible_faults": ["Short Circuit", "Earth Fault", "Overload", "Faulty Breaker"],
        "solution": "1. Check insulation resistance (Megger). 2. Verify load hasn't increased. 3. Replace breaker if it trips without load."
    }
}

# --- ELECTRICIAN'S ACADEMY (VIVA PREP) ---
TECHNICAL_NOTES = {
    "Star-Delta": "Star-Delta starting reduces the starting current to 1/3rd of the DOL current. Used for motors > 5HP to protect the grid and windings.",
    "SWG (Standard Wire Gauge)": "A higher SWG number means a thinner wire. 18 SWG is thicker than 22 SWG.",
    "Power Factor": "The ratio of Real Power (kW) to Apparent Power (kVA). Ideal is 1.0, typical industrial is 0.85.",
    "Winding Basics": "Running winding (Main) has thicker wire and more turns to handle constant load. Starting winding (Aux) has thinner wire and is used for torque."
}

WINDING_DATA = {
    "fans": {
        "ceiling_fan_14_pole": {
            "starting_coil_turns": 360,
            "running_coil_turns": 380,
            "starting_wire_swg": 36,
            "running_wire_swg": 36,
            "capacitor": "2.5 uF"
        },
        "ceiling_fan_12_pole": {
            "starting_coil_turns": 420,
            "running_coil_turns": 450,
            "starting_wire_swg": 35,
            "running_wire_swg": 35,
            "capacitor": "2.5 uF"
        }
    },
    "mixers": {
        "mixer_grinder_500W": {
            "field_coil_turns": 400,
            "armature_turns": "Varies by slots, roughly 60 turns per slot",
            "wire_swg": 26,
            "troubleshooting": ["Check carbon brushes for wear", "Test continuity of armature", "Check for bearing jam"]
        }
    },
    "motors": {
        "water_pump_1HP_single_phase": {
            "running_turns": "40, 42, 44 (graded)",
            "starting_turns": "60, 62",
            "running_wire_swg": "20 / 21", 
            "starting_wire_swg": "22 / 23",
            "capacitor": "20uF / 25uF",
            "turns_running": "60, 60, 60, 60",
            "turns_starting": "90, 90"
        },
        "water_pump_1.5HP_single_phase": {
            "running_wire_swg": "19 / 20",
            "starting_wire_swg": "21 / 22",
            "capacitor": "36uF",
            "turns_running": "50, 50, 50, 50",
            "turns_starting": "80, 80"
        },
        "water_pump_2HP_single_phase": {
            "running_wire_swg": "18 / 19",
            "starting_wire_swg": "20 / 21",
            "capacitor": "50uF / 60uF",
            "turns_running": "45, 45, 45, 45",
            "turns_starting": "75, 75"
        },
        "water_pump_3HP_single_phase": {
            "running_wire_swg": "16 / 17",
            "starting_wire_swg": "19 / 20",
            "capacitor": "72uF / 100uF",
            "turns_running": "35, 35, 35",
            "turns_starting": "60, 60"
        }
    }
}
