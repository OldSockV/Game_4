import arcade
import math
import random
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
MOVEMENT_SPEED = 14
DEAD_ZONE = 2
JUMP_SPEED = 12
GRAVITY = 0


class TestPlayer(arcade.Sprite):
    """Contains the player class and all its features"""
    def __init__(self):
        super().__init__()
        self.cur_texture = 0
        self.cur_texture2 = 0
        self.health = 4
        self.gun = Gun()
        self.A = False
        self.D = False
        self.W = False
        self.attacking = False
        self.grapling = False
        self.beaning = False
        self.beanter = False
        self.button = False
        self.roll = False
        self.b = False
        self.Q = False
        self.S = False
        self.E = False
        self.anti_e = False
        self.time = 0
        self.tim = 0
        self.scale = 0.29
        self.texture = arcade.load_texture("Player/guy.png")
        self.cur_texture = 0
        self.bullet_list = None
        self.effect_list = None

        # puts all the textures into lists in Left / Right configuration for easy use
        self.idle = []
        self.idleR = []
        for i in range(4):
            texture = arcade.load_texture("Spritesheets/spec-Sheet.png", x=i*320, y=0,
                                          width=320, height=320)
            self.idleR.append(texture)
        self.idleL = []
        for i in range(4):
            texture = arcade.load_texture("Spritesheets/spec-Sheet.png", x=i*320, y=0,
                                          width=320, height=320, mirrored=True)
            self.idleL.append(texture)

        self.walking = []
        self.walkingR = []
        for i in range(8):
            texture = arcade.load_texture("Spritesheets/spec-Sheet_walk.png", x=i*320, y=0,
                                          width=320, height=320)
            self.walkingR.append(texture)
        self.walkingL = []
        for i in range(8):
            texture = arcade.load_texture("Spritesheets/spec-Sheet_walk.png", x=i*320, y=0,
                                          width=320, height=320, mirrored=True)
            self.walkingL.append(texture)

        self.running = []
        self.runningR = []
        for i in range(6):
            texture = arcade.load_texture("Spritesheets/run(nocoat)2.png", x=i*320, y=0,
                                          width=320, height=320)
            self.runningR.append(texture)
        self.runningL = []
        for i in range(6):
            texture = arcade.load_texture("Spritesheets/run(nocoat)2.png", x=i*320, y=0,
                                          width=320, height=320, mirrored=True)
            self.runningL.append(texture)

        self.sliding = []
        self.slidingR = []
        for i in range(6):
            texture = arcade.load_texture("Spritesheets/Glide_spec.png",
                                          x=i*320, y=0, width=320, height=320, mirrored=False)
            self.slidingR.append(texture)
        self.slidingL = []
        for i in range(6):
            texture = arcade.load_texture("Spritesheets/Glide_spec.png",
                                          x=i*320, y=0, width=320, height=320, mirrored=True)
            self.slidingL.append(texture)
        self.climbing = []
        self.climbingR = []
        for i in range(9):
            texture = arcade.load_texture("Spritesheets/Climb-Sheet.png",
                                          x=i * 800, y=0, width=800, height=960, mirrored=False)
            self.climbingR.append(texture)
        self.climbingL = []
        for i in range(9):
            texture = arcade.load_texture("Spritesheets/Climb-Sheet.png",
                                          x=i * 800, y=0, width=800, height=960, mirrored=True)
            self.climbingL.append(texture)

        self.jump_text = []
        texture1 = arcade.load_texture("Player/jump.png", mirrored=False)
        texture2 = arcade.load_texture("Player/jump.png", mirrored=True)
        self.jump_text.append(texture1)
        self.jump_text.append(texture2)

        self.running.append(self.runningR)
        self.running.append(self.runningL)
        self.walking.append(self.walkingR)
        self.walking.append(self.walkingL)
        self.idle.append(self.idleR)
        self.idle.append(self.idleL)
        self.sliding.append(self.slidingR)
        self.sliding.append(self.slidingL)
        self.climbing.append(self.climbingR)
        self.climbing.append(self.climbingL)

        self.x = 0
        self.y = 0
        self.x_t = 0
        self.y_t = 0
        self.FACING = 0
        self.is_climbing = False

        self.interacting = False

        self.workpleasex = 0
        self.workpleasey = 0

        self.setup()

    def update_animation(self, delta_time: float = 1/60):
        """ updates the animation that is appropriate for the situation """
        # uses different counters for different animations
        self.cur_texture += 1
        self.cur_texture2 += 1
        if self.cur_texture >= 8 * 4:
            self.cur_texture = 0
        if self.cur_texture2 >= 6 * 6:
            self.cur_texture2 = 0
        if self.change_x > 1:
            self.FACING = 0
        elif self.change_x < -1:
            self.FACING = 1
        if self.beanter:
            self.texture = arcade.load_texture("Player/slide.png")
        elif self.beaning:
            self.texture = arcade.load_texture("Player/slide.png", mirrored=True)
        elif not self.physics_engines[0].can_jump() and abs(self.change_x) > 10:
            self.texture = self.jump_text[self.FACING]
        elif -1 < self.change_x < 1 and self.physics_engines[0].can_jump():
            self.texture = self.idle[self.FACING][(self.cur_texture//2) // 4]
        elif (-1 > self.change_x or self.change_x > 1) and self.physics_engines[0].can_jump():
            if -14 > self.change_x or self.change_x > 14:
                self.texture = self.running[self.FACING][self.cur_texture2 // 6]
            else:
                self.texture = self.walking[self.FACING][self.cur_texture // 4]

    def jump(self):
        """I put jumping in a class cause it was easier to track in the code."""
        self.change_y = 20

    def setup(self):
        self.gun.center_x = -100
        self.gun.center_y = -100

    def update(self):
        self.update_animation()
        # "t" is a variable i use that controls the maximum speed of the character that depends on wether they are using
        # the gun or not.
        if self.attacking or self.grapling:
            t = 1
        else:
            t = 6
        # movement
        if self.A and self.change_x > -2*t:
            if self.change_x > 0:
                self.change_x -= 1*t
            self.change_x -= 0.5
        if self.D and self.change_x < 2*t:
            if self.change_x < 0:
                self.change_x += 1*t
            self.change_x += 0.5
        if (not self.A and not self.D) or self.attacking:
            if self.physics_engines[0].can_jump():
                self.change_x = self.change_x - (self.change_x/4)
            else:
                self.change_x = self.change_x - (self.change_x/200)

        # does calculations for cun position and angle.
        if self.attacking:
            self.gun.center_x = self.center_x
            self.gun.center_y = self.center_y
            diff_x = self.x - self.center_x
            diff_y = self.y - self.center_y
            self.gun.angle = math.degrees(math.atan2(diff_y, diff_x))
            if self.gun.angle < -90 or self.gun.angle > 90:
                self.gun.texture = arcade.load_texture("Player/gun.png", flipped_vertically=True)
                self.texture = arcade.load_texture("Player/guy_s.png", mirrored=True)
            else:
                self.gun.texture = arcade.load_texture("Player/gun.png")
                self.texture = arcade.load_texture("Player/guy_s.png")
        if self.physics_engines[0].can_jump() and self.change_y == 0:
            self.beaning = False
            self.beanter = False

        # more gun angle calculations
        diff_x = self.x_t - self.center_x
        diff_y = self.y_t - self.center_y
        self.gun.angle = math.degrees(math.atan2(diff_y, diff_x))
        if self.gun.angle < -90 or self.gun.angle > 90:
            if self.attacking:
                self.gun.texture = arcade.load_texture("Player/gun.png", flipped_vertically=True)
                self.texture = arcade.load_texture("Player/guy_s.png", mirrored=True)
        else:
            if self.attacking:
                self.gun.texture = arcade.load_texture("Player/gun.png")
                self.texture = arcade.load_texture("Player/guy_s.png")
        felice = False

        # when the attack button is pressed the gun will begin the shooting animation
        # and releases the bullet when the correct frame is active.
        if self.button:
            self.gun.shot = True
            if self.gun.cur_texture >= 8:
                felice = True
                self.button = False
        if felice:  # the code that fires off the bullet
            bullet = Bullet()
            diff_x = self.x_t - self.gun.center_x
            diff_y = self.y_t - self.gun.center_y
            angle = math.atan2(diff_y, diff_x)
            bullet.angle = math.degrees(angle) - 90
            bullet.center_x = self.gun.center_x + math.cos(angle) * 30
            bullet.center_y = self.gun.center_y + math.sin(angle) * 30
            bullet.change_x = math.cos(angle) * 20
            bullet.change_y = math.sin(angle) * 20
            self.bullet_list.append(bullet)
        if self.gun.shot:  # when shooting, animate
            self.gun.update_animation()
        if self.Q:  # no longer important melee attack that works exactly like bullets except stationary
            swipe = Swipe()
            diff_x = self.x_t - self.center_x
            diff_y = self.y_t - self.center_y
            angle = math.atan2(diff_y, diff_x)
            swipe.angle = math.degrees(angle) + 225
            swipe.stored_x = math.cos(angle) * 40
            swipe.stored_y = math.sin(angle) * 40
            swipe.center_x = self.center_x + swipe.stored_x
            swipe.center_x = self.center_x + swipe.stored_x
            swipe.center_y = self.center_y + swipe.stored_y
            self.bullet_list.append(swipe)
            self.Q = False
        # doing updates for bullets and removes them when they are far enough away.
        for bullet in self.bullet_list:
            bullet.update_animation()
            if ((bullet.center_x or bullet.center_y) < -100 or (bullet.center_x > 12000 or bullet.center_y > 4000)) \
                    and not bullet.swipe:
                bullet.remove_from_sprite_lists()
                del bullet
            elif bullet.swipe:
                bullet.center_x = self.center_x + bullet.stored_x
                bullet.center_y = self.center_y + bullet.stored_y
                if bullet.kill:
                    bullet.remove_from_sprite_lists()
                    del bullet
        # when moving in air the player generates smoke particles. why? idk i wanted to.
        if self.change_y != 0:
            self.tim += 1
            if self.tim % 3 == 0:
                puff = Smoke()
                puff.center_x = self.center_x + random.randint(-30, 30)
                puff.center_y = self.center_y - 15 - random.randint(-10, 10)
                puff.scale = 0.6
                self.effect_list.append(puff)

    def on_key_press(self, key: int):
        """ Player control """
        if key == arcade.key.A:
            self.A = True
            if -2 < self.change_x and not self.attacking:
                self.change_x -= 2
        elif key == arcade.key.D:
            self.D = True
            if self.change_x < 2 and not self.attacking:
                self.change_x += 2
        elif key == arcade.key.Q:
            self.Q = True

        if (key == arcade.key.W or key == arcade.key.SPACE) and self.physics_engines[0].can_jump():
            self.jump()
            self.W = True
        elif (key == arcade.key.W or key == arcade.key.SPACE or key == arcade.key.UP) and self.beaning:
            self.change_y = 25
            self.change_x = -15
        elif (key == arcade.key.W or key == arcade.key.SPACE or key == arcade.key.UP) and self.beanter:
            self.change_y = 25
            self.change_x = 15

    def on_key_release(self, key: int, _modifiers: int):
        if key == arcade.key.A:
            self.A = False
        elif key == arcade.key.D:
            self.D = False
        if (key == arcade.key.W or key == arcade.key.SPACE) and self.change_y > 0:
            self.change_y *= 0.4

    def on_mouse_press(self, button: int):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.attacking = True
        elif button == arcade.MOUSE_BUTTON_LEFT and not self.gun.shot and self.attacking:
            self.button = True

    def on_mouse_release(self, button: int):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.attacking = False
            self.button = False
            self.gun.center_x = -100
            self.gun.center_y = -100
            self.texture = arcade.load_texture("Player/guy.png")


class Gun(arcade.Sprite):
    """Contains the gun associated with the player."""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Player/gun.png")
        self.cur_texture = 0
        self.shooting = []
        self.shootingL = []
        self.shot = False
        for i in range(5):
            texture = arcade.load_texture("Spritesheets/gun.png", x=i*320, y=0, height=320, width=320)
            self.shooting.append(texture)
        for i in range(5):
            texture = arcade.load_texture("Spritesheets/gun.png", x=i*320, y=0, height=320, width=320,
                                          flipped_vertically=True)
            self.shootingL.append(texture)
        self.scale = 0.29

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture >= 5*4:
            self.cur_texture = 0
            self.shot = False
        if self.angle > 90 or self.angle < -90:
            self.texture = self.shootingL[self.cur_texture // 4]
        else:
            self.texture = self.shooting[self.cur_texture // 4]


class Bullet(arcade.Sprite):
    """Contains the bullet sprite"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Player/Bullet2.png")
        self.scale = 0.29
        self.swipe = False


class Smoke(arcade.Sprite):
    """Contains the little smoke particles that appear while in the air"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Spritesheets/smoke.png", x=0, y=0, height=320, width=320)
        self.smok = []
        for i in range(4):
            texture = arcade.load_texture("Spritesheets/smoke.png", x=i*320, y=0, height=320, width=320)
            self.smok.append(texture)
        self.angle = random.randint(0, 360)
        self.scale = 1
        self.cur_texture = 0
        self.kill = False

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture >= (4 * 6)-1:
            self.kill = True
        self.texture = self.smok[self.cur_texture // 6]

    def update(self):
        self.alpha -= 7
        self.update_animation()
        if self.kill:
            self.remove_from_sprite_lists()
            del self


class Swipe(arcade.Sprite):
    """A melee slash attack that is technically in the game (press Q) but has no purpose."""
    def __init__(self):
        super().__init__()
        self.stat = []
        self.kill = False
        self.swipe = True
        self.cur_texture = 0
        for i in range(7):
            texture = arcade.load_texture("Spritesheets/swipe-Sheet.png", x=i*320, y=0, height=320, width=320)
            self.stat.append(texture)
        self.texture = arcade.load_texture("Spritesheets/swipe-Sheet.png", x=0, y=0, height=320, width=320)
        self.scale = 0.4

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture >= (7 * 3)-1:
            self.kill = True
        self.texture = self.stat[self.cur_texture // 3]
