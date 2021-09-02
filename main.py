import arcade
# import random

import conversations
import player
import enemy
import math
import text
import conv2
import Turrets
import Dialogues.Test_level
import json
with open("tsx&world/game.world") as forest_world:
    data = json.load(forest_world)

import boss

SIZE = 1
SCREEN_WIDTH = int(1200 / SIZE)
SCREEN_HEIGHT = int(700 / SIZE)
SCREEN_ALT = 0.3 * SIZE
JUMP_SPEED = 14
GRAVITY = 1


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        """ Initializer """
        arcade.set_background_color((26, 21, 24))
        self.player = player.TestPlayer()
        self.enemy = enemy.TestEnemy(self.player)
        self.conv = conv2.Conv()
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
        self.dd = None
        self.back_list = None
        self.back_list2 = None
        self.barrier_list = None
        self.tick = 0
        self.numb_interact = None

        self.backdrop = None
        self.enemy_physics_engine = None

        self.tiling_list = None
        self.detail_list = None
        self.all_list = None

        self.actuator_list = None
        self.levers = None
        self.platform_list = None
        self.alt_all_list = None
        self.physics_engine_plat = None
        self.S = False
        self.E = False
        self.interacting = False
        self.second_platform_check = False

        self.printed = False
        self.text_list = None

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

        self.dialogue_select = 0

        self.boss = boss.Boss()
        self.shade = arcade.Sprite()
        self.shade.texture = arcade.load_texture("Misc_level_stuff/Shade.png")
        self.shade.scale = 20
        self.shade.alpha = 0
        self.z = False

        self.shade_list = None
        self.gate_list = None
        self.numb = None
        self.numb_door = None
        self.numb_target = None
        self.numb_levers = None
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
        self.turret_list = None
        self.turret_beams = None
        self.respawning = False
        self.end_times = 0
        self.numb_platforms = None
        self.reset_point = 'S6_1'
        self.saved_prev = None
        self.saved_facing = 0
        self.game_end = False
        self.ready = False
        self.dramatimer = 0

        self.boss_battle = False
        self.inside_bossroom = False
        self.bossbattle_prelude = -1

        self.can_interact = Target()

        """This loads all the textures of doors, levers and actuators so i can later check the texture loaded
           in tiled, and compare it to the dictionary, and then assign the appropriate association value."""
        test = []
        test2 = []
        test3 = []
        for y in range(4):
            for x in range(6):
                texture = arcade.load_texture("Tilesets/act-Sheet.png", x=x * 160,
                                              y=0 + (y * 160), height=160, width=160)
                test.append(texture)
        self.example = {
            test[0]: 1, test[1]: 2, test[2]: 3, test[3]: 4, test[4]: 5, test[5]: 6,
            test[6]: 7, test[7]: 8, test[8]: 9, test[9]: 10, test[10]: 11, test[11]: 12,
            test[12]: 1, test[13]: 2, test[14]: 3, test[15]: 4, test[16]: 5, test[17]: 6,
            test[18]: 7, test[19]: 8, test[20]: 9, test[21]: 10, test[22]: 11, test[23]: 12,
        }
        for y in range(6):
            for x in range(7):
                texture = arcade.load_texture("Tilesets/Turret_4.png", x=(x * 320), y=(y * 320), height=320,
                                              width=320)
                test2.append(texture)
        self.example2 = {
            test2[0]: 99, test2[7]: 99, test2[14]: 99, test2[21]: 99, test2[28]: 99, test2[35]: 99,
            test2[1]: 1, test2[2]: 2, test2[3]: 3, test2[4]: 4, test2[5]: 5, test2[6]: 6,
            test2[8]: 7, test2[9]: 8, test2[10]: 9, test2[11]: 10, test2[12]: 11, test2[13]: 12,
            test2[15]: 13, test2[16]: 14, test2[17]: 15, test2[18]: 16, test2[19]: 17, test2[20]: 18,
            test2[22]: 19, test2[23]: 20, test2[24]: 21, test2[25]: 22, test2[26]: 23, test2[27]: 24,
            test2[29]: 25, test2[30]: 26, test2[31]: 27, test2[32]: 28, test2[33]: 29, test2[34]: 30,
            test2[36]: 31, test2[37]: 32, test2[38]: 33, test2[39]: 34, test2[40]: 35, test2[41]: 36
        }
        for x in range(7):
            texture = arcade.load_texture("Tilesets/Levers.png", x=(x * 320), y=0, height=320, width=320)
            test3.append(texture)
        self.example3 = {
            test3[0]: 99,
            test3[1]: 1, test3[2]: 2, test3[3]: 3, test3[4]: 4, test3[5]: 5, test3[6]: 6
        }

        self.ventures = []

        self.setup()

    def load_level(self, level):
        """This is the Level loading program.
           it runs through and checks all the layers and lists that may be in the tiled level,
           and assigns the sprites to a sprite list.
           also handles all gates, doors, and interactibles."""
        self.my_map = level
        self.wall_list = arcade.tilemap.process_layer(self.my_map, 'Platforms',
                                                      0.3, use_spatial_hash=True)
        print(self.current)
        layer_list = []
        self.player.change_x = 0
        self.player.change_y = 0
        for i in range(len(self.my_map.layers)):  # checks all map layers and records their position in the list.
            b = self.my_map.layers[i].name
            if b == "Gate":
                self.numb = i
            if b == 'Door':
                self.numb_door = i
            if b == 'Actuators':
                self.numb_target = i
            if b == 'Platforms':
                self.numb_platforms = i
            if b == 'Levers':
                self.numb_levers = i
            if b == 'Interactibles':
                self.numb_interact = i
            layer_list.append(b)

        # all if "name" after this are checking if a layer is in the current map, and loading that map if it is.
        if 'Shadow' in layer_list:  # check if layer in map
            self.shade_list = arcade.tilemap.process_layer(self.my_map, 'Shadow',
                                                           0.3, use_spatial_hash=False)
            self.grass_list.extend(self.shade_list)  # Replace the list with the new layer
        else:
            for i in self.shade_list[::-1]:  # Otherwise remove any items in the list from the previous level.
                i.remove_from_sprite_lists()
                del i
        # every other module is exactly the same as this one so i will not repeat.
        if 'Grass' in layer_list:
            self.grass_list = arcade.tilemap.process_layer(self.my_map, 'Grass',
                                                           0.3, use_spatial_hash=False)
        else:
            for i in self.grass_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Details' in layer_list:
            self.detail_list = arcade.tilemap.process_layer(self.my_map, 'Details',
                                                            0.3, use_spatial_hash=False)
            self.grass_list.extend(self.detail_list)
        else:
            for i in self.detail_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Back' in layer_list:
            self.back_list = arcade.tilemap.process_layer(self.my_map, 'Back',
                                                          0.3, use_spatial_hash=False)
        else:
            for i in self.back_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Back2' in layer_list:
            self.back_list2 = arcade.tilemap.process_layer(self.my_map, 'Back2',
                                                           0.3, use_spatial_hash=False)
        else:
            for i in self.back_list2[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Climbable' in layer_list:
            self.platform_list = arcade.tilemap.process_layer(self.my_map, "Climbable",
                                                              0.3, use_spatial_hash=True)
        else:
            for i in self.platform_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Interactibles' in layer_list:
            self.interactables_list = arcade.process_layer(self.my_map, 'Interactibles',
                                                           0.3, use_spatial_hash=False)
        else:
            for i in self.interactables_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Grapple' in layer_list:
            self.grapple_list = arcade.process_layer(self.my_map, 'Grapple',
                                                     0.3, use_spatial_hash=False)
        else:
            for i in self.grapple_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if "Barbs" in layer_list:
            self.barb_list = arcade.process_layer(self.my_map, 'Barbs',
                                                  0.3, use_spatial_hash=False)
        else:
            for i in self.barb_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Respawn' in layer_list:
            self.res_list = arcade.process_layer(self.my_map, 'Respawn',
                                                 0.3, use_spatial_hash=False)
        else:
            for i in self.res_list[::-1]:
                i.remove_from_sprite_lists()
                del i
        if 'Actuators' in layer_list:
            self.actuator_list = arcade.process_layer(self.my_map, 'Actuators',
                                                      0.3, use_spatial_hash=False)
            for i in self.actuator_list:
                # give all items in this list its texture as a variable on level start
                # so it can be used as an identifyer.
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
        if 'Turrets' in layer_list:  # turrets have multiple states and need many lists to keep track
            turret_list_cord = arcade.process_layer(self.my_map, 'Turrets',
                                                    0.3, use_spatial_hash=False)
            turrettext_list = []
            turrettext_list2 = []
            turrettext_list3 = []
            for y in range(2):
                # this code reads through all the different turret directions and checks each entry in the list to
                # assign it to the appropriate list.
                for i in range(6):
                    texture = arcade.load_texture("Tilesets/Turret_4.png", x=320 + (i * 320), y=0 + (320 * y),
                                                  height=320, width=320)
                    turrettext_list.append(texture)
                    texture2 = arcade.load_texture("Tilesets/Turret_4.png", x=320 + (i * 320), y=640 + (320 * y),
                                                   height=320, width=320)
                    turrettext_list2.append(texture2)
                    texture3 = arcade.load_texture("Tilesets/Turret_4.png", x=320 + (i * 320), y=1280 + (320 * y),
                                                   height=320, width=320)
                    turrettext_list3.append(texture3)
            for i in turret_list_cord:
                # sets up all turrets as sprites and gives them appropriate class and location.
                first = i.texture
                turret = Turrets.BigGun()
                turret.texture = first
                turret.direct = "Left"
                turret.center_x = i.center_x
                turret.center_y = i.center_y
                self.turret_list.append(turret)
                turret.associate = self.example2[turret.texture]

            for turret in self.turret_list:
                # assigns the appropriate directional variable and appropriate association variable.
                if turret.associate >= 25:
                    turret.direct = "Right"
                    turret.associate -= 24
                elif turret.associate >= 12:
                    turret.direct = "Down"
                    turret.associate -= 12
                else:
                    turret.direct = 'Left'
                if turret.associate >= 6:
                    turret.associate -= 6
                    turret.active = True
                    turret.origin = turret.texture
                    if turret.direct == "Left":
                        turret.off = turrettext_list[turret.associate - 1]
                    elif turret.direct == "Down":
                        turret.off = turrettext_list2[turret.associate - 1]
                    elif turret.direct == "Right":
                        turret.off = turrettext_list3[turret.associate - 1]
                else:
                    turret.active = False
                    if turret.direct == "Left":
                        turret.origin = turrettext_list[turret.associate + 5]
                    elif turret.direct == "Down":
                        turret.origin = turrettext_list2[turret.associate + 5]
                    elif turret.direct == "Right":
                        turret.origin = turrettext_list3[turret.associate + 5]
                    turret.off = turret.texture

                x = math.floor(turret.center_x//48)
                y = math.floor(turret.center_y//48)
                s = len(self.my_map.layers[0].layer_data)
                b = 0
                # checks distance from turret to nearest wall in the beam path to create a laser that only goes as far
                # as to just hit the nearest wall.
                if turret.direct == 'Left':
                    while self.my_map.layers[self.numb_platforms].layer_data[s - y][x - b] == 0:
                        b += 1
                        if x - b <= -1:
                            break
                    turret.dist = b
                elif turret.direct == 'Down':
                    while self.my_map.layers[self.numb_platforms].layer_data[(s - y) + b][x] == 0:
                        b += 1
                        if y - b <= -1:
                            break
                    turret.dist = b
                elif turret.direct == 'Right':
                    while self.my_map.layers[self.numb_platforms].layer_data[s - y][x + b] == 0:
                        b += 1
                        if x + b >= s:
                            break
                    turret.dist = b
        else:
            for tur in self.turret_list[::-1]:
                tur.remove_from_sprite_lists()
                del tur
        if 'Ledges' in layer_list:
            self.ledges = arcade.process_layer(self.my_map, 'Ledges',
                                               0.3, use_spatial_hash=False)
        else:
            for led in self.ledges[::-1]:
                led.remove_from_sprite_lists()
                del led
        if 'Levers' in layer_list:
            self.levers = arcade.process_layer(self.my_map, 'Levers',
                                               0.3, use_spatial_hash=False)
            for i in self.levers:
                # give all items in this list its texture as a variable on level start
                # so it can be used as an identifyer.
                i.identify = 1
                i.origin = i.texture
        else:
            for lev in self.levers[::-1]:
                lev.remove_from_sprite_lists()
                del lev
        if 'Gate' in layer_list:
            self.gate_list = arcade.process_layer(self.my_map, 'Gate',
                                                  0.3, use_spatial_hash=False)
            if self.prev is None:
                self.player.center_x = 540
                self.player.center_y = 48*12
            else:
                for i in self.gate_list:
                    if f"{i.properties['dest']}.tmx" == f"{self.prev}.tmx":
                        # this checks which was the previous level the player was in and places them
                        # just outside the gate that leads back to that level so that it looks as though they passed
                        # through a corridor from one level to another.
                        if self.player.FACING == 1:
                            move_val = -1
                        else:
                            move_val = 1
                        self.player.center_x = i.center_x + (move_val * 50)
                        self.player.center_y = i.center_y - 24
        # that is all tile lists finished :)

        """ a lot of code after this is dedicated to looking at all doors, actuators and doors and giving them the
        appropriate association variable to connect it to the right colour chanel for activation"""
        alttext_list = []
        for p in range(2):
            for i in range(6):  # cucles through all the images in the door sheet and saves it to a list
                texture = arcade.load_texture("Tilesets/act-Sheet.png", x=i * 160, y=480 - (p * 160), height=160,
                                              width=160)
                alttext_list.append(texture)
        for door in self.door_list:
            # this gives all doors their on or off state, and their association value
            door.associate = self.example[door.texture]
            if door.associate >= 6:
                door.open = True
                door.origin = alttext_list[door.associate - 1]
                door.off = door.texture
                door.associate -= 6
            else:
                door.origin = door.texture
                door.off = alttext_list[door.associate - 1]
                door.open = False
        alttext_list1 = []
        for i in range(6):  # this does the exact same as the door code except for the actuators.
            texture = arcade.load_texture("Tilesets/act-Sheet.png", x=i * 160, y=160, height=160, width=160)
            alttext_list1.append(texture)
        for hit in self.actuator_list:
            hit.associate = self.example[hit.texture]
            hit.origin = hit.texture
            hit.open = True
            hit.off = alttext_list1[hit.associate - 1]
        alttext_list2 = []
        for i in range(7):  # this does the exact same as the door code except for the levers.
            texture = arcade.load_texture("Tilesets/Levers.png", x=i * 320, y=320, height=320, width=320)
            alttext_list2.append(texture)
        for lev in self.levers:
            lev.associate = self.example3[lev.texture]
            lev.origin = lev.texture
            lev.on = False
            lev.off = alttext_list2[lev.associate]

        # releoading all collision lists for the physics engine so that it wont stack multiple physics engines.
        self.all_list = None
        self.all_list = arcade.SpriteList()
        self.all_list.extend(self.wall_list)
        self.all_list.extend(self.platform_list)
        self.all_list.extend(self.door_list)

        self.alt_all_list = None
        self.alt_all_list = arcade.SpriteList()
        self.alt_all_list.extend(self.wall_list)
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
        for door in self.door_list:
            if door.open:
                self.all_list.remove(door)
                self.alt_all_list.remove(door)
        self.player.health = 4  # regen player to full
        self.health.texture = self.health.state[abs(self.player.health - 4)]

        # special conditions for these levels, activating events in these levels like unlocking abilities, setting the
        # new major checkpoint, and starting the bossfight room.
        if self.current == "S6_win":
            self.ableto_wall_jump = True
            self.reset_point = 'S6_win'
            self.saved_prev = self.prev
            self.saved_facing = self.player.FACING
        elif self.current == "S6_1":
            self.reset_point = 'S6_1'
            self.saved_prev = self.prev
            self.saved_facing = self.player.FACING
        elif self.current == "S6_5":
            self.reset_point = 'S6_5'
            self.saved_prev = self.prev
            self.saved_facing = self.player.FACING
        elif self.current == "S6_84":
            self.reset_point = 'S6_84'
            self.saved_prev = self.prev
            self.saved_facing = self.player.FACING

        if self.current == "S6_boss":
            self.inside_bossroom = True
            self.boss.center_x = 40 * 48
            self.boss.center_y = 21 * 48
            self.boss.gun.center_x = self.boss.center_x
            self.boss.gun.center_y = self.boss.center_y
            self.boss.skin.center_x = self.boss.center_x
            self.boss.skin.center_y = self.boss.center_y

        # check for if the player has already been in the current room so that a entering room conversation doesnt
        # appear twice. If this is the first time, it will start a conversation with the same name as the level.
        if (self.current not in self.ventures and self.current in conversations.enter_level) or (self.current is None):
            self.ventures.append(self.current)
            self.stop_doing_shit()  # stops all player variables
            self.interacting = True  # stops the player from being able to move and use other abilities
            self.target_x = self.player.center_x
            self.target_y = self.player.center_y + SCREEN_HEIGHT // 12
            self.conv.center_x = self.player.center_x
            # sets the screen in a sensible position so that it doesnt clip outside the map and keeps the player
            # in focus
            if self.player.center_x - SCREEN_WIDTH//2 <= 0:
                self.conv.center_x = SCREEN_WIDTH//2
            elif self.player.center_x + SCREEN_WIDTH//2 >= len(self.my_map.layers[0].layer_data[0]) * 48:
                self.conv.center_x = len(self.my_map.layers[0].layer_data[0]) * 48 - SCREEN_WIDTH//2
            self.conv.center_y = self.player.center_y - SCREEN_HEIGHT // 3
            if self.player.center_y - SCREEN_HEIGHT//3 - 100 <= 0:
                self.conv.center_y = SCREEN_HEIGHT//6

            if self.current is not None:
                if self.current in conversations.enter_level:
                    # reads the conversation dictionary and checks if there
                    # is a conversation tree with the same name as the loaded level.
                    self.conv.setup(tree=self.current, enter='enter')
            else:
                # this is used for the start level because it returns "None"
                self.conv.setup(tree="S6_1", enter='enter')
                self.ventures.append("S6_1")

            # sets the screen in the right place.
            self.view_left = self.player.center_x - SCREEN_WIDTH//2
            self.view_bottom = self.player.center_y - SCREEN_HEIGHT//2
            if self.view_left <= 0:
                self.view_left = 0
            elif self.view_left >= (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH:
                self.view_left = (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH
            if self.view_bottom <= 0:
                self.view_bottom = 0
            elif self.view_bottom >= len(self.my_map.layers[0].layer_data) * 48:
                self.view_bottom = len(self.my_map.layers[0].layer_data) * 48
            arcade.set_viewport(self.view_left // 1,
                                (SCREEN_WIDTH + self.view_left - 1) // 1,
                                self.view_bottom // 1,
                                (SCREEN_HEIGHT + self.view_bottom - 1) // 1)

    def setup(self):
        """
            Its the setup.
            Innitialise all the sprite_lists,
            and set important x's and y's.
        """
        self.wall_list = arcade.SpriteList()
        self.back_list = arcade.SpriteList()
        self.back_list2 = arcade.SpriteList()
        self.tiling_list = arcade.SpriteList()
        self.effect_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()
        self.player.bullet_list = arcade.SpriteList()
        self.player.effect_list = arcade.SpriteList()
        self.detail_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.all_list = arcade.SpriteList()
        self.alt_all_list = arcade.SpriteList()
        self.actuator_list = arcade.SpriteList()
        self.levers = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.text_list = arcade.SpriteList()
        self.interactables_list = arcade.SpriteList()
        self.grapple_list = arcade.SpriteList()
        self.gate_list = arcade.SpriteList()
        self.barb_list = arcade.SpriteList()
        self.res_list = arcade.SpriteList()
        self.ledges = arcade.SpriteList()
        self.turret_list = arcade.SpriteList()
        self.turret_beams = arcade.SpriteList()
        self.shade_list = arcade.SpriteList()

        self.player.center_y = 1000
        self.player.center_x = 1000
        self.rope = arcade.Sprite()
        self.rope.texture = arcade.load_texture("Player/roap3.png")
        self.rope.center_x = -100
        self.rope.center_y = -100
        self.rope.scale = 0.1

        # just fixing the player hitbox to better fit the character build and ignore the scarf flapping.
        self.player.set_hit_box(((-50.0, -130.0), (-30.0, -160.0), (30.0, -160.0), (50.0, -140.0), (50.0, 100.0),
                                 (20.0, 130.0), (-30.0, 130.0), (-50.0, 100.0)))

        self.backdrop = arcade.Sprite()
        self.backdrop.texture = arcade.load_texture("Backdrop/Scene1.png")
        self.backdrop.center_x = 2000
        self.backdrop.center_y = 1000
        self.backdrop.scale = 3

        """---------Start Level----------"""
        self.load_level(arcade.read_tmx("Worlds/Forest/S6_1.tmx"))

    def update(self, delta_time: float):
        if self.game_end:  # runs if the player activates the endscreen
            if not self.ready:  # transition to black
                if self.shade.alpha <= 250:
                    self.shade.alpha += 2
                else:
                    self.dramatimer += 1
                    if self.dramatimer >= 80:  # activate the final conversation, and final thanks.
                        # (basically end the game)
                        self.interacting = True
                        self.shade.alpha = 255
                        self.conv.setup(tree='end', enter='talk')
                        self.ready = True
        elif not self.respawning:  # if the player isnt currently dead, run the game normally
            if self.shade.alpha > 4:  # at some points the screen is dark, and this transitions it back to bright.
                self.end_times -= 0.3
                self.shade.alpha = 255 * (((math.cos(self.end_times - math.pi)) / 2) + 0.5) // 1
                if self.shade.alpha <= 4:
                    self.shade.alpha = 0
                    self.end_times = 0

            # this is a check for all the things that decide wether or not you should pass through platforms.
            # if you are either: pressing S, is jumping, or were inside a platform in the previous update,
            # you will pass through.
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

            # check for if youre trying to flip a lever
            for lev in self.levers:
                if arcade.check_for_collision(lev, self.player):
                    if self.E:
                        self.hitted(target=lev)
                        self.E = False

            # check for if a bullet has hit a target, and run the door switching function if it did.
            for target in self.actuator_list:
                collide = arcade.check_for_collision_with_list(target, self.player.bullet_list)
                if collide:
                    for bullet in self.player.bullet_list:
                        b = arcade.check_for_collision_with_list(bullet, self.actuator_list)
                        if b and not bullet.swipe:
                            bullet.remove_from_sprite_lists()
                            del bullet
                    self.hitted(target=target)

            # check for if a bullet has hit an enemy, if yes, kill it.
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
            # check for if a bullet has hit a wall
            for bullet in self.player.bullet_list:
                if not bullet.swipe:
                    c = arcade.check_for_collision_with_list(bullet, self.alt_all_list)
                    if c:
                        bullet.remove_from_sprite_lists()
                        del bullet

            """ ----------- LEDGE-CLIMBING ----------- """
            # this handles when the player comes into contact with a climbable ledge, checking one pixel to the right
            # and left of the player for contact. if they are, the player is teleported on top of the ledge tile and
            # is deactivated, then an animation of the player climbing the ledge plays.
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
            # this is a long bit of code that works a lot similarly to arcades built in "can_jump()" program
            # moving the player one pixel left and right, checking if its touching a wall, every update.
            # if the player is, they start hugging the wall and their descent is slowed drastically.
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

            # the animation of the player climbing the ledge is run here.
            if self.player.is_climbing:
                self.player.change_y = 0
                self.player.change_x = 0
                self.climb_guy.update_animation()
                if self.climb_guy.die:
                    self.climb_guy.die = False
                    self.player.is_climbing = False
                    self.player.texture = self.player.walking[self.player.FACING][0]
                    self.player.alpha = 255
                    self.climb_guy.alpha = 1
                    self.climb_guy.center_y = -100
                    self.climb_guy.center_x = -100
            else:
                # player movement is tunred off if they are currently climbing a ledge
                self.player.update()
            self.player.effect_list.update()
            self.player.bullet_list.update()

            """ -- boss room explanation -- """
            # a buch of checks for certain events in the boss room.
            # for the boss fight to start a few things have to happend,
            # for starters, the player has to be in the boss room.
            # then, the player has to touch the respawn point in the middle of the room, wich starts the prelude.
            # during this prelude the screen focuses on the boss as it wakes up, when a timer becomes zero,
            # the camera returns to the player and the fight begins.
            if self.inside_bossroom and not self.boss_battle and self.bossbattle_prelude == -1:
                if arcade.check_for_collision_with_list(self.player, self.res_list):
                    self.bossbattle_prelude = 200
                    for door in self.door_list:  # when the boss wakes up the doors on the left close.
                        if door.associate == 2:
                            door.texture = door.origin
                            self.all_list.append(door)
                            self.alt_all_list.append(door)
                            door.open = False
            if self.boss.win:  # when the player wins the doors on the right open up.
                for door in self.door_list:
                    if door.associate == 5:
                        if not door.open:
                            door.texture = door.off
                            self.all_list.remove(door)
                            self.alt_all_list.remove(door)
                            door.open = True

            # the grappling check looks for the closest grapple point, if that point is within 500px's then grappling
            # can occur, otherwise nothing happens.
            p = False
            for i in self.grapple_list:
                x_diff = self.player.center_x - i.center_x
                y_diff = self.player.center_y - i.center_y
                i.dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
                if i.dist < 500:  # check the hypotenuse (distance to) the grapple point from the player.
                    self.attach_point_x = i.center_x
                    self.attach_point_y = i.center_y
                    if not self.grappling:
                        self.origin_dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
                    p = True
            if not p:
                self.grappling = False

            # code that handles the grappling mechanic that actually isnt used in the game. ;(
            # "p" is a check to make sure the player is still in range of the grapple point.
            if self.grappling and p:
                # finds measurements relative to the point and player
                self.player.grapling = True
                self.player.physics_engines[0].gravity_constant = 0
                diff_x = self.player.center_x - self.attach_point_x
                diff_y = self.player.center_y - self.attach_point_y
                self.grapple_angle = math.atan2(diff_y, diff_x)
                self.grapple_dist = math.sqrt((diff_x ** 2) + (diff_y ** 2))

                # math to find the right location for the rope between the player and point
                self.rope.center_x = (self.player.center_x + self.attach_point_x) / 2
                self.rope.center_y = (self.player.center_y + self.attach_point_y) / 2
                grapple_acc = self.grapple_angle - math.pi/2  # calculation of the expected acceleration of the grapple
                if grapple_acc < 0:
                    grapple_acc += math.pi*2
                # fancy calculations aedan helped me with that needed gravity constants to find the expected velocity
                # of the player as they swing like spiderman across the ruins.
                self.grapple_velocity += GRAVITY*1.4 * 0.4 * math.sin(grapple_acc)
                self.grapple_angle += self.grapple_velocity * delta_time * 0.2
                self.player.change_y = 0
                # setting the players cords as the expected point using previos math.
                self.player.center_x = self.attach_point_x + math.cos(self.grapple_angle) * self.origin_dist
                self.player.center_y = self.attach_point_y + math.sin(self.grapple_angle) * self.origin_dist

                self.rope.angle = math.degrees(self.grapple_angle) - 90
                self.rope.height = self.origin_dist
            else:
                self.rope.center_x = -1000
                self.rope.center_y = -1000

            # as talked about before, in the boss room explanation.
            if self.bossbattle_prelude == 0 and self.inside_bossroom:  # a timer check
                self.boss_battle = True
                self.boss.start = True
                self.boss.alpha = 254
                self.boss.gun.alpha = 254
            if self.bossbattle_prelude > 0 and self.inside_bossroom:  # another timer check
                # in here the boss waking up plays, and the camera is forced to focus on the boss.
                self.bossbattle_prelude -= 1
                self.boss.gun.alpha = (250 * ((201 - self.bossbattle_prelude)/200)) + 1
                self.boss.alpha = (250 * ((201 - self.bossbattle_prelude)/200)) + 1
                character_offset_x = int(self.boss.center_x) - int(self.view_left + (SCREEN_WIDTH // 2))
                character_offset_y = int(self.boss.center_y) - int(self.view_bottom + (SCREEN_HEIGHT // 2))

            elif not self.interacting:  # camera targeting when normal gameplay
                # setting the target location for the camera to be on the player
                character_offset_x = int(self.player.center_x) - int(self.view_left + (SCREEN_WIDTH // 2))
                character_offset_y = int(self.player.center_y) - int(self.view_bottom + (SCREEN_HEIGHT // 2))
            else:  # camera targeting when in a conversation
                # setting the target location as slightly above the conversation box
                character_offset_x = int(self.target_x) - int(self.view_left + (SCREEN_WIDTH // 2))
                character_offset_y = int(self.target_y) - int(self.view_bottom + (SCREEN_HEIGHT // 2))

            if self.player.attacking:  # if the player is usning the gun, they can see much furhter than normal
                character_offset_x = character_offset_x + int((self.x_t-(SCREEN_WIDTH+(SCREEN_WIDTH*SCREEN_ALT*2))//2)
                                                              * 0.6)
                character_offset_y = character_offset_y + int((self.y_t-(SCREEN_HEIGHT+(SCREEN_HEIGHT*SCREEN_ALT*2))//2)
                                                              * 0.4)
            if not self.interacting:
                if self.bossbattle_prelude > 0 and self.inside_bossroom:
                    # removes the player movement addition so the camera doesnt wobble
                    # if you move during the boss waking up scene
                    self.view_left = self.view_left + (character_offset_x // 10)
                else:
                    # small detail that when the player moves the camera kindof conpensates, pushing ahead as you run
                    self.view_left = self.view_left + ((character_offset_x // 10) + self.player.change_x * 1.2)

                # checks for if the camera would reach outside of the map, and instead setting the corners of the screen
                # to be the limits of the map instead. (eg, if the left side of the screen would become negative,
                # it is set to zero instead.
                if self.view_left <= 0 + SCREEN_WIDTH*SCREEN_ALT:
                    # "screen_alt" is a variable that i use to chage how far back the camera is,
                    # basically how much you can see.
                    self.view_left = 0 + SCREEN_WIDTH*SCREEN_ALT
                elif self.view_left >= len(self.my_map.layers[0].layer_data[0])*48 - SCREEN_WIDTH*(1+SCREEN_ALT):
                    self.view_left = len(self.my_map.layers[0].layer_data[0])*48 - SCREEN_WIDTH*(1+SCREEN_ALT)
                self.view_bottom = self.view_bottom + (character_offset_y // 10) + 10
                if self.view_bottom <= 0 + SCREEN_HEIGHT*SCREEN_ALT:
                    self.view_bottom = 0 + SCREEN_HEIGHT*SCREEN_ALT
                elif self.view_bottom >= len(self.my_map.layers[0].layer_data)*48 - SCREEN_HEIGHT*(1+SCREEN_ALT):
                    self.view_bottom = len(self.my_map.layers[0].layer_data)*48 - SCREEN_HEIGHT*(1+SCREEN_ALT)
                arcade.set_viewport((self.view_left - SCREEN_WIDTH*SCREEN_ALT)//1, (SCREEN_WIDTH*(1+SCREEN_ALT) +
                                                                                    self.view_left - 1)//1,
                                    (self.view_bottom - SCREEN_HEIGHT*SCREEN_ALT)//1, (SCREEN_HEIGHT*(1+SCREEN_ALT) +
                                                                                       self.view_bottom - 1)//1)
            if self.timertoautofocus > 0:  # timertoautofocus is a timer function.
                self.timertoautofocus -= 1
            if self.interacting:
                # if the player is interacting, the camera will instead focus on the
                # item or character they are looking at instead of the player.
                self.view_left = self.view_left + (character_offset_x // 10)
                self.view_bottom = self.view_bottom + (character_offset_y // 10)
                if 5 >= abs(self.target_x) - abs(self.view_left + (SCREEN_WIDTH // 2)) or self.timertoautofocus <= 0:
                    self.view_left = self.target_x - SCREEN_WIDTH//2
                if 5 >= abs(((SCREEN_HEIGHT // 2) + self.view_bottom) - self.target_y) or self.timertoautofocus <= 0:
                    self.view_bottom = self.target_y - SCREEN_HEIGHT//2
                self.conv.update()

            # setting the location of the background but at a delay, so as you move right it moves away much slower,
            # creating the illusion that it is much furhter away.
            self.backdrop.center_x = (3100 + self.view_left // 2) - ((self.backdrop.width//5)*2)
            self.backdrop.center_y = (1600 + self.view_bottom // 6) - (self.backdrop.height//4)
            # giving the player the location of the mouse.
            self.player.x_t = self.x_t + self.view_left - (SCREEN_WIDTH*SCREEN_ALT)
            self.player.y_t = self.y_t + self.view_bottom - (SCREEN_HEIGHT*SCREEN_ALT)

            if self.player.beaning or self.player.beanter:  # check for if the player is climbing a wall
                self.player.change_y += 1

            if self.boss_battle:  # if the boss is active, it is updated.
                self.bossing()

            # running the checks for the bosses attacks, like if the player is hit.
            for beam in self.boss.attack_list:
                if beam.can_it:
                    a = arcade.check_for_collision(beam, self.player)
                    if a and self.player.health > 0:
                        # if the player is hit they will not return to the respawn point
                        # but will instead simply lose one hp
                        beam.can_it = False
                        self.player.health -= 1
                        self.health.texture = self.health.state[abs(self.player.health-4)]
                        if self.player.health <= 0:
                            # if the player dies, they return po the last major save point.
                            self.respawning = False
                            self.prev = self.saved_prev
                            self.player.change_x = 0
                            self.player.FACING = self.saved_facing
                            self.current = self.reset_point
                            self.load_level(arcade.tilemap.read_tmx(f"Worlds/Forest/{self.reset_point}.tmx"))
                            self.reset_boss()

            # this handles the location of the health, cursor,
            # and the shade that tunrs the screen black.
            wind = arcade.get_viewport()
            self.health.center_x = wind[0] + 640*0.3 + 10
            self.health.center_y = wind[3] - 160*0.3 - 10
            self.perm_x = self.x_t + self.view_left - (SCREEN_WIDTH*SCREEN_ALT)
            self.perm_y = self.y_t + self.view_bottom - (SCREEN_HEIGHT*SCREEN_ALT)
            self.curs.center_x = self.perm_x
            self.curs.center_y = self.perm_y
            self.shade.center_x = self.player.center_x
            self.shade.center_y = self.player.center_y

            # sets a new revive point in a level when the player touches one.
            if arcade.check_for_collision_with_list(self.player, self.res_list):
                for res in self.res_list:
                    if arcade.check_for_collision(res, self.player):
                        self.res_act = res

            # checks if the player is touching an interactible, setting the "interactive" icon over it when close by
            if arcade.check_for_collision_with_list(self.player, self.interactables_list):
                for inter in self.interactables_list:
                    if arcade.check_for_collision(inter, self.player):
                        self.can_interact.center_x = inter.center_x
                        self.can_interact.center_y = inter.center_y
            else:
                self.can_interact.center_x = -100
                self.can_interact.center_y = -100

            # takes the closest interactible and places a diamond shaped icon over it when close by,
            # it becomes more opaque the closer you are.
            for inter in self.interactables_list:
                x_dist = abs(inter.center_x - self.player.center_x)
                y_dist = abs(inter.center_y - self.player.center_y)
                dist = math.sqrt((x_dist ** 2) + (y_dist ** 2))
                if dist <= 280:  # maximum visible distance.
                    self.can_interact.center_x = inter.center_x
                    self.can_interact.center_y = inter.center_y
                    if dist <= 36:
                        self.can_interact.alpha = 254
                    else:
                        self.can_interact.alpha = 280 - dist

            # makes it so that the player can only be hit by a laserbeam once.
            b = False
            for i in self.turret_list:
                for beam in i.attack_list:
                    if beam.can_it:
                        s = arcade.check_for_collision(beam, self.player)
                        if s:
                            b = True

            # checks for collision with the gates that transport the player between levels.
            # when you collide with a gate, it reads the current level name, saves it as the previous level,
            # and makes the new level the name of the gate, then loads that level.
            if arcade.check_for_collision_with_list(self.player, self.gate_list):
                for i in self.gate_list:
                    if arcade.check_for_collision(i, self.player):
                        if self.current == "S6_boss":
                            self.reset_boss()
                        self.prev = self.current
                        self.current = i.properties['dest']
                        self.load_level(arcade.tilemap.read_tmx(f"Worlds/Forest/{i.properties['dest']}.tmx"))
                        self.view_left = self.player.center_x - SCREEN_WIDTH // 2
                        self.view_bottom = self.player.center_y - SCREEN_HEIGHT // 2

            # checks for collision with environmental dangers, if the player comes into contact with one of these,
            # the screen fades to black and you return at the previous save point.
            elif arcade.check_for_collision_with_list(self.player, self.barb_list) or b:
                if self.player.health > 0:
                    self.player.health -= 1
                    self.health.texture = self.health.state[abs(self.player.health - 4)]
                    self.respawning = True
            self.turret_list.update()
        else:  # if the player is taking damage, the game stops and fades to black
            self.end_times += 0.1
            self.shade.alpha = 255 * (((math.cos(self.end_times - math.pi)) / 2) + 0.5) // 1
            if self.shade.alpha >= 250:
                if self.player.health <= 0:
                    # if the player has no health left, they return to the last major save location.
                    self.respawning = False
                    self.prev = self.saved_prev
                    self.player.change_x = 0
                    self.player.FACING = self.saved_facing
                    self.current = self.reset_point
                    self.load_level(arcade.tilemap.read_tmx(f"Worlds/Forest/{self.reset_point}.tmx"))
                else:
                    # if the player has at least one health left, they return to a revive point.
                    self.respawning = False
                    self.player.center_x = self.res_act.center_x
                    self.player.center_y = self.res_act.center_y
                    self.view_left = self.player.center_x - SCREEN_WIDTH//2 - ((SCREEN_WIDTH*SCREEN_ALT)//2)
                    self.view_bottom = self.player.center_y - SCREEN_HEIGHT//2 - ((SCREEN_HEIGHT*SCREEN_ALT)//2)
                    self.player.change_x = 0
                    self.player.change_y = 0

    def on_draw(self):
        """its the on draw, it renders the whole game"""
        arcade.start_render()
        self.backdrop.draw()
        self.back_list2.draw()
        self.back_list.draw()
        self.res_list.draw()
        self.interactables_list.draw()
        self.platform_list.draw()
        self.levers.draw()
        self.effect_list.draw()
        self.rope.draw()
        self.player.draw()
        self.climb_guy.draw()
        self.player.gun.draw()
        self.tiling_list.draw()
        self.wall_list.draw()
        self.barb_list.draw()
        self.barb_list.update_animation()
        self.enemy_list.draw()
        self.player.effect_list.draw()
        self.actuator_list.draw()
        self.door_list.draw()
        self.player.bullet_list.draw()
        self.shade_list.draw()
        self.turret_list.draw()
        for turret in self.turret_list:  # some difficulties with the turret and its lasers
            turret.on_draw()
            turret.beam_list.update()
        self.grass_list.draw()
        self.detail_list.draw()
        self.grapple_list.draw()
        if self.inside_bossroom:  # only draws the boss when in the boss room.
            self.boss.on_draw()
        self.can_interact.draw()
        self.curs.draw()
        self.shade.draw()

        if self.interacting:  # shows the conversation box only when interacting.
            self.conv.on_draw()
        self.health.draw()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            exit()  # exit key
        if not self.player.is_climbing:  # stops player input while climing a ledge.
            if not self.interacting:  # stops player input while in a conversation.
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
                    self.grappling = True
                elif key == arcade.key.S:
                    self.S = True
                elif key == arcade.key.E:
                    self.e()
            else:  # all buttons available when in a conversation.
                self.conv.on_key_press(key)
                if self.conv.exit_time:
                    self.anti_e()
                    self.conv.exit_time = False
                if key == arcade.key.P:
                    self.anti_e()
            if not self.interacting:
                # all the "dev" shortcuts, like resetting health, teleporting, turning wall jump on earily,
                # and remote controlling doors.
                if key == arcade.key.KEY_1:
                    self.player.center_x = 500
                    self.player.center_y = 500
                if key == arcade.key.KEY_3:
                    self.player.health = 4
                if key == arcade.key.KEY_5:
                    self.ableto_wall_jump = True
                if key == arcade.key.KEY_7:
                    for door in self.door_list:
                        if not door.open:
                            self.all_list.remove(door)
                            self.alt_all_list.remove(door)
                            door.open = True
                        else:
                            self.all_list.append(door)
                            self.alt_all_list.append(door)
                            door.open = False

    def on_key_release(self, key: int, _modifiers: int):
        if not self.interacting:
            self.player.on_key_release(key, _modifiers)
            if key == arcade.key.LSHIFT and self.grappling:
                # causes the player to sortof "jump" when releasing their grapple.
                # the speed and direction of this thrust is dependant on the acceleration and velocity of the grapple
                # pre-release.
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
        # records the mouse location and a few calculations for specific uses.
        screen_bottom = self.view_bottom - (SCREEN_HEIGHT*SCREEN_ALT)
        screen_left = self.view_left - (SCREEN_WIDTH*SCREEN_ALT)
        self.x = x + screen_left
        self.y = y + screen_bottom

        self.player.workpleasex = self.view_left
        self.player.workpleasey = self.view_bottom
        self.x_t = x*(1+SCREEN_ALT*2)
        self.y_t = y*(1+SCREEN_ALT*2)
        self.player.x = self.x
        self.player.y = self.y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if not self.interacting:
            self.player.on_mouse_press(button)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.interacting:
            self.player.on_mouse_release(button)

    def anti_e(self):
        """Exits the conversation box"""
        self.interacting = False
        self.player.interacting = False
        for letter in self.text_list[::-1]:
            letter.remove_from_sprite_lists()
            del letter

    def stop_doing_shit(self):
        """Resets the player, stopping all active buttons."""
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

    def e(self):
        """Function ran when checking for interaction"""
        self.E = True
        if self.numb_interact is not None:
            for i in self.interactables_list:
                if arcade.check_for_collision(i, self.player):
                    # This chekcs the name of the tree given by the interactible against all conversations in the
                    # dictionary file, and loads the conversation tied to that conversation.
                    if i.properties['tree'] == 'end':
                        # special conversation that only runs for the end-of-game conversation, turning the screen
                        # black before showing the conversation. other than that no difference,
                        # for more detailed description, look at the next one where i explain the normal code.
                        self.game_end = True
                        self.shade.alpha = 0
                        self.stop_doing_shit()
                        self.target_x = self.player.center_x
                        self.target_y = self.player.center_y + SCREEN_HEIGHT // 12
                        self.conv.center_x = self.player.center_x
                        if self.player.center_x - SCREEN_WIDTH // 2 <= 0:
                            self.conv.center_x = SCREEN_WIDTH // 2
                        elif self.player.center_x + SCREEN_WIDTH // 2 >= len(self.my_map.layers[0].layer_data[0]) * 48:
                            self.conv.center_x = len(self.my_map.layers[0].layer_data[0]) * 48 - SCREEN_WIDTH // 2
                        self.conv.center_y = self.player.center_y - SCREEN_HEIGHT // 3
                        if self.player.center_y - SCREEN_HEIGHT // 3 - 100 <= 0:
                            self.conv.center_y = SCREEN_HEIGHT // 6
                        self.view_left = self.player.center_x - SCREEN_WIDTH // 2
                        self.view_bottom = self.player.center_y - SCREEN_HEIGHT // 2
                        if self.view_left <= 0:
                            self.view_left = 0
                        elif self.view_left >= (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH:
                            self.view_left = (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH
                        if self.view_bottom <= 0:
                            self.view_bottom = 0
                        elif self.view_bottom >= len(self.my_map.layers[0].layer_data) * 48:
                            self.view_bottom = len(self.my_map.layers[0].layer_data) * 48
                        arcade.set_viewport(self.view_left // 1,
                                            (SCREEN_WIDTH + self.view_left - 1) // 1,
                                            self.view_bottom // 1,
                                            (SCREEN_HEIGHT + self.view_bottom - 1) // 1)

                    else:  # runs for each conversation that isnt the end of game conversation.
                        self.E = False
                        text_tree = i.properties['tree']  # records the conversation name.
                        if i.properties['talk']:  # checks what type it is.
                            text_type = 'talk'
                        else:
                            text_type = 'invest'
                        self.stop_doing_shit()
                        self.interacting = True

                        # finds the right position for the conversation and the location the camera should focus on.
                        self.target_x = self.player.center_x
                        self.target_y = self.player.center_y + SCREEN_HEIGHT // 12
                        self.conv.center_x = self.player.center_x
                        if self.player.center_x - SCREEN_WIDTH // 2 <= 0:
                            self.conv.center_x = SCREEN_WIDTH // 2
                        elif self.player.center_x + SCREEN_WIDTH // 2 >= len(self.my_map.layers[0].layer_data[0]) * 48:
                            self.conv.center_x = len(self.my_map.layers[0].layer_data[0]) * 48 - SCREEN_WIDTH // 2
                        self.conv.center_y = self.player.center_y - SCREEN_HEIGHT // 3
                        if self.player.center_y - SCREEN_HEIGHT // 3 - 100 <= 0:
                            self.conv.center_y = SCREEN_HEIGHT // 6

                        # runs the conversaiton code from the conversation file
                        self.conv.setup(tree=text_tree, enter=text_type)

                        # sets the screen in the right position
                        self.view_left = self.player.center_x - SCREEN_WIDTH // 2
                        self.view_bottom = self.player.center_y - SCREEN_HEIGHT // 2
                        if self.view_left <= 0:
                            self.view_left = 0
                        elif self.view_left >= (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH:
                            self.view_left = (len(self.my_map.layers[0].layer_data[0]) * 48) - SCREEN_WIDTH
                        if self.view_bottom <= 0:
                            self.view_bottom = 0
                        elif self.view_bottom >= len(self.my_map.layers[0].layer_data) * 48:
                            self.view_bottom = len(self.my_map.layers[0].layer_data) * 48
                        arcade.set_viewport(self.view_left // 1,
                                            (SCREEN_WIDTH + self.view_left - 1) // 1,
                                            self.view_bottom // 1,
                                            (SCREEN_HEIGHT + self.view_bottom - 1) // 1)
                        self.timertoautofocus = 40

    def hitted(self, target):
        """When a activator is activated this code runs"""
        for door in self.door_list:  # runs through all doors in the level
            if door.associate == target.associate:  # opens or closes all doors with the right colour.
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
        for turret in self.turret_list:  # runs through all turrets in the level
            if turret.associate == target.associate:  # activates or deactivates all turrets with the right colour.
                if turret.active:
                    turret.texture = turret.off
                    turret.active = False
                else:
                    turret.texture = turret.origin
                    turret.active = True
        # updates the physics engine to account for the ne open and closed doors.
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
        if target.identify == 1:  # changing the texture of the thing that was hit.
            target.texture = target.off
        else:
            target.texture = target.origin
        target.identify = target.identify * -1  # variable recording its on/off position.

    def bossing(self):
        """Ran while bossbattle is active
        basically just updates the boss and finds the position of the player relative to the boss"""
        self.boss.update()
        diff_x = self.player.center_x - self.boss.center_x
        diff_y = self.player.center_y - self.boss.center_y
        angley = math.atan2(diff_y, diff_x)
        self.boss.angletoplayer = math.degrees(angley)

    def reset_boss(self):
        """When leaving the boss room to reset them."""
        self.inside_bossroom = False
        self.boss_battle = False
        self.bossbattle_prelude = -1
        self.boss.reset()


class Letter(arcade.Sprite):
    """Holds all the letters in my alphabet"""
    def __init__(self):
        super().__init__()
        self.capitals = []
        texture = arcade.load_texture("Text/fonts.png", x=1600, y=640, height=320, width=80)
        self.capitals.append(texture)
        for i in range(26):
            texture = arcade.load_texture("Text/fonts.png", x=(i*90)+5, y=320, height=320, width=80)
            self.capitals.append(texture)
        self.texture = arcade.load_texture("Text/fonts2.png", x=0, y=0, height=1, width=1)
        self.scale = 0.5
        self.is_letter = True


class Health(arcade.Sprite):
    """Sprite showing player health"""
    def __init__(self):
        super().__init__()
        self.state = []
        for i in range(5):
            texture = arcade.load_texture("Spritesheets/health-Sheet.png", x=i*640, y=0, height=160, width=640)
            self.state.append(texture)
        self.texture = self.state[0]
        self.scale = 0.5


class PClimb(arcade.Sprite):
    """The texture put on top of the player while climbing a ledge."""
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
        """Runs through the whole animation then deletes itself."""
        self.cur_texture += 1
        if self.cur_texture >= (6 * 8) - 1:
            self.cur_texture = 0
            self.die = True
        self.texture = self.climbing[self.face][(self.cur_texture//6)]


class Curs(arcade.Sprite):
    """Sprite holding the cursor sprite"""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Player/curs.png")
        self.scale = 0.5


class Target(arcade.Sprite):
    """While near an interactible this shows up to show where it is."""
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Text/can_interact.png")
        self.scale = 0.5
        self.angle = 45


class Last(arcade.View):
    """The view shown right before the game starts."""
    def __init__(self):
        super().__init__()
        self.start_overgrowth = False
        self.end_overgrowth = False
        self.overt = Titlecards()
        self.end_timer = 0
        self.end_overgrowth = False
        self.start_timer = 0

    def on_show(self):
        self.overt.texture = self.overt.text_list[3]
        self.overt.center_x = SCREEN_WIDTH // 2
        self.overt.center_y = SCREEN_HEIGHT // 2

    def on_draw(self):
        arcade.start_render()
        self.overt.draw()

    def update(self, delta_time: float):
        """Animates the OVERGROWTH titlecard to fade in, then out"""
        self.start_timer += 1
        if self.start_timer == 100:
            self.start_overgrowth = True
        if self.start_overgrowth:
            self.end_timer += 2
            self.overt.alpha = self.end_timer
            if self.overt.alpha >= 250:
                self.start_overgrowth = False
                self.end_overgrowth = True
                self.end_timer += 100
        elif self.end_overgrowth:
            self.end_timer -= 2
            if self.end_timer <= 255:
                self.overt.alpha = self.end_timer
                if self.overt.alpha <= 5:
                    game = Game()
                    self.window.show_view(game)

    def on_key_press(self, symbol: int, modifiers: int):
        # allows the player to skip this screen
        game = Game()
        self.window.show_view(game)


class Tutorial(arcade.View):
    """Shows the tutorial screen"""
    def __init__(self):
        super().__init__()
        arcade.set_background_color((20, 18, 24))
        self.sheet_list = arcade.SpriteList()
        # all these are the text that is displayed on the different pages.
        self.words = [
            "",
            "",
            "Here are my instructions of all the features of the game.",
            "",
            "  [PRESS ANY KEY TO CONTINUE TO NEXT PAGE]",
        ]
        self.movement = [
            "Movement:",
            "  Movement is controlled by pressing [A] and [D].",
            "  To jump press [W] or [SPACE].",
            "",
            "  You can choose to fall through wooden platforms by",
            "  pressing [S], allowing you to fall down through said",
            "  platforms.",
        ]
        self.ledge = [
            "Ledges and climbing:",
            "  Some ledges are marked with a little wooden",
            "  stake sticking out of the corner. If your",
            "  character collides with its side, you will ",
            "  automatically climb on top of the ground.",
            "",
            "  The first time doing it from the left and",
            "  right is ALWAYS laggy, there isnt really any",
            "  way around it.",
            "  Afterwards it should be smooth though."
        ]
        self.conversations = [
            "Controlling Conversations:",
            "  When presented with 1 to 4 choices (at the bottom)",
            "  the player can use the [1, 2, 3, 4] keys to select one.",
            "  Then press [E] or [ENTER] to continue.",
            "  If no options are presented, press [E] or [ENTER] to",
            "  continue the conversation.",
            "",
            "  Sometimes the selected choice will stay after the ",
            "  conversation continues, so if the selected text stays ",
            "  after you pressed E or enter, just ignore it.",
        ]
        self.doors = [
            "Doors and Levers:",
            "  Doors are brightly lit blocks that stop you from",
            "  progressing through a level, a faded semi translucent",
            "  door is open, and can be moved through.",
            "  To open and close a door, stand next to a lever and",
            "  press [E] to switch it.",
            "  All doors and levers are connected by colour, so when",
            "  a blue lever is pulled, all blue doors in the level",
            "  will switch its state, from closed to open and vice versa.",
            "  When some doors open others close. And some levels require",
            "  you to go back to previously closed areas."
        ]
        self.walljump = [
            "Walljump extra:",
            "  Small mechanic to remember for second half of the game,",
            "  when you are connected to a wall, you dont have to hold",
            "  yourself against the wall, they will stay there until you jump,",
            "  move in the other direction, or fall off.",
            "",
            "Additionally: if you are connected to a wall you can jump ",
            "  without pressing any direction to propell yourself in",
            "  the opposite direction of the wall."
        ]
        self.point = 0
        self.back = MenueScreens()
        # save all the pages to a list.
        self.dicts = [self.words, self.movement, self.ledge, self.conversations, self.doors, self.walljump]

    def cycle(self, dicts):
        """Cycles through the pages in the tutorial, and moves to the next slide."""
        p = 0
        for i in self.sheet_list[::-1]:
            i.remove_from_sprite_lists()
            del i
        for i in dicts:
            hand = text.gen_letter_list(dicts[p],
                                        40,
                                        (SCREEN_HEIGHT - (60*p) - 40), 0.25)
            self.sheet_list.extend(hand)
            p += 1

    def on_show(self):
        # shows the first page
        self.cycle(self.words)
        self.back.center_x = SCREEN_WIDTH//2
        self.back.center_y = SCREEN_HEIGHT//2
        self.back.texture = self.back.back_list[1]
        self.back.scale = self.back.scale_list[1]

    def on_draw(self):
        arcade.start_render()
        self.back.draw()
        self.sheet_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        self.point += 1
        # when the final page is turned, you are returned to the main screen
        if len(self.dicts) == self.point:
            game = Chooses()
            self.window.show_view(game)
        self.cycle(self.dicts[self.point])


class Chooses(arcade.View):
    """The train screen, where you can access the tutorial, proceed to the game, and exit."""
    def __init__(self):
        super().__init__()
        self.start = Buttons()
        self.start.type = 0
        self.instruct = Buttons()
        self.instruct.type = 1
        self.exitbut = Buttons()
        self.exitbut.type = 2
        self.buttons = arcade.SpriteList()
        self.buttons.append(self.start)
        self.buttons.append(self.instruct)
        self.buttons.append(self.exitbut)
        self.shade = Shade()
        self.select = Select()
        self.sadmouse = Select()
        self.sadmouse.texture = arcade.load_texture("Backdrop/mouse.png")

        self.back = MenueScreens()

    def on_show(self):
        i = 0
        # creates buttonns and other things.
        for but in self.buttons:
            i += 1
            but.center_x = 200
            but.center_y = 300 - i*80
            but.texture = but.back_list[but.type]
        self.shade.center_x = SCREEN_WIDTH//2
        self.shade.center_y = SCREEN_HEIGHT//2
        self.shade.alpha = 255
        self.back.center_x = SCREEN_WIDTH//2
        self.back.center_y = SCREEN_HEIGHT//2
        self.back.texture = self.back.back_list[2]
        self.back.scale = self.back.scale_list[2]
        self.select.center_x = self.start.center_x - 160
        self.select.center_y = self.start.center_y

    def on_draw(self):
        arcade.start_render()
        self.back.draw()
        self.buttons.draw()
        self.select.draw()
        self.shade.draw()

    def update(self, delta_time: float):
        # when entering this screen it is black, then fades into view.
        if self.shade.alpha >= 1:
            self.shade.alpha -= 1

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # checks for touching the buttons, turning a button into the active button when touched.
        self.sadmouse.center_x = x
        self.sadmouse.center_y = y
        if arcade.check_for_collision_with_list(self.sadmouse, self.buttons):
            for i in self.buttons:
                if arcade.check_for_collision(i, self.sadmouse):
                    self.select.center_x = i.center_x - 160
                    self.select.center_y = i.center_y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if arcade.check_for_collision_with_list(self.sadmouse, self.buttons):
            for i in self.buttons:  # if you clicked on a button the corresponding screen is opened.
                if arcade.check_for_collision(i, self.sadmouse):
                    if i.type == 0:
                        game = Last()
                        self.window.show_view(game)
                    elif i.type == 1:
                        game = Tutorial()
                        self.window.show_view(game)
                    elif i.type == 2:
                        exit()


class Start(arcade.View):
    """The start animatic showing the title card."""
    def __init__(self):
        super().__init__()
        self.back = MenueScreens()
        self.tit = Titlecards()
        self.back.type = 0
        self.und_tit = Titlecards()
        self.guide = Titlecards()
        self.tit.type = 0
        self.shade = Shade()
        self.und_tit.type = 1
        self.timer = 0
        self.timer2 = 0
        self.start_timer = 250
        self.distant_fin = False
        self.act_going = False
        self.final = False
        self.final_timer = 0
        self.end_timer = 0
        self.proceed = False

    def on_show(self):
        """ Setting all the elements in the intro screen """
        self.shade.center_x = SCREEN_WIDTH // 2
        self.shade.center_y = SCREEN_HEIGHT // 2

        self.back.texture = self.back.back_list[0]
        self.back.scale = self.back.scale_list[0]
        self.back.center_x = SCREEN_WIDTH // 2
        self.back.center_y = SCREEN_HEIGHT // 2

        self.tit.texture = self.tit.text_list[0]
        self.tit.center_x = SCREEN_WIDTH // 2
        self.tit.center_y = SCREEN_HEIGHT // 2

        self.und_tit.texture = self.und_tit.text_list[1]
        self.und_tit.center_x = SCREEN_WIDTH // 2
        self.und_tit.center_y = SCREEN_HEIGHT // 2

        self.guide.texture = self.guide.text_list[2]
        self.guide.center_x = SCREEN_WIDTH // 2
        self.guide.center_y = SCREEN_HEIGHT // 4

        arcade.set_viewport(0, SCREEN_WIDTH,
                            0, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()
        self.back.draw()
        self.tit.draw()
        self.und_tit.draw()
        self.guide.draw()
        self.shade.draw()

    def update(self, delta_time: float):
        """ Playing the fade in animation for all the elements. """
        # its just a bunch of things fading in and out of view.
        if self.proceed:
            self.end_timer += 3
            self.shade.alpha = self.end_timer
            if self.shade.alpha >= 250:
                self.shade.alpha = 255
                game = Chooses()
                self.window.show_view(game)
        if self.start_timer >= 5:
            self.start_timer -= 3
            self.shade.alpha = self.start_timer
        else:
            self.timer += 2
            if not self.distant_fin:
                self.tit.alpha = self.timer
                if self.tit.alpha >= 250:
                    self.distant_fin = True
                elif self.timer == 160:
                    self.act_going = True
            if self.act_going:
                self.timer2 += 3
                self.und_tit.alpha = self.timer2
                if self.und_tit.alpha >= 250:
                    self.act_going = False
                    self.final = True
            elif self.final:
                self.final_timer += 1.5
                if self.final_timer >= 100:
                    self.guide.alpha = int(self.final_timer - 100)
                    if self.final_timer >= 260:
                        self.final = False

    def on_key_press(self, symbol: int, modifiers: int):
        self.proceed = True


class Shade(arcade.Sprite):
    """ The dark screen to block the window """
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Misc_level_stuff/Shade.png")
        self.scale = 20
        self.alpha = 250


class Select(arcade.Sprite):
    """ little icon showing the active button in train view """
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Backdrop/select.png")


class Buttons(arcade.Sprite):
    """ The three buttons in main screen """
    def __init__(self):
        super().__init__()
        self.type = 0
        t1 = arcade.load_texture("Backdrop/Buttons1.png")
        t2 = arcade.load_texture("Backdrop/Buttons2.png")
        t3 = arcade.load_texture("Backdrop/Buttons3.png")
        self.back_list = [t1, t2, t3]
        self.texture = self.back_list[0]


class MenueScreens(arcade.Sprite):
    """ All backdrops before starting the actual game """
    def __init__(self):
        super().__init__()
        self.type = 0
        t1 = arcade.load_texture("Backdrop/Spec_backgroundblue.png")
        t2 = arcade.load_texture("Backdrop/Forest_back2.png")
        t3 = arcade.load_texture("Backdrop/anime train.png")
        self.back_list = [t1, t2, t3]
        self.scale_list = [0.6, 1.2, 0.95]
        self.texture = self.back_list[0]


class Titlecards(arcade.Sprite):
    """ all the titles for transition screens """
    def __init__(self):
        super().__init__()
        self.alpha = 1
        self.type = 0
        t1 = arcade.load_texture("Backdrop/Texts1.png")
        t2 = arcade.load_texture("Backdrop/Texts2.png")
        t3 = arcade.load_texture("Backdrop/Texts3.png")
        t4 = arcade.load_texture("Backdrop/Texts4.png")
        self.text_list = [t1, t2, t3, t4]
        self.texture = self.text_list[0]


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "GAME", fullscreen=False)
    window.center_window()
    game = Start()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
