enter_level = {
    "S6_1": {
        "1": {
            "start": ["    [exiting the tram]",
                      " [Proceed to mission objective]",
                      ""],
            'inp': ["Location", "Personal Info"],
            'next': ["2", "1.1"],
            'resp': [["", "   [Loading mission briefing]", ""], ["", "[ACCESSING PERSONAL INFO]", ""]],
            'face1': "voi",
            'face2': "",
            'altface1': [None, None],
            'altface2': [None, None]
        },
        "1.1": {
            "start": ["", "[ENTER MORE SPECIFIC INQUIRY]", ""],
            'inp': ["System Scan", "Personal Data", "Personal Logs", "Return"],
            'next': [None, None, None, "1"],
            'resp': [["Exo-Core : ACTIVE   Climbing Gear : OFFLINE",
                      "Propulsion Booster : OFFLINE   Grav Beam : OFFLINE", "Zero Point Blaster : ACTIVE"],
                     ["", "Not accessable at this time.", ""], ["", "Not accessable at this time.", ""], None],
            'face1': "voi",
            'face2': "p_ne",
            'altface1': [None, None, None],
            'altface2': ['', 'p_em', 'p_em']
        },
        "2": {
            "start": ["", "The Overgrowth", ""],
            'inp': ["..."],
            'next': ["leave"],
            'resp': [None],
            'face1': "voi",
            'face2': "p_ne",
            'altface1': [None],
            'altface2': [None]
        }
    },
    "S6_2": {
        "1": {
            "start": ["   Rough terrain ahead.",
                      "",
                      "   [W] or [SPACE] to jump"],
            'inp': [""],
            'next': ["leave"],
            'resp': [None],
            'face1': "",
            'face2': "",
        },
    },
    "S6_3": {  # this is the 4th level
        "1": {
            "start": ["Pieces of the old ruins are showing",
                      "through the undergrowth.",
                      "Some old artifacts are poking through."],
            'inp': ["Artifacts"],
            'next': ["2"],
            'resp': [["The Distand Planes are covered in",
                      "old artifacts, showing glimpses of a",
                      "time long past."]],
            'face1': "voi",
            'face2': "",
        },
        "2": {
            "start": ["Sometimes pieces of the old world",
                      "give advice or warning of",
                      "what might be ahead of us."],
            'inp': [""],
            'next': ["leave"],
            'resp': [["    You can press [E]", "to interact with an artifact", ""]],
            'face1': "voi",
            'face2': "",
        },
    },
    "S6_4": {  # this is the 3rd level
        "1": {
            "start": ["Most ledges are climbable,",
                      "allowing you to grab on to a ledge",
                      "and hoist yourelf up."],
            'inp': [""],
            'next': ['leave'],
            'resp': [None],
            'face1': "",
            'face2': "",
        },
    }

}

talking = {

}

investigate = {
    "statue": {
        "1": {
            "start": ["1",
                      "1",
                      "1"],
            'inp': ["11"],
            'next': [None],
            'resp': [None],
            'face1': "p_ne",
            'face2': "",
        }
    },
    "pylon_1": {
        "1": {
            "start": ["Some form of table or altar.",
                      "Some faded writing can be made out on the",
                      "stone, but i never studied the language."],
            'inp': ["..."],
            'next': ['leave'],
            'resp': [['An archeologist could spend years studying',
                      'this. But youre not an archeologist.',
                      '  You should continue forward.']],
            'face1': "p_ne",
            'face2': "",
            'altface1': ["voi"],
            'altface2': ["p_em"]
        }
    },
    "walkway": {
        "1": {
            "start": ["  These caves go much deeper than any",
                      "  exploration has gone so far.",
                      ""],
            'inp': ["Life", "Structure", "EXIT"],
            'next': [None, "2", "leave"],
            'resp': [["Life readings state only floral life.",
                      "Conditions don't allow faunal life.",
                      "Insectoids however, seem to be flouroushing."],
                     ["The Overgrowth is a large cavelike area",
                      "of The Distant Planes, consisting mostly of moss ",
                      "and clay. Using tree roots to support."],
                     ["The mission is urgent,", "  Can't waste time looking", "  at scenery."]],
            'face1': "p_ne",
            'face2': "",
            'altface1': ["voi", "p_ne", "voi"],
            'altface2': [None, None, None]
        },
        "2": {
            "start": ["Below the massive layers of moss",
                      "there is an intricite maze of old ruins.",
                      "Although, they are mostly collapsed now."],
            'inp': ["Ruins", "Back"],
            'next': [None, "1"],
            'resp': [["Though severely worn down, and largely",
                      "collapsed, much of the traps and",
                      "machinery inside still works. So watch out."],
                     None],
            'face1': "voi",
            'face2': "",
        }

    },

}
