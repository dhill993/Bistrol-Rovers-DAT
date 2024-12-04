
metrics_per_position = {
    "Full Back": [
        "Dribbles Stopped %",
        "DA OBV",
        "OP Passes into Box",
        "Successful Dribbles",
        "Successful Crosses",
        "Ball Recoveries",
        "Deep Progressions",
        "PADJ Tackles",
        "PADJ Interceptions",
        "Aerial Win %"
    ],
    "Centre Back": [
        "Aerial Win %",
        "Blocks/Shots",
        "Dribbles Stopped %",
        "PADJ Tackles",
        "PADJ Interceptions",
        "PADJ Clearances",
        "Defensive Actions",
        "Defensive Regains",
        "DA OBV",
        "Ball Recoveries"
    ],
    "Number 6": [
        "PADJ Tackles",
        "PADJ Interceptions",
        "Defensive Actions",
        "Passing %",
        "Ball Recoveries",
        "Aerial Win %",
        "Dribbles Stopped %",
        "Padj Pressures",
        "DA OBV",
        "Deep Progressions"
    ],
    "Number 8": [
        "OP F3 Passes",
        "PINTIN",
        "Shots",
        "Deep Progressions",
        "xG Buildup",
        "OP Key Passes",
        "Dribbles",
        "Pass OBV",
        "Ball Recoveries",
        "OBV D&C"
    ],
    "Number 10": [
        "Shots",
        "xG",
        "OBV",
        "Ball Recoveries",
        "OP Key Passes",
        "Successful Dribbles",
        "PINTIN",
        "xG Assisted",
        "Carries",
        "Shooting %"
    ],
    "Winger": [
        "xG",
        "Shots",
        "OP Key Passes",
        "Dribbles",
        "Successful Dribbles",
        "OBV",
        "Carries",
        "PINTIN",
        "Successful Crosses",
        "xG Assisted"
    ],
    "Centre Forward": [
        "NP Goals",
        "Shots",
        "Shooting %",
        "xG",
        "xG/Shot",
        "Shot Touch %",
        "Aerial Win %",
        "Touches in Box",
        "xG Assisted",
        "Shot OBV"
    ]
}


profiles_zcore = {
    "Centre Back": [
        {
            "Profile Name": "No Nonsense Centre Back",
            "Using Metrics":[
            "Blocks/Shots",
            "Dribbles Stopped %",
            "PADJ Tackles",
            "PADJ Interceptions",
            "PADJ Clearances",
            "Defensive Actions",
            ],
            "Weighted Metrics": ["Aerial Win %", "Defensive Regains", "Ball Recoveries", "DA OBV"],
            "Z Score Name": "No Nonsense CB Score"
        },
        {
            "Profile Name": "Outside Centre Back",
            "Using Metrics":[
            "Blocks/Shots",
            "Dribbles Stopped %",
            "PADJ Tackles",
            "PADJ Interceptions",
            "PADJ Clearances",
            "Defensive Actions",
            ],
            "Weighted Metrics": ["Carries", "CARRY LENGTH", "DRIBBLES", "OP F3 PASSES"],
            "Z Score Name": "Outside CB Score"
        },
        {
            "Profile Name": "Adventures Wide Centre Back",
            "Using Metrics": [
                "Aerial Win%", "Defensive Actions", "Defensive Regains", "Ball Recoveries",
                "PAdj Tackles", "PAdj Interceptions", "Dribbles Stopped%", "xGBuildup",
                "Carry Length", "Dribbles", "Successful Dribbles", "OP F3 Passes"
            ],
            "Weighted Metrics": [
                "xGBuildup", "Dribbles Stopped%", "Carry Length", "Dribbles",
                "Successful Dribbles", "OP F3 Passes"
            ],
            "Z Score Name": "Adventures Wide CB Score"
        }
    ],
    "Full Back": [
        {
            "Profile Name": "Progressive Wing Back",
            "Using Metrics": [
                "PAdj Tackles", "PAdj Interceptions", "Dribbles Stopped%", "xGBuildup",
                "Carry Length", "Carry%", "Dribbles", "Successful Dribbles", "OP F3 Passes",
                "xG Assisted", "OP Key Passes", "Scoring Contribution", "PinTin",
                "Successful Crosses", "Crossing%", "Ball Recov. F2", "D&C OBV"
            ],
            "Weighted Metrics": [
                "xGBuildup", "Carry Length", "Successful Dribbles", "xG Assisted", 
                "PinTin", "Successful Crosses", "D&C OBV"
            ],
            "Z Score Name": "Progressive WB Score"
        },
        {
            "Profile Name": "Direct Wing Back",
            "Using Metrics": [
                "PAdj Tackles", "PAdj Interceptions", "Dribbles Stopped%", "Carry Length",
                "Carry%", "Dribbles", "Successful Dribbles", "OP F3 Passes", "xG Assisted",
                "Successful Crosses", "Crossing%", "Ball Recov. F2", "D&C OBV"
            ],
            "Weighted Metrics": ["Carry Length", "Dribbles", "Successful Dribbles", "D&C OBV"],
            "Z Score Name": "Direct WB Score"
        }
    ],
    "Defensive Midfielder": [
        {
            "Profile Name": "Defensive 6",
            "Using Metrics": [
                "PAdj Tackles", "PAdj Interceptions", "Dribbles Stopped%", "Defensive Actions",
                "Defensive Regains", "Ball Recoveries", "Aerial Win%", "DA OBV"
            ],
            "Weighted Metrics": ["Defensive Actions", "Defensive Regains", "Ball Recoveries", "DA OBV", "PAdj Interceptions"],
            "Z Score Name": "Defensive 6 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
                "PAdj Interceptions", "Ball Recoveries", "Deep Progressions", "OP F3 Passes",
                "Throughballs", "Shots", "Pass OBV", "OP Key Passes"
            ],
            "Weighted Metrics": ["Deep Progressions", "OP Key Passes", "OP F3 Passes"],
            "Z Score Name": "Progressive 8 Score"
        }
    ],
    "Winger": [
        {
            "Profile Name": "Providing Winger",
            "Using Metrics": [
                "Successful Dribbles", "Scoring Contribution", "Assists", "xG Assisted",
                "Key Passes", "Shots", "PinTin", "Crossing%", "Successful Crosses"
            ],
            "Weighted Metrics": ["Successful Crosses", "xG Assisted", "Scoring Contribution", "OP Key Passes"],
            "Z Score Name": "Providing Winger Score"
        },
        {
            "Profile Name": "Goal Threat Winger",
            "Using Metrics": [
                "Dribbles", "Scoring Contribution", "Assists", "xG Assisted", "Shots",
                "PinTin", "xG/Shot", "Touches in Box"
            ],
            "Weighted Metrics": ["Shots", "xG/Shot", "Touches in Box"],
            "Z Score Name": "Goal Threat Winger Score"
        }

    ],
    "Attacking Midfielder": [
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
                "PAdj Interceptions", "Ball Recoveries", "Deep Progressions", "OP F3 Passes",
                "Throughballs", "Shots", "Pass OBV", "OP Key Passes"
            ],
            "Weighted Metrics": ["Deep Progressions", "OP Key Passes", "OP F3 Passes"],
            "Z Score Name": "Progressive 8 Score"
        },
        {
            "Profile Name": "Creative 10",
            "Using Metrics": [
                "xG", "Shots", "Assists", "xG Assisted", "Key Passes",
                "Scoring Contribution", "PinTin", "Throughballs"
            ],
            "Weighted Metrics": ["xG Assisted", "Key Passes", "Scoring Contribution", "PinTin"],
            "Z Score Name": "Creative 10 Score"
        }
    ],
    "Centre Forward": [
        {
            "Profile Name": "Workhorse 9",
            "Using Metrics": [
                "xG", "Shots", "Assists", "xG Assisted", "Scoring Contribution",
                "PinTin", "PAdj Pressures", "Counterpress Regains"
            ],
            "Weighted Metrics": ["PinTin", "PAdj Pressures", "Counterpress Regains"],
            "Z Score Name": "Workhorse 9 Score"
        },
        {
            "Profile Name": "Dominant CF",
            "Using Metrics": [
                "xG", "Shots", "Shooting%", "Shot Touch%", "Aerial Win%",
                "Touches in Box", "Shot OBV"
            ],
            "Weighted Metrics": ["Shot Touch%", "Aerial Win%", "Touches in Box"],
            "Z Score Name": "Dominant CF Score"
        }
    ]
}