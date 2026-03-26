def get_mermaid_diagram(circuit_type: str, lang: str = "English") -> str:
    """
    Returns Mermaid.js code for various electrical diagrams.
    Labels are translated based on the chosen language.
    """
    
    # Simple Translation Dictionary for Diagram Labels
    trans = {
        "Phase": {"English": "Phase (L)", "Telugu (తెలుగు)": "దశ (L)", "Hindi (हिंदी)": "फेज (L)", "Tamil (தமிழ்)": "கட்டம் (L)", "Malayalam (മലയാളం)": "ഫേസ് (L)"},
        "Neutral": {"English": "Neutral (N)", "Telugu (తెలుగు)": "న్యూట్రల్ (N)", "Hindi (हिंदी)": "न्यूट्रल (N)", "Tamil (தமிழ்)": "நடுநிலை (N)", "Malayalam (മലയാളം)": "ന്യൂട്രൽ (N)"},
        "Switch": {"English": "Switch", "Telugu (తెలుగు)": "స్విచ్", "Hindi (हिंदी)": "स्विच", "Tamil (தமிழ்)": "சுவிட்ச்", "Malayalam (മലയാളം)": "സ്വിച്ച്"},
        "Load/Bulb": {"English": "Load/Bulb", "Telugu (తెలుగు)": "లోడ్ / బల్బ్", "Hindi (हिंदी)": "लोड / बल्ब", "Tamil (தமிழ்)": "பளு / பல்பு", "Malayalam (മലയാളം)": "ലോഡ് / ബൾബ്"},
        "Capacitor": {"English": "Capacitor", "Telugu (తెలుగు)": "కెపాసిటర్", "Hindi (हिंदी)": "कैपेसिटर", "Tamil (தமிழ்)": "மின்தேக்கி", "Malayalam (മലയാളం)": "കപ്പാസിറ്റർ"},
        "Fan": {"English": "Fan Motor", "Telugu (తెలుగు)": "ఫ్యాన్ మోటార్", "Hindi (हिंदी)": "पंखे की मोटर", "Tamil (தமிழ்)": "மின்விசிறி", "Malayalam (മലയാളం)": "ഫാൻ മോട്ടോർ"},
        "Regulator": {"English": "Regulator", "Telugu (తెలుగు)": "రెగ్యులేటర్", "Hindi (हिंदी)": "रेगुलेटर", "Tamil (தமிழ்)": "ரெகுலேட்டர்", "Malayalam (മലയാളం)": "റെഗുലേറ്റർ"}
    }

    def t(word):
        return trans.get(word, {}).get(lang, word)

    if circuit_type == "1-Way Switch":
        return f"""
        graph LR
            P["{t('Phase')}"] --> Sw["{t('Switch')}"]
            Sw --> L["{t('Load/Bulb')}"]
            L --> N["{t('Neutral')}"]
            style Sw fill:#f96,stroke:#333
            style L fill:#ff9,stroke:#333
        """

    elif circuit_type == "Ceiling Fan with Regulator":
        return f"""
        graph TD
            P["{t('Phase')}"] --> Sw["{t('Switch')}"]
            Sw --> Reg["{t('Regulator')}"]
            Reg --> Fan["{t('Fan')}"]
            Fan --> N["{t('Neutral')}"]
            
            subgraph Connection
            Fan --- Cap["{t('Capacitor')}"]
            end
            
            style Reg fill:#aaf,stroke:#333
            style Cap fill:#9f9,stroke:#333
        """

    elif circuit_type == "2-Way Switch (Staircase)":
        return f"""
        graph LR
            P["{t('Phase')}"] --> Sw1["{t('Switch')} 1"]
            Sw1 -- Traveller 1 --- Sw2["{t('Switch')} 2"]
            Sw1 -- Traveller 2 --- Sw2
            Sw2 --> L["{t('Load/Bulb')}"]
            L --> N["{t('Neutral')}"]
            style Sw1 fill:#f96
            style Sw2 fill:#f96
        """

    elif circuit_type == "Motor Direct Online (DOL)":
        return f"""
        graph TD
            MCB["3-Ph MCB"] --> Contactor["Power Contactor"]
            Contactor --> OLR["Overload Relay"]
            OLR --> Motor["3-Ph Motor"]
            
            subgraph Control_Circuit
            C_Phase["Control Phase"] --> Stop["Stop Push (NC)"]
            Stop --> Start["Start Push (NO)"]
            Start --> Coil["Contactor Coil (A1)"]
            Coil --> C_Neutral["Neutral (A2)"]
            end
        """

    elif circuit_type == "Star-Delta Motor Starter":
        return f"""
        graph TD
            MCCB["3-Ph Main MCCB"] --> MC["Main Contactor"]
            MC --> OLR["Overload Relay"]
            OLR --> Motor["3-Ph Motor (6 Terminals)"]
            
            subgraph Star_Delta_Group
            SC["Star Contactor"] --- DC["Delta Contactor"]
            end
            
            MC --- DC
            DC --- Motor
            SC --- Motor
            
            style SC fill:#aaf
            style DC fill:#f96
            style MC fill:#9f9
        """
