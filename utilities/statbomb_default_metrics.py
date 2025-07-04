# Centralized metrics and profiles for StatsBomb analysis.
# All metric names are normalized to match your metrics_mapping and processed DataFrame.

metrics_per_position = {
    "Full Back": [
        "Dribbles Stopped %",
        "Carries",
        "OP XG ASSISTED",
        "Successful Dribbles",
        "Successful Crosses",
        "Ball Recoveries",
        "OP Passes Into Box",
        "PR. Pass %",
        "PADJ Interceptions",
        "Aerial Win %"
    ],
    "Centre Back": [
        "Aerial Win %",
        "Dribbles Stopped %",
        "PADJ Tackles",
        "PADJ Interceptions",
        "PADJ Clearances",
        "Defensive Regains",
        "DA OBV",
        "Ball Recoveries",
        "Pass Forward %",
        "PR. Pass %"
    ],
    "Outside Centre Back": [
        "Aerial Win %",
        "Dribbles Stopped %",
        "PADJ Tackles",
        "PADJ Interceptions",
        "PR. Pass %",
        "Carries",
        "Successful Crosses",
        "Dribbles",
        "OP Passes Into Box",
        "OP F3 Passes"
    ],
    "Number 6": [
        "PADJ Tackles",
        "PADJ Interceptions",
        "Pass Forward %",
        "Ball Recoveries",
        "Aerial Win %",
        "Dribbles Stopped %",
        "DA OBV",
        "Deep Progressions",
        "PR. Pass %",
        "Pass OBV"
    ],
    "Number 8": [
        "PINTIN",
        "Shots",
        "Aerial Win %",
        "xG Assisted",
        "OP Key Passes",
        "Dribbles",
        "Carries",
        "OP Passes Into Box",
        "OBV D&C",
        "PR. Pass %"
    ],
    "Number 10": [
        "Shots",
        "xG",
        "Scoring Contribution",
        "OP Key Passes",
        "Successful Dribbles",
        "PINTIN",
        "xG Assisted",
        "Carries",
        "Shooting %",
        "PR. Pass %"
    ],
    "Winger": [
        "xG",
        "Shots",
        "OP Key Passes",
        "Dribbles",
        "Successful Dribbles",
        "OBV",
        "PINTIN",
        "Successful Crosses",
        "xG Assisted",
        "OBV D&C"
    ],
    "Centre Forward": [
        "NP Goals",
        "Shots",
        "Shooting %",
        "xG",
        "xG/Shot",
        "Shot Touch %",
        "Touches in Box",
        "Carries",
        "Shot OBV",
        "Fouls Won"
    ],
    "Goal Keeper": [
        "GK AGGRESSIVE DIST",
        "CLAIMS %",
        "PR. Pass %",
        "SHOT STOPPING %",
        "OP F3 Passes",
        "GSAA",
        "SAVE %",
        "XSV %",
        "POSITIVE OUTCOME",
        "GOALKEEPER OBV"
    ]
}

profiles_zcore = {
    "Centre Back": [
        {
            "Profile Name": "No Nonsense Centre Back",
            "Using Metrics": [
                "Blocks/Shots",
                "Dribbles Stopped %",
                "PADJ Tackles",
                "PADJ Interceptions",
                "PADJ Clearances",
                "Defensive Actions"
            ],
            "Weighted Metrics": [
                "Aerial Win %", "Defensive Regains", "Ball Recoveries", "DA OBV"
            ],
            "Z Score Name": "No Nonsense CB Score"
        },
        {
            "Profile Name": "Outside Centre Back",
            "Using Metrics": [
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
            "Weighted Metrics": [
                "Carries", "Dribbles", "OP F3 Passes"
            ],
            "Z Score Name": "Outside CB Score"
        },
        {
            "Profile Name": "Ball Playing Centre Back",
            "Using Metrics": [
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
            "Weighted Metrics": [
                "Passing %", "Pass OBV", "PR. Pass %"
            ],
            "Z Score Name": "Ball Playing CB Score"
        }
    ],
    "Full Back": [
        {
            "Profile Name": "Defensive Full Back",
            "Using Metrics": [
                "Dribbles Stopped %",
                "OP Passes Into Box",
                "Successful Dribbles",
                "PADJ Tackles",
                "Aerial Win %"
            ],
            "Weighted Metrics": [
                "Ball Recoveries", "DA OBV", "Defensive Regains", "PADJ Interceptions"
            ],
            "Z Score Name": "Defensive Full Score"
        },
        {
            "Profile Name": "Progressive Wing Back",
            "Using Metrics": [
                "Dribbles Stopped %",
                "DA OBV",
                "OP Passes Into Box",
                "Successful Dribbles",
                "Ball Recoveries",
                "PADJ Tackles",
                "PADJ Interceptions",
                "Aerial Win %"
            ],
            "Weighted Metrics": [
                "Successful Crosses", "OP XG ASSISTED", "Deep Progressions", "OBV D&C"
            ],
            "Z Score Name": "Progressive WB Score"
        }
    ],
    "Winger": [
        {
            "Profile Name": "Direct Winger",
            "Using Metrics": [
                "xG",
                "Shots",
                "Dribbles",
                "Successful Dribbles",
                "OBV",
                "Carries",
                "PINTIN"
            ],
            "Weighted Metrics": [
                "OBV D&C", "OP Passes Into Box", "Successful Crosses", "Carries"
            ],
            "Z Score Name": "Direct Winger Score"
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
            "Weighted Metrics": [
                "xG", "Dribbles", "Successful Dribbles", "Touches in Box"
            ],
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
            "Weighted Metrics": [
                "PINTIN", "xG Assisted", "OP Key Passes"
            ],
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
                "Shot OBV",
                "Shot Touch %"
            ],
            "Weighted Metrics": [
                "Aerial Win %", "Touches in Box"
            ],
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
                "Shot OBV",
                "xG Assisted"
            ],
            "Weighted Metrics": [
                "Dribbles", "Carries", "PADJ Pressures"
            ],
            "Z Score Name": "Mobile Forward Score"
        }
    ],
    "Number 6": [
        {
            "Profile Name": "Progressive 6",
            "Using Metrics": [
                "PADJ Tackles",
                "Defensive Actions",
                "Passing %",
                "Aerial Win %",
                "Dribbles Stopped %",
                "PADJ Pressures",
                "DA OBV"
            ],
            "Weighted Metrics": [
                "Deep Progressions", "xG Buildup", "Pass OBV", "PR. Pass %"
            ],
            "Z Score Name": "Progressive 6 Score"
        },
        {
            "Profile Name": "Progressive 8",
            "Using Metrics": [
                "Passing %",
                "Ball Recoveries",
                "Aerial Win %",
                "Dribbles Stopped %",
                "PADJ Pressures",
                "Deep Progressions"
            ],
            "Weighted Metrics": [
                "PADJ Tackles", "PADJ Interceptions", "Defensive Actions", "Defensive Regains", "DA OBV"
            ],
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
            "Weighted Metrics": [
                "PINTIN", "OP Key Passes", "OBV D&C", "xG Assisted"
            ],
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
                "OP Key Passes",
                "Dribbles",
                "Pass OBV",
                "OBV D&C"
            ],
            "Weighted Metrics": [
                "Deep Progressions", "xG Buildup", "Pass OBV", "PR. Pass %"
            ],
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
            "Weighted Metrics": [
                "PADJ Tackles", "PADJ Interceptions", "Defensive Actions", "Defensive Regains", "DA OBV"
            ],
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
                "Ball Recoveries"
            ],
            "Weighted Metrics": [
                "PINTIN", "OP Key Passes", "OBV D&C", "xG Assisted"
            ],
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
            "Weighted Metrics": [
                "PINTIN", "OP Key Passes", "OBV", "xG Assisted"
            ],
            "Z Score Name": "Creative 10 Score"
        },
        {
            "Profile Name": "Creative 8",
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
            "Weighted Metrics": [
                "PINTIN", "OP Key Passes", "OBV", "xG Assisted"
            ],
            "Z Score Name": "Creative 8 Score"
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
            "Weighted Metrics": [
                "Shots", "Shooting %", "Touches in Box", "OBV", "xG"
            ],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ],
    "Number 10": [
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
            "Weighted Metrics": [
                "PINTIN", "OP Key Passes", "OBV", "xG Assisted"
            ],
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
                "Carries"
            ],
            "Weighted Metrics": [
                "Shots", "Shooting %", "Touches in Box", "OBV", "xG"
            ],
            "Z Score Name": "Goal Threat 10 Score"
        }
    ],
    "Goal Keeper": [
        {
            "Profile Name": "Shot Stopper",
            "Using Metrics": [
                "SHOT STOPPING %",
                "SAVE %",
                "XSV %",
                "GSAA"
            ],
            "Weighted Metrics": [
                "CLAIMS %", "POSITIVE OUTCOME", "GOALKEEPER OBV"
            ],
            "Z Score Name": "Shot Stopper Score"
        },
        {
            "Profile Name": "Sweeper Keeper",
            "Using Metrics": [
                "GK AGGRESSIVE DIST",
                "PR. Pass %",
                "OP F3 Passes"
            ],
            "Weighted Metrics": [
                "POSITIVE OUTCOME", "GOALKEEPER OBV"
            ],
            "Z Score Name": "Sweeper Keeper Score"
        }
    ]
}
