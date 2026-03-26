def get_svg_diagram(circuit_type: str, lang: str = "English") -> str:
    """
    Generates high-fidelity SVG code for professional electrical schematics.
    Includes symbols for Phase, Neutral, Switch, Bulb, Motor, and Capacitor.
    """
    # Translation Dictionary for Labels
    trans = {
        "Phase": {"English": "Phase (L)", "Telugu (తెలుగు)": "దశ (L)", "Hindi (हिंदी)": "फेज (L)", "Tamil (தமிழ்)": "கட்டம் (L)", "Malayalam (മലയാളം)": "ഫేస్ (L)"},
        "Neutral": {"English": "Neutral (N)", "Telugu (తెలుగు)": "న్యూట్రల్ (N)", "Hindi (हिंदी)": "न्यूट्रल (N)", "Tamil (தமிழ்)": "நడుநிலை (N)", "Malayalam (മലയാളം)": "ന്യൂട്രൽ (N)"},
        "Switch": {"English": "Switch", "Telugu (తెలుగు)": "స్విచ్", "Hindi (हिंदी)": "स्विచ్", "Tamil (தமிழ்)": "சுவிட்ச்", "Malayalam (മലയാളം)": "സ്വിച്ച്"},
        "Load": {"English": "Bulb/Load", "Telugu (తెలుగు)": "బల్బ్", "Hindi (हिंदी)": "बल्ब", "Tamil (தமிழ்)": "பல்பு", "Malayalam (മലയാളം)": "ബൽബ്"},
        "Motor": {"English": "Motor", "Telugu (తెలుగు)": "మోటార్", "Hindi (हिंदी)": "मोटर", "Tamil (தமிழ்)": "மோட்டார்", "Malayalam (മലയാളം)": "മോട്ടോർ"},
        "Cap": {"English": "Capacitor", "Telugu (తెలుగు)": "కెపాసిటర్", "Hindi (हिंदी)": "कैपेसिटर", "Tamil (தமிழ்)": "மின்தேக்கி", "Malayalam (മലയാളം)": "കപ്പാసిറ്റർ"}
    }
    def t(word): return trans.get(word, {}).get(lang, word)

    # Styles
    styles = """
    <style>
        .wire { stroke: #333; stroke-width: 3; fill: none; }
        .phase { stroke: #d32f2f; }
        .neutral { stroke: #1976d2; }
        .node { fill: #fff; stroke: #333; stroke-width: 2; }
        .text { font-family: 'Segoe UI', Arial; font-size: 14px; fill: #333; font-weight: bold; }
        .comp-box { fill: #f5f5f5; stroke: #999; stroke-dasharray: 4; }
    </style>
    """
    
    if circuit_type == "1-Way Switch":
        return f"""
        <svg viewBox="0 0 500 250" xmlns="http://www.w3.org/2000/svg">
            {styles}
            <!-- Phase Line -->
            <path class="wire phase" d="M 50 100 L 150 100" />
            <text x="40" y="90" class="text" text-anchor="middle">{t('Phase')}</text>
            
            <!-- Switch Symbol -->
            <path class="wire" d="M 150 100 L 220 70" /> <!-- Switch Lever -->
            <circle cx="150" cy="100" r="5" class="node" />
            <circle cx="230" cy="100" r="5" class="node" />
            <text x="190" y="60" class="text" text-anchor="middle">{t('Switch')}</text>
            
            <!-- Connection to Load -->
            <path class="wire phase" d="M 230 100 L 320 100" />
            
            <!-- Bulb Symbol (Circle with X) -->
            <circle cx="350" cy="100" r="30" class="node" style="fill:#fff9c4;" />
            <path class="wire" d="M 330 80 L 370 120" />
            <path class="wire" d="M 330 120 L 370 80" />
            <text x="350" y="60" class="text" text-anchor="middle">{t('Load')}</text>
            
            <!-- Neutral Return -->
            <path class="wire neutral" d="M 380 100 L 450 100" />
            <text x="450" y="90" class="text" text-anchor="middle">{t('Neutral')}</text>
        </svg>
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
