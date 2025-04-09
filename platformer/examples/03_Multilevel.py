import arcade
from platformer.platformer_base import PlatformerBase


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
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.set_player(image_source)

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


def main():
    Platformer.startup()


if __name__ == "__main__":
    main()
