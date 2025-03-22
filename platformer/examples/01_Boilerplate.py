from platformer.platformer_base import PlatformerBase


class Platformer(PlatformerBase):
    def setup_hook(self):
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.set_player(image_source)

        map_name = ":resources:tiled_maps/map.json"
        self.load_map(map_name)


def main():
    Platformer.startup()


if __name__ == "__main__":
    main()
