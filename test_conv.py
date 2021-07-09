import arcade
import text

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((26, 21, 24))
        self.printed_text = None
        self.printed_text1 = None
        self.printed_text2 = None
        self.printed_text_list = None
        self.active_icon = arcade.Sprite()
        self.active_icon.var = []
        for i in range(2):
            texture = arcade.load_texture("Text/pentagons.png", x=480*2, y=480*2+480*i, height=480, width=480)
            self.active_icon.var.append(texture)
        self.active_icon.texture = self.active_icon.var[0]
        self.active_icon.scale = 0.3
        self.interact = False
        self.printed_text = None

        self.box = arcade.Sprite()
        self.box.texture = arcade.load_texture("Text/textbox_self1.png")
        self.box.scale = 0.3
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
        self.conv = self.chatt.e['test1']
        self.b = None
        
        self.active_input = None
        self.active_output = None
        self.return_available = False  # not apliccable to real code
        self.switch_chatt = False

        self.setup()

    def setup(self):
        self.printed_text_list = arcade.SpriteList()
        self.box.center_x = SCREEN_WIDTH//2
        self.box.center_y = SCREEN_HEIGHT//4
        self.active_icon.center_x = self.box.center_x - 480
        self.active_icon.center_y = self.box.center_y + 27
        self.printed_text_list = arcade.SpriteList()
        self.option_start()

    def on_draw(self):
        arcade.start_render()
        self.box.draw()
        self.active_icon.draw()
        if self.response is not None:
            self.response.draw()
            self.response1.draw()
            self.response2.draw()
        else:
            if self.printed_text is not None:
                self.printed_text.draw()
            self.printed_text_list.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.E:
            if self.active_icon.texture == self.active_icon.var[0]:
                self.active_icon.texture = self.active_icon.var[1]
            else:
                self.active_icon.texture = self.active_icon.var[0]
        if key == arcade.key.R:
            self.active_icon.texture = arcade.load_texture("Text/pentagons.png", x=0, y=0,
                                                           height=480, width=480)
        elif key == arcade.key.T:
            self.active_icon.texture = arcade.load_texture("Text/pentagons.png", x=480*2, y=480,
                                                           height=480, width=480)
        if not self.interact and not self.exit_time:
            if key == arcade.key.KEY_1:
                self.select = 1
                self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][0]
                self.act_1()
            elif key == arcade.key.KEY_2:
                self.select = 2
                self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][1]
                self.act_1()
            elif key == arcade.key.KEY_3 and 3 <= len(self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}']):
                self.select = 3
                self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][2]
                self.act_1()
            elif key == arcade.key.KEY_4 and 4 <= len(self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}']):
                self.select = 4
                self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][3]
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
                if self.chatt.e['test1']['output1'][f'out{self.select}'] is not None:
                    self.b = self.chatt.e['test1']['output1'][f'out{self.select}']
                self.b = None
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
            self.active_input = self.chatt.e['test1']['dialog1']["inp0"]
            self.active_output = self.chatt.e['test1']['dialog1']["out0"]
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
            self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][0]
            self.act_1()

    def act_1(self):
        self.printed_text = text.gen_letter_list(self.output, ((SCREEN_WIDTH // 5 * self.select) + 4) - 2 + 100,
                                                 (SCREEN_HEIGHT // 20) + 2, 0.25, 36)

    def read_list(self):
        if self.chatt.e['test1']['output1'][f'out{self.conv_point}'][self.select-1] is not None:
            b = len(self.chatt.e['test1']['output1'][f'out{self.conv_point}'][self.select-1])
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
        self.output = self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][0]
        self.act_1()

    def act_2(self):
        self.interact = True
        self.response = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                             [self.select-1][0],
                                             SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 10, 0.25, 36)
        self.response1 = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                              [self.select - 1][1],
                                              SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 7, 0.25, 36)
        self.response2 = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                              [self.select - 1][2],
                                              SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 4, 0.25, 36)
        if self.chatt.e['test1']['continuous'][f'inp{self.conv_point}'][self.select-1] is not None:
            self.conv_point = self.chatt.e['test1']['continuous'][f'inp{self.conv_point}'][self.select-1]
            self.switch_chatt = True
        self.inactive_available = True

    def in_case_two(self):
        self.interact = True
        self.response = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                             [self.select - 1][3],
                                             SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 10, 0.25, 36)
        self.response1 = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                              [self.select - 1][4],
                                              SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 7, 0.25, 36)
        self.response2 = text.gen_letter_list(self.chatt.e['test1']['output1'][f'out{self.conv_point}']
                                              [self.select - 1][5],
                                              SCREEN_WIDTH // 18 * 5, SCREEN_HEIGHT // 26 * 4, 0.25, 36)
        self.twice = False

    def option_start(self):
        for i in range(len(self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'])):
            hand = text.gen_letter_list(self.chatt.e['test1']['dialog1'][f'inp{self.conv_point}'][i],
                                        SCREEN_WIDTH/5*(i+1) + 4+100,
                                        SCREEN_HEIGHT // 20, 0.25, 36)
            for s in hand:
                s.alpha = 100
            self.printed_text_list.extend(hand)

    def exit_conv(self):
        self.b = None
        self.inactive_available = False
        self.interact = False
        self.response = None
        self.response1 = None
        self.response2 = None
        self.printed_text = None

        self.return_available = True  # not apliccable to real code


class ChattOption:
    def __init__(self):
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

                }
            },
            'bad': ('yyyyyy', "ssss", "sss")
        }


class Target:
    def __init__(self):
        self.res = {
            1: "1",
            2: "2",
            3: "3",
            4: "4"
        }


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "GAME")
    game = Game()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
