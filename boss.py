import arcade
import math
import random


class Boss(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/b2.png")
        self.scale = 0.3
        self.phase = 1
        self.gun = Gun()
        self.t = -200
        self.beam_list = None
        self.attack_list = None
        self.setup()
        self.att_don = 0
        self.round = 0

    def setup(self):
        self.beam_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

    def on_draw(self):
        self.draw()
        self.gun.draw()
        if self.beam_list is not None:
            self.beam_list.draw()
        if self.attack_list is not None:
            self.attack_list.draw()

    def update(self):
        self.t += 1
        if self.att_don > 100:
            self.att_don = 0
            if not self.phase == 3:
                self.phase += 1
            elif self.round == 3 and self.phase == 2:
                self.phase = -1
                self.round = -1
            else:
                self.phase = 1
                self.round += 1
        if self.t % 40 == 1 and (self.phase == 1 or self.round >= 1) and self.t > 0:
            beam = Beam()
            beam.center_x = self.center_x + math.cos(math.radians(self.gun.angle)) * 30
            beam.center_y = self.center_y + math.sin(math.radians(self.gun.angle)) * 30
            beam.angle = self.gun.angle
            self.beam_list.append(beam)
            if self.phase == 1:
                self.att_don += 10
        if self.t % 10 == 1 and (self.phase == 2 or self.round >= 2):
            core = Beam()
            core.center_y = 1000
            core.center_x = random.randint(400, 4208)
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


class Gun(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/b3.png")
        self.scale = 0.3


class Beam(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/beam.png")
        self.scale = 0.3
