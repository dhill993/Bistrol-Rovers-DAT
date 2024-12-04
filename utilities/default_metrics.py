
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
        "PADJ Pressures",
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
            "Weighted Metrics": ["Carries", "Dribbles", "OP F3 Passes"],
            "Z Score Name": "Outside CB Score"
        },
        {
            "Profile Name": "Ball Playing Centre Back",
            "Using Metrics":[
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
            "Weighted Metrics": ["Passing %", "Pass OBV"],
            "Z Score Name": "Ball Playing CB Score"
        },
    ],
    "Full Back": [
        {
            "Profile Name": "Progressive Wing Back",
            "Using Metrics": [
            "Dribbles Stopped %",
            "DA OBV",
            "OP Passes into Box",
            "Successful Dribbles",
            "Ball Recoveries",
            "PADJ Tackles",
            "PADJ Interceptions",
            "Aerial Win %"
            ],
            "Weighted Metrics": [
                "Successful Crosses", "xG Assisted", "Deep Progressions", "OBV D&C"
            ],
            "Z Score Name": "Progressive WB Score"
        },
    ],
    "Winger": [
        {
            "Profile Name": "Providing Winger",
            "Using Metrics": [
            "xG",
            "Shots",
            "Dribbles",
            "Successful Dribbles",
            "OBV",
            "Carries",
            "PINTIN",
            ],
            "Weighted Metrics": ["Pass OBV", "xG Assisted", "Successful Crosses", "OP Key Passes"],
            "Z Score Name": "Providing Winger Score"
        },
        {
            "Profile Name": "Goal Threat Winger",
            "Using Metrics": [
            "Shots",
            "OP Key Passes",
            "OBV",
            "Carries",
            "PINTIN",
            "Successful Crosses",
            "xG Assisted"
            ],
            "Weighted Metrics": ["xG", "Dribbles", "Successful Dribbles", "Touches in Box"],
            "Z Score Name": "Goal Threat Winger Score"
        }

    ],
    "Centre Forward": [
        {
            "Profile Name": "Providing Forward",
            "Using Metrics": [
            "NP Goals",
            "Shots",
            "Shooting %",
            "xG",
            "xG/Shot",
            "Shot Touch %",
            "Aerial Win %",
            "Touches in Box",
            "Shot OBV"
            ],
            "Weighted Metrics": ["PINTIN", "xG Assisted", "OP Key Passes"],
            "Z Score Name": "Providing Forward Score"
        },
        {
            "Profile Name": "Target Man Forward",
            "Using Metrics": [
            "NP Goals",
            "Shots",
            "Shooting %",
            "xG",
            "xG/Shot",
            "xG Assisted",
            "Shot OBV"
            ],
            "Weighted Metrics": ["Shot Touch %", "Aerial Win %", "Touches in Box"],
            "Z Score Name": "Target Man Forward Score"
        },
        {
            "Profile Name": "Mobile Forward",
            "Using Metrics": [
            "NP Goals",
            "Shots",
            "Shooting %",
            "xG",
            "xG/Shot",
            "Shot Touch %",
            "Aerial Win %",
            "Touches in Box",
            "Shot OBV"
            ],
            "Weighted Metrics": ["Dribbles", "Carries", "PINTIN", "xG Assisted", "PADJ Pressures"],
            "Z Score Name": "Mobile Forward Score"
        }
    ],
    "Number 6": [
        {
            "Profile Name": "Progressive 6",
            "Using Metrics": [
            "PADJ Tackles",
            "PADJ Interceptions",
            "Defensive Actions",
            "Passing %",
            "Ball Recoveries",
            "Aerial Win %",
            "Dribbles Stopped %",
            "PADJ Pressures",
            "DA OBV",
            ],
            "Weighted Metrics": ["Deep Progressions", "xG Buildup", "Pass OBV", "PADJ Interceptions", "Ball Recoveries"],
            "Z Score Name": "Progressive 6 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
            "PADJ Tackles",
            "PADJ Interceptions",
            "Defensive Actions",
            "Passing %",
            "Ball Recoveries",
            "Aerial Win %",
            "Dribbles Stopped %",
            "PADJ Pressures",
            "DA OBV",
            "Deep Progressions"
            ],
            "Weighted Metrics": ["PADJ Tackles", "PADJ Interceptions", "Defensive Actions", "Defensive Regains", "DA OBV",],
            "Z Score Name": "Progressive 8 Score"
        },
        {
            "Profile Name": "Progressive 10",
            "Using Metrics": [
            "PADJ Tackles",
            "PADJ Interceptions",
            "Defensive Actions",
            "Passing %",
            "Ball Recoveries",
            "Aerial Win %",
            "Dribbles Stopped %",
            "PADJ Pressures",
            "DA OBV",
            "Deep Progressions"
            ],
            "Weighted Metrics": ["PINTIN", "OP Key Passes", "OBV D&C", "xG Assisted"],
            "Z Score Name": "Progressive 10 Score"
        }

    ],
    "Number 8": [
        {
            "Profile Name": "Progressive 6",
            "Using Metrics": [
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
            "Weighted Metrics": ["Deep Progressions", "xG Buildup", "Pass OBV", "PADJ Interceptions", "Ball Recoveries"],
            "Z Score Name": "Progressive 6 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
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
            "Weighted Metrics": ["PADJ Tackles", "PADJ Interceptions", "Defensive Actions", "Defensive Regains", "DA OBV",],
            "Z Score Name": "Progressive 8 Score"
        },
        {
            "Profile Name": "Progressive 10",
            "Using Metrics": [
            "OP F3 Passes",
            "Shots",
            "Deep Progressions",
            "xG Buildup",
            "Dribbles",
            "Pass OBV",
            "Ball Recoveries",
            ],
            "Weighted Metrics": ["PINTIN", "OP Key Passes", "OBV D&C", "xG Assisted"],
            "Z Score Name": "Progressive 10 Score"
        },
        {
            "Profile Name": "Creative 10",
            "Using Metrics": [
            "OP F3 Passes",
            "Shots",
            "Deep Progressions",
            "xG Buildup",
            "Dribbles",
            "Pass OBV",
            "Ball Recoveries",
            "OBV D&C"
            ],
            "Weighted Metrics": ["PINTIN", "OP Key Passes", "OBV", "xG Assisted"],
            "Z Score Name": "Creative 10 Score"
        },
        {
            "Profile Name": "Goal Threat 10",
            "Using Metrics": [
            "OP F3 Passes",
            "PINTIN",
            "Deep Progressions",
            "xG Buildup",
            "OP Key Passes",
            "Dribbles",
            "Pass OBV",
            "Ball Recoveries",
            "OBV D&C"
            ],
            "Weighted Metrics": ["Shots", "Shooting %", "Touches in Box", "OBV", "xG"],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ],
    "Number 10" :[
        {
            "Profile Name": "Creative 10",
            "Using Metrics": [
            "Shots",
            "xG",
            "Ball Recoveries",
            "Successful Dribbles",
            "Carries",
            "Shooting %"
            ],
            "Weighted Metrics": ["PINTIN", "OP Key Passes", "OBV", "xG Assisted"],
            "Z Score Name": "Creative 10 Score"
        },
        {
            "Profile Name": "Goal Threat 10",
            "Using Metrics": [
            "Ball Recoveries",
            "OP Key Passes",
            "Successful Dribbles",
            "PINTIN",
            "xG Assisted",
            "Carries",
            ],
            "Weighted Metrics": ["Shots", "Shooting %", "Touches in Box", "OBV", "xG"],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ]
}