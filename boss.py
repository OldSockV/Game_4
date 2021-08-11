import arcade
import math
import random


class Boss(arcade.Sprite):
    """The final boss of the game"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/eye thingy-Sheet.png", x=0, y=0, height=384, width=384)
        self.phase = 1
        self.alpha = 1
        self.skin = skin()
        self.gun = Gun()
        self.t = -200
        self.beam_list = None
        self.attack_list = None
        self.setup()
        self.att_don = 0
        self.round = 0
        self.win = False
        self.angletoplayer = 0
        self.start = False

    def setup(self):
        self.beam_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()
        self.skin.center_x = self.center_x
        self.skin.center_y = self.center_y

    def on_draw(self):
        self.draw()
        self.gun.draw()
        self.skin.draw()
        if self.beam_list is not None:
            self.beam_list.draw()
        if self.attack_list is not None:
            self.attack_list.draw()

    def update(self):
        """
        Basically, the boss cycles through phases moving through its attacks, until it reaches phase 3,
        then moves on to the next round, where difficulty is increased.
        Once it reaches a specific round and phase, the boss will stop fighting. and the exit will open.
        """
        self.t += 1
        self.skin.center_x = self.center_x
        self.skin.center_y = self.center_y
        self.gun.center_x = self.center_x + math.cos(math.radians(self.angletoplayer)) * 20
        self.gun.center_y = self.center_y + math.sin(math.radians(self.angletoplayer)) * 20
        self.gun.angle = 0
        if self.att_don > 100:
            self.att_don = 0
            print("round", self.round, "| phase", self.phase)
            if self.round == 1 and self.phase == 2:
                self.win = True
                print("game end")
                self.phase = -1
                self.round = -1
            if not self.phase == 3:
                self.phase += 1
            else:
                self.phase = 1
                self.round += 1
        if not self.win:
            if self.t % 40 == 1 and (self.phase == 1 or self.round >= 1) and self.t > 0:
                beam = Beam()
                beam.center_x = self.center_x + math.cos(math.radians(self.angletoplayer)) * 40
                beam.center_y = self.center_y + math.sin(math.radians(self.angletoplayer)) * 40
                beam.angle = self.angletoplayer
                self.beam_list.append(beam)
                if self.phase == 1:
                    self.att_don += 10
            if self.t % 10 == 1 and (self.phase == 2 or self.round >= 2):
                core = Beam()
                core.center_y = self.center_y - 600
                core.center_x = random.randint(int(self.center_x - 1400), int(self.center_x + 1400))
                core.angle = 90
                self.beam_list.append(core)
                self.att_don += 2
            if self.t % 30 == 1 and (self.phase == 3 or self.round >= 3):
                core = Beam()
                core.center_y = self.center_y + random.randint(-14, 10) * 40
                core.center_x = 0
                self.beam_list.append(core)
                if not self.round == 3:
                    self.att_don += 7
        for beam in self.beam_list:
            beam.scale += 0.4
            beam.alpha -= 2
            if beam.scale >= 20:
                attk = Beam()
                attk.center_x = beam.center_x
                attk.center_y = beam.center_y
                attk.angle = beam.angle
                attk.can_it = True
                attk.texture = arcade.load_texture("Player/Sprite-0001.png")
                attk.scale = 10
                self.attack_list.append(attk)
                beam.remove_from_sprite_lists()
                del beam
        for attk in self.attack_list:
            attk.alpha -= 20
            if attk.alpha < 30:
                attk.remove_from_sprite_lists()
                del attk

    def reset(self):
        """Turns off the boss for when you win, if you were to move between levels before the end of the fight."""
        for i in self.attack_list[::-1]:
            i.remove_from_sprite_lists()
            del i
        for beam in self.beam_list[::-1]:
            beam.remove_from_sprite_lists()
            del beam
        self.phase = 1
        self.t = -200
        self.att_don = 0
        self.round = 0
        self.win = False
        self.angletoplayer = 0


class Gun(arcade.Sprite):
    """The Eye of the boss, which shoots the targeting lazers"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/eye thingy-Sheet.png", x=384, y=0, height=384, width=384)
        self.alpha = 1


class skin(arcade.Sprite):
    """The gray exterior shell of the boss"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/eye thingy-Sheet.png", x=384*2, y=0, height=384, width=384)


class Beam(arcade.Sprite):
    """The beam attack produced by the boss"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/beam.png")
        self.scale = 0.3
