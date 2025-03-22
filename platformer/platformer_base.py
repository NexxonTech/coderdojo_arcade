import arcade
from arcade import Window, Sprite, PhysicsEnginePlatformer, Camera2D, SceneKeyError

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class PlatformerBase(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite = None
        self.player_starting_pos = None
        self.physics_engine = None

    @classmethod
    def startup(cls):
        window = cls()
        window.setup()
        arcade.run()

    def set_player(self, player_sprite_source, center_x = 64, center_y = 128):
        self.player_sprite = Sprite(player_sprite_source, CHARACTER_SCALING)
        self.player_starting_pos = (center_x, center_y)

    def load_player(self, player_sprite_source = None, center_x = 64, center_y = 128):
        if player_sprite_source:
            self.set_player(player_sprite_source, center_x, center_y)

        try:
            self.scene.remove_sprite_list_by_name("Player")
        except KeyError:
            pass

        self.player_sprite.center_x = self.player_starting_pos[0]
        self.player_sprite.center_y = self.player_starting_pos[1]
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene.get_sprite_list("Platforms")
        )

    def load_map(self, map_name):
        if self.player_sprite:
            self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

            if self.tile_map.background_color:
                arcade.set_background_color(self.tile_map.background_color)

            self.load_player()
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.Q:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

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

        self.update_hook()

        self.center_camera_to_player()
