import arcade
import text
# import math
import random
import conversations

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


class Conv(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.storage = conversations.enter_level["S6_1"]
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.active_icon = arcade.Sprite()
        self.secondary_icon = arcade.Sprite()
        self.secondary_icon.var = []
        self.active_icon.var = []

        # Loads all the face icons in for the conversations as a list.
        for p in range(5):
            for i in range(7):
                texture = arcade.load_texture("Text/pentagons2.png", x=480 * i, y=480 * p, height=480, width=480)
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
        self.twice_fin = False
        self.inactive_available = False
        self.exit_time = False
        self.active_input = None
        self.active_output = None
        self.switch_chatt = False

        self.conv = None
        self.chatt = ChattOption()
        self.conv = self.storage['1']

    def conversation(self, tree_name):
        """ Controlls conversation progression """
        # Checks the name of the tree name that was issued,
        # then runs through that branches dictionary, finding all the
        # details needed to set up the chatt accordingly.
        if self.conv["next"][self.select - 1] is not None and self.switch_chatt:
            self.conv = self.storage[tree_name]
            self.switch_chatt = False
        # checks the icons to be used.
        self.active_icon.texture = self.chatt.face[self.conv['face1']]
        self.secondary_icon.texture = self.chatt.face[self.conv['face2']]
        # if i leave the icon input blank it will select the correct texture so that only the sides of the box that has
        # a face will have a border around it.
        if self.conv['face1'] != '' and self.conv['face2'] != '':
            self.texture = arcade.load_texture("Text/textbox_self_mult1.png")
        elif self.conv['face2'] == '' and self.conv['face1'] != '':
            self.texture = arcade.load_texture("Text/textbox_self_mult2.png")
        else:
            self.texture = arcade.load_texture("Text/textbox_self_mult3.png")
        self.twice_fin = False
        self.select = 1
        self.output = self.conv['inp'][0]
        self.act_1()
        self.remove_hand()
        self.read_list()
        self.act_2()
        self.option_start()

    def remove_hand(self):
        """ Code that removes dialogue choice icons """
        for hand in self.printed_text_list[::-1]:
            hand.remove_from_sprite_lists()
            del hand

    def on_draw(self):
        self.draw()
        self.active_icon.draw()
        self.secondary_icon.draw()
        # makes things only draw when they are actual text to stop crashes.
        if self.response is not None:
            self.response.draw()
            self.response1.draw()
            self.response2.draw()
        if self.printed_text is not None:
            self.printed_text.draw()
        if self.printed_text_list is not None:
            self.printed_text_list.draw()

    def setup(self, tree, enter):
        self.reset()
        # selecting the different dictionaries depeding on the type of information needed.
        if enter == 'enter':
            self.storage = conversations.enter_level[tree]
        elif enter == 'talk':
            self.storage = conversations.talking[tree]
        elif enter == 'invest':
            self.storage = conversations.investigate[tree]
        self.conv = self.storage["1"]
        self.printed_text_list = arcade.SpriteList()
        self.active_icon.center_x = self.center_x - 480
        self.active_icon.center_y = self.center_y + 27
        self.secondary_icon.center_x = self.center_x + 480
        self.secondary_icon.center_y = self.center_y + 27
        self.printed_text_list = arcade.SpriteList()
        self.conversation('1')
        self.option_start()
        self.read_list()
        self.interact = False

    def act_1(self):
        """Changing the selected chatt option"""
        self.printed_text = text.gen_letter_list(self.output, (((self.center_x - self.width // 2 +
                                                                 ((1200 // 5) * self.select)) + 4) - 2 + 100),
                                                 (self.center_y + ((self.height * 1.5) // 20) - self.height // 3)
                                                 - 5, 0.25)

    def read_list(self):
        """Reads the response and goes through a second check if the response requires more than one block of text"""
        if self.conv['resp'] is not None:
            self.twice = True

    def act_2(self):
        """ Reads the response list and generates up to three lines of text that is presented in the dialogue box """
        self.interact = True
        self.remove_hand()
        self.output = ""
        self.response = text.gen_letter_list(
            self.conv['start'][0],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)), (self.center_y +
                                                                         ((self.height * 1.5) // 26 * 10) -
                                                                         self.height // 3), 0.25)
        p = 0
        for i in self.response:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p

        self.response1 = text.gen_letter_list(
            self.conv['start'][1],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)), (self.center_y +
                                                                         ((self.height * 1.5) // 26 * 7) -
                                                                         self.height // 3), 0.25)
        p = 0
        for i in self.response1:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p

        self.response2 = text.gen_letter_list(
            self.conv['start'][2],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)), (self.center_y +
                                                                         ((self.height * 1.5) // 26 * 4) -
                                                                         self.height // 3), 0.25)
        p = 0
        for i in self.response2:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.inactive_available = True

    def in_case_two(self):
        """if the response is two blocks long this makes the first block print before the rest of the response"""
        self.remove_hand()
        self.interact = True
        if self.conv['face1'] != '':
            one = True
        else:
            one = False
        if self.conv['face2'] != '':
            two = True
        else:
            two = False
        # checks if the two parts of the text should have different faces.
        if "altface1" in self.conv:
            if self.conv["altface1"][self.select - 1] is not None:
                self.active_icon.texture = self.chatt.face[self.conv["altface1"][self.select - 1]]
                if self.conv['altface1'] != '':
                    one = True
                else:
                    one = False
        if "altface2" in self.conv:
            if self.conv["altface2"][self.select - 1] is not None:
                self.secondary_icon.texture = self.chatt.face[self.conv["altface2"][self.select - 1]]
                if self.conv['altface2'] != '':
                    two = True
                else:
                    two = False
        # changes the textbox borders according to the new faces.
        if one and two:
            self.texture = arcade.load_texture("Text/textbox_self_mult1.png")
        elif one and not two:
            self.texture = arcade.load_texture("Text/textbox_self_mult2.png")
        else:
            self.texture = arcade.load_texture("Text/textbox_self_mult3.png")

        # sets the new conversation
        self.response = text.gen_letter_list(
            self.conv['resp'][self.select - 1][0],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)),
            (self.center_y + ((self.height * 1.5) // 26 * 10) -
             self.height // 3), 0.25)
        p = 0
        for i in self.response:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response1 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][1],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)),
            (self.center_y + ((self.height * 1.5) // 26 * 7) -
             self.height // 3), 0.25)
        p = 0
        for i in self.response1:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.response2 = text.gen_letter_list(
            self.conv['resp'][self.select - 1][2],
            (self.center_x - self.width // 2 + (self.width // 18 * 5)),
            (self.center_y + ((self.height * 1.5) // 26 * 4) -
             self.height // 3), 0.25)
        p = 0
        for i in self.response2:
            p += 1
            i.origin = [i.center_x, i.center_y]
            i.displacement = p
        self.twice = False
        self.twice_fin = True

    def option_start(self):
        """ Prints the dialogue options for the player """
        for i in range(len(self.conv['inp'])):
            hand = text.gen_letter_list(self.conv['inp'][i],
                                        (self.center_x - self.width // 2 + (self.width / 5 * (i + 1)) + 4 + 100),
                                        (self.center_y + (self.height // 20) - self.height // 3), 0.25)
            for s in hand:
                s.alpha = 100
            self.printed_text_list.extend(hand)

    def on_key_press(self, key: int):
        if not self.interact:
            # switching the selected dialogue choice with buttons 1-4
            if key == arcade.key.KEY_1:
                self.select = 1
                self.output = self.conv['inp'][0]
                self.act_1()
            elif key == arcade.key.KEY_2 and 2 <= len(self.conv['inp']):
                self.select = 2
                self.output = self.conv['inp'][1]
                self.act_1()
            elif key == arcade.key.KEY_3 and 3 <= len(self.conv['inp']):
                self.select = 3
                self.output = self.conv['inp'][2]
                self.act_1()
            elif key == arcade.key.KEY_4 and 4 <= len(self.conv['inp']):
                self.select = 4
                self.output = self.conv['inp'][3]
                self.act_1()
        if key == arcade.key.ENTER or key == arcade.key.E:
            # when enter or E is pressed, the chosen dialogue choice continues the conversation
            if (self.conv['resp'][self.select - 1] is not None) and self.twice_fin is False:
                self.in_case_two()
            elif self.conv['next'][self.select - 1] == "leave":
                self.exit_time = True
            else:
                self.switch_chatt = True
                self.twice_fin = False
                self.conversation(tree_name=self.conv['next'][self.select - 1])
                self.interact = False

    def reset(self):
        """ Resets the text functions to default """
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.interact = False
        self.select = 1
        self.output = None
        self.printed_text_list = None
        self.response = None
        self.response1 = None
        self.response2 = None
        self.twice = False
        self.inactive_available = False
        self.active_input = None
        self.active_output = None
        self.switch_chatt = False


class ChattOption:
    """ Holds all images of the Face-Icons
    and assigns them to a dictionary with a name to be used in conversation code """
    def __init__(self):
        self.faces = []
        for y in range(5):
            for x in range(7):
                texture = arcade.load_texture("Text/pentagons2.png", x=480 * x, y=480 * y,
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

            "": self.faces[12],

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
