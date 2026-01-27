metrics_per_position = {
    "Full Back": [
        "INTERCEPTIONS PER 90",
        "DEFENSIVE DUELS PER 90",
        "DEFENSIVE DUELS WON %",
        "PROGRESSIVE RUNS PER 90",
        "CROSSES PER 90",
        "AERIAL DUELS WON %",
        "DRIBBLES PER 90",
        "PASSES TO PENALTY AREA PER 90",
        "PROGRESSIVE PASSES PER 90",
        "xA"
    ],
    "Centre Back": [
        "INTERCEPTIONS PER 90",
        "DEFENSIVE DUELS PER 90",
        "DEFENSIVE DUELS WON %",
        "AERIAL DUELS PER 90",
        "AERIAL DUELS WON %",
        "DUELS PER 90",
        "DUELS WON %",
        "PASSES PER 90",
        "Received PASSES PER 90"
    ],
    
    "Outside Centre Back": [
        "INTERCEPTIONS PER 90",
        "PROGRESSIVE PASSES PER 90",
        "DEFENSIVE DUELS WON %",
        "AERIAL DUELS PER 90",
        "AERIAL DUELS WON %",
        "DUELS PER 90",
        "DUELS WON %",
        "CROSSES PER 90",
        "DRIBBLES PER 90"
    ],
    "Number 6": [
        "INTERCEPTIONS PER 90",
        "DEFENSIVE DUELS PER 90",
        "DEFENSIVE DUELS WON %",
        "ACCURATE PASSES %",
        "AERIAL DUELS WON %",
        "DUELS PER 90",
        "DUELS WON %",
        "PASSES TO FINAL THIRD PER 90",
        "PASSES PER 90",
        "Received PASSES PER 90"
    ],
    "Number 8": [
        "SHOTS PER 90",
        "xG PER 90",
        "TOUCHES IN BOX PER 90",
        "PASSES TO PENALTY AREA PER 90",
        "KEY PASSES PER 90",
        "DRIBBLES PER 90",
        "PROGRESSIVE PASSES PER 90",
        "AERIAL DUELS WON %",
        "PROGRESSIVE RUNS PER 90",
        "SUCCESSFUL DRIBBLES %",
],
    "Number 10": [
        "SHOTS PER 90",
        "xG PER 90",
        "TOUCHES IN BOX PER 90",
        "PASSES TO PENALTY AREA PER 90",
        "KEY PASSES PER 90",
        "DRIBBLES PER 90",
        "PROGRESSIVE PASSES PER 90",
        "xA PER 90",
        "PROGRESSIVE RUNS PER 90",
        "SHOTS ON TARGET %",
    ],
    "Winger": [
        "xG PER 90",
        "SHOTS PER 90",
        "KEY PASSES PER 90",
        "DRIBBLES PER 90",
        "SUCCESSFUL DRIBBLES %",
        "PROGRESSIVE RUNS PER 90",
        "ACCELERATIONS PER 90",
        "PASSES TO PENALTY AREA PER 90",
        "CROSSES PER 90",
        "ACCURATE CROSSES %",
    ],
    "Centre Forward": [
        "NON PENALTY GOALS PER 90",
        "SHOTS PER 90",
        "SHOTS ON TARGET %",
        "xG PER 90",
        "GOAL CONVERSION %",
        "PROGRESSIVE RUNS PER 90",
        "TOUCHES IN BOX PER 90",
        "xA PER 90",
        "ASSISTS PER 90",
        "KEY PASSES PER 90",
    ],
    "Goal Keeper": [
        "Clean sheets",
        "Save rate (%)",
        "Prevented goals per 90",
        "ACCURATE PASSES %",
        "Exits Per 90",
        "AERIAL DUELS PER 90"
    ]
}

profiles_zcore = {
    "Centre Back": [
        {
            "Profile Name": "No Nonsense Centre Back",
            "Using Metrics":[
            "INTERCEPTIONS PER 90",
            "DUELS PER 90",
            "DUELS WON %",
            "PASSES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %", "AERIAL DUELS PER 90", "AERIAL DUELS WON %"],
            "Z Score Name": "No Nonsense CB Score"
        },
        {
            "Profile Name": "Outside Centre Back",
            "Using Metrics":[
            "INTERCEPTIONS PER 90",
            "DEFENSIVE DUELS PER 90",
            "DEFENSIVE DUELS WON %",
            "AERIAL DUELS PER 90",
            "AERIAL DUELS WON %",
            "DUELS PER 90",
            "DUELS WON %",
            "PASSES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["DRIBBLES PER 90", "PROGRESSIVE RUNS PER 90", "PASSES TO FINAL THIRD PER 90"],
            "Z Score Name": "Outside CB Score"
        },
        {
            "Profile Name": "Ball Playing Centre Back",
            "Using Metrics":[
            "INTERCEPTIONS PER 90",
            "DEFENSIVE DUELS PER 90",
            "DEFENSIVE DUELS WON %",
            "AERIAL DUELS PER 90",
            "AERIAL DUELS WON %",
            "DUELS PER 90",
            "DUELS WON %",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["PASSES PER 90", "PROGRESSIVE PASSES PER 90", "ACCURATE PASSES %"],
            "Z Score Name": "Ball Playing CB Score"
        },
        {
            "Profile Name": "SET PIECE CENTRE BACK ",
            "Using Metrics":[
            "INTERCEPTIONS PER 90",
            "DEFENSIVE DUELS PER 90",
            "DUELS PER 90",
            "DUELS WON %",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["AERIAL DUELS PER 90", "AERIAL DUELS WON %", "DEFENSIVE DUELS WON %", "xG PER 90", "Head goals per 90"],
            "Z Score Name": "SET Piece CB Score"
        },

    ],
    "Full Back": [
        {
            "Profile Name": "Progressive Wing Back",
            "Using Metrics": [
            "INTERCEPTIONS PER 90",
            "DEFENSIVE DUELS PER 90",
            "DEFENSIVE DUELS WON %",
            "AERIAL DUELS WON %",
            "PASSES TO PENALTY AREA PER 90",
            "PASSES TO FINAL THIRD PER 90",
            ],
            "Weighted Metrics": [
                "PROGRESSIVE RUNS PER 90", "CROSSES PER 90", "DRIBBLES PER 90", "xA"
            ],
            "Z Score Name": "Progressive WB Score"
        },
    ],
    "Winger": [
        {
            "Profile Name": "Direct Winger",
            "Using Metrics": [
            "xG PER 90",
            "SHOTS PER 90",
            "SUCCESSFUL DRIBBLES %",
            "PROGRESSIVE RUNS PER 90",
            "PASSES TO PENALTY AREA PER 90",
            "ACCURATE CROSSES %",
            "KEY PASSES PER 90",
            ],
            "Weighted Metrics": ["DRIBBLES PER 90", "ACCELERATIONS PER 90", "CROSSES PER 90"],
            "Z Score Name": "Direct Winger Score"
        },
        {
            "Profile Name": "Goal Threat Winger",
            "Using Metrics": [
            "KEY PASSES PER 90",
            "PROGRESSIVE RUNS PER 90",
            "ACCELERATIONS PER 90",
            "PASSES TO PENALTY AREA PER 90",
            "CROSSES PER 90",
            "ACCURATE CROSSES %",
            ],
            "Weighted Metrics": ["xG PER 90", "SHOTS PER 90", "SHOTS ON TARGET %", "DRIBBLES PER 90", "SUCCESSFUL DRIBBLES %", "TOUCHES IN BOX PER 90" ,],
            "Z Score Name": "Goal Threat Winger Score"
        }

    ],
    "Centre Forward": [
        {
            "Profile Name": "Providing Forward",
            "Using Metrics": [
            "NON PENALTY GOALS PER 90",
            "SHOTS PER 90",
            "SHOTS ON TARGET %",
            "xG PER 90",
            "GOAL CONVERSION %",
            "PROGRESSIVE RUNS PER 90",
            "AERIAL DUELS WON %",
            "ASSISTS PER 90",
            ],
            "Weighted Metrics": ["KEY PASSES PER 90", "xA PER 90", "TOUCHES IN BOX PER 90", "PASSES TO PENALTY AREA PER 90"],
            "Z Score Name": "Providing Forward Score"
        },
        {
            "Profile Name": "Target Man Forward",
            "Using Metrics": [
            "NON PENALTY GOALS PER 90",
            "SHOTS ON TARGET %",
            "xG PER 90",
            "GOAL CONVERSION %",
            "PROGRESSIVE RUNS PER 90",
            "xA PER 90",
            "ASSISTS PER 90",
            ],
            "Weighted Metrics": ["AERIAL DUELS PER 90", "AERIAL DUELS WON %", "TOUCHES IN BOX PER 90"],
            "Z Score Name": "Target Man Forward Score"
        },
        {
            "Profile Name": "Mobile Forward",
            "Using Metrics": [
            "NON PENALTY GOALS PER 90",
            "SHOTS PER 90",
            "SHOTS ON TARGET %",
            "xG PER 90",
            "GOAL CONVERSION %",
            "AERIAL DUELS WON %",
            "TOUCHES IN BOX PER 90",
            "xA PER 90",
            "ASSISTS PER 90",
            ],
            "Weighted Metrics": ["DRIBBLES PER 90", "ACCELERATIONS PER 90", "PROGRESSIVE RUNS PER 90"],
            "Z Score Name": "Mobile Forward Score"
        }
    ],
    "Number 6": [
        {
            "Profile Name": "Progressive 6",
            "Using Metrics": [
            "DEFENSIVE DUELS PER 90",
            "DEFENSIVE DUELS WON %",
            "AERIAL DUELS WON %",
            "DUELS PER 90",
            "DUELS WON %",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            "INTERCEPTIONS PER 90"
            ],
            "Weighted Metrics": ["PROGRESSIVE PASSES PER 90", "ACCURATE PASSES %", "PASSES PER 90"],
            "Z Score Name": "Progressive 6 Score"
        },
        {
            "Profile Name": "Defensive 8",
            "Using Metrics": [
            "ACCURATE PASSES %",
            "AERIAL DUELS WON %",
            "DUELS PER 90",
            "PASSES TO FINAL THIRD PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %", "INTERCEPTIONS PER 90", "DUELS WON %",],
            "Z Score Name": "Defensive 8 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
            "INTERCEPTIONS PER 90",
            "DEFENSIVE DUELS PER 90",
            "DEFENSIVE DUELS WON %",
            "ACCURATE PASSES %",
            "AERIAL DUELS WON %",
            "DUELS PER 90",
            "DUELS WON %",
            "PASSES TO FINAL THIRD PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["KEY PASSES PER 90", "DRIBBLES PER 90", "xA PER 90",],
            "Z Score Name": "Progressive 8 Score"
        }

    ],
    "Number 8": [
        {
            "Profile Name": "Progressive 6",
            "Using Metrics": [
            "PASSES TO PENALTY AREA PER 90",
            "SHOTS PER 90",
            "PROGRESSIVE RUNS PER 90",
            "KEY PASSES PER 90",
            "DRIBBLES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            "TOUCHES IN BOX PER 90",
            ],
            "Weighted Metrics": ["PROGRESSIVE PASSES PER 90", "ACCURATE PASSES %", "PASSES PER 90"],
            "Z Score Name": "Progressive 6 Score"
        },
        {
            "Profile Name": "Defensive 8",
            "Using Metrics": [
            "PASSES TO FINAL THIRD PER 90",
            "PASSES TO PENALTY AREA PER 90",
            "SHOTS PER 90",
            "PROGRESSIVE PASSES PER 90",
            "PROGRESSIVE RUNS PER 90",
            "KEY PASSES PER 90",
            "DRIBBLES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            "TOUCHES IN BOX PER 90",
            ],
            "Weighted Metrics": ["DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %", "INTERCEPTIONS PER 90", "DUELS WON %",],
            "Z Score Name": "Defensive 8 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
            "PASSES TO FINAL THIRD PER 90",
            "PASSES TO PENALTY AREA PER 90",
            "SHOTS PER 90",
            "PROGRESSIVE PASSES PER 90",
            "PROGRESSIVE RUNS PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            "TOUCHES IN BOX PER 90",
            ],
            "Weighted Metrics": ["KEY PASSES PER 90", "DRIBBLES PER 90", "xA PER 90",],
            "Z Score Name": "Progressive 8 Score"
        },
        {
            "Profile Name": "Creative 10",
            "Using Metrics": [
            "PASSES TO FINAL THIRD PER 90",
            "SHOTS PER 90",
            "PROGRESSIVE RUNS PER 90",
            "DRIBBLES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            "TOUCHES IN BOX PER 90",
            ],
            "Weighted Metrics": ["KEY PASSES PER 90", "xA PER 90", "PROGRESSIVE PASSES PER 90", "PASSES TO PENALTY AREA PER 90"],
            "Z Score Name": "Creative 10 Score"
        },
        {
            "Profile Name": "Goal Threat 10",
            "Using Metrics": [
            "PASSES TO FINAL THIRD PER 90",
            "PASSES TO PENALTY AREA PER 90",
            "PROGRESSIVE PASSES PER 90",
            "PROGRESSIVE RUNS PER 90",
            "KEY PASSES PER 90",
            "OFFENSIVE DUELS PER 90",
            "OFFENSIVE DUELS WON %",
            ],
            "Weighted Metrics": ["SHOTS PER 90", "TOUCHES IN BOX PER 90", "DRIBBLES PER 90", "SHOTS ON TARGET %", "xG PER 90"],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ],
    "Number 10" :[
        {
            "Profile Name": "Creative 10",
            "Using Metrics": [
            "SHOTS PER 90",
            "xG PER 90",
            "TOUCHES IN BOX PER 90",
            "DRIBBLES PER 90",
            "PROGRESSIVE RUNS PER 90",
            "SHOTS ON TARGET %",
            ],
            "Weighted Metrics": ["KEY PASSES PER 90", "xA PER 90", "PROGRESSIVE PASSES PER 90", "PASSES TO PENALTY AREA PER 90"],
            "Z Score Name": "Creative 10 Score"
        },
        {
            "Profile Name": "Goal Threat 10",
            "Using Metrics": [
            "PASSES TO PENALTY AREA PER 90",
            "KEY PASSES PER 90",
            "PROGRESSIVE PASSES PER 90",
            "xA PER 90",
            "PROGRESSIVE RUNS PER 90",
            ],
            "Weighted Metrics": ["SHOTS PER 90", "TOUCHES IN BOX PER 90", "DRIBBLES PER 90", "SHOTS ON TARGET %", "xG PER 90"],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ]
}
