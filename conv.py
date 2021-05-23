import arcade
import text
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


class Conv(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.active_icon = arcade.Sprite()
        self.secondary_icon = arcade.Sprite()
        self.secondary_icon.var = []
        self.active_icon.var = []
        for p in range(5):
            for i in range(7):
                texture = arcade.load_texture("Text/pentagons2.png", x=480 * i, y=480*p, height=480, width=480)
                self.active_icon.var.append(texture)
                self.secondary_icon.var.append(texture)
        self.active_icon.texture = self.active_icon.var[random.randint(0, 34)]
        self.secondary_icon.texture = self.secondary_icon.var[random.randint(0, 34)]
        self.active_icon.scale = 0.3
        self.secondary_icon.scale = 0.3
        self.interact = False
        self.printed_text = None

        self.texture = arcade.load_texture("Text/textbox_self1.png")
        self.scale = 0.3
        self.select = 1
        self.output = None
        self.printed_text_list = None
        self.response = None
        self.response1 = None
        self.response2 = None
        self.chatt = ChattOption()
        self.twice = False
        self.inactive_available = False
        self.exit_time = False

        self.conv_point = 0
        self.conv = None
        self.conv = self.chatt.e["test1"]

        self.active_input = None
        self.active_output = None
        self.return_available = False  # not apliccable to real code
        self.switch_chatt = False

        ''' ----------------- CONVERSATION DICTIONARY USED ----------------- '''
        self.location = 'bad'

        self.setup()

    def setup(self):
        self.reset()
        self.printed_text_list = arcade.SpriteList()
        self.active_icon.center_x = self.center_x - 480
        self.active_icon.center_y = self.center_y + 27
        self.secondary_icon.center_x = self.center_x + 480
        self.secondary_icon.center_y = self.center_y + 27
        self.printed_text_list = arcade.SpriteList()
        self.option_start()

    def reset(self):
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.interact = False
        self.printed_text = None
        self.select = 1
        self.output = None
        self.printed_text_list = None
        self.response = None
        self.response1 = None
        self.response2 = None
        self.twice = False
        self.inactive_available = False
        self.exit_time = False
        self.conv_point = 0
        self.active_input = None
        self.active_output = None
        self.return_available = False  # not apliccable to real code
        self.switch_chatt = False

    def on_draw(self):
        self.draw()
        self.active_icon.draw()
        self.secondary_icon.draw()
        if self.response is not None:
            self.response.draw()
            self.response1.draw()
            self.response2.draw()
        else:
            if self.printed_text is not None:
                self.printed_text.draw()
            self.printed_text_list.draw()

    def on_key_press(self, key: int):
        if key == arcade.key.E:
            if self.active_icon.texture == self.active_icon.var[0]:
                self.active_icon.texture = self.active_icon.var[1]
            else:
                self.active_icon.texture = self.active_icon.var[0]
        if key == arcade.key.R:
            self.active_icon.texture = arcade.load_texture("Text/pentagons2.png", x=0, y=0,
                                                           height=480, width=480)
        elif key == arcade.key.T:
            self.active_icon.texture = self.active_icon.var[random.randint(0, 34)]
        if not self.interact and not self.exit_time:
            if key == arcade.key.KEY_1:
                self.select = 1
                self.output = self.conv['dialog1'][f'inp{self.conv_point}'][0]
                self.act_1()
            elif key == arcade.key.KEY_2:
                self.select = 2
                self.output = self.conv['dialog1'][f'inp{self.conv_point}'][1]
                self.act_1()
            elif key == arcade.key.KEY_3 and 3 <= len(self.conv['dialog1'][f'inp{self.conv_point}']):
                self.select = 3
                self.output = self.conv['dialog1'][f'inp{self.conv_point}'][2]
                self.act_1()
            elif key == arcade.key.KEY_4 and 4 <= len(self.conv['dialog1'][f'inp{self.conv_point}']):
                self.select = 4
                self.output = self.conv['dialog1'][f'inp{self.conv_point}'][3]
                self.act_1()
        if key == arcade.key.ENTER:
            if not self.interact:
                for hand in self.printed_text_list[::-1]:
                    hand.remove_from_sprite_lists()
                    del hand
                self.read_list()
            if self.switch_chatt:
                self.cycle_conv()
                self.switch_chatt = False
            elif self.return_available:
                self.return_available = False
                self.exit_time = False
                self.option_start()
            elif self.exit_time:
                self.exit_conv()
            elif self.twice:
                self.in_case_two()
            elif self.inactive_available:
                self.inactive_available = False
                self.interact = False
                self.response = None
                self.response1 = None
                self.response2 = None
                self.option_start()
            else:
                self.act_2()
        if key == arcade.key.I:
            self.cycle_conv()
        if key == arcade.key.KEY_9:
            self.active_input = self.conv['dialog1']["inp0"]
            self.active_output = self.conv['dialog1']["out0"]
        if key == arcade.key.KEY_5 or key == arcade.key.KEY_6 or key == arcade.key.KEY_7:
            if key == arcade.key.KEY_5:
                self.conv_point = 0
            if key == arcade.key.KEY_6:
                self.conv_point = 1
            if key == arcade.key.KEY_7:
                self.conv_point = 2
            for hand in self.printed_text_list[::-1]:
                hand.remove_from_sprite_lists()
                del hand
            self.exit_conv()
            self.option_start()
            self.return_available = False
            self.exit_time = False
            self.select = 1
            self.output = self.conv['dialog1'][f'inp{self.conv_point}'][0]
            self.act_1()

    def act_1(self):
        self.printed_text = text.gen_letter_list(self.output, (((self.center_x - self.width // 2 +
                                                                 ((1200 // 5) * self.select)) + 4) - 2 + 100),
                                                 (self.center_y + ((self.height * 1.5) // 20) - self.height//3)
                                                 - 5, 0.25)

    def read_list(self):
        if self.conv['output1'][f'out{self.conv_point}'][self.select - 1] is not None:
            b = len(self.conv['output1'][f'out{self.conv_point}'][self.select - 1])
            if b > 3:
                self.twice = True
        else:
            self.exit_time = True

    def cycle_conv(self):
        for hand in self.printed_text_list[::-1]:
            hand.remove_from_sprite_lists()
            del hand
        self.exit_conv()
        self.option_start()
        self.return_available = False
        self.exit_time = False
        self.select = 1
        self.output = self.conv['dialog1'][f'inp{self.conv_point}'][0]
        self.act_1()

    def act_2(self):
        self.interact = True
        self.response = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][0],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 10) - self.height//3), 0.25)
        self.response1 = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][1],
            (self.center_x - self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 7) - self.height//3), 0.25)
        self.response2 = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][2],
            (self.center_x - self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 4) - self.height//3), 0.25)
        if self.conv['continuous'][f'inp{self.conv_point}'][self.select - 1] is not None:
            self.conv_point = self.conv['continuous'][f'inp{self.conv_point}'][self.select - 1]
            self.switch_chatt = True
        self.inactive_available = True

    def in_case_two(self):
        self.interact = True
        self.response = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][3],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 10) - self.height//3), 0.25)
        self.response1 = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][4],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 7) - self.height//3), 0.25)
        self.response2 = text.gen_letter_list(
            self.conv['output1'][f'out{self.conv_point}'][self.select - 1][5],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 4) - self.height//3), 0.25)
        self.twice = False

    def option_start(self):
        for i in range(len(self.conv['dialog1'][f'inp{self.conv_point}'])):
            hand = text.gen_letter_list(self.conv['dialog1'][f'inp{self.conv_point}'][i],
                                        (self.center_x-self.width//2 + (self.width / 5 * (i + 1)) + 4 + 100),
                                        (self.center_y + (self.height // 20) - self.height//3), 0.25)
            for s in hand:
                s.alpha = 100
            self.printed_text_list.extend(hand)

    def exit_conv(self):
        self.inactive_available = False
        self.interact = False
        self.response = None
        self.response1 = None
        self.response2 = None
        self.printed_text = None

        self.return_available = True  # not apliccable to real code


class ChattOption:
    def __init__(self):
        self.faces = []
        for i in range(5):
            for b in range(7):
                texture = arcade.load_texture("Text/pentagons2.png", x=480*b, y=480*i,
                                              height=480, width=480, mirrored=False)
                self.faces.append(texture)
        self.face = {
            "p_ne": self.faces[0],
            "p_an": self.faces[1],
            "p_co": self.faces[2],
            "p_em": self.faces[3],
            "p_wa": self.faces[4],
            "p_pi": self.faces[5],
            "p_ha": self.faces[6],

            "p_fl": self.faces[13],
            "p_d1": self.faces[8],
            "p_d2": self.faces[9],
            "p_d3": self.faces[10],

            "aed": self.faces[14],
            "bl_a": self.faces[15],
            "da_a": self.faces[16],
            "smo1": self.faces[17],
            "smo2": self.faces[18],
            "and": self.faces[19],

            "red": self.faces[21],
            "gre": self.faces[22],
            "yel": self.faces[23],
            "?1": self.faces[24],
            "?2": self.faces[25],

            "scr_1": self.faces[28],
            "scr_2": self.faces[29],
            "scr_3": self.faces[30],
            "voi": self.faces[31],
            "skel1": self.faces[32],
            "skel2": self.faces[33],
            "nek": self.faces[34]
        }
        self.e = {
            'test1': {
                "dialog1": {
                    "inp0": ["Lore", "Double", "Continue", "Leave"],
                    "inp1": ["Continue2", "Return", "But what about..."],
                    "inp2": ["1", "2", "Return"],

                    "inp3": ["Huh, ok"],
                    "inp4": ["double", "single1", "single2", "NVM"],
                },
                "continuous": {
                    "inp0": [4, None, 1, None],
                    "inp1": [2, 0, 3],
                    "inp2": [None, None, 0],

                    "inp3": [2],
                    "inp4": [None, None, None, 0]
                },
                "output1": {
                    "out0": [["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", ",.?!          spacing"],
                             ["", "continuation line", "",
                              "Test for double lined text.", "After this string there will", "be more text:"],
                             ["What, you egg?", "He stabs him.", ""], None],
                    "out1": [["", "", "       go away",
                              "", "    youre stinky", ""],
                             ["", "", ""], ["Heres an example of some", "funky stuff.", ""]],
                    "out2": [["            you", "         have", "      gay"],
                             ["              the", "you                house", "  e n t e r"],
                             ["  p ", "    a", "        n         t"]],

                    'out3': [["", "", "       go away",
                              "", "    youre stinky", ""]],  # self.e['test1']['output1']["out1"][0],
                    'out4': [["example of two spaced dialogue:", "       2", "",
                              "example of two spaced dialogue:", "       1", ""],
                             ["example of single spaced dialogue", "      1", ""],
                             ["example of single spaced dialogue", "      2", ""],
                             ["   Anything else?", "", ""]]
                },
                "face": {
                    "out0": [self.faces[5], self.faces[0], self.faces[8], self.faces[16]],
                    "out1": [],
                    "out2": [],
                    "out3": [],
                    #  "out4": [self.faces["p_an"], self.faces["red"], self.faces['scr_1'], self.faces["aed"]]
                }
            },
            'bad': {
                "dialog1": {
                    "inp0": ["hi", "bye"],
                },
                "continuous": {
                    "inp0": [None, None],
                },
                "output1": {
                    "out0": [["hello!", "", ""], None],
                }
            }
        }


class Target:
    def __init__(self):
        self.res = {
            1: "1",
            2: "2",
            3: "3",
            4: "4"
        }
