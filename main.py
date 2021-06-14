import arcade
import player
import enemy
import math
import text
import conv
import Dialogues.Test_level
import json
with open("game.world") as forest_world:
    data = json.load(forest_world)

import boss


# UPDATES_PER_FRAME = 4
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_ALT = 0.3
JUMP_SPEED = 14
GRAVITY = 1


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        """ Initializer """
        arcade.set_background_color((26, 21, 24))
        self.player = player.TestPlayer()
        self.enemy = enemy.TestEnemy(self.player)
        self.conv = conv.Conv()
        self.dictionaries = Dialogues.Test_level.ChattOption()
        self.health = Health()
        self.enemy_list = None
        self.physics_engine = None
        self.wall_list = None
        self.effect_list = None
        self.attach_point = None
        self.grapple_angle = None
        self.grapple_dist = None
        self.grappling = False
        self.rope = None
        self.x = 0
        self.y = 0
        self.x_t = 0
        self.y_t = 0
        self.tru_x = 0
        self.tru_y = 0
        self.updates_per_sec = 60
        self.attach_point_x = None
        self.attach_point_y = None
        self.origin_dist = None
        self.grapple_velocity = None
        self.time = 0
        self.level = 0
        self.view_left = 0
        self.view_bottom = 0
        self.grass_list = None
        self.back_list = None
        self.barrier_list = None
        self.tick = 0

        self.backdrop = None
        self.backdrops_list = None
        self.enemy_physics_engine = None

        self.tiling_list = None
        self.detail_list = None
        self.all_list = None

        self.actuator_list = None
        self.platform_list = None
        self.alt_all_list = None
        self.physics_engine_plat = None
        self.S = False
        self.E = False
        self.interacting = False
        self.second_platform_check = False

        self.printed = False
        self.text_list = None

        self.character = Character()
        self.interactables_list = None
        self.output = 0
        self.target_x = 0
        self.target_y = 0
        self.my_map = None
        self.type = 0
        self.timertoautofocus = 0

        self.grapple_list = None
        self.door_list = None

        self.ableto_shoot = True
        self.ableto_wall_jump = False
        self.ableto_grapple = True

        self.conversation = text.Conversation()
        self.dialogue_select = 0

        # joke please remove
        self.dont = False
        self.boss = boss.Boss()
        self.shade = arcade.Sprite()
        self.shade.texture = arcade.load_texture("Shade.png")
        self.shade.scale = 20
        self.shade.alpha = 30
        self.z = False

        self.gate_list = None
        self.numb = None
        self.numb_door = None
        self.numb_target = None
        self.prev = None
        self.world_map = {}
        self.current = None
        self.room_list = []
        self.barb_list = None
        self.ledges = None
        self.res_list = None
        self.res_act = None
        self.cur_texture = 0
        self.climb_guy = PClimb()
        self.curs = Curs()
        self.perm_x = 0
        self.perm_y = 0

        self.setup()

    def load_level(self, level):
        self.my_map = level
        self.wall_list = arcade.tilemap.process_layer(self.my_map, 'Platforms',
                                                      0.3, use_spatial_hash=True)
        layer_list = []
        print(f'num layers{len(self.my_map.layers)}')
        for i in range(len(self.my_map.layers)):
            b = self.my_map.layers[i].name
            if b == "Gate":
                self.numb = i
            if b == 'Door':
                self.numb_door = i
            if b == 'Actuators':
                self.numb_target = i
            layer_list.append(b)
        if 'Grass' in layer_list:
            self.grass_list = arcade.tilemap.process_layer(self.my_map, 'Grass',
                                                           0.3, use_spatial_hash=False)
        if 'Details' in layer_list:
            self.detail_list = arcade.tilemap.process_layer(self.my_map, 'Details',
                                                            0.3, use_spatial_hash=False)
            self.grass_list.extend(self.detail_list)
        if 'Back' in layer_list:
            self.tiling_list = arcade.tilemap.process_layer(self.my_map, 'Back',
                                                            0.3, use_spatial_hash=False)
        if 'Background' in layer_list:
            self.back_list = arcade.tilemap.process_layer(self.my_map, 'Background',
                                                          0.3, use_spatial_hash=False)
        if 'Climbable' in layer_list:
            self.platform_list = arcade.tilemap.process_layer(self.my_map, "Climbable",
                                                              0.3, use_spatial_hash=True)
        if 'Interactibles' in layer_list:
            self.interactables_list = arcade.process_layer(self.my_map, 'Interactibles',
                                                           0.3, use_spatial_hash=False)
        if 'Grapple' in layer_list:
            self.grapple_list = arcade.process_layer(self.my_map, 'Grapple',
                                                     0.3, use_spatial_hash=False)
        if "Barbs" in layer_list:
            self.barb_list = arcade.process_layer(self.my_map, 'Barbs',
                                                  0.3, use_spatial_hash=False)
        if 'Respawn' in layer_list:
            self.res_list = arcade.process_layer(self.my_map, 'Respawn',
                                                 0.3, use_spatial_hash=False)
        if 'Actuators' in layer_list:
            self.actuator_list = arcade.process_layer(self.my_map, 'Actuators',
                                                      0.3, use_spatial_hash=False)
            for i in self.actuator_list:
                i.identify = 1
                i.origin = i.texture
        else:
            for i in self.actuator_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Door' in layer_list:
            self.door_list = arcade.process_layer(self.my_map, 'Door',
                                                  0.3, use_spatial_hash=False)
        else:
            for i in self.door_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Ledges' in layer_list:
            self.ledges = arcade.process_layer(self.my_map, 'Ledges',
                                               0.3, use_spatial_hash=False)
            print("ledges = True")
        if 'Gate' in layer_list:
            self.gate_list = arcade.process_layer(self.my_map, 'Gate',
                                                  0.3, use_spatial_hash=False)
            print(self.my_map.layers[self.numb])
            if self.prev is None:
                self.player.center_x = 600
                self.player.center_y = 600
            else:
                for i in self.gate_list:
                    print("prev", f"{self.prev}.tmx")
                    print("dest", f"{i.properties['dest']}.tmx")
                    if f"{i.properties['dest']}.tmx" == f"{self.prev}.tmx":
                        print("---------------------------------------------------------------------")
                        if self.player.FACING == 1:
                            move_val = -1
                        else:
                            move_val = 1
                        self.player.center_x = i.center_x + (move_val * 50)
                        self.player.center_y = i.center_y
            self.view_left = self.player.center_x - SCREEN_WIDTH//2
            self.view_bottom = self.player.center_y - SCREEN_HEIGHT//2

        penis_list = []
        unpeen_list = []
        for p in range(2):
            for i in range(6):
                texture = arcade.load_texture("act-Sheet.png", x=i*160, y=480-p*160, height=160, width=160)
                penis_list.append(texture)
        for door in self.door_list:
            x = math.floor(door.center_x / 48)
            y = math.floor(door.center_y / 48)
            door.associate = self.my_map.layers[self.numb_door].layer_data[(len(self.my_map.layers[2].layer_data[0])-1) - y][x] - 194
            if door.associate >= 6:
                door.open = True
                door.origin = penis_list[door.associate]
                door.off = door.texture
                door.associate -= 6
            else:
                door.origin = door.texture
                door.off = penis_list[door.associate]
                door.open = False
            # print("associate", door.associate)
        penis_list1 = []
        for i in range(6):
            texture = arcade.load_texture("act-Sheet.png", x=i * 160, y=160, height=160, width=160)
            penis_list1.append(texture)
        for hit in self.actuator_list:
            x = math.floor(hit.center_x / 48)
            y = math.floor(hit.center_y / 48)
            hit.associate = self.my_map.layers[self.numb_target].layer_data[(len(self.my_map.layers[2].layer_data[0])-1) - y][x] - 182
            print("tar_acc", hit.associate)
            hit.origin = hit.texture
            hit.open = True
            hit.off = penis_list1[hit.associate]

        self.all_list = None
        self.all_list = arcade.SpriteList()
        self.all_list.extend(self.wall_list)
        self.all_list.extend(self.tiling_list)
        self.all_list.extend(self.platform_list)
        self.all_list.extend(self.door_list)

        self.alt_all_list = None
        self.alt_all_list = arcade.SpriteList()
        self.alt_all_list.extend(self.wall_list)
        self.alt_all_list.extend(self.tiling_list)
        self.alt_all_list.extend(self.door_list)

        self.player.physics_engines = [None, None]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.all_list,
            gravity_constant=GRAVITY)
        self.physics_engine_plat = arcade.PhysicsEnginePlatformer(
            self.player,
            self.alt_all_list,
            gravity_constant=GRAVITY)

        self.player.physics_engines[0] = self.physics_engine
        self.player.physics_engines[1] = self.physics_engine_plat
        print("roooms", self.room_list)
        for door in self.door_list:
            print(door.open)
            if door.open:
                self.all_list.remove(door)
                self.alt_all_list.remove(door)

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.back_list = arcade.SpriteList()
        self.tiling_list = arcade.SpriteList()
        self.effect_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()
        self.player.bullet_list = arcade.SpriteList()
        self.player.effect_list = arcade.SpriteList()
        self.backdrops_list = arcade.SpriteList()
        self.detail_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.all_list = arcade.SpriteList()
        self.alt_all_list = arcade.SpriteList()
        self.actuator_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.text_list = arcade.SpriteList()
        self.interactables_list = arcade.SpriteList()
        self.grapple_list = arcade.SpriteList()
        self.gate_list = arcade.SpriteList()
        self.barb_list = arcade.SpriteList()
        self.res_list = arcade.SpriteList()
        self.ledges = arcade.SpriteList()
        """self.platform_list = arcade.SpriteList()"""
        """self.all_list_p = arcade.SpriteList()"""
        # self.level_setup()

        self.player.center_y = 500
        self.player.center_x = 500
        # self.load_level(arcade.read_tmx(f"Levels/Forest/Leaves/{data['maps'][self.level]['fileName']}"))
        """-------REAL---------"""
        # self.load_level(arcade.read_tmx("untitled2.tmx"))
        """---------TEST----------"""
        self.load_level(arcade.read_tmx("2.tmx"))
        self.rope = arcade.Sprite()
        self.rope.texture = arcade.load_texture("roap3.png")
        self.rope.center_x = -100
        self.rope.center_y = -100
        self.rope.scale = 0.1

        self.player.set_hit_box(((-50.0, -130.0), (-30.0, -160.0), (30.0, -160.0), (50.0, -140.0), (50.0, 100.0),
                                 (20.0, 130.0), (-30.0, 130.0), (-50.0, 100.0)))

        self.backdrop = arcade.Sprite()
        # self.backdrop.texture = arcade.load_texture("Backdrop/Spec_background - Copy.png")
        self.backdrop.texture = arcade.load_texture("Backdrop/Forest_back2.png")
        self.backdrop.center_x = 2000
        self.backdrop.center_y = 1000
        self.backdrop.scale = 1.7*2
        """for i in range(5):
            boi = enemy.TestEnemy(self.player)
            boi.center_x = random.randint(100, 6000)
            boi.center_y = random.randint(100, 6000)
            self.enemy_list.append(boi)
        for boi in self.enemy_list:
            boi.enemy_physics_engine = arcade.PhysicsEngineSimple(
                boi,
                self.all_list)"""

        self.character.center_x = 96*19
        self.character.center_y = 96*3.5
        self.character.is_guy = True
        self.interactables_list.append(self.character)

        self.conv.center_x = 1000
        self.conv.center_y = 1000
        self.conv.setup()

        self.boss.center_x = 48*320*0.3/2
        self.boss.center_y = 2500
        self.boss.gun.center_x = self.boss.center_x
        self.boss.gun.center_y = self.boss.center_y

    def update(self, delta_time: float):
        c = arcade.check_for_collision_with_list(self.player, self.platform_list)
        if self.player.change_y > 0 or self.S or self.second_platform_check or self.player.S:
            self.player.physics_engines[1].update()
        else:
            self.player.physics_engines[0].update()
        if c:
            self.second_platform_check = True
        else:
            self.second_platform_check = False
        self.enemy_list.update()
        # self.actuator_list.update()
        for target in self.actuator_list:
            collide = arcade.check_for_collision_with_list(target, self.player.bullet_list)
            if collide:
                for bullet in self.player.bullet_list:
                    b = arcade.check_for_collision_with_list(bullet, self.actuator_list)
                    if b and not bullet.swipe:
                        bullet.remove_from_sprite_lists()
                        del bullet
                for door in self.door_list:
                    if door.associate == target.associate:
                        if not door.open:
                            door.texture = door.off
                            self.all_list.remove(door)
                            self.alt_all_list.remove(door)
                            door.open = True
                        else:
                            door.texture = door.origin
                            self.all_list.append(door)
                            self.alt_all_list.append(door)
                            door.open = False
                        print(door.open)
                self.player.physics_engines = [None, None]
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player,
                    self.all_list,
                    gravity_constant=GRAVITY)
                self.physics_engine_plat = arcade.PhysicsEnginePlatformer(
                    self.player,
                    self.alt_all_list,
                    gravity_constant=GRAVITY)
                self.player.physics_engines[0] = self.physics_engine
                self.player.physics_engines[1] = self.physics_engine_plat
                if target.identify == 1:
                    target.texture = target.off
                else:
                    target.texture = target.origin
                target.identify = target.identify * -1
        for boi in self.enemy_list:
            boi.update_animation()
            boi.enemy_physics_engine.update()
            a = arcade.check_for_collision_with_list(boi, self.player.bullet_list)
            if a:
                for bullet in self.player.bullet_list:
                    b = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                    if b and not bullet.swipe:
                        bullet.remove_from_sprite_lists()
                        del bullet
                boi.remove_from_sprite_lists()
                del boi
        for bullet in self.player.bullet_list:
            if not bullet.swipe:
                c = arcade.check_for_collision_with_list(bullet, self.alt_all_list)
                if c:
                    bullet.remove_from_sprite_lists()
                    del bullet

        """ ----------- LEDGE-CLIMBING ----------- """
        if not self.player.physics_engines[1].can_jump() and not self.player.grapling:
            self.player.center_x += 1
            if arcade.check_for_collision_with_list(self.player, self.ledges):
                for i in self.ledges:
                    if arcade.check_for_collision(i, self.player):
                        self.player.alpha = 0
                        self.player.is_climbing = True
                        self.player.center_x = i.center_x
                        self.player.center_y = i.center_y + (240*0.3)
                        self.player.beanter = False
                        self.player.beaning = False
                        self.climb_guy.alpha = 255
                        self.climb_guy.face = self.player.FACING
                        self.climb_guy.center_y = self.player.center_y
                        self.climb_guy.center_x = self.player.center_x
            self.player.center_x -= 2
            if arcade.check_for_collision_with_list(self.player, self.ledges):
                for i in self.ledges:
                    if arcade.check_for_collision(i, self.player):
                        self.player.alpha = 0
                        self.player.is_climbing = True
                        self.player.center_x = i.center_x
                        self.player.center_y = i.center_y + (240*0.3)
                        self.player.beanter = False
                        self.player.beaning = False
                        self.climb_guy.alpha = 255
                        self.climb_guy.face = self.player.FACING
                        self.climb_guy.center_y = self.player.center_y
                        self.climb_guy.center_x = self.player.center_x
            self.player.center_x += 1

        ''' ----------- WALL-JUMPING ----------- '''
        if not self.player.physics_engines[1].can_jump() and not self.player.grapling and self.ableto_wall_jump:
            self.player.center_x += 1
            if arcade.check_for_collision_with_list(self.player, self.alt_all_list):
                self.player.beaning = True
            else:
                self.player.beaning = False
            self.player.center_x -= 2
            if arcade.check_for_collision_with_list(self.player, self.alt_all_list):
                self.player.beanter = True
            else:
                self.player.beanter = False
            self.player.center_x += 1
            if self.player.beanter or self.player.beaning:
                self.player.center_y -= 96
                if arcade.check_for_collision_with_list(self.player, self.alt_all_list):
                    self.player.beaning = False
                    self.player.beanter = False
                else:
                    self.player.change_y = -2
                self.player.center_y += 96

        if self.player.is_climbing:
            self.player.change_y = 0
            self.player.change_x = 0
            self.climb_guy.update_animation()
            if self.climb_guy.die:
                self.climb_guy.die = False
                self.player.is_climbing = False
                self.player.alpha = 255
                self.climb_guy.alpha = 1
                self.climb_guy.center_y = -100
                self.climb_guy.center_x = -100
        else:
            self.player.update()
        self.player.effect_list.update()
        self.player.bullet_list.update()

        p = False
        for i in self.grapple_list:
            x_diff = self.player.center_x - i.center_x
            y_diff = self.player.center_y - i.center_y
            i.dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
            if i.dist < 500:
                self.attach_point_x = i.center_x
                self.attach_point_y = i.center_y
                if not self.grappling:
                    self.origin_dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
                p = True
        if not p:
            self.grappling = False

        if self.grappling and p:
            self.player.grapling = True
            self.player.physics_engines[0].gravity_constant = 0
            diff_x = self.player.center_x - self.attach_point_x
            diff_y = self.player.center_y - self.attach_point_y
            self.grapple_angle = math.atan2(diff_y, diff_x)
            self.grapple_dist = math.sqrt((diff_x ** 2) + (diff_y ** 2))

            self.rope.center_x = (self.player.center_x + self.attach_point_x) / 2
            self.rope.center_y = (self.player.center_y + self.attach_point_y) / 2
            grapple_acc = self.grapple_angle - math.pi/2
            if grapple_acc < 0:
                grapple_acc += math.pi*2
            self.grapple_velocity += GRAVITY*1.4 * 0.4 * math.sin(grapple_acc)
            self.grapple_angle += self.grapple_velocity * delta_time * 0.2
            self.player.change_y = 0
            self.player.center_x = self.attach_point_x + math.cos(self.grapple_angle) * self.origin_dist
            self.player.center_y = self.attach_point_y + math.sin(self.grapple_angle) * self.origin_dist

            self.rope.angle = math.degrees(self.grapple_angle) - 90
            self.rope.height = self.origin_dist
        else:
            self.rope.center_x = -1000
            self.rope.center_y = -1000
        if not self.interacting:
            character_offset_x = int(self.player.center_x) - int(self.view_left + (SCREEN_WIDTH // 2))
            character_offset_y = int(self.player.center_y) - int(self.view_bottom + (SCREEN_HEIGHT // 2))
        else:
            character_offset_x = int(self.target_x) - int(self.view_left + (SCREEN_WIDTH // 2))
            character_offset_y = int(self.target_y) - int(self.view_bottom + (SCREEN_HEIGHT // 2))
        if self.player.attacking:
            character_offset_x = character_offset_x + int(self.tru_x*0.6)
            character_offset_y = character_offset_y + int(self.tru_y*0.4)
        if not self.interacting:
            if self.view_left != (int(self.player.center_x - (SCREEN_WIDTH // 2))) or self.player.attacking:
                self.view_left = self.view_left + ((character_offset_x // 10) + self.player.change_x * 1.2)
                if self.view_left <= 0 + SCREEN_WIDTH*SCREEN_ALT:
                    self.view_left = 0 + SCREEN_WIDTH*SCREEN_ALT
                elif self.view_left >= len(self.my_map.layers[0].layer_data[0])*48 - SCREEN_WIDTH*(1+SCREEN_ALT):
                    self.view_left = len(self.my_map.layers[0].layer_data[0])*48 - SCREEN_WIDTH*(1+SCREEN_ALT)
            if self.view_bottom != (int(self.player.center_y - (SCREEN_HEIGHT // 2))) or self.player.attacking:
                self.view_bottom = self.view_bottom + (character_offset_y // 10) + 10
                if self.view_bottom <= 0 + SCREEN_HEIGHT*SCREEN_ALT:
                    self.view_bottom = 0 + SCREEN_HEIGHT*SCREEN_ALT
                elif self.view_bottom >= len(self.my_map.layers[0].layer_data)*48 - SCREEN_HEIGHT*(1+SCREEN_ALT):
                    self.view_bottom = len(self.my_map.layers[0].layer_data)*48 - SCREEN_HEIGHT*(1+SCREEN_ALT)
            arcade.set_viewport((self.view_left - SCREEN_WIDTH*SCREEN_ALT)//1, (SCREEN_WIDTH*(1+SCREEN_ALT) + self.view_left - 1)//1,
                                (self.view_bottom - SCREEN_HEIGHT*SCREEN_ALT)//1, (SCREEN_HEIGHT*(1+SCREEN_ALT) + self.view_bottom - 1)//1)

        if self.timertoautofocus > 0:
            self.timertoautofocus -= 1
        if self.interacting:
            self.view_left = self.view_left + (character_offset_x // 10)
            self.view_bottom = self.view_bottom + (character_offset_y // 10)
            if 5 >= abs(self.target_x) - abs(self.view_left + (SCREEN_WIDTH // 2)) or self.timertoautofocus <= 0:
                self.view_left = self.target_x - SCREEN_WIDTH//2
            if 5 >= abs(((SCREEN_HEIGHT // 2) + self.view_bottom) - self.target_y) or self.timertoautofocus <= 0:
                self.view_bottom = self.target_y - SCREEN_HEIGHT//2
            changed = True
            if changed and not self.dont:  # joke
                arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left - 1,
                                    self.view_bottom, SCREEN_HEIGHT + self.view_bottom - 1)
            if self.conv.return_available:
                self.interacting = False

        self.backdrop.center_x = 2000 + self.view_left // 2
        self.backdrop.center_y = 1000 + self.view_bottom // 6
        self.player.x_t = self.x_t + self.view_left
        self.player.y_t = self.y_t + self.view_bottom

        if self.player.joystick:
            c = arcade.check_for_collision_with_list(self.player, self.interactables_list)
            if not c:
                self.player.E = False
            if self.player.E:
                self.e()
            elif not self.player.E:
                self.anti_e()

        if self.player.beaning or self.player.beanter:
            self.player.change_y += 1
        if not self.interacting:
            self.bossing()
        for beam in self.boss.attack_list:
            if beam.can_it:
                a = arcade.check_for_collision(beam, self.player)
                if a and self.player.health > 0:
                    beam.can_it = False
                    self.player.health -= 1
                    self.health.texture = self.health.state[abs(self.player.health-4)]
                    if self.player.health <= 0:
                        exit()
        wind = arcade.get_viewport()
        self.health.center_x = wind[0] + 640*0.3 + 10
        self.health.center_y = wind[3] - 160*0.3 - 10
        self.perm_x = self.x_t + self.view_left
        self.perm_y = self.y_t + self.view_bottom
        self.curs.center_x = self.perm_x
        self.curs.center_y = self.perm_y
        # self.health.center_x = self.view_left + 640*0.3 + 10
        # self.health.center_y = self.view_bottom + SCREEN_HEIGHT - 160*0.3 - 10

        self.shade.center_x = self.player.center_x
        self.shade.center_y = self.player.center_y
        if self.z:
            self.shade.alpha += 0.2
            if self.shade.alpha >= 60:
                self.z = False
        if self.shade.alpha <= 40:
            self.z = True
            for i in self.wall_list:
                i.color = arcade.color.LIGHT_GRAY

        if arcade.check_for_collision_with_list(self.player, self.res_list):
            for res in self.res_list:
                if arcade.check_for_collision(res, self.player):
                    self.res_act = res

        if arcade.check_for_collision_with_list(self.player, self.gate_list):
            for i in self.gate_list:
                if arcade.check_for_collision(i, self.player):
                    self.prev = self.current
                    self.current = i.properties['dest']
                    self.load_level(arcade.tilemap.read_tmx(f"{i.properties['dest']}.tmx"))
        elif arcade.check_for_collision_with_list(self.player, self.barb_list):
            if self.player.health > 0:
                self.player.health -= 1
                self.health.texture = self.health.state[abs(self.player.health - 4)]
                if self.player.health <= 0:
                    exit()
                else:
                    self.player.center_x = self.res_act.center_x
                    self.player.center_y = self.res_act.center_y
                    self.player.change_x = 0
                    self.player.change_y = 0

    def on_draw(self):
        arcade.start_render()
        self.backdrops_list.draw()
        self.backdrop.draw()
        self.back_list.draw()

        self.res_list.draw()

        self.character.draw()
        self.interactables_list.draw()

        self.platform_list.draw()
        self.effect_list.draw()
        self.rope.draw()
        self.player.pointer.draw()
        self.player.draw()
        self.climb_guy.draw()
        self.player.gun.draw()
        self.tiling_list.draw()
        self.wall_list.draw()
        self.barb_list.draw()
        self.enemy_list.draw()
        self.player.effect_list.draw()
        self.actuator_list.draw()
        self.door_list.draw()
        self.player.bullet_list.draw()
        self.detail_list.draw()
        self.grass_list.draw()
        self.grapple_list.draw()
        self.boss.on_draw()
        self.curs.draw()
        # self.shade.draw() # joke

        if self.interacting:
            self.conv.on_draw()
        self.health.draw()

    def on_key_press(self, key: int, modifiers: int):
        if not self.player.is_climbing:
            if not self.interacting:
                self.player.on_key_press(key)
                if key == arcade.key.KEY_2:
                    self.player.center_y = 500
                    self.player.center_x = 1000
                elif key == arcade.key.LSHIFT and self.ableto_grapple:
                    diff_x = self.player.center_x - self.attach_point_x
                    diff_y = self.player.center_y - self.attach_point_y
                    self.grapple_angle = math.atan2(diff_y, diff_x)
                    self.grapple_dist = math.sqrt((diff_x ** 2) + (diff_y ** 2))
                    self.grapple_velocity = (-math.sqrt(
                        (self.player.change_x ** 2) + (self.player.change_y ** 2)) / self.grapple_dist)
                    # self.origin_dist = math.sqrt((diff_x ** 2) + (diff_y ** 2))
                    self.grappling = True
                elif key == arcade.key.S:
                    self.S = True
                elif key == arcade.key.E:
                    self.e()
                elif key == arcade.key.K:
                    self.stop_doing_shit()
                    self.interacting = True
                    self.target_x = self.player.center_x
                    self.target_y = self.player.center_y + SCREEN_HEIGHT//12
                    self.conv.center_x = self.player.center_x
                    self.conv.center_y = self.player.center_y - SCREEN_HEIGHT//4
                    self.conv.conv_point = 0
                    self.conv.setup()
            else:
                self.conv.on_key_press(key)
                if key == arcade.key.E:
                    self.anti_e()
            if key == arcade.key.P:  # joke
                if not self.dont:
                    arcade.set_viewport(self.view_left, SCREEN_WIDTH*2 + self.view_left - 1,
                                        self.view_bottom, SCREEN_HEIGHT*2 + self.view_bottom - 1)
                    self.dont = True
                else:
                    self.dont = False
            if key == arcade.key.KEY_1:
                self.player.center_x = 500
                self.player.center_y = 500
            if key == arcade.key.KEY_3:
                self.player.health = 4
            if key == arcade.key.M:
                print(len(self.my_map.layers[2].layer_data))
                print(len(self.my_map.layers[2].layer_data[0]))
            if key == arcade.key.KEY_5:
                self.ableto_wall_jump = True
            if key == arcade.key.KEY_7:
                for door in self.door_list:
                    if not door.open:
                        self.all_list.remove(door)
                        self.alt_all_list.remove(door)
                        # door.texture = door.off
                        door.open = True
                    else:
                        self.all_list.append(door)
                        self.alt_all_list.append(door)
                        # door.texture = door.origin
                        door.open = False

    def on_key_release(self, key: int, _modifiers: int):
        if not self.interacting:
            self.player.on_key_release(key, _modifiers)
            if key == arcade.key.LSHIFT and self.grappling:
                self.grappling = False
                self.player.grapling = False
                self.player.physics_engines[0].gravity_constant = GRAVITY

                diff_x = self.attach_point_x - self.player.center_x
                diff_y = self.attach_point_y - self.player.center_y
                c = (self.grapple_velocity / (2 * math.pi)) * (2 * math.pi * self.grapple_dist)
                perp_angle = math.atan2(diff_x, diff_y)
                self.player.change_x = (math.cos(perp_angle) * (c / 60)) / 4
                self.player.change_y = (math.sin(-perp_angle) * (c / 60)) / 2
            elif key == arcade.key.LSHIFT:
                self.grappling = False
                self.player.grapling = False
                self.player.physics_engines[0].gravity_constant = GRAVITY
            elif key == arcade.key.S:
                self.S = False
            elif key == arcade.key.E:
                self.E = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.x = x + self.view_left
        self.y = y + self.view_bottom
        self.player.workpleasex = self.view_left
        self.player.workpleasey = self.view_bottom
        self.x_t = x
        self.y_t = y
        self.tru_x = x - ((SCREEN_WIDTH+(SCREEN_ALT*2)) / 2)
        self.tru_y = y - ((SCREEN_HEIGHT+(SCREEN_ALT*2)) / 2)
        self.player.x = self.x
        self.player.y = self.y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if not self.interacting:
            self.player.on_mouse_press(button)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if not self.interacting:
            self.player.on_mouse_release(button)

    def anti_e(self):
        self.interacting = False
        self.player.interacting = False
        for letter in self.text_list[::-1]:
            letter.remove_from_sprite_lists()
            del letter

    def stop_doing_shit(self):
        self.E = True
        self.S = False
        self.grappling = False
        self.player.grapling = False
        self.player.W = False
        self.player.A = False
        self.player.D = False
        self.player.Q = False
        self.player.attacking = False
        self.player.interacting = True
        self.player.button = False
        self.player.gun.center_x = -100
        self.player.gun.center_y = -100
        self.player.pointer.center_y = -900000
        self.player.pointer.center_x = -900000

    def e(self):
        self.E = True
        x = math.floor(self.player.center_x / 96)
        y = math.floor(self.player.center_y / 96)
        self.dialogue_select = 0
        self.target_x = x * 96 + 48
        self.target_y = y * 96 + 48
        c = arcade.check_for_collision(self.player, self.character)
        if self.my_map.layers[7].layer_data[31-y][x] != 0 or c:
            if c:
                text_happening = 99
            else:
                text_happening = self.my_map.layers[7].layer_data[31 - y][x] - 162
                self.conv.conv = self.dictionaries.interactibles[f"obj{text_happening}"]
            self.output = text_happening
            self.interacting = True
            self.stop_doing_shit()
            self.timertoautofocus = 40

            self.target_x = self.player.center_x
            self.target_y = self.player.center_y + SCREEN_HEIGHT // 12
            self.conv.center_x = self.player.center_x
            self.conv.center_y = self.player.center_y - SCREEN_HEIGHT // 4
            self.conv.conv_point = 0
            self.conv.setup()

    def bossing(self):
        # self.boss.update()
        diff_x = self.player.center_x - self.boss.gun.center_x
        diff_y = self.player.center_y - self.boss.gun.center_y
        angley = math.atan2(diff_y, diff_x)
        self.boss.gun.angle = math.degrees(angley)
        if self.boss.gun.angle > 90 or self.boss.gun.angle < -90:
            self.boss.texture = arcade.load_texture("Enemy/b2.png", mirrored=True)
        else:
            self.boss.texture = arcade.load_texture("Enemy/b2.png", mirrored=False)


class Character(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("character_boi.png")
        self.scale = 0.3


class Letter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.capitals = []
        texture = arcade.load_texture("Letters/fonts.png", x=1600, y=640, height=320, width=80)
        self.capitals.append(texture)
        for i in range(26):
            texture = arcade.load_texture("Letters/fonts.png", x=(i*90)+5, y=320, height=320, width=80)
            self.capitals.append(texture)
        self.texture = arcade.load_texture("Letters/fonts2.png", x=0, y=0, height=1, width=1)
        self.scale = 0.5
        self.is_letter = True


class Health(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.state = []
        for i in range(5):
            texture = arcade.load_texture("Spritesheets/health-Sheet.png", x=i*640, y=0, height=160, width=640)
            self.state.append(texture)
        self.texture = self.state[0]
        self.scale = 0.5


class PClimb(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.cur_texture = 0
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
        self.climbing.append(self.climbingR)
        self.climbing.append(self.climbingL)
        self.texture = self.climbing[0][0]
        self.scale = 0.3
        self.alpha = 0
        self.face = 0
        self.die = False

    def update_animation(self, delta_time: float = 1/60):
        self.cur_texture += 1
        if self.cur_texture >= (6 * 9) - 1:
            self.cur_texture = 0
            self.die = True
        self.texture = self.climbing[self.face][(self.cur_texture//6)]


class Curs(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("curs.png")
        self.scale = 0.5


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "GAME", fullscreen=False)
    window.center_window()
    game = Game()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
