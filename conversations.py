enter_forest = {
    "1": {
        "Start": ["start of conversation", "option 1 will continue the covnversation", "but 2 and 3 will give unique text, then return you to this screen"],
        'inp': ["1", "2", "3"],
        'next': ["2", "1", "1"],
        'resp': [None,
                 ["response from 2", "", ""],
                 ["response from 3", "", ""]],
        'face1': "p_ne",
        'face2': "",
        'altface1': [None, None, "p_an"],
        'altface2': [None, None, "red"]
    },
    "2": {
        "Start": ["this is screen 2", "option 1 will continue the conversation, 2 will return here", "and option 3 will send you back to phase 1"],
        'inp': ["1", "2", "3"],
        'resp': [["response from 1", "", "going to 3"],
                 None,
                 None],
        'next': ["3", "2", "1"],
        'face1': "p_an",
        'face2': "p_d1"
    },
    "3": {
        "Start": ["screen 3", "this is the last screen for this test", "1 will send you to the start, and 2 will resend you here."],
        'inp': ["1", "2"],
        'resp': [None,
                 ["", "returning to final page", ""]],
        'next': ["1", "3"],
        'face1': "p_co",
        'face2': "?1"
    },
    "4": {
        "Start": ["t", "t", "t"],
        'inp': ["1", "2", "3", "5"],
        'resp': [["response from 4", "", ""],
                 ["response from 4", "", ""],
                 ["response from 4", "", ""],
                 ["response from 4", "", ""]],
        'next': ["1", "2", "3", "5"],
        'face1': "p_em",
        'face2': "scr_1"
    },
    "5": {
        "Start": ["q", "q", "q"],
        'inp': ["1", "2", "3", "4"],
        'resp': [["response from 5", "", ""],
                 ["response from 5", "", ""],
                 ["response from 5", "", ""],
                 ["response from 5", "", ""]],
        'next': ["1", "2", "3", "4"],
        'face1': "p_wa",
        'face2': "nek"
    }
}


special = [

]
