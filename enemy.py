import arcade
import math
import random
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
JUMP_SPEED = 14
GRAVITY = 0


class TestEnemy(arcade.Sprite):
    def __init__(self, player):
        super().__init__()
        self.cur_texture = 0
        self.flap = []
        self.flap2 = []
        s = random.randint(1, 6)
        for i in range(2):
            texture = arcade.load_texture("Spritesheets/enemy1-Sheet.png", x=(640*s-320)+i*320, y=0, height=320,
                                          width=320)
            self.flap.append(texture)
        for i in range(2):
            texture = arcade.load_texture("Spritesheets/enemy1-Sheet.png", x=(640*s-320)+i*320, y=0, height=320,
                                          width=320, mirrored=True)
            self.flap2.append(texture)
        self.texture = self.flap[0]
        self.player = player
        self.mirrored = False
        self.scale = 0.4
        self.t = 0

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture >= 2 * 8:
            self.cur_texture = 0
        if self.mirrored:
            self.texture = self.flap[self.cur_texture // 8]
        else:
            self.texture = self.flap2[self.cur_texture // 8]

    def update(self):
        self.t += 1
        if self.t >= 20:
            diff_x = self.center_x - self.player.center_x
            diff_y = self.center_y - self.player.center_y
            if diff_x > 0:
                self.mirrored = True
            else:
                self.mirrored = False
            rad = math.atan2(diff_y, diff_x)
            self.change_x = math.cos(rad) * -4 + random.randint(-4, 4)
            self.change_y = math.sin(rad) * -4 + random.randint(-4, 4)
            self.t = 0
