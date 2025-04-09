import arcade
from arcade import Sprite, TextureAnimation, TextureKeyframe

from platformer.platformer_base import PlatformerBase


class AnimatedPlayerSprite(Sprite):
    def __init__(self, player_textures_prefix, keyframe_duration = 60):
        super().__init__()

        self.direction = 1
        self.current_tick = 0
        self.idle_texture = arcade.load_texture(player_textures_prefix + "_idle.png")
        self.jumping_texture = arcade.load_texture(player_textures_prefix + "_jump.png")

        keyframes = [TextureKeyframe(arcade.load_texture(player_textures_prefix + "_walk" + str(frame_id) + ".png"), keyframe_duration) for frame_id in range(0, 8)]
        self.animation = TextureAnimation(keyframes)

        self.update_animation()

    def update_animation(self, delta_time = 1 / 60, *args, **kwargs):
        if self.change_y == 0:
            if self.change_x != 0:
                self.current_tick += delta_time

                if (self.change_x * self.direction) < 0:
                    self.direction *= -1
                    self.reverse()

                curr_keyframe = self.animation.get_keyframe(self.current_tick, True)
                self.texture = curr_keyframe[1].texture if self.direction == 1 else curr_keyframe[1].texture.flip_horizontally()
            else:
                self.current_tick = 0
                self.texture = self.idle_texture if self.direction == 1 else self.idle_texture.flip_horizontally()
        else:
            self.texture = self.jumping_texture if self.direction == 1 else self.jumping_texture.flip_horizontally()


class Platformer(PlatformerBase):
    def __init__(self):
        super().__init__()

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        self.level = 0

    def load_level(self):
        if self.level == 0:
            map_name = ":resources:tiled_maps/map2_level_1.json"
            self.load_map(map_name)
        elif self.level == 1:
            map_name = ":resources:tiled_maps/map2_level_2.json"
            self.load_map(map_name)

    def setup_hook(self):
        player_textures_prefix = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        self.set_player(AnimatedPlayerSprite(player_textures_prefix))

        self.load_level()

    def update_hook(self):
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        if not self.scene["Coins"]:
            self.level += 1
            self.load_level()

        self.player_sprite.update_animation()


def main():
    Platformer.startup()


if __name__ == "__main__":
    main()
