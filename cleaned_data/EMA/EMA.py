survey_mapping = {
    "Sleep": {
        "hour": {
            "text": "How many hours did you sleep last night?",
            "options": {
                1: "<3",
                2: "3.5",
                3: "4",
                4: "4.5",
                5: "5",
                6: "5.5",
                7: "6",
                8: "6.5",
                9: "7",
                10: "7.5",
                11: "8",
                12: "8.5",
                13: "9",
                14: "9.5",
                15: "10",
                16: "10.5",
                17: "11",
                18: "11.5",
                19: "12",
            },
        },
        "rate": {
            "text": "How would rate your overall sleep last night?",
            "options": {
                1: "Very good",
                2: "Fairly good",
                3: "Fairly bad",
                4: "Very bad",
            },
        },
        "social": {
            "text": "How often did you have trouble staying awake yesterday while in class, eating meals or engaging in social activity?",
            "options": {1: "None", 2: "Once", 3: "Twice", 4: "Three or more times"},
        },
        "location": {"text": "", "options": {}},
    },
    "Exercise": {
        "have": {
            "text": "Did you do vigorous exercise today (don't include walking) such as run, swim, cycle, play a sport",
            "options": {1: "Yes", 2: "No"},
        },
        "schedule": {
            "text": "If no did you want to but couldn't because of your schedule?",
            "options": {1: "Yes", 2: "No"},
        },
        "exercise": {
            "text": "If you exercised how long did you exercise for?",
            "options": {
                1: "None",
                2: "<30 mins",
                3: "30-60 mins",
                4: "60-90 mins",
                5: ">90mins",
            },
        },
        "walk": {
            "text": "How long did you walk for today?",
            "options": {
                1: "None",
                2: "<30 mins",
                3: "30-60 mins",
                4: "60-90 mins",
                5: ">90mins",
            },
        },
        "location": {"text": "", "options": {}},
    },
    "Social": {
        "number": {
            "text": "How many people did you have contact with yesterday...",
            "options": {
                1: "0-4 persons",
                2: "5-9 persons",
                3: "10-19 persons",
                4: "20-49 persons",
                5: "50-99 persons",
                6: "over 100 persons",
            },
        },
        "location": {"text": "", "options": {}},
    },
    "Mood": {
        "happyornot": {
            "text": "Do you feel AT ALL happy right now?",
            "options": {1: "Yes", 2: "No"},
        },
        "happy": {
            "text": 'If you answered "Yes" on the first question, how happy do you feel?',
            "options": {
                1: "a little bit",
                2: "somewhat",
                3: "very much",
                4: "extremely",
            },
        },
        "sadornot": {
            "text": "Do you feel AT ALL sad right now?",
            "options": {1: "Yes", 2: "No"},
        },
        "sad": {
            "text": 'If you answered "Yes" on the third question, how sad do you feel?',
            "options": {
                1: "a little bit",
                2: "somewhat",
                3: "very much",
                4: "extremely",
            },
        },
        "location": {"text": "", "options": {}},
    },
    "Stress": {
        "level": {
            "text": "Right now, I am...",
            "options": {
                1: "A little stressed",
                2: "Definitely stressed",
                3: "Stressed out",
                4: "Feeling good",
                5: "Feeling great",
            },
        },
        "location": {"text": "", "options": {}},
    },
    "Class": {
        "course_id": {"text": "What's the class name? (e.g., CS65)", "options": {}},
        "experience": {
            "text": "I enjoyed the class today.",
            "options": {
                1: "neutral",
                2: "strongly agree",
                3: "agree",
                4: "disagree",
                5: "strongly disagree",
            },
        },
        "hours": {
            "text": "How many hours did you spent on coursework outside class since the last class?",
            "options": {
                1: "0",
                2: "1",
                3: "2",
                4: "3",
                5: "4",
                6: "5",
                7: "6",
                8: "7",
                9: "8",
                10: "9",
                11: "10",
                12: ">10",
            },
        },
        "due": {
            "text": "Do you have an assignment (due), quizz or exam today?",
            "options": {1: "Yes", 2: "No"},
        },
        "location": {"text": "", "options": {}},
    },
    "Behavior": {
        qid: {
            "text": qtext,
            "options": {
                1: "Not at all",
                2: "A little",
                3: "Somewhat",
                4: "Very",
                5: "Extremely",
            },
        }
        for qid, qtext in {
            "enthusiastic": "In the past 15 minutes, I was extraverted, enthusiastic.",
            "critical": "......, I was critical, quarrelsome.",
            "dependable": "......, I was dependable, self-disciplined.",
            "anxious": "......, I was anxious, easily upset.",
            "experiences": "......, I was open to new experiences, complex.",
            "reserved": "......, I was reserved, quiet.",
            "sympathetic": "......, I was sympathetic, warm.",
            "disorganized": "......, I was disorganized, careless.",
            "calm": "......, I was calm, emotionally stable.",
            "conventional": "......, I was conventional, uncreative.",
        }.items()
    }
    | {"location": {"text": "location", "options": {}}},
    "Events": {
        "positive": {
            "text": "Rate the intensity of your Most Positive Events on a scale ranging from 1 (very weak) to 7 (very intense).",
            "options": {i: str(i) for i in range(1, 8)},
        },
        "negative": {
            "text": "Rate the intensity of your Most Negative Events on a scale.",
            "options": {i: str(i) for i in range(1, 8)},
        },
        "pevent": {
            "text": "What was the positive event (single word or short comment)?",
            "options": {},
        },
        "nevent": {"text": "What was the negative event?", "options": {}},
        "location": {"text": "", "options": {}},
    },
    "Class 2": {
        "challenge": {
            "text": "Last week's lab was difficult and challenged me.",
            "options": {
                1: "Agree Strongly",
                2: "Agree Moderately",
                3: "Agree Slightly",
                4: "Disagree Slightly",
                5: "Disagree Moderately",
                6: "Disagree Strongly",
            },
        },
        "effort": {
            "text": "I put a great deal of effort into the course last week.",
            "options": {
                1: "Agree Strongly",
                2: "Agree Moderately",
                3: "Agree Slightly",
                4: "Disagree Slightly",
                5: "Disagree Moderately",
                6: "Disagree Strongly",
            },
        },
        "grade": {
            "text": "I expect to get the following grade for this course.",
            "options": {
                1: "A",
                2: "A-",
                3: "B+",
                4: "B",
                5: "B-",
                6: "C+",
                7: "C",
                8: "C-",
            },
        },
        "location": {"text": "", "options": {}},
    },
}
