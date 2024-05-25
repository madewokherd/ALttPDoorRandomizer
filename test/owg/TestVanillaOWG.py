from BaseClasses import World
from DoorShuffle import link_doors
from Doors import create_doors
from Dungeons import create_dungeons, get_dungeon_item_pool
from OverworldShuffle import link_overworld
from source.overworld.EntranceShuffle2 import link_entrances_new
from ItemList import difficulties, generate_itempool
from Items import ItemFactory
from OverworldGlitchRules import create_owg_connections
from Regions import create_regions, create_dungeon_regions, create_shops, mark_light_dark_world_regions
from RoomData import create_rooms
from Rules import set_rules
from test.TestBase import TestBase


class TestVanillaOWG(TestBase):
    def setUp(self):
        self.world = World(1, {1:'vanilla'}, {1:'vanilla'}, {1:'vanilla'}, {1:'owglitches'}, {1:'open'}, {1:'random'}, {1:'normal'}, {1:'normal'}, 'none', 'on', {1:'ganon'}, 'balanced', {1:'items'},
                           {1:True}, {1:False}, False, None, {1:False})
        self.world.difficulty_requirements[1] = difficulties['normal']
        self.world.intensity = {1:1}
        create_regions(self.world, 1)
        create_dungeon_regions(self.world, 1)
        create_shops(self.world, 1)
        create_doors(self.world, 1)
        create_rooms(self.world, 1)
        create_dungeons(self.world, 1)
        link_overworld(self.world, 1)
        link_entrances_new(self.world, 1)
        link_doors(self.world, 1)
        create_owg_connections(self.world, 1)
        generate_itempool(self.world, 1)
        self.world.required_medallions[1] = ['Ether', 'Quake']
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.world.get_location('Agahnim 1', 1).item = None
        self.world.get_location('Agahnim 2', 1).item = None
        self.world.precollected_items.clear()
        self.world.itempool.append(ItemFactory('Pegasus Boots', 1))
        mark_light_dark_world_regions(self.world, 1)
        set_rules(self.world, 1)