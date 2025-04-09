from typing import Optional

import arcade
from arcade import Window, Sprite, PhysicsEnginePlatformer, Camera2D, SceneKeyError

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1


class PlatformerBase(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene: Optional[arcade.Scene] = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite = None
        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False

    @classmethod
    def startup(cls):
        window = cls()
        window.setup()
        arcade.run()

    def reset_player_pos(self, center_x = None, center_y = None):
        self.player_sprite.center_x = center_x if center_x is not None else 64
        self.player_sprite.center_y = center_y if center_y is not None else 128

    def set_player(self, player_sprite, center_x = None, center_y = None):
        if isinstance(player_sprite, Sprite):
            self.player_sprite = player_sprite
        else:
            self.player_sprite = Sprite(player_sprite, CHARACTER_SCALING)

        self.reset_player_pos(center_x, center_y)

    def load_player(self, player_sprite = None, center_x = None, center_y = None):
        if player_sprite is not None:
            self.set_player(player_sprite, center_x, center_y)

        try:
            self.scene.remove_sprite_list_by_name("Player")
        except KeyError:
            pass

        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene.get_sprite_list("Platforms")
        )

    def load_map(self, map_name, new_player_x = None, new_player_y = None):
        if self.player_sprite is not None:
            self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

            if self.tile_map.background_color:
                arcade.set_background_color(self.tile_map.background_color)

            self.load_player()
            self.reset_player_pos(new_player_x, new_player_y)
        else:
            raise RuntimeError("You should set a Player before trying to load a level!")

    def setup_hook(self):
        pass

    def setup(self):
        self.camera = Camera2D()
        self.gui_camera = Camera2D()

        self.setup_hook()

    def draw_gui_hook(self):
        pass

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        self.draw_gui_hook()

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and self.physics_engine.can_jump():
            self.physics_engine.jump(PLAYER_JUMP_SPEED)
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W, arcade.key.SPACE]:
            self.up_pressed = True
            self.update_player_speed()
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
            self.update_player_speed()
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.Q:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W, arcade.key.SPACE]:
            self.up_pressed = False
            self.update_player_speed()
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
            self.update_player_speed()
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False
            self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x, screen_center_y = self.player_sprite.position
        if screen_center_x < self.camera.viewport_width/2:
            screen_center_x = self.camera.viewport_width/2
        if screen_center_y < self.camera.viewport_height/2:
            screen_center_y = self.camera.viewport_height/2
        user_centered = screen_center_x, screen_center_y

        self.camera.position = arcade.math.lerp_2d(
            self.camera.position, user_centered, 1,
        )

    def update_hook(self):
        pass

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_player()

        self.update_hook()
