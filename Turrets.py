import arcade
import math
import random


class BigGun(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Turret_4.png")
        self.time = 0
        self.scale = 0.3
        self.shootie = 1
        self.active = False
        self.beam_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

    def on_draw(self):
        self.beam_list.draw()
        self.attack_list.draw()

    def update(self):
        self.time += 1
        print("-Tick-", self.time)
        if self.time % 100 == 1:
            self.shootie *= -1
        if self.time % 15 == 1 and self.shootie == 1:
            beam = BigBeam()
            beam.center_x = self.center_x
            beam.center_y = self.center_y
            beam.angle = self.angle - 180
            self.beam_list.append(beam)
            print("--------SPAWNED BEAM---------")
        for beam in self.beam_list:
            beam.scale += 0.4
            beam.alpha -= 2
            if beam.scale >= 20:
                attk = BigBeam()
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


class BigBeam(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Enemy/beam.png")
        self.scale = 0.3
