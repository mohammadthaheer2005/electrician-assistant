"""
Knowledge Base for standard motor winding data.
This acts as a lookup table/RAG augmentation for the AI.
"""

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
            "running_wire_swg": 23,
            "starting_wire_swg": 25,
            "capacitor": "10-15 uF"
        },
        "water_pump_2HP_single_phase": {
            "running_turns": "30, 32, 34",
            "starting_turns": "45, 47",
            "running_wire_swg": 21,
            "starting_wire_swg": 23,
            "capacitor": "20-25 uF"
        }
    }
}
