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
