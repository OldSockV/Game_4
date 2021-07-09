import arcade
import text
import math
import random
import conversations

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


class Conv(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.storage = conversations.enter_forest
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
        self.twice = False
        self.inactive_available = False
        self.exit_time = False

        self.conv_point = 0
        self.conv = None
        self.chatt = ChattOption()

        self.active_input = None
        self.active_output = None
        self.return_available = False  # not apliccable to real code
        self.switch_chatt = False

        self.types = {
            '1': [1, None, None],
            '2': [None, 1, None],
            '3': [None, None, 1],
            '12': [1, 1, None],
            '13': [1, None, 1],
            '23': [None, 1, 1],
            '123': [1, 1, 1]
        }
        self.effects = {
            'wobble': self.wobble,
            'shake': self.shake
        }

        self.setup()

    def wobble(self, letter):
        letter.center_y = letter.origin[1] + math.sin(letter.displacement / ((200 / letter.displacement) + 1)) * 10
        letter.displacement += 1

    def shake(self, letter):
        letter.center_y = letter.origin[1] + random.randint(-10, 10)
        letter.center_x = letter.origin[0] + random.randint(-10, 10)

    def conversation(self, face, face2, tree_name, tree_phase, effect, effect_nums):
        self.conv = self.storage(tree_name)
        self.active_icon.texture = self.chatt.face[self.storage[face]]
        self.secondary_icon.texture = self.chatt.face[self.storage[face2]]

    def on_draw(self):
        self.draw()
        self.active_icon.draw()
        self.secondary_icon.draw()
        if self.response is not None:
            self.response.draw()
            self.response1.draw()
            self.response2.draw()
        if self.printed_text is not None:
            self.printed_text.draw()
            for i in self.printed_text:
                i.center_x += random.randint(-10, 10)
                i.center_y += random.randint(-10, 10)
        self.printed_text_list.draw()

    def setup(self):
        self.printed_text_list = arcade.SpriteList()
        self.active_icon.center_x = self.center_x - 480
        self.active_icon.center_y = self.center_y + 27
        self.secondary_icon.center_x = self.center_x + 480
        self.secondary_icon.center_y = self.center_y + 27
        self.printed_text_list = arcade.SpriteList()

    def act_1(self):
        self.printed_text = text.gen_letter_list(self.output, (((self.center_x - self.width // 2 +
                                                                 ((1200 // 5) * self.select)) + 4) - 2 + 100),
                                                 (self.center_y + ((self.height * 1.5) // 20) - self.height//3)
                                                 - 5, 0.25)

    def read_list(self):
        if self.conv['inp'] is not None:
            b = len(self.conv['resp'][self.select - 1])
            if b > 3:
                self.twice = True
        else:
            self.exit_time = True

    def act_2(self):
        self.interact = True
        print("act_2")
        self.response = text.gen_letter_list(
            self.conv['resp'][self.select - 1][0],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)), (self.center_y +
                                                                         ((self.height * 1.5) // 26 * 10) -
                                                                         self.height//3), 0.25)
        p = 0
        for i in self.response:
            p+=1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response1 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][1],
            (self.center_x - self.width//2 + (self.width // 18 * 5)), (self.center_y +
                                                                       ((self.height * 1.5) // 26 * 7) -
                                                                       self.height//3), 0.25)
        p = 0
        for i in self.response1:
            p+=1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response2 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][2],
            (self.center_x - self.width//2 + (self.width // 18 * 5)), (self.center_y +
                                                                       ((self.height * 1.5) // 26 * 4) -
                                                                       self.height//3), 0.25)
        p = 0
        for i in self.response2:
            p+=1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        """if self.conv['next'][self.select - 1] is not None:
            self.conv_point = self.conv['next'][self.select - 1]
            self.switch_chatt = True"""
        self.inactive_available = True

    def in_case_two(self):
        self.interact = True
        print("in_case_two")
        self.response = text.gen_letter_list(
            self.conv['resp'][self.select - 1][3],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 10) -
                                                                     self.height//3), 0.25)
        p = 0
        for i in self.response:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response1 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][4],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 7) -
                                                                     self.height//3), 0.25)
        p = 0
        for i in self.response1:
            p+=1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response2 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][5],
            (self.center_x-self.width//2 + (self.width // 18 * 5)), (self.center_y + ((self.height * 1.5) // 26 * 4) -
                                                                     self.height//3), 0.25)
        p = 0
        for i in self.response2:
            p+=1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.twice = False

    def option_start(self):
        for i in range(len(self.conv['resp'])):
            hand = text.gen_letter_list(self.conv['resp'][i],
                                        (self.center_x-self.width//2 + (self.width / 5 * (i + 1)) + 4 + 100),
                                        (self.center_y + (self.height // 20) - self.height//3), 0.25)
            for s in hand:
                s.alpha = 100
            self.printed_text_list.extend(hand)

    def on_key_press(self, key: int):
        if not self.interact and not self.exit_time:
            if key == arcade.key.KEY_1:
                self.select = 1
                self.output = self.conv['inp'][0]
                self.act_1()
            elif key == arcade.key.KEY_2:
                self.select = 2
                self.output = self.conv['inp'][1]
                self.act_1()
            elif key == arcade.key.KEY_3 and 3 <= len(self.conv['inp'][3]):
                self.select = 3
                self.output = self.conv['inp'][2]
                self.act_1()
            elif key == arcade.key.KEY_4 and 4 <= len(self.conv['inp']):
                self.select = 4
                self.output = self.conv['inp'][3]
                self.act_1()
        if key == arcade.key.ENTER:
            if not self.interact:
                for hand in self.printed_text_list[::-1]:
                    hand.remove_from_sprite_lists()
                    del hand
                self.read_list()
            elif self.return_available:
                self.return_available = False
                self.exit_time = False
                self.option_start()
            elif self.twice:
                self.in_case_two()
            elif self.inactive_available:
                print("inactive_available (enter)")
                self.inactive_available = False
                self.interact = False
                """self.response = None
                self.response1 = None
                self.response2 = None"""
                self.option_start()
            else:
                self.act_2()

    def reset(self):
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.interact = False
        self.select = 1
        self.output = None
        self.printed_text_list = None
        print("reset")
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


