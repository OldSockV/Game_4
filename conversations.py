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
    },
    "S6_5": {
        "1": {
            "start": ["There is a drop ahead,",
                      "to enter the ruins you have to open",
                      "the doors using that lever down there."],
            'inp': ["...", "Doors"],
            'next': ['leave', 'leave'],
            'resp': [None, ["Inside the ruins are many anchient doors.",
                            "They are each assigned a colour, so when",
                            "a blue lever is pulled, all blue doors open."]],
            'face1': "voi",
            'face2': "",
        },
    },
    "S6_5.5": {
        "1": {
            "start": ["Those spikes will damage your suit.",
                      "If you come into mortal danger i will",
                      "revert you to the last [SAVE POINT]"],
            'inp': ["Exit", "Save point", "How?"],
            'next': ['leave', "2", None],
            'resp': [None, ["Ive marked all locations with a yellow [S]",
                            "when i need to revert you, you will reappear",
                            "at the previous save point."],
                     ["idk man, it just works my dude.", "",
                      "I can only write so much lore."]],
            'face1': "voi",
            'face2': "",
            "altface1": [None, None, 'scr_1'],
            "altface2": [None, None, None]
        },
        "2": {
            "start": ["When you touch a new save point, that",
                      "will then be your active save point.",
                      ""],
            'inp': [""],
            'next': ['leave'],
            'resp': [["when you reach 0 armor or luck or health",
                      "HP, etc. I wont be able to bring you back",
                      "and you will die."]],
            'face1': "voi",
            'face2': "",
        },
    },
    "S6_5.7": {
        "1": {
            "start": ["These actuators work differently.",
                      "You will have to hit them with your",
                      "blaster to activate the doors."],
            'inp': ["2"],
            'next': ["2"],
            'resp': [["To aim with your blaster, hold",
                      " [RIGHT MOUSE BUTTON]  and then",
                      "press [LEFT MOUSE BUTTON] to fire"]],
            'face1': "",
            'face2': "",
        },
        "2": {
            "start": ["PS: If your health becomes critically",
                      "low, i reccomend going back one level to ",
                      "reset both the level, and your health."],
            'inp': [""],
            'next': ['leave'],
            'resp': [None],
            'face1': "scr_3",
            'face2': "",
        },
    },
    "S6_6": {
        "1": {
            "start": ["This area is the final test for the ruins,",
                      "After this area i will no longer give you ",
                      "assistance."],
            'inp': ["."],
            'next': ["2"],
            'resp': [["I will still, however, give you",
                      "insight and analasys to increase",
                      "mission success chance."]],
            'face1': "voi",
            'face2': "",
        },
        "2": {
            "start": ["",
                      " [DIRECTIONS CAN BE FOUND",
                      "   ON THE STONE TABLET]"],
            'inp': [""],
            'next': ['leave'],
            'resp': [None],
            'face1': "",
            'face2': "",
        },
    },

    "S6_win": {
        "1": {
            "start": ["So,",
                      " you made it through the front door.",
                      ""],
            'inp': [""],
            'next': ["2"],
            'resp': [["", "  Impressive", ""]],
            'face1': "red",
            'face2': "",
        },
        "2": {
            "start": ["So, newbie. You dont look like",
                      "the Terminus type, what are you",
                      "doing all the way out here?"],
            'inp': ["Directions", "Ruins", "Terminus type?"],
            'next': ["4", None, "3"],
            'resp': [["  I need to reach these coordinates.", "there's a package that need retrieving.", ""],
                     ["    Archeologist huh? Sorry,", "but if you wnat an experts help,",
                      "youre gonna have to find someone else."],
                     ["You look more sorted for the", "old dust fields, or back at the big city.",
                      ""]],
            'face1': "red",
            'face2': "p_ne",
            'altface1': ['p_ne', None, None],
            'altface2': ['red', '', 'p_an']
        },
        "4": {
            "start": ["Oh, thats just up past the canyon.",
                      " We've even got a camp up there.",
                      ""],
            'inp': ["I cant get up the steep walls. "],
            'next': ["5"],
            'resp': [["I'll just give you mine, ", "i have a spare back at base.", "  Come meet me there"]],
            'face1': "red",
            'face2': "p_em",
            'altface1': [None],
            'altface2': ['p_ne']
        },
        "5": {
            "start": ["",
                      "   [ Climbing Gear Aquired ]",
                      ""],
            'inp': [""],
            'next': ["leave"],
            'resp': [["[You can now slide on walls and", " then jump off them to", " reach new areas.]"]],
            'face1': "",
            'face2': "",
        },
        "3": {
            "start": ["Don't get me wrong, you seem capable.",
                      "But out here in the real world,",
                      "  Things can be dangeourous."],
            'inp': ["Back", "Danger?", "How far out?"],
            'next': ["2", None, "3.5"],
            'resp': [None, ["Well, lets just say some old traps", "are the least of your worries", "out here."],
                     ["Well, were about 50 klicks from any", "known civilisation, and gang juristdiction",
                      "has no bearing on anything around for miles."]],
            'face1': "red",
            'face2': "p_pi",
            'altface1': [None, None, None],
            'altface2': [None, "", ""]
        },
        "3.5": {
            "start": ["And on top of that, noone wants",
                      "to control this area anyways. Theres ",
                      "no profit on overgrown death traps."],
            'inp': [""],
            'next': ["3"],
            'resp': [None],
            'face1': "red",
            'face2': "",
        },
    },
    "S6_71": {
        "1": {
            "start": ["Now that you have the climbing gear",
                      "you will be able to return to the tram",
                      "and enter the upper levels."],
            'inp': [""],
            'next': ["leave"],
            'resp': [["while connected to a wall you can",
                      "jump off the surface of it to propel",
                      "yourself forward."]],
            'face1': "voi",
            'face2': "",
        }
    },

}

talking = {
    "win1": {
        "1": {
            "start": ["Go on, show me you can",
                      " survive out here freshmeat.",
                      ""],
            'inp': [""],
            'next': ['leave'],
            'resp': [None],
            'face1': "red",
            'face2': "",
        }
    },
    "Blue": {
        "1": {
            "start": ["Greetings stranger,",
                      "",
                      "1"],
            'inp': ["11"],
            'next': [None],
            'resp': [None],
            'face1': "p_ne",
            'face2': "",
        }
    },
    "blue_boss": {
        "1": {
            "start": ["Greetings stranger,",
                      "",
                      "1"],
            'inp': ["11"],
            'next': [None],
            'resp': [None],
            'face1': "p_ne",
            'face2': "",
        }
    },
    "change": {
        "1": {
            "start": ["Greetings stranger,",
                      "",
                      "1"],
            'inp': ["11"],
            'next': [None],
            'resp': [None],
            'face1': "p_ne",
            'face2': "",
        }
    },
    "red_boss": {
        "1": {
            "start": ["Greetings stranger,",
                      "",
                      "1"],
            'inp': ["11"],
            'next': [None],
            'resp': [None],
            'face1': "p_ne",
            'face2': "",
        }
    },
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
    "directions": {
        "1": {
            "start": ["go right, use yellow switch.",
                      "go left, up and over to use the blue switch.",
                      "then return here to go down and up on the other side."],
            'inp': [""],
            'next': ["leave"],
            'resp': [None],
            'face1': "",
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
    "camp_pillar": {
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
    "camp2": {
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
    "camp2pillar": {
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

}
