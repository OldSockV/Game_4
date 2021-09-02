"""
Turret function i intended to place in some puzzle levels but never ended up using.
"""
import arcade


class BigGun(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.scale = 0.3
        self.active = False
        self.shootie = 1
        self.beam_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()
        self.dist = 0
        self.direct = 'Left'

    def on_draw(self):
        self.beam_list.draw()
        self.attack_list.draw()

    def update(self):
        if self.active:
            self.time += 1
            # depending on the direction of the turret, different code for beam.
            if len(self.beam_list) == 0 and len(self.attack_list) == 0:
                beam = BigBeam()
                if self.direct == 'Left':
                    beam.center_x = self.center_x-((self.dist*48)/2)
                    beam.center_y = self.center_y
                    beam.angle = 0
                elif self.direct == 'Down':
                    beam.center_x = self.center_x
                    beam.center_y = self.center_y - ((self.dist * 48) / 2)
                    beam.angle = 90
                elif self.direct == 'Right':
                    beam.center_x = self.center_x + ((self.dist * 48) / 2)
                    beam.center_y = self.center_y
                    beam.angle = 0
                beam.width = self.dist * 48
                self.beam_list.append(beam)
        for beam in self.beam_list:  # updating all attacks, slowly removing them and all that.
            beam.height += 2
            beam.alpha -= 2
            if beam.height >= 96:
                attk = BigBeam()
                attk.texture = arcade.load_texture("Player/Beam1.png")
                attk.center_x = beam.center_x
                attk.center_y = beam.center_y
                attk.angle = beam.angle
                attk.timer = 0
                attk.can_it = True
                attk.width = self.dist*48
                attk.height = 72
                # makes the hit box correct. as some issues appeared beforehand.
                attk.set_hit_box((((-self.dist*80), 110), ((-self.dist*80), -110), ((self.dist*80), -110), ((self.dist*80), 110)))
                self.attack_list.append(attk)
                beam.remove_from_sprite_lists()
                del beam
        for attk in self.attack_list:
            if not self.active:
                attk.alpha -= 20
                if attk.alpha < 30:
                    attk.remove_from_sprite_lists()
                    del attk


class BigBeam(arcade.Sprite):
    """The attack sprite of the turrets."""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Player/Beam.png")
        self.scale = 0.3
        self.height = 10
