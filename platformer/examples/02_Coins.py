import arcade
from platformer.platformer_base import PlatformerBase


class Platformer(PlatformerBase):
    def __init__(self):
        super().__init__()

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

    def setup_hook(self):
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.set_player(image_source)

        map_name = ":resources:tiled_maps/map.json"
        self.load_map(map_name)

    def update_hook(self):
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)


def main():
    Platformer.startup()


if __name__ == "__main__":
    main()
