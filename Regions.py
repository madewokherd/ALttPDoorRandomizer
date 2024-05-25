import collections
from Items import ItemFactory
from BaseClasses import Region, Location, Entrance, RegionType, Terrain, Shop, ShopType, LocationType, PotItem, PotFlags
from PotShuffle import key_drop_data, vanilla_pots, choose_pots, PotSecretTable

from source.dungeon.EnemyList import setup_enemy_locations, enemy_names


def create_regions(world, player):
    world.regions += [
        create_menu_region(player, 'Menu', None, ['Links House S&Q', 'Sanctuary S&Q', 'Old Man S&Q', 'Other World S&Q']),
        create_menu_region(player, 'Flute Sky', None, ['Flute Spot 1', 'Flute Spot 2', 'Flute Spot 3', 'Flute Spot 4',
                          'Flute Spot 5', 'Flute Spot 6', 'Flute Spot 7', 'Flute Spot 8']),

        create_lw_region(player, 'Master Sword Meadow', ['Master Sword Pedestal'], ['Master Sword Meadow SC']),
        create_lw_region(player, 'Lost Woods West Area', None, ['Lost Woods Bush (West)', 'Lost Woods NW', 'Lost Woods SW', 'Lost Woods SC']),
        create_lw_region(player, 'Lost Woods East Area', ['Mushroom'], ['Lost Woods Gamble', 'Lost Woods Hideout Drop', 'Lost Woods Hideout Stump', 'Lost Woods Bush (East)', 'Lost Woods SE', 'Lost Woods EN']),
        create_lw_region(player, 'Lumberjack Area', None, ['Lumberjack Tree Tree', 'Lumberjack Tree Cave', 'Lumberjack House', 'Lumberjack WN', 'Lumberjack SW']),
        create_lw_region(player, 'West Death Mountain (Top)', ['Ether Tablet'], ['Tower of Hera', 'Spectacle Rock Approach', 'West Death Mountain Drop', 'West Death Mountain EN']),
        create_lw_region(player, 'Spectacle Rock Ledge', ['Spectacle Rock'], ['Spectacle Rock Leave', 'Spectacle Rock Ledge Drop']),
        create_lw_region(player, 'West Death Mountain (Bottom)', ['Old Man Drop Off'], ['Old Man Cave (East)', 'Old Man House (Bottom)', 'Old Man House (Top)',
                          'Death Mountain Return Cave (East)', 'Spectacle Rock Cave', 'Spectacle Rock Cave Peak', 'Spectacle Rock Cave (Bottom)',
                          'Old Man Drop Off', 'West Death Mountain Teleporter', 'West Death Mountain ES']),
        create_lw_region(player, 'Old Man Drop Off', ['Old Man'], None),
        create_lw_region(player, 'East Death Mountain (Top West)', None, ['DM Hammer Bridge (West)', 'East Death Mountain WN']),
        create_lw_region(player, 'East Death Mountain (Top East)', None, ['Paradox Cave (Top)', 'DM Hammer Bridge (East)', 'Floating Island Bridge (East)',
                          'EDM To Spiral Ledge Drop', 'EDM To Fairy Ledge Drop', 'EDM To Mimic Ledge Drop', 'EDM Ledge Drop', 'East Death Mountain EN']),
        create_lw_region(player, 'Death Mountain Floating Island', ['Floating Island'], ['Floating Island Bridge (West)']),
        create_lw_region(player, 'Spiral Cave Ledge', None, ['Spiral Cave', 'Spiral Ledge Drop', 'Spiral Mimic Bridge (West)']),
        create_lw_region(player, 'Mimic Cave Ledge', None, ['Mimic Cave', 'Spiral Mimic Bridge (East)']),
        create_lw_region(player, 'Spiral Mimic Ledge Extend', None, ['Spiral Ledge Approach', 'Mimic Ledge Approach', 'Spiral Mimic Ledge Drop']),
        create_lw_region(player, 'Fairy Ascension Ledge', None, ['Fairy Ascension Cave (Top)', 'Fairy Ascension Ledge Drop']),
        create_lw_region(player, 'Fairy Ascension Plateau', None, ['Fairy Ascension Cave (Bottom)', 'Fairy Ascension Rocks (Inner)', 'Fairy Ascension Plateau Ledge Drop']),
        create_lw_region(player, 'East Death Mountain (Bottom Left)', None, ['DM Broken Bridge (West)', 'East Death Mountain WS']),
        create_lw_region(player, 'East Death Mountain (Bottom)', None, ['Spiral Cave (Bottom)', 'Hookshot Fairy', 'Paradox Cave (Bottom)', 'Paradox Cave (Middle)',
                          'DM Broken Bridge (East)', 'Fairy Ascension Rocks (Outer)', 'East Death Mountain Teleporter']),
        create_lw_region(player, 'Death Mountain TR Pegs Area', None, ['TR Pegs Ledge Entry', 'Death Mountain TR Pegs WN']),
        create_lw_region(player, 'Death Mountain TR Pegs Ledge', None, ['TR Pegs Ledge Leave', 'TR Pegs Ledge Drop', 'TR Pegs Teleporter']),
        create_lw_region(player, 'Mountain Pass Area', None, ['Mountain Pass Rock (Outer)', 'Mountain Pass NW', 'Mountain Pass SE']),
        create_lw_region(player, 'Mountain Pass Ledge', None, ['Death Mountain Return Cave (West)', 'Mountain Pass Ledge Drop'], 'a ledge in the foothills'),
        create_lw_region(player, 'Mountain Pass Entry', None, ['Old Man Cave (West)', 'Mountain Pass Rock (Inner)', 'Mountain Pass Entry Ledge Drop']),
        create_lw_region(player, 'Zora Waterfall Area', None, ['Zora Waterfall Water Entry', 'Zora Waterfall SE', 'Zora Waterfall NE']),
        create_lw_region(player, 'Zora Waterfall Water', None, ['Zora Waterfall Approach', 'Zora Waterfall Landing', 'Zora Whirlpool'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Zora Waterfall Entryway', None, ['Waterfall of Wishing', 'Zora Waterfall Water Drop']),
        create_lw_region(player, 'Zoras Domain', ['King Zora', 'Zora\'s Ledge'], ['Zoras Domain SW']),
        create_lw_region(player, 'Lost Woods Pass West Area', None, ['Lost Woods Pass NW', 'Lost Woods Pass SW']),
        create_lw_region(player, 'Lost Woods Pass East Top Area', None, ['Lost Woods Pass Hammer (North)', 'Lost Woods Pass NE']),
        create_lw_region(player, 'Lost Woods Pass Portal Area', None, ['Lost Woods Pass Hammer (South)', 'Lost Woods Pass Rock (North)', 'Kakariko Teleporter']),
        create_lw_region(player, 'Lost Woods Pass East Bottom Area', None, ['Lost Woods Pass Rock (South)', 'Lost Woods Pass SE']),
        create_lw_region(player, 'Kakariko Fortune Area', None, ['Fortune Teller (Light)', 'Kakariko Fortune NE', 'Kakariko Fortune EN', 'Kakariko Fortune ES', 'Kakariko Fortune SC']),
        create_lw_region(player, 'Kakariko Pond Area', None, ['Kakariko Pond Whirlpool', 'Kakariko Pond NE', 'Kakariko Pond WN', 'Kakariko Pond WS',
                          'Kakariko Pond SW', 'Kakariko Pond SE', 'Kakariko Pond EN', 'Kakariko Pond ES']),
        create_lw_region(player, 'Sanctuary Area', None, ['Sanctuary', 'Sanctuary WS', 'Sanctuary EC']),
        create_lw_region(player, 'Bonk Rock Ledge', None, ['Bonk Rock Cave', 'Bonk Rock Ledge Drop', 'Sanctuary WN']),
        create_lw_region(player, 'Graveyard Area', None, ['Sanctuary Grave', 'Kings Grave Rocks (Outer)', 'Graveyard Ladder (Bottom)', 'Graveyard WC', 'Graveyard EC']),
        create_lw_region(player, 'Graveyard Ledge', None, ['Graveyard Cave', 'Graveyard Ledge Drop', 'Graveyard Ladder (Top)']),
        create_lw_region(player, 'Kings Grave Area', None, ['Kings Grave', 'Kings Grave Rocks (Inner)']),
        create_lw_region(player, 'River Bend Area', None, ['North Fairy Cave Drop', 'North Fairy Cave', 'River Bend Water Drop', 'River Bend WC', 'River Bend SW']),
        create_lw_region(player, 'River Bend East Bank', None, ['River Bend East Water Drop', 'River Bend SE', 'River Bend EC', 'River Bend ES']),
        create_lw_region(player, 'River Bend Water', None, ['River Bend West Pier', 'River Bend East Pier', 'River Bend Whirlpool', 'River Bend EN', 'River Bend SC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Potion Shop Area', None, ['Potion Shop', 'Potion Shop Water Drop', 'Potion Shop Rock (South)', 'Potion Shop WC', 'Potion Shop WS']),
        create_lw_region(player, 'Potion Shop Northeast', None, ['Potion Shop Northeast Water Drop', 'Potion Shop Rock (North)', 'Potion Shop EC']),
        create_lw_region(player, 'Potion Shop Water', None, ['Potion Shop WN', 'Potion Shop EN'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Zora Approach Area', None, ['Zora Approach Rocks (West)', 'Zora Approach Bottom Ledge Drop', 'Zora Approach Water Drop', 'Zora Approach WC']),
        create_lw_region(player, 'Zora Approach Ledge', None, ['Zora Approach Rocks (East)', 'Zora Approach Ledge Drop', 'Zora Approach NE']),
        create_lw_region(player, 'Zora Approach Water', None, ['Zora Approach WN'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Kakariko Village', ['Bottle Merchant'], ['Kakariko Well Drop', 'Kakariko Well Cave', 'Blinds Hideout', 'Elder House (West)', 'Elder House (East)',
                          'Snitch Lady (West)', 'Snitch Lady (East)', 'Chicken House', 'Sick Kids House', 'Kakariko Shop', 'Tavern (Front)', 'Tavern North',
                          'Kakariko Southwest Bush (North)', 'Kakariko Yard Bush (South)', 'Kakariko NW', 'Kakariko NC', 'Kakariko NE', 'Kakariko ES', 'Kakariko SE']),
        create_lw_region(player, 'Kakariko Southwest', None, ['Light World Bomb Hut', 'Kakariko Southwest Bush (South)']),
        create_lw_region(player, 'Kakariko Bush Yard', None, ['Bush Covered House', 'Kakariko Yard Bush (North)']),
        create_lw_region(player, 'Forgotten Forest Area', None, ['Forgotten Forest NW', 'Forgotten Forest NE', 'Forgotten Forest ES']),
        create_lw_region(player, 'Hyrule Castle Area', None, ['Hyrule Castle Secret Entrance Drop', 'Hyrule Castle East Rock (Inner)', 'Hyrule Castle Southwest Bush (North)',
                          'Hyrule Castle Main Gate (South)', 'Castle Gate Teleporter', 'Hyrule Castle WN', 'Hyrule Castle SE']),
        create_lw_region(player, 'Hyrule Castle Southwest', None, ['Hyrule Castle Southwest Bush (South)', 'Hyrule Castle SW']),
        create_lw_region(player, 'Hyrule Castle Courtyard', None, ['Hyrule Castle Entrance (South)', 'Hyrule Castle Courtyard Bush (South)', 'Hyrule Castle Main Gate (North)', 'Castle Gate Teleporter (Inner)']),
        create_lw_region(player, 'Hyrule Castle Courtyard Northeast', None, ['Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Courtyard Bush (North)']),
        create_lw_region(player, 'Hyrule Castle Ledge', None, ['Hyrule Castle Entrance (West)', 'Agahnims Tower', 'Hyrule Castle Entrance (East)', 'Inverted Pyramid Entrance', 'Inverted Pyramid Hole',
                          'Hyrule Castle Ledge Courtyard Drop', 'Hyrule Castle Ledge Drop'], 'the castle rampart'),
        create_lw_region(player, 'Hyrule Castle East Entry', None, ['Hyrule Castle East Rock (Outer)', 'Hyrule Castle ES']),
        create_lw_region(player, 'Hyrule Castle Water', None, [], 'Light World', Terrain.Water),
        create_lw_region(player, 'Wooden Bridge Area', None, ['Wooden Bridge Bush (South)', 'Wooden Bridge Water Drop', 'Wooden Bridge NW', 'Wooden Bridge SW']),
        create_lw_region(player, 'Wooden Bridge Northeast', None, ['Wooden Bridge Bush (North)', 'Wooden Bridge Northeast Water Drop', 'Wooden Bridge NE']),
        create_lw_region(player, 'Wooden Bridge Water', None, ['Wooden Bridge NC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Eastern Palace Area', None, ['Sahasrahlas Hut', 'Eastern Palace', 'Eastern Palace SW', 'Eastern Palace SE']),
        create_lw_region(player, 'Eastern Cliff', None, ['Sand Dunes Cliff Ledge Drop', 'Stone Bridge East Cliff Ledge Drop', 'Tree Line Cliff Ledge Drop', 'Eastern Palace Cliff Ledge Drop']),
        create_lw_region(player, 'Blacksmith Area', None, ['Blacksmiths Hut', 'Bat Cave Cave', 'Blacksmith Ledge Peg (West)', 'Blacksmith WS']),
        create_lw_region(player, 'Blacksmith Ledge', None, ['Bat Cave Drop', 'Blacksmith Ledge Peg (East)']),
        create_lw_region(player, 'Sand Dunes Area', None, ['Sand Dunes NW', 'Sand Dunes WN', 'Sand Dunes SC']),
        create_lw_region(player, 'Maze Race Area', None, ['Maze Race ES']),
        create_lw_region(player, 'Maze Race Ledge', None, ['Two Brothers House (West)', 'Maze Race Game'], 'a race against time'),
        create_lw_region(player, 'Maze Race Prize', ['Maze Race'], ['Maze Race Ledge Drop']), # this is a separate region to make OWG item get possible without allowing the Entrance access
        create_lw_region(player, 'Kakariko Suburb Area', None, ['Library', 'Two Brothers House (East)', 'Kakariko Gamble Game', 'Kakariko Suburb NE', 'Kakariko Suburb WS', 'Kakariko Suburb ES']),
        create_lw_region(player, 'Flute Boy Area', ['Flute Spot'], ['Flute Boy SC']),
        create_lw_region(player, 'Flute Boy Pass', None, ['Flute Boy WS', 'Flute Boy SW']),
        create_lw_region(player, 'Central Bonk Rocks Area', None, ['Bonk Fairy (Light)', 'Central Bonk Rocks NW', 'Central Bonk Rocks SW',
                          'Central Bonk Rocks EN', 'Central Bonk Rocks EC', 'Central Bonk Rocks ES']),
        create_lw_region(player, 'Links House Area', None, ['Links House', 'Links House NE', 'Links House WN', 'Links House WC', 'Links House WS', 'Links House SC', 'Links House ES']),
        create_lw_region(player, 'Stone Bridge North Area', None, ['Stone Bridge (Southbound)', 'Stone Bridge NC', 'Stone Bridge EN']),
        create_lw_region(player, 'Stone Bridge South Area', None, ['Stone Bridge (Northbound)', 'Stone Bridge WS', 'Stone Bridge SC']),
        create_lw_region(player, 'Stone Bridge Water', None, ['Stone Bridge WC', 'Stone Bridge EC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Hobo Bridge', ['Hobo'], ['Hobo EC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Central Cliffs', None, ['Central Bonk Rocks Cliff Ledge Drop', 'Links House Cliff Ledge Drop', 'Stone Bridge Cliff Ledge Drop', 'Lake Hylia Northwest Cliff Ledge Drop', 'Lake Hylia Island FAWT Ledge Drop', 'Stone Bridge EC Cliff Water Drop', 'Tree Line WC Cliff Water Drop', 'C Whirlpool Outer Cliff Ledge Drop', 'C Whirlpool Cliff Ledge Drop', 'C Whirlpool Portal Cliff Ledge Drop', 'Statues Cliff Ledge Drop']),
        create_lw_region(player, 'Tree Line Area', None, ['Lake Hylia Fairy', 'Tree Line WN', 'Tree Line NW', 'Tree Line SE']),
        create_lw_region(player, 'Tree Line Water', None, ['Tree Line WC', 'Tree Line SC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Eastern Nook Area', None, ['Long Fairy Cave', 'East Hyrule Teleporter', 'Eastern Nook NE']),
        create_lw_region(player, 'Desert Area', None, ['Aginahs Cave', 'Desert Statue Move', 'Checkerboard Ledge Approach', 'Desert ES']),
        create_lw_region(player, 'Desert Ledge', ['Desert Ledge'], ['Desert Palace Entrance (West)', 'Desert Ledge Rocks (Outer)', 'Desert Ledge Drop'], 'the desert ledge'),
        create_lw_region(player, 'Desert Ledge Keep', None, ['Desert Palace Entrance (North)', 'Desert Ledge Rocks (Inner)'], 'the desert ledge'),
        create_lw_region(player, 'Desert Checkerboard Ledge', None, ['Checkerboard Cave', 'Checkerboard Ledge Drop', 'Checkerboard Ledge Leave']),
        create_lw_region(player, 'Desert Stairs', None, ['Desert Palace Entrance (South)']),
        create_lw_region(player, 'Desert Mouth', None, ['Desert Palace Entrance (East)', 'Desert Mouth Drop'], 'a sandy vista'),
        create_lw_region(player, 'Desert Teleporter Ledge', None, ['Desert Teleporter Drop', 'Desert Teleporter']),
        create_lw_region(player, 'Desert Northern Cliffs', None, ['Checkerboard Cliff Ledge Drop', 'Suburb Cliff Ledge Drop', 'Cave 45 Cliff Ledge Drop', 'Desert C Whirlpool Cliff Ledge Drop', 'Desert Pass Cliff Ledge Drop', 'Dam Cliff Ledge Drop']),
        create_lw_region(player, 'Bombos Tablet Ledge', ['Bombos Tablet'], ['Bombos Tablet Drop', 'Desert EC']),
        create_lw_region(player, 'Flute Boy Approach Area', None, ['Flute Boy Bush (South)', 'Cave 45 Approach', 'Flute Boy Approach NW', 'Flute Boy Approach EC']),
        create_lw_region(player, 'Flute Boy Bush Entry', None, ['Flute Boy Bush (North)', 'Flute Boy Approach NC']),
        create_lw_region(player, 'Cave 45 Ledge', None, ['Cave 45', 'Cave 45 Ledge Drop', 'Cave 45 Leave']),
        create_lw_region(player, 'C Whirlpool Area', None, ['C Whirlpool Rock (Bottom)', 'C Whirlpool Pegs (Outer)', 'C Whirlpool Water Entry', 'C Whirlpool EN', 'C Whirlpool ES', 'C Whirlpool SC']),
        create_lw_region(player, 'C Whirlpool Portal Area', None, ['C Whirlpool Pegs (Inner)', 'South Hyrule Teleporter']),
        create_lw_region(player, 'C Whirlpool Water', None, ['C Whirlpool Landing', 'C Whirlpool', 'C Whirlpool EC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'C Whirlpool Outer Area', None, ['C Whirlpool Rock (Top)', 'C Whirlpool WC', 'C Whirlpool NW']),
        create_lw_region(player, 'Statues Area', None, ['Light Hype Fairy', 'Statues Water Entry', 'Statues NC', 'Statues WN', 'Statues WS', 'Statues SC']),
        create_lw_region(player, 'Statues Water', None, ['Statues Landing', 'Statues WC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Lake Hylia Northwest Bank', None, ['Lake Hylia Fortune Teller', 'Lake Hylia Shop', 'Lake Hylia Water Drop', 'Lake Hylia NW']),
        create_lw_region(player, 'Lake Hylia Northeast Bank', None, ['Lake Hylia Northeast Water Drop', 'Lake Hylia NE']),
        create_lw_region(player, 'Lake Hylia South Shore', None, ['Mini Moldorm Cave', 'Lake Hylia South Water Drop', 'Lake Hylia WS', 'Lake Hylia ES']),
        create_lw_region(player, 'Lake Hylia Central Island', None, ['Capacity Upgrade', 'Lake Hylia Central Water Drop', 'Lake Hylia Teleporter']),
        create_lw_region(player, 'Lake Hylia Island', ['Lake Hylia Island'], ['Lake Hylia Island Water Drop']),
        create_lw_region(player, 'Lake Hylia Water', None, ['Lake Hylia Central Island Pier', 'Lake Hylia Island Pier', 'Lake Hylia West Pier', 'Lake Hylia East Pier',
                          'Lake Hylia Water D Approach', 'Lake Hylia Whirlpool', 'Lake Hylia NC', 'Lake Hylia EC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Lake Hylia Water D', None, ['Lake Hylia Water D Leave']),
        create_lw_region(player, 'Ice Cave Area', None, ['Ice Rod Cave', 'Good Bee Cave', '20 Rupee Cave', 'Ice Cave Water Drop', 'Ice Cave SE']),
        create_lw_region(player, 'Ice Cave Water', None, ['Ice Cave Pier', 'Ice Cave SW'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Desert Pass Area', ['Middle Aged Man'], ['Desert Fairy', '50 Rupee Cave', 'Middle Aged Man', 'Desert Pass Ladder (South)', 'Desert Pass Rocks (North)', 'Desert Pass WS', 'Desert Pass EC']),
        create_lw_region(player, 'Middle Aged Man', ['Purple Chest'], None),
        create_lw_region(player, 'Desert Pass Southeast', None, ['Desert Pass Rocks (South)', 'Desert Pass ES']),
        create_lw_region(player, 'Desert Pass Ledge', None, ['Desert Pass Ladder (North)', 'Desert Pass Ledge Drop', 'Desert Pass WC']),
        create_lw_region(player, 'Dam Area', ['Sunken Treasure'], ['Dam', 'Dam WC', 'Dam WS', 'Dam NC', 'Dam EC']),
        create_lw_region(player, 'South Pass Area', None, ['South Pass WC', 'South Pass NC', 'South Pass ES']),
        create_lw_region(player, 'Octoballoon Area', None, ['Octoballoon Water Drop', 'Octoballoon WS', 'Octoballoon NE']),
        create_lw_region(player, 'Octoballoon Water', None, ['Octoballoon Pier', 'Octoballoon Whirlpool', 'Octoballoon WC'], 'Light World', Terrain.Water),
        create_lw_region(player, 'Octoballoon Water Ledge', None, ['Octoballoon Waterfall Water Drop', 'Octoballoon NW'], 'Light World', Terrain.Water),

        create_dw_region(player, 'Skull Woods Forest', None, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)',
                          'Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Rock (East)', 'Skull Woods SE']),
        create_dw_region(player, 'Skull Woods Portal Entry', None, ['Skull Woods Rock (West)', 'Skull Woods SC']),
        create_dw_region(player, 'Skull Woods Forest (West)', None, ['Skull Woods Second Section Hole', 'Skull Woods Second Section Door (West)', 'Skull Woods Final Section'], 'a deep, dark forest'),
        create_dw_region(player, 'Skull Woods Forgotten Path (Southwest)', None, ['Skull Woods Forgotten Bush (West)', 'Skull Woods SW']),
        create_dw_region(player, 'Skull Woods Forgotten Path (Northeast)', None, ['Skull Woods Forgotten Bush (East)', 'Skull Woods EN']),
        create_dw_region(player, 'Dark Lumberjack Area', None, ['Dark Lumberjack Shop', 'Dark Lumberjack WN', 'Dark Lumberjack SW']),
        create_dw_region(player, 'West Dark Death Mountain (Top)', None, ['GT Approach', 'West Dark Death Mountain Drop', 'West Dark Death Mountain EN']),
        create_dw_region(player, 'GT Stairs', None, ['Ganons Tower', 'GT Leave']),
        create_dw_region(player, 'West Dark Death Mountain (Bottom)', None, ['Spike Cave', 'Dark Death Mountain Fairy', 'Dark Death Mountain Teleporter (West)', 'West Dark Death Mountain ES']),
        create_dw_region(player, 'East Dark Death Mountain (Top)', None, ['Superbunny Cave (Top)', 'Hookshot Cave', 'East Dark Death Mountain Drop', 'East Dark Death Mountain WN', 'East Dark Death Mountain EN']),
        create_dw_region(player, 'Dark Death Mountain Floating Island', None, ['Hookshot Cave Back Entrance', 'Floating Island Drop'], 'a dark floating island'),
        create_dw_region(player, 'Dark Death Mountain Ledge', None, ['Dark Death Mountain Ledge (West)', 'Dark Death Mountain Ledge (East)'], 'a dark ledge'),
        create_dw_region(player, 'Dark Death Mountain Isolated Ledge', None, ['Turtle Rock Isolated Ledge Entrance'], 'a dark vista'),
        create_dw_region(player, 'East Dark Death Mountain (Bottom)', None, ['Superbunny Cave (Bottom)', 'Dark Death Mountain Shop', 'East Dark Death Mountain Bushes', 'East Dark Death Mountain Teleporter']),
        create_dw_region(player, 'East Dark Death Mountain (Bushes)', None, []),
        create_dw_region(player, 'East Dark Death Mountain (Bottom Left)', None, ['East Dark Death Mountain WS']),
        create_dw_region(player, 'Turtle Rock Area', None, ['Turtle Rock', 'Turtle Rock Tail Ledge Drop', 'Turtle Rock WN']),
        create_dw_region(player, 'Turtle Rock Ledge', ['Turtle Medallion Pad'], ['Turtle Rock Ledge Drop', 'Turtle Rock Teleporter']),
        create_dw_region(player, 'Bumper Cave Area', None, ['Bumper Cave Rock (Outer)', 'Bumper Cave NW', 'Bumper Cave SE']),
        create_dw_region(player, 'Bumper Cave Ledge', ['Bumper Cave Ledge'], ['Bumper Cave (Top)', 'Bumper Cave Ledge Drop'], 'a ledge with an item'),
        create_dw_region(player, 'Bumper Cave Entry', None, ['Bumper Cave (Bottom)', 'Bumper Cave Rock (Inner)', 'Bumper Cave Entry Drop']),
        create_dw_region(player, 'Catfish Area', ['Catfish'], ['Catfish SE']),
        create_dw_region(player, 'Skull Woods Pass West Area', None, ['Skull Woods Pass Bush Row (West)', 'Skull Woods Pass NW', 'Skull Woods Pass SW']),
        create_dw_region(player, 'Skull Woods Pass East Top Area', None, ['Skull Woods Pass Bush Row (East)', 'Skull Woods Pass Bush (North)', 'Skull Woods Pass NE']),
        create_dw_region(player, 'Skull Woods Pass Portal Area', None, ['Skull Woods Pass Bush (South)', 'Skull Woods Pass Rock (North)', 'West Dark World Teleporter']),
        create_dw_region(player, 'Skull Woods Pass East Bottom Area', None, ['Skull Woods Pass Rock (South)', 'Skull Woods Pass SE']),
        create_dw_region(player, 'Dark Fortune Area', None, ['Fortune Teller (Dark)', 'Dark Fortune NE', 'Dark Fortune EN', 'Dark Fortune ES', 'Dark Fortune SC']),
        create_dw_region(player, 'Outcast Pond Area', None, ['Outcast Pond NE', 'Outcast Pond WN', 'Outcast Pond WS', 'Outcast Pond SW', 'Outcast Pond SE', 'Outcast Pond EN', 'Outcast Pond ES']),
        create_dw_region(player, 'Dark Chapel Area', None, ['Dark Sanctuary Hint', 'Dark Chapel WN', 'Dark Chapel WS', 'Dark Chapel EC']),
        create_dw_region(player, 'Dark Graveyard Area', None, ['Dark Graveyard Bush (South)', 'Dark Graveyard WC', 'Dark Graveyard EC']),
        create_dw_region(player, 'Dark Graveyard North', None, ['Dark Graveyard Bush (North)']),
        create_dw_region(player, 'Qirn Jump Area', None, ['Qirn Jump Water Drop', 'Qirn Jump WC', 'Qirn Jump SW']),
        create_dw_region(player, 'Qirn Jump East Bank', None, ['Qirn Jump East Water Drop', 'Qirn Jump SE', 'Qirn Jump EC', 'Qirn Jump ES']),
        create_dw_region(player, 'Qirn Jump Water', None, ['Qirn Jump Pier', 'Qirn Jump Whirlpool', 'Qirn Jump EN', 'Qirn Jump SC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Dark Witch Area', None, ['Dark Potion Shop', 'Dark Witch Water Drop', 'Dark Witch Rock (South)', 'Dark Witch WC', 'Dark Witch WS']),
        create_dw_region(player, 'Dark Witch Northeast', None, ['Dark Witch Northeast Water Drop', 'Dark Witch Rock (North)', 'Dark Witch EC']),
        create_dw_region(player, 'Dark Witch Water', None, ['Dark Witch WN', 'Dark Witch EN'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Catfish Approach Area', None, ['Catfish Approach Rocks (West)', 'Catfish Approach Bottom Ledge Drop', 'Catfish Approach Water Drop', 'Catfish Approach WC']),
        create_dw_region(player, 'Catfish Approach Ledge', None, ['Catfish Approach Rocks (East)', 'Catfish Approach Ledge Drop', 'Catfish Approach NE']),
        create_dw_region(player, 'Catfish Approach Water', None, ['Catfish Approach WN'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Village of Outcasts', None, ['Chest Game', 'Thieves Town', 'C-Shaped House', 'Brewery', 'Bush Yard Pegs (Outer)',
                          'Village of Outcasts NW', 'Village of Outcasts NC', 'Village of Outcasts NE', 'Village of Outcasts ES', 'Village of Outcasts SE']),
        create_dw_region(player, 'Village of Outcasts Bush Yard', None, ['Dark World Shop', 'Bush Yard Pegs (Inner)']),
        create_dw_region(player, 'Shield Shop Area', None, ['Shield Shop Fence Drop (Outer)', 'Shield Shop NW', 'Shield Shop NE']),
        create_dw_region(player, 'Shield Shop Fence', None, ['Red Shield Shop', 'Shield Shop Fence Drop (Inner)']),
        create_dw_region(player, 'Pyramid Area', ['Pyramid Crack', 'Pyramid'], ['Pyramid Hole', 'Pyramid Crack', 'Pyramid ES']),
        create_dw_region(player, 'Pyramid Crack', None, ['Pyramid Fairy']),
        create_dw_region(player, 'Pyramid Exit Ledge', None, ['Pyramid Entrance', 'Pyramid Exit Ledge Drop']),
        create_dw_region(player, 'Pyramid Pass', None, ['Post Aga Teleporter', 'Pyramid SW', 'Pyramid SE']),
        create_dw_region(player, 'Pyramid Water', None, [], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Broken Bridge Area', None, ['Broken Bridge Hammer Rock (South)', 'Broken Bridge Water Drop', 'Broken Bridge SW']),
        create_dw_region(player, 'Broken Bridge Northeast', None, ['Broken Bridge Hammer Rock (North)', 'Broken Bridge Hookshot Gap', 'Broken Bridge Northeast Water Drop', 'Broken Bridge NE']),
        create_dw_region(player, 'Broken Bridge West', None, ['Broken Bridge West Water Drop', 'Broken Bridge NW']),
        create_dw_region(player, 'Broken Bridge Water', None, ['Broken Bridge NC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Palace of Darkness Area', None, ['Palace of Darkness Hint', 'Palace of Darkness', 'Palace of Darkness SW', 'Palace of Darkness SE']),
        create_dw_region(player, 'Darkness Cliff', None, ['Dark Dunes Cliff Ledge Drop', 'Hammer Bridge North Cliff Ledge Drop', 'Dark Tree Line Cliff Ledge Drop', 'Palace of Darkness Cliff Ledge Drop']),
        create_dw_region(player, 'Hammer Pegs Area', ['Dark Blacksmith Ruins'], ['Hammer Peg Cave', 'Peg Area Rocks (East)']),
        create_dw_region(player, 'Hammer Pegs Entry', None, ['Peg Area Rocks (West)', 'Hammer Pegs WS']),
        create_dw_region(player, 'Dark Dunes Area', None, ['Dark Dunes NW', 'Dark Dunes WN', 'Dark Dunes SC']),
        create_dw_region(player, 'Dig Game Area', ['Digging Game'], ['Dig Game To Ledge Drop', 'Dig Game ES']),
        create_dw_region(player, 'Dig Game Ledge', None, ['Dig Game Ledge Drop', 'Dig Game EC']),
        create_dw_region(player, 'Frog Area', None, ['Frog Ledge Drop', 'Frog Rock (Outer)', 'Archery Game Rock (North)', 'Frog NE']),
        create_dw_region(player, 'Frog Prison', ['Frog'], ['Frog Rock (Inner)']),
        create_dw_region(player, 'Archery Game Area', None, ['Archery Game', 'Archery Game Rock (South)', 'Frog WC', 'Frog WS', 'Frog ES']),
        create_dw_region(player, 'Stumpy Area', ['Stumpy'], ['Stumpy SC']),
        create_dw_region(player, 'Stumpy Pass', None, ['Stumpy WS', 'Stumpy SW']),
        create_dw_region(player, 'Dark Bonk Rocks Area', None, ['Bonk Fairy (Dark)', 'Dark Bonk Rocks NW', 'Dark Bonk Rocks SW', 'Dark Bonk Rocks EN', 'Dark Bonk Rocks EC', 'Dark Bonk Rocks ES']),
        create_dw_region(player, 'Big Bomb Shop Area', None, ['Big Bomb Shop', 'Big Bomb Shop NE', 'Big Bomb Shop WN', 'Big Bomb Shop WC', 'Big Bomb Shop WS', 'Big Bomb Shop SC', 'Big Bomb Shop ES']),
        create_dw_region(player, 'Hammer Bridge North Area', None, ['Hammer Bridge Pegs (North)', 'Hammer Bridge Water Drop', 'Hammer Bridge NC', 'Hammer Bridge EN']),
        create_dw_region(player, 'Hammer Bridge South Area', None, ['Hammer Bridge Pegs (South)', 'Hammer Bridge WS', 'Hammer Bridge SC']),
        create_dw_region(player, 'Hammer Bridge Water', None, ['Hammer Bridge Pier', 'Hammer Bridge EC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Dark Central Cliffs', None, ['Dark Bonk Rocks Cliff Ledge Drop', 'Bomb Shop Cliff Ledge Drop', 'Hammer Bridge South Cliff Ledge Drop', 'Ice Lake Northwest Cliff Ledge Drop', 'Ice Palace Island FAWT Ledge Drop',
                          'Hammer Bridge EC Cliff Water Drop', 'Dark Tree Line WC Cliff Water Drop', 'Dark C Whirlpool Outer Cliff Ledge Drop', 'Dark C Whirlpool Cliff Ledge Drop', 'Dark C Whirlpool Portal Cliff Ledge Drop', 'Hype Cliff Ledge Drop']),
        create_dw_region(player, 'Dark Tree Line Area', None, ['Dark Lake Hylia Fairy', 'Dark Tree Line WN', 'Dark Tree Line NW', 'Dark Tree Line SE']),
        create_dw_region(player, 'Dark Tree Line Water', None, ['Dark Tree Line WC', 'Dark Tree Line SC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Darkness Nook Area', None, ['East Dark World Hint', 'East Dark World Teleporter', 'Palace of Darkness Nook NE']),
        create_dw_region(player, 'Mire Area', None, ['Mire Shed', 'Misery Mire', 'Mire Fairy', 'Mire Hint']),
        create_dw_region(player, 'Mire Teleporter Ledge', None, ['Mire Teleporter Ledge Drop', 'Mire Teleporter']),
        create_dw_region(player, 'Mire Northern Cliffs', None, ['Mire Cliff Ledge Drop', 'Dark Checkerboard Cliff Ledge Drop', 'Archery Game Cliff Ledge Drop', 'Stumpy Approach Cliff Ledge Drop', 'Mire C Whirlpool Cliff Ledge Drop', 'Swamp Nook Cliff Ledge Drop', 'Swamp Cliff Ledge Drop', 'Mirror To Bombos Tablet Ledge']),
        create_dw_region(player, 'Stumpy Approach Area', None, ['Stumpy Approach Bush (South)', 'Stumpy Approach NW', 'Stumpy Approach EC']),
        create_dw_region(player, 'Stumpy Approach Bush Entry', None, ['Stumpy Approach Bush (North)', 'Stumpy Approach NC']),
        create_dw_region(player, 'Dark C Whirlpool Area', None, ['Dark C Whirlpool Rock (Bottom)', 'Dark C Whirlpool Pegs (Outer)', 'Dark C Whirlpool Water Entry',
                          'Dark C Whirlpool EN', 'Dark C Whirlpool ES', 'Dark C Whirlpool SC']),
        create_dw_region(player, 'Dark C Whirlpool Portal Area', None, ['Dark C Whirlpool Pegs (Inner)', 'South Dark World Teleporter']),
        create_dw_region(player, 'Dark C Whirlpool Water', None, ['Dark C Whirlpool Landing', 'Dark C Whirlpool EC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Dark C Whirlpool Outer Area', None, ['Dark C Whirlpool Rock (Top)', 'Dark C Whirlpool WC', 'Dark C Whirlpool NW']),
        create_dw_region(player, 'Hype Cave Area', None, ['Hype Cave', 'Hype Cave Water Entry', 'Hype Cave NC', 'Hype Cave WN', 'Hype Cave WS', 'Hype Cave SC']),
        create_dw_region(player, 'Hype Cave Water', None, ['Hype Cave Landing', 'Hype Cave WC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Ice Lake Northwest Bank', None, ['Dark Lake Hylia Shop', 'Ice Lake Water Drop', 'Ice Lake NW']),
        create_dw_region(player, 'Ice Lake Northeast Bank', None, ['Ice Lake Northeast Water Drop', 'Ice Lake Iceberg Bomb Jump', 'Ice Lake NE']),
        create_dw_region(player, 'Ice Lake Southwest Ledge', None, ['Ice Lake Southwest Water Drop', 'Ice Lake WS']),
        create_dw_region(player, 'Ice Lake Southeast Ledge', None, ['Ice Lake Southeast Water Drop', 'Ice Lake ES']),
        create_dw_region(player, 'Ice Lake Water', None, ['Ice Lake Northeast Pier', 'Ice Lake NC', 'Ice Lake EC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Ice Lake Iceberg', None, ['Ice Lake Iceberg Water Entry', 'Ice Lake Northeast Pier Hop', 'Ice Lake Teleporter']),
        create_dw_region(player, 'Ice Palace Area', None, ['Ice Palace']),
        create_dw_region(player, 'Shopping Mall Area', None, ['Dark Lake Hylia Ledge Fairy', 'Dark Lake Hylia Ledge Hint', 'Dark Lake Hylia Ledge Spike Cave', 'Shopping Mall Water Drop', 'Shopping Mall SE']),
        create_dw_region(player, 'Shopping Mall Water', None, ['Shopping Mall Pier', 'Shopping Mall SW'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Swamp Nook Area', None, ['Swamp Nook EC', 'Swamp Nook ES']),
        create_dw_region(player, 'Swamp Area', None, ['Swamp Palace', 'Swamp WC', 'Swamp WS', 'Swamp NC', 'Swamp EC']),
        create_dw_region(player, 'Dark South Pass Area', None, ['Dark South Pass WC', 'Dark South Pass NC', 'Dark South Pass ES']),
        create_dw_region(player, 'Bomber Corner Area', None, ['Bomber Corner Water Drop', 'Bomber Corner WS', 'Bomber Corner NE']),
        create_dw_region(player, 'Bomber Corner Water', None, ['Bomber Corner Pier', 'Bomber Corner Whirlpool', 'Bomber Corner WC'], 'Dark World', Terrain.Water),
        create_dw_region(player, 'Bomber Corner Water Ledge', None, ['Bomber Corner Waterfall Water Drop', 'Bomber Corner NW'], 'Dark World', Terrain.Water),

        create_cave_region(player, 'Lost Woods Gamble', 'a game of chance'),
        create_cave_region(player, 'Lost Woods Hideout (top)', 'a drop\'s exit', ['Lost Woods Hideout'], ['Lost Woods Hideout (top to bottom)']),
        create_cave_region(player, 'Lost Woods Hideout (bottom)', 'a drop\'s exit', None, ['Lost Woods Hideout Exit']),
        create_cave_region(player, 'Lumberjack Tree (top)', 'a drop\'s exit', ['Lumberjack Tree'], ['Lumberjack Tree (top to bottom)']),
        create_cave_region(player, 'Lumberjack Tree (bottom)', 'a drop\'s exit', None, ['Lumberjack Tree Exit']),
        create_cave_region(player, 'Lumberjack House', 'a boring house'),
        create_cave_region(player, 'Old Man Cave (West)', 'a connector', ['Lost Old Man'], ['Old Man Cave E']),
        create_cave_region(player, 'Old Man Cave (East)', 'a connector', None, ['Old Man Cave Exit (East)', 'Old Man Cave W']),
        create_cave_region(player, 'Old Man Cave Ledge', 'a connector', None, ['Old Man Cave Exit (West)', 'Old Man Cave Dropdown']),
        create_cave_region(player, 'Old Man House', 'a connector', None, ['Old Man House Exit (Bottom)', 'Old Man House Front to Back']),
        create_cave_region(player, 'Old Man House Back', 'a connector', None, ['Old Man House Exit (Top)', 'Old Man House Back to Front']),
        create_cave_region(player, 'Death Mountain Return Cave (left)', 'a connector', None, ['Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave E']),
        create_cave_region(player, 'Death Mountain Return Cave (right)', 'a connector', None, ['Death Mountain Return Cave Exit (East)', 'Death Mountain Return Cave W']),
        create_cave_region(player, 'Spectacle Rock Cave (Top)', 'a connector', ['Spectacle Rock Cave'], ['Spectacle Rock Cave Drop', 'Spectacle Rock Cave Exit (Top)']),
        create_cave_region(player, 'Spectacle Rock Cave (Bottom)', 'a connector', None, ['Spectacle Rock Cave Exit', 'Spectacle Rock Cave East Edge']),
        create_cave_region(player, 'Spectacle Rock Cave Pool', 'a connector', None, ['Spectacle Rock Cave West Edge']),
        create_cave_region(player, 'Spectacle Rock Cave (Peak)', 'a connector', None, ['Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave Exit (Peak)']),
        create_cave_region(player, 'Spiral Cave (Top)', 'a connector', ['Spiral Cave'], ['Spiral Cave (top to bottom)', 'Spiral Cave Exit (Top)']),
        create_cave_region(player, 'Spiral Cave (Bottom)', 'a connector', None, ['Spiral Cave Exit']),
        create_cave_region(player, 'Mimic Cave', 'Mimic Cave', ['Mimic Cave']),
        create_cave_region(player, 'Fairy Ascension Cave (Bottom)', 'a connector', None, ['Fairy Ascension Cave Climb', 'Fairy Ascension Cave Exit (Bottom)']),
        create_cave_region(player, 'Fairy Ascension Cave (Drop)', 'a connector', None, ['Fairy Ascension Cave Pots']),
        create_cave_region(player, 'Fairy Ascension Cave (Top)', 'a connector', None, ['Fairy Ascension Cave Exit (Top)', 'Fairy Ascension Cave Drop']),
        create_cave_region(player, 'Hookshot Fairy', 'fairies deep in a cave'),
        create_cave_region(player, 'Paradox Cave Front', 'a connector', None, ['Paradox Cave Push Block Reverse', 'Paradox Cave Exit (Bottom)', 'Paradox Shop']),
        create_cave_region(player, 'Paradox Cave Chest Area', 'a connector', ['Paradox Cave Lower - Far Left', 'Paradox Cave Lower - Left',
                                                  'Paradox Cave Lower - Right', 'Paradox Cave Lower - Far Right', 'Paradox Cave Lower - Middle'],
                                                  ['Paradox Cave Push Block', 'Paradox Cave Bomb Jump', 'Paradox Cave Chest Area NE']),
        create_cave_region(player, 'Paradox Cave Bomb Area', 'a connector', ['Paradox Cave Upper - Left', 'Paradox Cave Upper - Right']),
        create_cave_region(player, 'Paradox Cave', 'a connector', None, ['Paradox Cave Exit (Middle)', 'Paradox Cave Climb', 'Paradox Cave Drop']),
        create_cave_region(player, 'Paradox Cave (Top)', 'a connector', None, ['Paradox Cave Exit (Top)', 'Paradox Cave Descent']),
        create_cave_region(player, 'Paradox Shop', 'a common shop', ['Paradox Shop - Left', 'Paradox Shop - Middle', 'Paradox Shop - Right']),
        create_cave_region(player, 'Waterfall of Wishing', 'a cave with two chests', ['Waterfall Fairy - Left', 'Waterfall Fairy - Right']),
        create_cave_region(player, 'Fortune Teller (Light)', 'a fortune teller'),
        create_cave_region(player, 'Bonk Rock Cave', 'a cave with a chest', ['Bonk Rock Cave']),
        create_dungeon_region(player, 'Sewer Drop', 'a drop\'s exit', None, ['Sewer Drop']), # This exists only to be referenced for access checks
        create_cave_region(player, 'Graveyard Cave', 'a cave with an item', ['Graveyard Cave']),
        create_cave_region(player, 'Kings Grave', 'a cave with a chest', ['King\'s Tomb']),
        create_cave_region(player, 'North Fairy Cave', 'a drop\'s exit', None, ['North Fairy Cave Exit']),
        create_cave_region(player, 'Potion Shop', 'the potion shop', ['Potion Shop', 'Potion Shop - Left', 'Potion Shop - Middle', 'Potion Shop - Right']),
        create_cave_region(player, 'Kakariko Well (top)', 'a drop', ['Kakariko Well - Left', 'Kakariko Well - Middle', 'Kakariko Well - Right', 'Kakariko Well - Bottom'],
                                                  ['Kakariko Well (top to bottom)', 'Kakariko Well (top to back)']),
        create_cave_region(player, 'Kakariko Well (back)', 'a drop', ['Kakariko Well - Top']),
        create_cave_region(player, 'Kakariko Well (bottom)', 'a drop\'s exit', None, ['Kakariko Well Exit']),
        create_cave_region(player, 'Blinds Hideout', 'a bounty of five items', [ "Blind's Hideout - Left", "Blind's Hideout - Right",
                                                  "Blind's Hideout - Far Left", "Blind's Hideout - Far Right"], ['Blinds Hideout N']),
        create_cave_region(player, 'Blinds Hideout (Top)', 'a bounty of five items', ["Blind's Hideout - Top"]),
        create_cave_region(player, 'Elder House', 'a connector', None, ['Elder House Exit (East)', 'Elder House Exit (West)']),
        create_cave_region(player, 'Snitch Lady (East)', 'a boring house'),
        create_cave_region(player, 'Snitch Lady (West)', 'a boring house'),
        create_cave_region(player, 'Chicken House', 'a house with a chest', ['Chicken House']),
        create_cave_region(player, 'Sick Kids House', 'the sick kid', ['Sick Kid']),
        create_cave_region(player, 'Bush Covered House', 'the grass man'),
        create_cave_region(player, 'Light World Bomb Hut', 'a restock room'),
        create_cave_region(player, 'Kakariko Shop', 'a common shop', ['Kakariko Shop - Left', 'Kakariko Shop - Middle', 'Kakariko Shop - Right']),
        create_cave_region(player, 'Tavern', 'the tavern', ['Kakariko Tavern']),
        create_cave_region(player, 'Tavern (Front)', 'the tavern'),
        create_cave_region(player, 'Hyrule Castle Secret Entrance', 'a drop\'s exit', ['Link\'s Uncle', 'Secret Passage'], ['Hyrule Castle Secret Entrance Exit']),
        create_cave_region(player, 'Sahasrahlas Hut', 'Sahasrahla', ['Sahasrahla\'s Hut - Left', 'Sahasrahla\'s Hut - Middle', 'Sahasrahla\'s Hut - Right', 'Sahasrahla']),
        create_cave_region(player, 'Blacksmiths Hut', 'the smith', ['Blacksmith'], ['Missing Smith']),
        create_cave_region(player, 'Missing Smith', None, ['Missing Smith']),
        create_cave_region(player, 'Bat Cave (right)', 'a drop', ['Magic Bat'], ['Bat Cave Door']),
        create_cave_region(player, 'Bat Cave (left)', 'a drop\'s exit', None, ['Bat Cave Exit']),
        create_cave_region(player, 'Two Brothers House', 'a connector', None, ['Two Brothers House Exit (East)', 'Two Brothers House Exit (West)']),
        create_cave_region(player, 'Library', 'the library', ['Library']),
        create_cave_region(player, 'Kakariko Gamble Game', 'a game of chance'),
        create_cave_region(player, 'Bonk Fairy (Light)', 'a fairy fountain', None, ['Bonk Fairy (Light) Pool']),
        create_cave_region(player, 'Bonk Fairy Pool', 'a fairy fountain'),
        create_cave_region(player, 'Links House', 'your house', ['Link\'s House'], ['Links House Exit']),
        create_cave_region(player, 'Chris Houlihan Room', 'I AM ERROR', None, ['Chris Houlihan Room Exit']),
        create_cave_region(player, 'Lake Hylia Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, 'Long Fairy Cave', 'a fairy fountain'),
        create_cave_region(player, 'Checkerboard Cave', 'a cave with an item', ['Checkerboard Cave']),
        create_cave_region(player, 'Aginahs Cave', 'a cave with a chest', ['Aginah\'s Cave']),
        create_cave_region(player, 'Cave 45', 'a cave with an item', ['Cave 45']),
        create_cave_region(player, 'Light Hype Fairy', 'a fairy fountain'),
        create_cave_region(player, 'Lake Hylia Fortune Teller', 'a fortune teller'),
        create_cave_region(player, 'Lake Hylia Shop', 'a common shop', ['Lake Hylia Shop - Left', 'Lake Hylia Shop - Middle', 'Lake Hylia Shop - Right']),
        create_cave_region(player, 'Capacity Upgrade', 'the queen of fairies', ['Capacity Upgrade - Left', 'Capacity Upgrade - Right'], ['Capacity Upgrade East']),
        create_cave_region(player, 'Capacity Fairy Pool', 'near the queen of fairies', None, ['Capacity Fairy Pool West']),
        create_cave_region(player, 'Mini Moldorm Cave', 'a bounty of five items', ['Mini Moldorm Cave - Far Left', 'Mini Moldorm Cave - Left',
                                                  'Mini Moldorm Cave - Right', 'Mini Moldorm Cave - Far Right', 'Mini Moldorm Cave - Generous Guy']),
        create_cave_region(player, 'Ice Rod Cave', 'a cave with a chest', ['Ice Rod Cave']),
        create_cave_region(player, 'Good Bee Cave', 'a cold bee', None, ['Good Bee Cave Front to Back']),
        create_cave_region(player, 'Good Bee Cave (back)', 'a cold bee', None, ['Good Bee Cave Back to Front']),
        create_cave_region(player, '20 Rupee Cave', 'a cave with some cash'),
        create_cave_region(player, 'Desert Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, '50 Rupee Cave', 'a cave with some cash'),
        create_cave_region(player, 'Dam', 'the dam', ['Floodgate', 'Floodgate Chest']),

        create_cave_region(player, 'Dark Lumberjack Shop', 'a common shop', ['Dark Lumberjack Shop - Left', 'Dark Lumberjack Shop - Middle', 'Dark Lumberjack Shop - Right']),
        create_cave_region(player, 'Dark Death Mountain Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, 'Spike Cave', 'Spike Cave', ['Spike Cave']),
        create_cave_region(player, 'Hookshot Cave (Front)', 'a connector', None, ['Hookshot Cave Front Exit', 'Hookshot Cave Front to Middle',
                                                  'Hookshot Cave Bonk Path', 'Hookshot Cave Hook Path']),
        create_cave_region(player, 'Hookshot Cave (Bonk Islands)', 'a connector', ['Hookshot Cave - Bottom Right']),
        create_cave_region(player, 'Hookshot Cave (Hook Islands)', 'a connector', ['Hookshot Cave - Top Right', 'Hookshot Cave - Top Left', 'Hookshot Cave - Bottom Left']),
        create_cave_region(player, 'Hookshot Cave (Middle)', 'a connector', None, ['Hookshot Cave Middle to Back', 'Hookshot Cave Middle to Front']),
        create_cave_region(player, 'Hookshot Cave (Back)', 'a connector', None, ['Hookshot Cave Back to Middle', 'Hookshot Cave Back to Fairy', 'Hookshot Cave Back Exit']),
        create_cave_region(player, 'Hookshot Cave (Fairy Pool)', 'a connector', None, ['Hookshot Cave Fairy to Back']),
        create_cave_region(player, 'Superbunny Cave (Top)', 'a connector', ['Superbunny Cave - Top', 'Superbunny Cave - Bottom'], ['Superbunny Cave Exit (Top)']),
        create_cave_region(player, 'Superbunny Cave (Bottom)', 'a connector', None, ['Superbunny Cave Climb', 'Superbunny Cave Exit (Bottom)']),
        create_cave_region(player, 'Dark Death Mountain Shop', 'a common shop', ['Dark Death Mountain Shop - Left', 'Dark Death Mountain Shop - Middle', 'Dark Death Mountain Shop - Right']),
        create_cave_region(player, 'Bumper Cave (bottom)', 'a connector', None, ['Bumper Cave Exit (Bottom)', 'Bumper Cave Bottom to Top']),
        create_cave_region(player, 'Bumper Cave (top)', 'a connector', None, ['Bumper Cave Exit (Top)', 'Bumper Cave Top To Bottom']),
        create_cave_region(player, 'Fortune Teller (Dark)', 'a fortune teller'),
        create_cave_region(player, 'Dark Sanctuary Hint', 'a storyteller', None, ['Dark Sanctuary Hint Exit']),
        create_cave_region(player, 'Dark Potion Shop', 'a common shop', ['Dark Potion Shop - Left', 'Dark Potion Shop - Middle', 'Dark Potion Shop - Right']),
        create_cave_region(player, 'Chest Game', 'a game of 16 chests', ['Chest Game']),
        create_cave_region(player, 'C-Shaped House', 'a house with a chest', ['C-Shaped House']),
        create_cave_region(player, 'Brewery', 'a house with a chest', ['Brewery']),
        create_cave_region(player, 'Village of Outcasts Shop', 'a common shop', ['Village of Outcasts Shop - Left', 'Village of Outcasts Shop - Middle', 'Village of Outcasts Shop - Right']),
        create_cave_region(player, 'Red Shield Shop', 'the rare shop', ['Red Shield Shop - Left', 'Red Shield Shop - Middle', 'Red Shield Shop - Right']),
        create_cave_region(player, 'Pyramid Fairy', 'a cave with two chests', ['Pyramid Fairy - Left', 'Pyramid Fairy - Right']),
        create_cave_region(player, 'Pyramid', 'a drop\'s exit', ['Ganon'], ['Ganon Drop']),
        create_cave_region(player, 'Bottom of Pyramid', 'a drop\'s exit', None, ['Pyramid Exit']),
        create_cave_region(player, 'Palace of Darkness Hint', 'a storyteller'),
        create_cave_region(player, 'Hammer Peg Cave', 'a cave with an item', ['Peg Cave']),
        create_cave_region(player, 'Archery Game', 'a game of skill'),
        create_cave_region(player, 'Bonk Fairy (Dark)', 'a fairy fountain', None, ['Bonk Fairy (Dark) Pool']),
        create_cave_region(player, 'Big Bomb Shop', 'the bomb shop', ['Big Bomb'], ['Big Bomb Shop Exit']),
        create_cave_region(player, 'Dark Lake Hylia Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, 'East Dark World Hint', 'a storyteller'),
        create_cave_region(player, 'Mire Shed', 'a cave with two chests', ['Mire Shed - Left', 'Mire Shed - Right']),
        create_cave_region(player, 'Mire Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, 'Mire Hint', 'a storyteller'),
        create_cave_region(player, 'Hype Cave', 'a bounty of five items', ['Hype Cave - Top', 'Hype Cave - Middle Right', 'Hype Cave - Middle Left',
                                                  'Hype Cave - Bottom', 'Hype Cave - Generous Guy']),
        create_cave_region(player, 'Dark Lake Hylia Shop', 'a common shop', ['Dark Lake Hylia Shop - Left', 'Dark Lake Hylia Shop - Middle', 'Dark Lake Hylia Shop - Right']),
        create_cave_region(player, 'Dark Lake Hylia Ledge Healer Fairy', 'a fairy fountain'),
        create_cave_region(player, 'Dark Lake Hylia Ledge Hint', 'a storyteller'),
        create_cave_region(player, 'Dark Lake Hylia Ledge Spike Cave', 'a spiky hint')
    ]


def create_dungeon_regions(world, player):
    std_flag = world.mode[player] == 'standard'
    world.regions += [
        create_dungeon_region(player, 'Sanctuary Portal', 'Hyrule Castle', None, ['Sanctuary Exit', 'Enter HC (Sanc)']),
        create_dungeon_region(player, 'Hyrule Castle West Portal', 'Hyrule Castle', None, ['Hyrule Castle Exit (West)', 'Enter HC (West)']),
        create_dungeon_region(player, 'Hyrule Castle South Portal', 'Hyrule Castle', None, ['Hyrule Castle Exit (South)', 'Enter HC (South)']),
        create_dungeon_region(player, 'Hyrule Castle East Portal', 'Hyrule Castle', None, ['Hyrule Castle Exit (East)', 'Enter HC (East)']),
        create_dungeon_region(player, 'Eastern Portal', 'Eastern Palace', None, ['Eastern Palace Exit', 'Enter Eastern Palace']),
        create_dungeon_region(player, 'Desert West Portal', 'Desert Palace', None, ['Desert Palace Exit (West)', 'Enter Desert (West)']),
        create_dungeon_region(player, 'Desert South Portal', 'Desert Palace', None, ['Desert Palace Exit (South)', 'Enter Desert (South)']),
        create_dungeon_region(player, 'Desert East Portal', 'Desert Palace', None, ['Desert Palace Exit (East)', 'Enter Desert (East)']),
        create_dungeon_region(player, 'Desert Back Portal', 'Desert Palace', None, ['Desert Palace Exit (North)', 'Enter Desert (North)']),
        create_dungeon_region(player, 'Hera Portal', 'Tower of Hera', None, ['Tower of Hera Exit', 'Enter Hera']),
        create_dungeon_region(player, 'Agahnims Tower Portal', 'Castle Tower', None, ['Agahnims Tower Exit', 'Enter Agahnims Tower']),
        create_dungeon_region(player, 'Palace of Darkness Portal', 'Palace of Darkness', None, ['Palace of Darkness Exit', 'Enter Palace of Darkness']),
        create_dungeon_region(player, 'Swamp Portal', 'Swamp Palace', None, ['Swamp Palace Exit', 'Enter Swamp']),
        create_dungeon_region(player, 'Skull 1 Portal', 'Skull Woods', None, ['Skull Woods First Section Exit', 'Enter Skull Woods 1']),
        create_dungeon_region(player, 'Skull 2 East Portal', 'Skull Woods', None, ['Skull Woods Second Section Exit (East)', 'Enter Skull Woods 2 (East)']),
        create_dungeon_region(player, 'Skull 2 West Portal', 'Skull Woods', None, ['Skull Woods Second Section Exit (West)', 'Enter Skull Woods 2 (West)']),
        create_dungeon_region(player, 'Skull 3 Portal', 'Skull Woods', None, ['Skull Woods Final Section Exit', 'Enter Skull Woods 3']),
        create_dungeon_region(player, 'Thieves Town Portal', "Thieves' Town", None, ['Thieves Town Exit', 'Enter Thieves Town']),
        create_dungeon_region(player, 'Ice Portal', 'Ice Palace', None, ['Ice Palace Exit', 'Enter Ice Palace']),
        create_dungeon_region(player, 'Mire Portal', 'Misery Mire', None, ['Misery Mire Exit', 'Enter Misery Mire']),
        create_dungeon_region(player, 'Turtle Rock Main Portal', 'Turtle Rock', None, ['Turtle Rock Exit (Front)', 'Enter Turtle Rock (Main)']),
        create_dungeon_region(player, 'Turtle Rock Lazy Eyes Portal', 'Turtle Rock', None, ['Turtle Rock Ledge Exit (West)', 'Enter Turtle Rock (Lazy Eyes)']),
        create_dungeon_region(player, 'Turtle Rock Chest Portal', 'Turtle Rock', None, ['Turtle Rock Ledge Exit (East)', 'Enter Turtle Rock (Chest)']),
        create_dungeon_region(player, 'Turtle Rock Eye Bridge Portal', 'Turtle Rock', None, ['Turtle Rock Isolated Ledge Exit', 'Enter Turtle Rock (Laser Bridge)']),
        create_dungeon_region(player, 'Ganons Tower Portal', "Ganon's Tower", None, ['Ganons Tower Exit', 'Enter Ganons Tower']),

        create_dungeon_region(player, 'Hyrule Castle Lobby', 'Hyrule Castle', None,
                              ['Hyrule Castle Lobby W', 'Hyrule Castle Lobby E', 'Hyrule Castle Lobby WN', 'Hyrule Castle Lobby North Stairs', 'Hyrule Castle Lobby S']),
        create_dungeon_region(player, 'Hyrule Castle West Lobby', 'Hyrule Castle', None,
                              ['Hyrule Castle West Lobby E', 'Hyrule Castle West Lobby N', 'Hyrule Castle West Lobby EN', 'Hyrule Castle West Lobby S']),
        create_dungeon_region(player, 'Hyrule Castle East Lobby', 'Hyrule Castle', None,
                              ['Hyrule Castle East Lobby W', 'Hyrule Castle East Lobby N', 'Hyrule Castle East Lobby NW', 'Hyrule Castle East Lobby S']),
        create_dungeon_region(player, 'Hyrule Castle East Hall', 'Hyrule Castle', None,
                              ['Hyrule Castle East Hall W', 'Hyrule Castle East Hall S', 'Hyrule Castle East Hall SW']),
        create_dungeon_region(player, 'Hyrule Castle West Hall', 'Hyrule Castle', None, ['Hyrule Castle West Hall E', 'Hyrule Castle West Hall S']),
        create_dungeon_region(player, 'Hyrule Castle Back Hall', 'Hyrule Castle', None, ['Hyrule Castle Back Hall E', 'Hyrule Castle Back Hall W', 'Hyrule Castle Back Hall Down Stairs']),
        create_dungeon_region(player, 'Hyrule Castle Throne Room', 'Hyrule Castle', None, ['Hyrule Castle Throne Room Tapestry', 'Hyrule Castle Throne Room South Stairs']),
        create_dungeon_region(player, 'Hyrule Castle Behind Tapestry', 'Hyrule Castle', None, ['Hyrule Castle Throne Room N', 'Hyrule Castle Tapestry Backwards']),

        create_dungeon_region(player, 'Hyrule Dungeon Map Room', 'Hyrule Castle', ['Hyrule Castle - Map Chest', 'Hyrule Castle - Map Guard Key Drop'], ['Hyrule Dungeon Map Room Key Door S', 'Hyrule Dungeon Map Room Up Stairs']),
        create_dungeon_region(player, 'Hyrule Dungeon North Abyss', 'Hyrule Castle', None, ['Hyrule Dungeon North Abyss South Edge', 'Hyrule Dungeon North Abyss Key Door N']),
        create_dungeon_region(player, 'Hyrule Dungeon North Abyss Catwalk', 'Hyrule Castle', None, ['Hyrule Dungeon North Abyss Catwalk Edge', 'Hyrule Dungeon North Abyss Catwalk Dropdown']),
        create_dungeon_region(player, 'Hyrule Dungeon South Abyss', 'Hyrule Castle', None, ['Hyrule Dungeon South Abyss North Edge', 'Hyrule Dungeon South Abyss West Edge']),
        create_dungeon_region(player, 'Hyrule Dungeon South Abyss Catwalk', 'Hyrule Castle', None, ['Hyrule Dungeon South Abyss Catwalk North Edge', 'Hyrule Dungeon South Abyss Catwalk West Edge']),
        create_dungeon_region(player, 'Hyrule Dungeon Guardroom', 'Hyrule Castle', None, ['Hyrule Dungeon Guardroom Catwalk Edge', 'Hyrule Dungeon Guardroom Abyss Edge', 'Hyrule Dungeon Guardroom N']),
        create_dungeon_region(player, 'Hyrule Dungeon Armory Main', 'Hyrule Castle', None, ['Hyrule Dungeon Armory S', 'Hyrule Dungeon Armory Interior Key Door N', 'Hyrule Dungeon Armory ES']),
        create_dungeon_region(player, 'Hyrule Dungeon Armory Boomerang', 'Hyrule Castle', ['Hyrule Castle - Boomerang Chest', 'Hyrule Castle - Boomerang Guard Key Drop'], ['Hyrule Dungeon Armory Boomerang WS']),
        create_dungeon_region(player, 'Hyrule Dungeon Armory North Branch', 'Hyrule Castle', None, ['Hyrule Dungeon Armory Interior Key Door S', 'Hyrule Dungeon Armory Down Stairs']),
        create_dungeon_region(player, 'Hyrule Dungeon Staircase', 'Hyrule Castle', None, ['Hyrule Dungeon Staircase Up Stairs', 'Hyrule Dungeon Staircase Down Stairs']),
        create_dungeon_region(player, 'Hyrule Dungeon Cellblock', 'Hyrule Castle', ['Hyrule Castle - Big Key Drop'], ['Hyrule Dungeon Cellblock Up Stairs', 'Hyrule Dungeon Cellblock Door']),
        create_dungeon_region(player, 'Hyrule Dungeon Cell', 'Hyrule Castle',
                              ["Hyrule Castle - Zelda's Chest"] if not std_flag else
                              ["Hyrule Castle - Zelda's Chest", 'Zelda Pickup'],
                              ['Hyrule Dungeon Cell Exit']),


        create_dungeon_region(player, 'Sewers Behind Tapestry', 'Hyrule Castle', None, ['Sewers Behind Tapestry S', 'Sewers Behind Tapestry Down Stairs']),
        create_dungeon_region(player, 'Sewers Rope Room', 'Hyrule Castle', None, ['Sewers Rope Room Up Stairs', 'Sewers Rope Room North Stairs']),
        create_dungeon_region(player, 'Sewers Dark Cross', 'Hyrule Castle', ['Sewers - Dark Cross'], ['Sewers Dark Cross Key Door N', 'Sewers Dark Cross South Stairs']),
        create_dungeon_region(player, 'Sewers Water', 'Hyrule Castle', None, ['Sewers Water S', 'Sewers Water W']),
        create_dungeon_region(player, 'Sewers Dark Aquabats', 'Hyrule Castle', None,
                              ['Sewers Dark Aquabats ES', 'Sewers Dark Aquabats N']),
        create_dungeon_region(player, 'Sewers Key Rat', 'Hyrule Castle', ['Hyrule Castle - Key Rat Key Drop'],
                              ['Sewers Key Rat S', 'Sewers Key Rat NE']),
        create_dungeon_region(player, 'Sewers Secret Room Blocked Path', 'Hyrule Castle', None, ['Sewers Secret Room Up Stairs']),
        create_dungeon_region(player, 'Sewers Rat Path', 'Hyrule Castle', None, ['Sewers Secret Room Key Door S', 'Sewers Secret Room Push Block', 'Sewers Rat Path WS', 'Sewers Rat Path WN']),
        create_dungeon_region(player, 'Sewers Secret Room', 'Hyrule Castle', ['Sewers - Secret Room - Left', 'Sewers - Secret Room - Middle', 'Sewers - Secret Room - Right'],
                              ['Sewers Secret Room ES', 'Sewers Secret Room EN']),
        create_dungeon_region(player, 'Sewers Yet More Rats', 'Hyrule Castle', None, ['Sewers Pull Switch Down Stairs', 'Sewers Yet More Rats S']),
        create_dungeon_region(player, 'Sewers Pull Switch', 'Hyrule Castle', None, ['Sewers Pull Switch N', 'Sewers Pull Switch S']),
        create_dungeon_region(player, 'Sanctuary', 'Hyrule Castle',
                              ['Sanctuary'] if not std_flag else ['Sanctuary', 'Zelda Drop Off'],
                              ['Sanctuary S', 'Sanctuary N', 'Sanctuary Mirror Route']),

        # Eastern Palace
        create_dungeon_region(player, 'Eastern Lobby', 'Eastern Palace', None, ['Eastern Lobby N', 'Eastern Lobby S', 'Eastern Lobby NW', 'Eastern Lobby NE']),
        create_dungeon_region(player, 'Eastern Lobby Bridge', 'Eastern Palace', None, ['Eastern Lobby Bridge S', 'Eastern Lobby Bridge N']),
        create_dungeon_region(player, 'Eastern Lobby Left Ledge', 'Eastern Palace', None, ['Eastern Lobby Left Ledge SW']),
        create_dungeon_region(player, 'Eastern Lobby Right Ledge', 'Eastern Palace', None, ['Eastern Lobby Right Ledge SE']),
        create_dungeon_region(player, 'Eastern Cannonball', 'Eastern Palace', ['Eastern Palace - Cannonball Chest'], ['Eastern Cannonball S', 'Eastern Cannonball N']),
        create_dungeon_region(player, 'Eastern Cannonball Ledge', 'Eastern Palace', None, ['Eastern Cannonball Ledge WN', 'Eastern Cannonball Ledge Key Door EN']),
        create_dungeon_region(player, 'Eastern Courtyard Ledge', 'Eastern Palace', None, ['Eastern Courtyard Ledge S', 'Eastern Courtyard Ledge W', 'Eastern Courtyard Ledge E']),
        create_dungeon_region(player, 'Eastern East Wing', 'Eastern Palace', None, ['Eastern East Wing W', 'Eastern East Wing EN', 'Eastern East Wing ES']),
        create_dungeon_region(player, 'Eastern Pot Switch', 'Eastern Palace', None, ['Eastern Pot Switch WN', 'Eastern Pot Switch SE']),
        create_dungeon_region(player, 'Eastern Map Balcony', 'Eastern Palace', None, ['Eastern Map Balcony WS', 'Eastern Map Balcony Hook Path']),
        create_dungeon_region(player, 'Eastern Map Room', 'Eastern Palace', ['Eastern Palace - Map Chest'], ['Eastern Map Room NE', 'Eastern Map Room Drop Down']),
        create_dungeon_region(player, 'Eastern West Wing', 'Eastern Palace', None, ['Eastern West Wing E', 'Eastern West Wing WS']),
        create_dungeon_region(player, 'Eastern Stalfos Spawn', 'Eastern Palace', None, ['Eastern Stalfos Spawn ES', 'Eastern Stalfos Spawn NW']),
        create_dungeon_region(player, 'Eastern Compass Room', 'Eastern Palace', ['Eastern Palace - Compass Chest'], ['Eastern Compass Room EN', 'Eastern Compass Room SW']),
        create_dungeon_region(player, 'Eastern Hint Tile', 'Eastern Palace', None, ['Eastern Hint Tile EN', 'Eastern Hint Tile WN']),
        create_dungeon_region(player, 'Eastern Hint Tile Blocked Path', 'Eastern Palace', None, ['Eastern Hint Tile Blocked Path SE', 'Eastern Hint Tile Push Block']),
        create_dungeon_region(player, 'Eastern Courtyard', 'Eastern Palace', ['Eastern Palace - Big Chest'], ['Eastern Courtyard WN', 'Eastern Courtyard EN', 'Eastern Courtyard N', 'Eastern Courtyard Potholes']),
        create_dungeon_region(player, 'Eastern Fairies', 'Eastern Palace', None, ['Eastern Fairies\' Warp']),
        create_dungeon_region(player, 'Eastern Map Valley', 'Eastern Palace', None, ['Eastern Map Valley WN', 'Eastern Map Valley SW']),
        create_dungeon_region(player, 'Eastern Dark Square', 'Eastern Palace', None, ['Eastern Dark Square NW', 'Eastern Dark Square Key Door WN', 'Eastern Dark Square EN']),
        create_dungeon_region(player, 'Eastern Dark Pots', 'Eastern Palace', ['Eastern Palace - Dark Square Pot Key'], ['Eastern Dark Pots WN']),
        create_dungeon_region(player, 'Eastern Big Key', 'Eastern Palace', ['Eastern Palace - Big Key Chest'], ['Eastern Big Key EN', 'Eastern Big Key NE']),
        create_dungeon_region(player, 'Eastern Darkness', 'Eastern Palace', ['Eastern Palace - Dark Eyegore Key Drop'], ['Eastern Darkness S', 'Eastern Darkness Up Stairs', 'Eastern Darkness NE']),
        create_dungeon_region(player, 'Eastern Rupees', 'Eastern Palace', None, ['Eastern Rupees SE']),
        create_dungeon_region(player, 'Eastern Attic Start', 'Eastern Palace', None, ['Eastern Attic Start Down Stairs', 'Eastern Attic Start WS']),
        create_dungeon_region(player, 'Eastern False Switches', 'Eastern Palace', None, ['Eastern False Switches ES', 'Eastern False Switches WS']),
        create_dungeon_region(player, 'Eastern Cannonball Hell', 'Eastern Palace', None, ['Eastern Cannonball Hell ES', 'Eastern Cannonball Hell WS']),
        create_dungeon_region(player, 'Eastern Single Eyegore', 'Eastern Palace', None, ['Eastern Single Eyegore ES', 'Eastern Single Eyegore NE']),
        create_dungeon_region(player, 'Eastern Duo Eyegores', 'Eastern Palace', None, ['Eastern Duo Eyegores SE', 'Eastern Duo Eyegores NE']),
        create_dungeon_region(player, 'Eastern Boss', 'Eastern Palace', None, ['Eastern Boss SE', 'Eastern Palace Boss']),
        create_dungeon_region(player, 'Eastern Boss Spoils', 'Eastern Palace', ['Eastern Palace - Boss', 'Eastern Palace - Prize', 'Eastern Palace - Boss Kill']),

        # Desert Palace
        create_dungeon_region(player, 'Desert Main Lobby', 'Desert Palace', None, ['Desert Main Lobby S', 'Desert Main Lobby N Edge', 'Desert Main Lobby Left Path', 'Desert Main Lobby Right Path']),
        create_dungeon_region(player, 'Desert Left Alcove', 'Desert Palace', None, ['Desert Main Lobby NW Edge', 'Desert Left Alcove Path']),
        create_dungeon_region(player, 'Desert Right Alcove', 'Desert Palace', None, ['Desert Main Lobby NE Edge', 'Desert Main Lobby E Edge', 'Desert Right Alcove Path']),
        create_dungeon_region(player, 'Desert Dead End', 'Desert Palace', None, ['Desert Dead End Edge']),
        create_dungeon_region(player, 'Desert East Lobby', 'Desert Palace', None, ['Desert East Lobby WS', 'Desert East Lobby S']),
        create_dungeon_region(player, 'Desert East Wing', 'Desert Palace', None, ['Desert East Wing ES', 'Desert East Wing Key Door EN', 'Desert East Wing W Edge', 'Desert East Wing N Edge']),
        create_dungeon_region(player, 'Desert Compass Room', 'Desert Palace', ['Desert Palace - Compass Chest'], ['Desert Compass Key Door WN', 'Desert Compass NE']),
        create_dungeon_region(player, 'Desert Cannonball', 'Desert Palace', ['Desert Palace - Big Key Chest'], ['Desert Cannonball S']),
        create_dungeon_region(player, 'Desert Arrow Pot Corner', 'Desert Palace', None, ['Desert Arrow Pot Corner S Edge', 'Desert Arrow Pot Corner W Edge', 'Desert Arrow Pot Corner NW']),
        create_dungeon_region(player, 'Desert Trap Room', 'Desert Palace', None, ['Desert Trap Room SW']),
        create_dungeon_region(player, 'Desert North Hall', 'Desert Palace', None, ['Desert North Hall SE Edge', 'Desert North Hall SW Edge', 'Desert North Hall W Edge', 'Desert North Hall E Edge', 'Desert North Hall NW', 'Desert North Hall NE']),
        create_dungeon_region(player, 'Desert Map Room', 'Desert Palace', ['Desert Palace - Map Chest'], ['Desert Map SW', 'Desert Map SE']),
        create_dungeon_region(player, 'Desert Sandworm Corner', 'Desert Palace', None, ['Desert Sandworm Corner S Edge', 'Desert Sandworm Corner E Edge', 'Desert Sandworm Corner NE', 'Desert Sandworm Corner WS']),
        create_dungeon_region(player, 'Desert Bonk Torch', 'Desert Palace', ['Desert Palace - Torch'], ['Desert Bonk Torch SE']),
        create_dungeon_region(player, 'Desert Circle of Pots', 'Desert Palace', None, ['Desert Circle of Pots ES', 'Desert Circle of Pots NW']),
        create_dungeon_region(player, 'Desert Big Chest Room', 'Desert Palace', ['Desert Palace - Big Chest'], ['Desert Big Chest SW']),
        create_dungeon_region(player, 'Desert West Wing', 'Desert Palace', None, ['Desert West Wing N Edge', 'Desert West Wing WS']),
        create_dungeon_region(player, 'Desert West Lobby', 'Desert Palace', None, ['Desert West Lobby ES', 'Desert West S', 'Desert West Lobby NW']),
        create_dungeon_region(player, 'Desert Fairy Fountain', 'Desert Palace', None, ['Desert Fairy Fountain SW']),
        create_dungeon_region(player, 'Desert Back Lobby', 'Desert Palace', None, ['Desert Back Lobby S', 'Desert Back Lobby NW']),
        create_dungeon_region(player, 'Desert Tiles 1', 'Desert Palace', ['Desert Palace - Desert Tiles 1 Pot Key'], ['Desert Tiles 1 SW', 'Desert Tiles 1 Up Stairs']),
        create_dungeon_region(player, 'Desert Bridge', 'Desert Palace', None, ['Desert Bridge Down Stairs', 'Desert Bridge SW']),
        create_dungeon_region(player, 'Desert Four Statues', 'Desert Palace', None, ['Desert Four Statues NW', 'Desert Four Statues ES']),
        create_dungeon_region(player, 'Desert Beamos Hall', 'Desert Palace', ['Desert Palace - Beamos Hall Pot Key'], ['Desert Beamos Hall WS', 'Desert Beamos Hall NE']),
        create_dungeon_region(player, 'Desert Tiles 2', 'Desert Palace', ['Desert Palace - Desert Tiles 2 Pot Key'], ['Desert Tiles 2 SE', 'Desert Tiles 2 NE']),
        create_dungeon_region(player, 'Desert Wall Slide', 'Desert Palace', None, ['Desert Wall Slide SE', 'Desert Wall Slide NW']),
        create_dungeon_region(player, 'Desert Boss', 'Desert Palace', None, ['Desert Boss SW', 'Desert Palace Boss']),
        create_dungeon_region(player, 'Desert Boss Spoils', 'Desert Palace', ['Desert Palace - Boss', 'Desert Palace - Prize', 'Desert Palace - Boss Kill']),

        # Hera
        create_dungeon_region(player, 'Hera Lobby', 'Tower of Hera', None, ['Hera Lobby S', 'Hera Lobby to Crystal', 'Hera Lobby to Front Barrier - Blue']),
        create_dungeon_region(player, 'Hera Lobby - Crystal', 'Tower of Hera', None, ['Hera Lobby Crystal Exit']),
        create_dungeon_region(player, 'Hera Front', 'Tower of Hera', None, ['Hera Front to Crystal', 'Hera Front to Lobby Barrier - Blue', 'Hera Front to Down Stairs Barrier - Blue', 'Hera Front to Up Stairs Barrier - Orange', 'Hera Front to Back Barrier - Orange', 'Hera Front to Back Bypass']),
        create_dungeon_region(player, 'Hera Front - Crystal', 'Tower of Hera', None, ['Hera Front Crystal Exit']),
        create_dungeon_region(player, 'Hera Down Stairs Landing', 'Tower of Hera', None, ['Hera Lobby Down Stairs', 'Hera Down Stairs to Front Barrier - Blue', 'Hera Down Stairs Landing to Ranged Crystal']),
        create_dungeon_region(player, 'Hera Down Stairs Landing - Ranged Crystal', 'Tower of Hera', None, ['Hera Down Stairs Landing Ranged Crystal Exit']),
        create_dungeon_region(player, 'Hera Up Stairs Landing', 'Tower of Hera', None, ['Hera Up Stairs to Front Barrier - Orange', 'Hera Lobby Up Stairs', 'Hera Up Stairs Landing to Ranged Crystal']),
        create_dungeon_region(player, 'Hera Up Stairs Landing - Ranged Crystal', 'Tower of Hera', None, ['Hera Up Stairs Landing Ranged Crystal Exit']),
        create_dungeon_region(player, 'Hera Back', 'Tower of Hera', ['Tower of Hera - Map Chest'], ['Hera Back to Front Barrier - Orange', 'Hera Lobby Key Stairs', 'Hera Back to Ranged Crystal']),
        create_dungeon_region(player, 'Hera Back - Ranged Crystal', 'Tower of Hera', None, ['Hera Back Ranged Crystal Exit']),
        create_dungeon_region(player, 'Hera Basement Cage', 'Tower of Hera', ['Tower of Hera - Basement Cage'], ['Hera Basement Cage to Crystal', 'Hera Basement Cage Up Stairs']),
        create_dungeon_region(player, 'Hera Basement Cage - Crystal', 'Tower of Hera', None, ['Hera Basement Cage Crystal Exit']),
        create_dungeon_region(player, 'Hera Tile Room', 'Tower of Hera', None, ['Hera Tile Room Up Stairs', 'Hera Tile Room EN']),
        create_dungeon_region(player, 'Hera Tridorm', 'Tower of Hera', None, ['Hera Tridorm WN', 'Hera Tridorm SE', 'Hera Tridorm to Crystal']),
        create_dungeon_region(player, 'Hera Tridorm - Crystal', 'Tower of Hera', None, ['Hera Tridorm Crystal Exit']),
        create_dungeon_region(player, 'Hera Torches', 'Tower of Hera', ['Tower of Hera - Big Key Chest'], ['Hera Torches NE']),
        create_dungeon_region(player, 'Hera Beetles', 'Tower of Hera', None, ['Hera Beetles Down Stairs', 'Hera Beetles WS', 'Hera Beetles Holes Front', 'Hera Beetles Holes Landing']),
        create_dungeon_region(player, 'Hera Startile Corner', 'Tower of Hera', None, ['Hera Startile Corner ES', 'Hera Startile Corner NW', 'Hera Startile Corner Holes Front', 'Hera Startile Corner Holes Landing']),
        create_dungeon_region(player, 'Hera Startile Wide', 'Tower of Hera', None, ['Hera Startile Wide SW', 'Hera Startile Wide Up Stairs', 'Hera Startile Wide Holes', 'Hera Startile Wide to Crystal']),
        create_dungeon_region(player, 'Hera Startile Wide - Crystal', 'Tower of Hera', None, ['Hera Startile Wide Crystal Exit']),
        create_dungeon_region(player, 'Hera 4F', 'Tower of Hera', ['Tower of Hera - Compass Chest'], ['Hera 4F Down Stairs', 'Hera 4F Up Stairs', 'Hera Big Chest Hook Path', 'Hera 4F Holes']),
        create_dungeon_region(player, 'Hera Big Chest Landing', 'Tower of Hera', ['Tower of Hera - Big Chest'], ['Hera Big Chest Landing Exit', 'Hera Big Chest Landing Holes']),
        create_dungeon_region(player, 'Hera 5F', 'Tower of Hera', None, ['Hera 5F Down Stairs', 'Hera 5F Up Stairs', 'Hera 5F Star Hole', 'Hera 5F Pothole Chain', 'Hera 5F Normal Holes', 'Hera 5F Orange Path']),
        create_dungeon_region(player, 'Hera 5F Pot Block', 'Tower of Hera', None),
        create_dungeon_region(player, 'Hera Fairies', 'Tower of Hera', None, ['Hera Fairies\' Warp']),
        create_dungeon_region(player, 'Hera Boss', 'Tower of Hera', None, ['Hera Boss Down Stairs', 'Hera Boss Outer Hole', 'Hera Boss Inner Hole', 'Tower of Hera Boss']),
        create_dungeon_region(player, 'Hera Boss Spoils', 'Tower of Hera', ['Tower of Hera - Boss', 'Tower of Hera - Prize', 'Tower of Hera - Boss Kill']),

        # AgaTower
        create_dungeon_region(player, 'Tower Lobby', 'Castle Tower', None, ['Tower Lobby NW', 'Tower Lobby S']),
        create_dungeon_region(player, 'Tower Gold Knights', 'Castle Tower', None, ['Tower Gold Knights SW', 'Tower Gold Knights EN']),
        create_dungeon_region(player, 'Tower Room 03', 'Castle Tower', ['Castle Tower - Room 03'], ['Tower Room 03 WN', 'Tower Room 03 Up Stairs']),
        create_dungeon_region(player, 'Tower Lone Statue', 'Castle Tower', None, ['Tower Lone Statue Down Stairs', 'Tower Lone Statue WN']),
        create_dungeon_region(player, 'Tower Dark Maze', 'Castle Tower', ['Castle Tower - Dark Maze'], ['Tower Dark Maze EN', 'Tower Dark Maze ES']),
        create_dungeon_region(player, 'Tower Dark Chargers', 'Castle Tower', None, ['Tower Dark Chargers WS', 'Tower Dark Chargers Up Stairs']),
        create_dungeon_region(player, 'Tower Dual Statues', 'Castle Tower', None, ['Tower Dual Statues Down Stairs', 'Tower Dual Statues WS']),
        create_dungeon_region(player, 'Tower Dark Pits', 'Castle Tower', None, ['Tower Dark Pits ES', 'Tower Dark Pits EN']),
        create_dungeon_region(player, 'Tower Dark Archers', 'Castle Tower', ['Castle Tower - Dark Archer Key Drop'], ['Tower Dark Archers WN', 'Tower Dark Archers Up Stairs']),
        create_dungeon_region(player, 'Tower Red Spears', 'Castle Tower', None, ['Tower Red Spears Down Stairs', 'Tower Red Spears WN']),
        create_dungeon_region(player, 'Tower Red Guards', 'Castle Tower', None, ['Tower Red Guards EN', 'Tower Red Guards SW']),
        create_dungeon_region(player, 'Tower Circle of Pots', 'Castle Tower', ['Castle Tower - Circle of Pots Key Drop'], ['Tower Circle of Pots NW', 'Tower Circle of Pots ES']),
        create_dungeon_region(player, 'Tower Pacifist Run', 'Castle Tower', None, ['Tower Pacifist Run WS', 'Tower Pacifist Run Up Stairs']),
        create_dungeon_region(player, 'Tower Push Statue', 'Castle Tower', None, ['Tower Push Statue Down Stairs', 'Tower Push Statue WS']),
        create_dungeon_region(player, 'Tower Catwalk', 'Castle Tower', None, ['Tower Catwalk ES', 'Tower Catwalk North Stairs']),
        create_dungeon_region(player, 'Tower Antechamber', 'Castle Tower', None, ['Tower Antechamber South Stairs', 'Tower Antechamber NW']),
        create_dungeon_region(player, 'Tower Altar', 'Castle Tower', None, ['Tower Altar SW', 'Tower Altar NW']),
        create_dungeon_region(player, 'Tower Agahnim 1', 'Castle Tower', ['Agahnim 1'], ['Tower Agahnim 1 SW']),

        # pod
        create_dungeon_region(player, 'PoD Lobby', 'Palace of Darkness', None, ['PoD Lobby N', 'PoD Lobby NW', 'PoD Lobby NE', 'PoD Lobby S']),
        create_dungeon_region(player, 'PoD Left Cage', 'Palace of Darkness', None, ['PoD Left Cage SW', 'PoD Left Cage Down Stairs']),
        create_dungeon_region(player, 'PoD Middle Cage', 'Palace of Darkness', None, ['PoD Middle Cage S', 'PoD Middle Cage SE', 'PoD Middle Cage N', 'PoD Middle Cage Down Stairs']),
        create_dungeon_region(player, 'PoD Shooter Room', 'Palace of Darkness', ['Palace of Darkness - Shooter Room'], ['PoD Shooter Room Up Stairs']),
        create_dungeon_region(player, 'PoD Pit Room', 'Palace of Darkness', None, ['PoD Pit Room S', 'PoD Pit Room NW', 'PoD Pit Room Bomb Hole', 'PoD Pit Room Block Path N']),
        create_dungeon_region(player, 'PoD Pit Room Blocked', 'Palace of Darkness', None, ['PoD Pit Room NE', 'PoD Pit Room Freefall', 'PoD Pit Room Block Path S']),
        create_dungeon_region(player, 'PoD Arena Main', 'Palace of Darkness', None, ['PoD Arena Main SW', 'PoD Arena Main to Ranged Crystal', 'PoD Arena Main to Landing Barrier - Blue', 'PoD Arena Main to Landing Bypass', 'PoD Arena Main to Right Bypass']),
        create_dungeon_region(player, 'PoD Arena Main - Ranged Crystal', 'Palace of Darkness', None, ['PoD Arena Main Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Arena North', 'Palace of Darkness', None, ['PoD Arena Main NW', 'PoD Arena Main NE', 'PoD Arena North Drop Down', 'PoD Arena North to Landing Barrier - Orange']),
        create_dungeon_region(player, 'PoD Arena Bridge', 'Palace of Darkness', ['Palace of Darkness - The Arena - Bridge'], ['PoD Arena Bridge SE', 'PoD Arena Bridge Drop Down', 'PoD Arena Bridge to Ranged Crystal']),
        create_dungeon_region(player, 'PoD Arena Bridge - Ranged Crystal', 'Palace of Darkness', None, ['PoD Arena Bridge Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Arena Landing', 'Palace of Darkness', None, ['PoD Arena Landing to Main Barrier - Blue', 'PoD Arena Landing to Right Barrier - Blue', 'PoD Arena Landing to North Barrier - Orange', 'PoD Arena Landing Bonk Path']),
        create_dungeon_region(player, 'PoD Arena Right', 'Palace of Darkness', None, ['PoD Arena Crystals E', 'PoD Arena Right to Landing Barrier - Blue', 'PoD Arena Right to Ranged Crystal']),
        create_dungeon_region(player, 'PoD Arena Right - Ranged Crystal', 'Palace of Darkness', None, ['PoD Arena Right Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Arena Ledge', 'Palace of Darkness', ['Palace of Darkness - The Arena - Ledge'], ['PoD Arena Ledge ES', 'PoD Arena Ledge to Ranged Crystal']),
        create_dungeon_region(player, 'PoD Arena Ledge - Ranged Crystal', 'Palace of Darkness', None, ['PoD Arena Ledge Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Sexy Statue', 'Palace of Darkness', None, ['PoD Sexy Statue W', 'PoD Sexy Statue NW']),
        create_dungeon_region(player, 'PoD Map Balcony', 'Palace of Darkness', ['Palace of Darkness - Map Chest'], ['PoD Map Balcony to Ranged Crystal', 'PoD Map Balcony WS', 'PoD Map Balcony South Stairs', 'PoD Map Balcony Drop Down', 'PoD Map Balcony ES']),
        create_dungeon_region(player, 'PoD Map Balcony - Ranged Crystal', 'Palace of Darkness', None, ['PoD Map Balcony Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Fairy Pool', 'Palace of Darkness', None, ['PoD Fairy Pool WS']),
        create_dungeon_region(player, 'PoD Conveyor', 'Palace of Darkness', None, ['PoD Conveyor North Stairs', 'PoD Conveyor SW']),
        create_dungeon_region(player, 'PoD Mimics 1', 'Palace of Darkness', None, ['PoD Mimics 1 NW', 'PoD Mimics 1 SW']),
        create_dungeon_region(player, 'PoD Jelly Hall', 'Palace of Darkness', None, ['PoD Jelly Hall NW', 'PoD Jelly Hall NE']),
        create_dungeon_region(player, 'PoD Warp Hint', 'Palace of Darkness', None, ['PoD Warp Hint SE', 'PoD Warp Hint Warp']),
        create_dungeon_region(player, 'PoD Warp Room', 'Palace of Darkness', None, ['PoD Warp Room Up Stairs', 'PoD Warp Room Warp']),
        create_dungeon_region(player, 'PoD Stalfos Basement', 'Palace of Darkness', ['Palace of Darkness - Stalfos Basement'], ['PoD Stalfos Basement Warp']),
        create_dungeon_region(player, 'PoD Basement Ledge', 'Palace of Darkness', None, ['PoD Basement Ledge Drop Down', 'PoD Basement Ledge Up Stairs']),
        create_dungeon_region(player, 'PoD Big Key Landing', 'Palace of Darkness', ['Palace of Darkness - Big Key Chest'], ['PoD Big Key Landing Down Stairs', 'PoD Big Key Landing Hole']),
        create_dungeon_region(player, 'PoD Falling Bridge Ledge', 'Palace of Darkness', None, ['PoD Falling Bridge WN', 'PoD Falling Bridge EN', 'PoD Falling Bridge Path S']),
        create_dungeon_region(player, 'PoD Falling Bridge Mid', 'Palace of Darkness', None, ['PoD Falling Bridge Mid Path S', 'PoD Falling Bridge Mid Path N']),
        create_dungeon_region(player, 'PoD Falling Bridge', 'Palace of Darkness', None, ['PoD Falling Bridge SW', 'PoD Falling Bridge Path N']),
        create_dungeon_region(player, 'PoD Dark Maze', 'Palace of Darkness', ['Palace of Darkness - Dark Maze - Top', 'Palace of Darkness - Dark Maze - Bottom'], ['PoD Dark Maze EN', 'PoD Dark Maze E']),
        create_dungeon_region(player, 'PoD Big Chest Balcony', 'Palace of Darkness', ['Palace of Darkness - Big Chest'], ['PoD Big Chest Balcony W']),
        create_dungeon_region(player, 'PoD Compass Room', 'Palace of Darkness', ['Palace of Darkness - Compass Chest'], ['PoD Compass Room SE', 'PoD Compass Room WN', 'PoD Compass Room W Down Stairs', 'PoD Compass Room E Down Stairs']),
        create_dungeon_region(player, 'PoD Dark Basement', 'Palace of Darkness', ['Palace of Darkness - Dark Basement - Left', 'Palace of Darkness - Dark Basement - Right'], ['PoD Dark Basement W Up Stairs', 'PoD Dark Basement E Up Stairs']),
        create_dungeon_region(player, 'PoD Harmless Hellway', 'Palace of Darkness', ['Palace of Darkness - Harmless Hellway'], ['PoD Harmless Hellway NE', 'PoD Harmless Hellway SE']),
        create_dungeon_region(player, 'PoD Mimics 2', 'Palace of Darkness', None, ['PoD Mimics 2 SW', 'PoD Mimics 2 NW']),
        create_dungeon_region(player, 'PoD Bow Statue Left', 'Palace of Darkness', None, ['PoD Bow Statue SW', 'PoD Bow Statue Left to Right Barrier - Orange', 'PoD Bow Statue Left to Right Bypass', 'PoD Bow Statue Left to Crystal']),
        create_dungeon_region(player, 'PoD Bow Statue Left - Crystal', 'Palace of Darkness', None, ['PoD Bow Statue Left Crystal Exit']),
        create_dungeon_region(player, 'PoD Bow Statue Right', 'Palace of Darkness', None, ['PoD Bow Statue Right to Left Barrier - Orange', 'PoD Bow Statue Right to Ranged Crystal', 'PoD Bow Statue Down Ladder']),
        create_dungeon_region(player, 'PoD Bow Statue Right - Ranged Crystal', 'Palace of Darkness', None, ['PoD Bow Statue Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Dark Pegs Landing', 'Palace of Darkness', None, ['PoD Dark Pegs Up Ladder', 'PoD Dark Pegs Landing to Right', 'PoD Dark Pegs Landing to Ranged Crystal']),
        create_dungeon_region(player, 'PoD Dark Pegs Right', 'Palace of Darkness', None, ['PoD Dark Pegs Right to Landing', 'PoD Dark Pegs Right to Middle Barrier - Orange', 'PoD Dark Pegs Right to Middle Bypass']),
        create_dungeon_region(player, 'PoD Dark Pegs Middle', 'Palace of Darkness', None, ['PoD Dark Pegs Middle to Right Barrier - Orange', 'PoD Dark Pegs Middle to Left Barrier - Blue', 'PoD Dark Pegs Middle to Ranged Crystal', 'PoD Dark Pegs Middle to Left Bypass']),
        create_dungeon_region(player, 'PoD Dark Pegs Left', 'Palace of Darkness', None, ['PoD Dark Pegs WN', 'PoD Dark Pegs Left to Middle Barrier - Blue', 'PoD Dark Pegs Left to Ranged Crystal']),
        create_dungeon_region(player, 'PoD Dark Pegs Landing - Ranged Crystal', 'Palace of Darkness', None, ['PoD Dark Pegs Landing Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Dark Pegs Middle - Ranged Crystal', 'Palace of Darkness', None, ['PoD Dark Pegs Middle Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Dark Pegs Left - Ranged Crystal', 'Palace of Darkness', None, ['PoD Dark Pegs Left Ranged Crystal Exit']),
        create_dungeon_region(player, 'PoD Lonely Turtle', 'Palace of Darkness', None, ['PoD Lonely Turtle SW', 'PoD Lonely Turtle EN']),
        create_dungeon_region(player, 'PoD Turtle Party', 'Palace of Darkness', None, ['PoD Turtle Party ES', 'PoD Turtle Party NW']),
        create_dungeon_region(player, 'PoD Dark Alley', 'Palace of Darkness', None, ['PoD Dark Alley NE']),
        create_dungeon_region(player, 'PoD Callback', 'Palace of Darkness', None, ['PoD Callback WS', 'PoD Callback Warp']),
        create_dungeon_region(player, 'PoD Boss', 'Palace of Darkness', None, ['PoD Boss SE', 'Palace of Darkness Boss']),
        create_dungeon_region(player, 'PoD Boss Spoils', 'Palace of Darkness', ['Palace of Darkness - Boss', 'Palace of Darkness - Prize', 'Palace of Darkness - Boss Kill']),

        # swamp
        create_dungeon_region(player, 'Swamp Lobby', 'Swamp Palace', None, ['Swamp Lobby S', 'Swamp Lobby Moat']),
        create_dungeon_region(player, 'Swamp Entrance', 'Swamp Palace', ['Swamp Palace - Entrance'], ['Swamp Entrance Down Stairs', 'Swamp Entrance Moat']),
        create_dungeon_region(player, 'Swamp Pot Row', 'Swamp Palace', ['Swamp Palace - Pot Row Pot Key'], ['Swamp Pot Row Up Stairs', 'Swamp Pot Row WN', 'Swamp Pot Row WS']),
        create_dungeon_region(player, 'Swamp Map Ledge', 'Swamp Palace', ['Swamp Palace - Map Chest'], ['Swamp Map Ledge EN']),
        create_dungeon_region(player, 'Swamp Trench 1 Approach', 'Swamp Palace', None, ['Swamp Trench 1 Approach ES', 'Swamp Trench 1 Approach Dry', 'Swamp Trench 1 Approach Key', 'Swamp Trench 1 Approach Swim Depart']),
        create_dungeon_region(player, 'Swamp Trench 1 Nexus', 'Swamp Palace', None, ['Swamp Trench 1 Nexus Approach', 'Swamp Trench 1 Nexus N', 'Swamp Trench 1 Nexus Key']),
        create_dungeon_region(player, 'Swamp Trench 1 Alcove', 'Swamp Palace', ['Swamp Palace - Trench 1 Pot Key'], ['Swamp Trench 1 Alcove S']),
        create_dungeon_region(player, 'Swamp Trench 1 Key Ledge', 'Swamp Palace', None, ['Swamp Trench 1 Key Ledge Dry', 'Swamp Trench 1 Key Approach', 'Swamp Trench 1 Key Ledge Depart', 'Swamp Trench 1 Key Ledge NW']),
        create_dungeon_region(player, 'Swamp Trench 1 Departure', 'Swamp Palace', None, ['Swamp Trench 1 Departure Dry', 'Swamp Trench 1 Departure Approach', 'Swamp Trench 1 Departure Key', 'Swamp Trench 1 Departure WS']),
        create_dungeon_region(player, 'Swamp Hammer Switch', 'Swamp Palace', ['Trench 1 Switch'], ['Swamp Hammer Switch SW', 'Swamp Hammer Switch WN']),
        create_dungeon_region(player, 'Swamp Hub', 'Swamp Palace', ['Swamp Palace - Big Chest'], ['Swamp Hub ES', 'Swamp Hub S', 'Swamp Hub WS', 'Swamp Hub WN', 'Swamp Hub Hook Path', 'Swamp Hub Side Hook Path']),
        create_dungeon_region(player, 'Swamp Hub Side Ledges', 'Swamp Palace', ['Swamp Palace - Hookshot Pot Key']),
        create_dungeon_region(player, 'Swamp Hub Dead Ledge', 'Swamp Palace', None, ['Swamp Hub Dead Ledge EN']),
        create_dungeon_region(player, 'Swamp Hub North Ledge', 'Swamp Palace', None, ['Swamp Hub North Ledge N', 'Swamp Hub North Ledge Drop Down']),
        create_dungeon_region(player, 'Swamp Donut Top', 'Swamp Palace', None, ['Swamp Donut Top N', 'Swamp Donut Top SE']),
        create_dungeon_region(player, 'Swamp Donut Bottom', 'Swamp Palace', None, ['Swamp Donut Bottom NE', 'Swamp Donut Bottom NW']),
        create_dungeon_region(player, 'Swamp Compass Donut', 'Swamp Palace', ['Swamp Palace - Compass Chest'], ['Swamp Compass Donut SW', 'Swamp Compass Donut Push Block']),
        create_dungeon_region(player, 'Swamp Crystal Switch Outer', 'Swamp Palace', None, ['Swamp Crystal Switch EN', 'Swamp Crystal Switch SE', 'Swamp Crystal Switch Outer to Inner Barrier - Blue', 'Swamp Crystal Switch Outer to Ranged Crystal', 'Swamp Crystal Switch Outer to Inner Bypass']),
        create_dungeon_region(player, 'Swamp Crystal Switch Outer - Ranged Crystal', 'Swamp Palace', None, ['Swamp Crystal Switch Outer Ranged Crystal Exit']),
        create_dungeon_region(player, 'Swamp Crystal Switch Inner', 'Swamp Palace', ['Trench 2 Switch'], ['Swamp Crystal Switch Inner to Crystal', 'Swamp Crystal Switch Inner to Outer Bypass', 'Swamp Crystal Switch Inner to Outer Barrier - Blue']),
        create_dungeon_region(player, 'Swamp Crystal Switch Inner - Crystal', 'Swamp Palace', None, ['Swamp Crystal Switch Inner Crystal Exit']),
        create_dungeon_region(player, 'Swamp Shortcut', 'Swamp Palace', None, ['Swamp Shortcut NE', 'Swamp Shortcut Blue Barrier']),
        create_dungeon_region(player, 'Swamp Trench 2 Pots', 'Swamp Palace', None, ['Swamp Trench 2 Pots ES', 'Swamp Trench 2 Pots Blue Barrier', 'Swamp Trench 2 Pots Dry', 'Swamp Trench 2 Pots Wet']),
        create_dungeon_region(player, 'Swamp Trench 2 Blocks', 'Swamp Palace', None, ['Swamp Trench 2 Blocks Pots', 'Swamp Trench 2 Blocks N']),
        create_dungeon_region(player, 'Swamp Trench 2 Alcove', 'Swamp Palace', ['Swamp Palace - Trench 2 Pot Key'], ['Swamp Trench 2 Alcove S']),
        create_dungeon_region(player, 'Swamp Trench 2 Departure', 'Swamp Palace', None, ['Swamp Trench 2 Departure Wet', 'Swamp Trench 2 Departure WS']),
        create_dungeon_region(player, 'Swamp Big Key Ledge', 'Swamp Palace', ['Swamp Palace - Big Key Chest'], ['Swamp Big Key Ledge WN']),
        create_dungeon_region(player, 'Swamp West Shallows', 'Swamp Palace', None, ['Swamp West Shallows ES', 'Swamp West Shallows Push Blocks']),
        create_dungeon_region(player, 'Swamp West Block Path', 'Swamp Palace', None, ['Swamp West Block Path Up Stairs', 'Swamp West Block Path Drop Down']),
        create_dungeon_region(player, 'Swamp West Ledge', 'Swamp Palace', ['Swamp Palace - West Chest'], ['Swamp West Ledge Drop Down', 'Swamp West Ledge Hook Path']),
        create_dungeon_region(player, 'Swamp Barrier Ledge', 'Swamp Palace', None, ['Swamp Barrier Ledge Drop Down', 'Swamp Barrier Ledge - Orange', 'Swamp Barrier Ledge Hook Path']),
        create_dungeon_region(player, 'Swamp Barrier', 'Swamp Palace', None, ['Swamp Barrier EN', 'Swamp Barrier - Orange']),
        create_dungeon_region(player, 'Swamp Attic', 'Swamp Palace', None, ['Swamp Attic Down Stairs', 'Swamp Attic Left Pit', 'Swamp Attic Right Pit']),
        create_dungeon_region(player, 'Swamp Push Statue', 'Swamp Palace', None, ['Swamp Push Statue S', 'Swamp Push Statue NW', 'Swamp Push Statue NE', 'Swamp Push Statue Down Stairs']),
        create_dungeon_region(player, 'Swamp Shooters', 'Swamp Palace', None, ['Swamp Shooters SW', 'Swamp Shooters EN']),
        create_dungeon_region(player, 'Swamp Left Elbow', 'Swamp Palace', None, ['Swamp Left Elbow WN', 'Swamp Left Elbow Down Stairs']),
        create_dungeon_region(player, 'Swamp Right Elbow', 'Swamp Palace', None, ['Swamp Right Elbow SE', 'Swamp Right Elbow Down Stairs']),
        create_dungeon_region(player, 'Swamp Drain Left', 'Swamp Palace', None, ['Swamp Drain Left Up Stairs', 'Swamp Drain WN']),
        create_dungeon_region(player, 'Swamp Drain Right', 'Swamp Palace', ['Swamp Drain'], ['Swamp Drain Right Switch', 'Swamp Drain Right Up Stairs']),
        create_dungeon_region(player, 'Swamp Flooded Room', 'Swamp Palace', None, ['Swamp Flooded Room Up Stairs', 'Swamp Flooded Room Ladder']),
        # this is more normal and allows getting the chests from doing this room backward in logic
        create_dungeon_region(player, 'Swamp Flooded Spot', 'Swamp Palace', ['Swamp Palace - Flooded Room - Left', 'Swamp Palace - Flooded Room - Right'], ['Swamp Flooded Room WS', 'Swamp Flooded Spot Ladder']),
        create_dungeon_region(player, 'Swamp Basement Shallows', 'Swamp Palace', None, ['Swamp Basement Shallows NW', 'Swamp Basement Shallows EN', 'Swamp Basement Shallows ES']),
        create_dungeon_region(player, 'Swamp Waterfall Room', 'Swamp Palace', ['Swamp Palace - Waterfall Room'], ['Swamp Waterfall Room SW', 'Swamp Waterfall Room NW', 'Swamp Waterfall Room NE']),
        create_dungeon_region(player, 'Swamp Refill', 'Swamp Palace', None, ['Swamp Refill SW']),
        create_dungeon_region(player, 'Swamp Behind Waterfall', 'Swamp Palace', None, ['Swamp Behind Waterfall SE', 'Swamp Behind Waterfall Up Stairs']),
        create_dungeon_region(player, 'Swamp C', 'Swamp Palace', None, ['Swamp C Down Stairs', 'Swamp C SE']),
        create_dungeon_region(player, 'Swamp Waterway', 'Swamp Palace', ['Swamp Palace - Waterway Pot Key'], ['Swamp Waterway NE', 'Swamp Waterway N', 'Swamp Waterway NW']),
        create_dungeon_region(player, 'Swamp I', 'Swamp Palace', None, ['Swamp I S']),
        create_dungeon_region(player, 'Swamp T', 'Swamp Palace', None, ['Swamp T SW', 'Swamp T NW']),
        create_dungeon_region(player, 'Swamp Boss', 'Swamp Palace', None, ['Swamp Boss SW', 'Swamp Palace Boss']),
        create_dungeon_region(player, 'Swamp Boss Spoils', 'Swamp Palace', ['Swamp Palace - Boss', 'Swamp Palace - Prize', 'Swamp Palace - Boss Kill']),

        # sw
        create_dungeon_region(player, 'Skull 1 Lobby', 'Skull Woods', None, ['Skull 1 Lobby S', 'Skull 1 Lobby WS', 'Skull 1 Lobby ES']),
        create_dungeon_region(player, 'Skull Map Room', 'Skull Woods', ['Skull Woods - Map Chest'], ['Skull Map Room WS', 'Skull Map Room SE']),
        create_dungeon_region(player, 'Skull Pot Circle', 'Skull Woods', None, ['Skull Pot Circle WN', 'Skull Pot Circle Star Path']),
        create_dungeon_region(player, 'Skull Pull Switch', 'Skull Woods', None, ['Skull Pull Switch EN', 'Skull Pull Switch S']),
        create_dungeon_region(player, 'Skull Big Chest', 'Skull Woods', ['Skull Woods - Big Chest'], ['Skull Big Chest N', 'Skull Big Chest Hookpath']),
        create_dungeon_region(player, 'Skull Pinball', 'Skull Woods', ['Skull Woods - Pinball Room'], ['Skull Pinball NE', 'Skull Pinball WS']),
        create_dungeon_region(player, 'Skull Pot Prison', 'Skull Woods', ['Skull Woods - Pot Prison'], ['Skull Pot Prison ES', 'Skull Pot Prison SE']),
        create_dungeon_region(player, 'Skull Compass Room', 'Skull Woods', ['Skull Woods - Compass Chest'], ['Skull Compass Room NE', 'Skull Compass Room ES', 'Skull Compass Room WS']),
        create_dungeon_region(player, 'Skull Left Drop', 'Skull Woods', None, ['Skull Left Drop ES']),
        create_dungeon_region(player, 'Skull 2 East Lobby', 'Skull Woods', None, ['Skull 2 East Lobby NW', 'Skull 2 East Lobby WS', 'Skull 2 East Lobby SW']),
        create_dungeon_region(player, 'Skull Big Key', 'Skull Woods', ['Skull Woods - Big Key Chest'], ['Skull Big Key SW', 'Skull Big Key EN']),
        create_dungeon_region(player, 'Skull Lone Pot', 'Skull Woods', None, ['Skull Lone Pot WN']),
        create_dungeon_region(player, 'Skull Small Hall', 'Skull Woods', None, ['Skull Small Hall ES', 'Skull Small Hall WS']),
        create_dungeon_region(player, 'Skull Back Drop', 'Skull Woods', ['Skull Star Tile'], ['Skull Back Drop Star Path']),
        create_dungeon_region(player, 'Skull 2 West Lobby', 'Skull Woods', ['Skull Woods - West Lobby Pot Key'], ['Skull 2 West Lobby ES', 'Skull 2 West Lobby Pits', 'Skull 2 West Lobby S']),
        create_dungeon_region(player, 'Skull 2 West Lobby Ledge', 'Skull Woods', None, ['Skull 2 West Lobby NW', 'Skull 2 West Lobby Ledge Pits']),
        create_dungeon_region(player, 'Skull X Room', 'Skull Woods', None, ['Skull X Room SW']),
        create_dungeon_region(player, 'Skull 3 Lobby', 'Skull Woods', None, ['Skull 3 Lobby NW', 'Skull 3 Lobby EN', 'Skull 3 Lobby SW']),
        create_dungeon_region(player, 'Skull East Bridge', 'Skull Woods', None, ['Skull East Bridge WN', 'Skull East Bridge WS']),
        create_dungeon_region(player, 'Skull West Bridge Nook', 'Skull Woods', ['Skull Woods - Bridge Room'], ['Skull West Bridge Nook ES']),
        create_dungeon_region(player, 'Skull Star Pits', 'Skull Woods', None, ['Skull Star Pits SW', 'Skull Star Pits ES']),
        create_dungeon_region(player, 'Skull Torch Room', 'Skull Woods', None, ['Skull Torch Room WS', 'Skull Torch Room WN']),
        create_dungeon_region(player, 'Skull Vines', 'Skull Woods', None, ['Skull Vines EN', 'Skull Vines NW']),
        create_dungeon_region(player, 'Skull Spike Corner', 'Skull Woods', ['Skull Woods - Spike Corner Key Drop'], ['Skull Spike Corner SW', 'Skull Spike Corner ES']),
        create_dungeon_region(player, 'Skull Final Drop', 'Skull Woods', None, ['Skull Final Drop WS', 'Skull Final Drop Hole']),
        create_dungeon_region(player, 'Skull Boss', 'Skull Woods', None, ['Skull Woods Boss']),
        create_dungeon_region(player, 'Skull Boss Spoils', 'Skull Woods', ['Skull Woods - Boss', 'Skull Woods - Prize', 'Skull Woods - Boss Kill']),

        # tt
        create_dungeon_region(player, 'Thieves Lobby', 'Thieves\' Town', ['Thieves\' Town - Map Chest'], ['Thieves Lobby S', 'Thieves Lobby N Edge', 'Thieves Lobby NE Edge', 'Thieves Lobby E']),
        create_dungeon_region(player, 'Thieves Ambush', 'Thieves\' Town', ['Thieves\' Town - Ambush Chest'], ['Thieves Ambush S Edge', 'Thieves Ambush SE Edge', 'Thieves Ambush ES Edge', 'Thieves Ambush EN Edge', 'Thieves Ambush E']),
        create_dungeon_region(player, 'Thieves Rail Ledge', 'Thieves\' Town', None, ['Thieves Rail Ledge NW', 'Thieves Rail Ledge W', 'Thieves Rail Ledge Drop Down']),
        create_dungeon_region(player, 'Thieves BK Corner', 'Thieves\' Town', None, ['Thieves BK Corner WN Edge', 'Thieves BK Corner WS Edge', 'Thieves BK Corner S Edge', 'Thieves BK Corner SW Edge', 'Thieves BK Corner NE']),
        create_dungeon_region(player, 'Thieves Compass Room', 'Thieves\' Town', ['Thieves\' Town - Compass Chest'], ['Thieves Compass Room NW Edge', 'Thieves Compass Room N Edge', 'Thieves Compass Room WS Edge', 'Thieves Compass Room W']),
        create_dungeon_region(player, 'Thieves Big Chest Nook', 'Thieves\' Town', ['Thieves\' Town - Big Key Chest'], ['Thieves Big Chest Nook ES Edge']),
        create_dungeon_region(player, 'Thieves Hallway', 'Thieves\' Town', ['Thieves\' Town - Hallway Pot Key'], ['Thieves Hallway SE', 'Thieves Hallway NE', 'Thieves Hallway WN', 'Thieves Hallway WS']),
        create_dungeon_region(player, 'Thieves Boss', 'Thieves\' Town', ['Revealing Light'], ['Thieves Boss SE', 'Thieves Town Boss']),
        create_dungeon_region(player, 'Thieves Boss Spoils', 'Thieves\' Town', ['Thieves\' Town - Boss', 'Thieves\' Town - Prize', 'Thieves\' Town - Boss Kill']),
        create_dungeon_region(player, 'Thieves Pot Alcove Mid', 'Thieves\' Town', None, ['Thieves Pot Alcove Mid ES', 'Thieves Pot Alcove Mid WS']),
        create_dungeon_region(player, 'Thieves Pot Alcove Bottom', 'Thieves\' Town', None, ['Thieves Pot Alcove Bottom SW']),
        create_dungeon_region(player, 'Thieves Pot Alcove Top', 'Thieves\' Town', None, ['Thieves Pot Alcove Top NW']),
        create_dungeon_region(player, 'Thieves Conveyor Maze', 'Thieves\' Town', None, ['Thieves Conveyor Maze SW', 'Thieves Conveyor Maze EN', 'Thieves Conveyor Maze WN', 'Thieves Conveyor Maze Down Stairs']),
        create_dungeon_region(player, 'Thieves Spike Track', 'Thieves\' Town', None, ['Thieves Spike Track WS', 'Thieves Spike Track ES', 'Thieves Spike Track NE']),
        create_dungeon_region(player, 'Thieves Hellway', 'Thieves\' Town', None, ['Thieves Hellway Orange Barrier', 'Thieves Hellway NW', 'Thieves Hellway Blue Barrier']),
        create_dungeon_region(player, 'Thieves Hellway N Crystal', 'Thieves\' Town', None, ['Thieves Hellway Crystal Blue Barrier', 'Thieves Hellway Crystal EN']),
        create_dungeon_region(player, 'Thieves Hellway S Crystal', 'Thieves\' Town', None, ['Thieves Hellway Crystal Orange Barrier', 'Thieves Hellway Crystal ES']),
        create_dungeon_region(player, 'Thieves Triple Bypass', 'Thieves\' Town', None, ['Thieves Triple Bypass WN', 'Thieves Triple Bypass EN', 'Thieves Triple Bypass SE']),
        create_dungeon_region(player, 'Thieves Spike Switch', 'Thieves\' Town', ['Thieves\' Town - Spike Switch Pot Key'], ['Thieves Spike Switch SW', 'Thieves Spike Switch Up Stairs']),
        create_dungeon_region(player, 'Thieves Attic', 'Thieves\' Town', None, ['Thieves Attic Down Stairs', 'Thieves Attic ES', 'Thieves Attic Orange Barrier', 'Thieves Attic Blue Barrier']),
        create_dungeon_region(player, 'Thieves Attic Switch', 'Thieves\' Town', None, ['Thieves Attic Switch Blue Barrier']),
        create_dungeon_region(player, 'Thieves Attic Hint', 'Thieves\' Town', None, ['Thieves Attic Hint Orange Barrier']),
        create_dungeon_region(player, 'Thieves Cricket Hall Left', 'Thieves\' Town', None, ['Thieves Cricket Hall Left WS', 'Thieves Cricket Hall Left Edge']),
        create_dungeon_region(player, 'Thieves Cricket Hall Right', 'Thieves\' Town', None, ['Thieves Cricket Hall Right Edge', 'Thieves Cricket Hall Right ES']),
        create_dungeon_region(player, 'Thieves Attic Window', 'Thieves\' Town', ['Thieves\' Town - Attic', 'Attic Cracked Floor'], ['Thieves Attic Window WS']),
        create_dungeon_region(player, 'Thieves Basement Block', 'Thieves\' Town', None, ['Thieves Basement Block Up Stairs', 'Thieves Basement Block WN', 'Thieves Basement Block Path']),
        create_dungeon_region(player, 'Thieves Blocked Entry', 'Thieves\' Town', None, ['Thieves Blocked Entry Path', 'Thieves Blocked Entry SW']),
        create_dungeon_region(player, 'Thieves Lonely Zazak', 'Thieves\' Town', None, ['Thieves Lonely Zazak WS', 'Thieves Lonely Zazak ES', 'Thieves Lonely Zazak NW']),
        create_dungeon_region(player, "Thieves Blind's Cell", 'Thieves\' Town', None, ["Thieves Blind's Cell WS", "Thieves Blind's Cell Door"]),
        create_dungeon_region(player, "Thieves Blind's Cell Interior", 'Thieves\' Town', ['Thieves\' Town - Blind\'s Cell', 'Suspicious Maiden'], ["Thieves Blind's Cell Exit"]),
        create_dungeon_region(player, 'Thieves Conveyor Bridge', 'Thieves\' Town', None, ['Thieves Conveyor Bridge EN', 'Thieves Conveyor Bridge ES', 'Thieves Conveyor Bridge WS', 'Thieves Conveyor Bridge Block Path']),
        create_dungeon_region(player, 'Thieves Conveyor Block', 'Thieves\' Town', None, ['Thieves Conveyor Block Path', 'Thieves Conveyor Block WN']),
        create_dungeon_region(player, 'Thieves Big Chest Room', 'Thieves\' Town', ['Thieves\' Town - Big Chest'], ['Thieves Big Chest Room ES']),
        create_dungeon_region(player, 'Thieves Trap', 'Thieves\' Town', None, ['Thieves Trap EN']),

        # ice
        create_dungeon_region(player, 'Ice Lobby', 'Ice Palace', None, ['Ice Lobby SE', 'Ice Lobby WS']),
        create_dungeon_region(player, 'Ice Jelly Key', 'Ice Palace', ['Ice Palace - Jelly Key Drop'], ['Ice Jelly Key ES', 'Ice Jelly Key Down Stairs']),
        create_dungeon_region(player, 'Ice Floor Switch', 'Ice Palace', None, ['Ice Floor Switch Up Stairs', 'Ice Floor Switch ES']),
        create_dungeon_region(player, 'Ice Cross Left', 'Ice Palace', None, ['Ice Cross Left WS', 'Ice Cross Left Push Block']),
        create_dungeon_region(player, 'Ice Cross Bottom', 'Ice Palace', None, ['Ice Cross Bottom SE', 'Ice Cross Bottom Push Block Left', 'Ice Cross Bottom Push Block Right']),
        create_dungeon_region(player, 'Ice Cross Right', 'Ice Palace', None, ['Ice Cross Right ES', 'Ice Cross Right Push Block Top', 'Ice Cross Right Push Block Bottom']),
        create_dungeon_region(player, 'Ice Cross Top', 'Ice Palace', None, ['Ice Cross Top NE', 'Ice Cross Top Push Block Bottom', 'Ice Cross Top Push Block Right']),
        create_dungeon_region(player, 'Ice Compass Room', 'Ice Palace', ['Ice Palace - Compass Chest'], ['Ice Compass Room NE']),
        create_dungeon_region(player, 'Ice Pengator Switch', 'Ice Palace', None, ['Ice Pengator Switch WS', 'Ice Pengator Switch ES']),
        create_dungeon_region(player, 'Ice Dead End', 'Ice Palace', None, ['Ice Dead End WS']),
        create_dungeon_region(player, 'Ice Big Key', 'Ice Palace', ['Ice Palace - Big Key Chest'], ['Ice Big Key Push Block', 'Ice Big Key Down Ladder']),
        create_dungeon_region(player, 'Ice Bomb Drop', 'Ice Palace', None, ['Ice Bomb Drop SE', 'Ice Bomb Drop Path']),
        create_dungeon_region(player, 'Ice Bomb Drop - Top', 'Ice Palace', None, ['Ice Bomb Drop Hole']),
        create_dungeon_region(player, 'Ice Stalfos Hint', 'Ice Palace', None, ['Ice Stalfos Hint SE']),
        create_dungeon_region(player, 'Ice Conveyor', 'Ice Palace', ['Ice Palace - Conveyor Key Drop'], ['Ice Conveyor NE', 'Ice Conveyor to Crystal', 'Ice Conveyor SW']),
        create_dungeon_region(player, 'Ice Conveyor - Crystal', 'Ice Palace', None, ['Ice Conveyor Crystal Exit']),
        create_dungeon_region(player, 'Ice Bomb Jump Ledge', 'Ice Palace', None, ['Ice Bomb Jump NW', 'Ice Bomb Jump Ledge Orange Barrier']),
        create_dungeon_region(player, 'Ice Bomb Jump Catwalk', 'Ice Palace', None, ['Ice Bomb Jump Catwalk Orange Barrier', 'Ice Bomb Jump EN']),
        create_dungeon_region(player, 'Ice Narrow Corridor', 'Ice Palace', None, ['Ice Narrow Corridor WN', 'Ice Narrow Corridor Down Stairs']),
        create_dungeon_region(player, 'Ice Pengator Trap', 'Ice Palace', None, ['Ice Pengator Trap Up Stairs', 'Ice Pengator Trap NE']),
        create_dungeon_region(player, 'Ice Spike Cross', 'Ice Palace', None, ['Ice Spike Cross SE', 'Ice Spike Cross WS', 'Ice Spike Cross ES', 'Ice Spike Cross NE']),
        create_dungeon_region(player, 'Ice Firebar', 'Ice Palace', None, ['Ice Firebar ES', 'Ice Firebar Down Ladder']),
        create_dungeon_region(player, 'Ice Falling Square', 'Ice Palace', None, ['Ice Falling Square SE', 'Ice Falling Square Hole']),
        create_dungeon_region(player, 'Ice Spike Room', 'Ice Palace', ['Ice Palace - Spike Room'], ['Ice Spike Room WS', 'Ice Spike Room Up Stairs', 'Ice Spike Room Down Stairs']),
        create_dungeon_region(player, 'Ice Right H', 'Ice Palace', None, ['Ice Hammer Block Down Stairs', 'Ice Hammer Block ES', 'Ice Right H Path']),
        create_dungeon_region(player, 'Ice Hammer Block', 'Ice Palace', ['Ice Palace - Hammer Block Key Drop', 'Ice Palace - Map Chest'], ['Ice Hammer Block Path']),
        create_dungeon_region(player, 'Ice Tongue Pull', 'Ice Palace', None, ['Ice Tongue Pull Up Ladder', 'Ice Tongue Pull WS']),
        create_dungeon_region(player, 'Ice Freezors', 'Ice Palace', ['Ice Palace - Freezor Chest'], ['Ice Freezors Up Ladder', 'Ice Freezors Hole', 'Ice Freezors Bomb Hole']),
        create_dungeon_region(player, 'Ice Freezors Ledge', 'Ice Palace', None, ['Ice Freezors Ledge ES', 'Ice Freezors Ledge Hole']),
        create_dungeon_region(player, 'Ice Tall Hint', 'Ice Palace', None, ['Ice Tall Hint WS', 'Ice Tall Hint SE', 'Ice Tall Hint EN']),
        create_dungeon_region(player, 'Ice Hookshot Ledge', 'Ice Palace', None, ['Ice Hookshot Ledge WN', 'Ice Hookshot Ledge Path']),
        create_dungeon_region(player, 'Ice Hookshot Balcony', 'Ice Palace', None, ['Ice Hookshot Balcony SW', 'Ice Hookshot Balcony Path']),
        create_dungeon_region(player, 'Ice Spikeball', 'Ice Palace', None, ['Ice Spikeball NW', 'Ice Spikeball Up Stairs']),
        create_dungeon_region(player, 'Ice Lonely Freezor', 'Ice Palace', None, ['Ice Lonely Freezor NE', 'Ice Lonely Freezor Down Stairs']),
        create_dungeon_region(player, 'Iced T', 'Ice Palace', ['Ice Palace - Iced T Room'], ['Iced T Up Stairs', 'Iced T EN']),
        create_dungeon_region(player, 'Ice Catwalk', 'Ice Palace', None, ['Ice Catwalk WN', 'Ice Catwalk NW']),
        create_dungeon_region(player, 'Ice Many Pots', 'Ice Palace', ['Ice Palace - Many Pots Pot Key'], ['Ice Many Pots SW', 'Ice Many Pots WS']),
        create_dungeon_region(player, 'Ice Crystal Right', 'Ice Palace', None, ['Ice Crystal Right ES', 'Ice Crystal Right NE', 'Ice Crystal Right Orange Barrier', 'Ice Crystal Right Blue Hole']),
        create_dungeon_region(player, 'Ice Crystal Left', 'Ice Palace', None, ['Ice Crystal Left WS', 'Ice Crystal Left Orange Barrier', 'Ice Crystal Left Blue Barrier']),
        create_dungeon_region(player, 'Ice Crystal Block', 'Ice Palace', ['Ice Block Drop'], ['Ice Crystal Block Hole', 'Ice Crystal Block Exit']),
        create_dungeon_region(player, 'Ice Big Chest View', 'Ice Palace', None, ['Ice Big Chest View ES']),
        create_dungeon_region(player, 'Ice Big Chest Landing', 'Ice Palace', ['Ice Palace - Big Chest'], ['Ice Big Chest Landing Push Blocks']),
        create_dungeon_region(player, 'Ice Backwards Room', 'Ice Palace', None, ['Ice Backwards Room SE', 'Ice Backwards Room Down Stairs', 'Ice Backwards Room Hole']),
        create_dungeon_region(player, 'Ice Anti-Fairy', 'Ice Palace', None, ['Ice Anti-Fairy Up Stairs', 'Ice Anti-Fairy SE']),
        create_dungeon_region(player, 'Ice Switch Room', 'Ice Palace', None, ['Ice Switch Room NE', 'Ice Switch Room ES', 'Ice Switch Room SE']),
        create_dungeon_region(player, 'Ice Refill', 'Ice Palace', None, ['Ice Refill WS', 'Ice Refill to Crystal']),
        create_dungeon_region(player, 'Ice Refill - Crystal', 'Ice Palace', None, ['Ice Refill Crystal Exit']),
        create_dungeon_region(player, 'Ice Fairy', 'Ice Palace', None, ['Ice Fairy Warp']),
        create_dungeon_region(player, 'Ice Antechamber', 'Ice Palace', None, ['Ice Antechamber NE', 'Ice Antechamber Hole']),
        create_dungeon_region(player, 'Ice Boss', 'Ice Palace', None, ['Ice Palace Boss']),
        create_dungeon_region(player, 'Ice Boss Spoils', 'Ice Palace', ['Ice Palace - Boss', 'Ice Palace - Prize', 'Ice Palace - Boss Kill']),

        # mire
        create_dungeon_region(player, 'Mire Lobby', 'Misery Mire', None, ['Mire Lobby S', 'Mire Lobby Gap']),
        create_dungeon_region(player, 'Mire Post-Gap', 'Misery Mire', None, ['Mire Post-Gap Gap', 'Mire Post-Gap Down Stairs']),
        create_dungeon_region(player, 'Mire 2', 'Misery Mire', None, ['Mire 2 Up Stairs', 'Mire 2 NE']),
        create_dungeon_region(player, 'Mire Hub', 'Misery Mire', None, ['Mire Hub SE', 'Mire Hub ES', 'Mire Hub E', 'Mire Hub NE', 'Mire Hub WN', 'Mire Hub WS', 'Mire Hub Upper Blue Barrier', 'Mire Hub Lower Blue Barrier']),
        create_dungeon_region(player, 'Mire Hub Right', 'Misery Mire', None, ['Mire Hub Right EN', 'Mire Hub Right Blue Barrier']),
        create_dungeon_region(player, 'Mire Hub Top', 'Misery Mire', None, ['Mire Hub Top NW', 'Mire Hub Top Blue Barrier']),
        create_dungeon_region(player, 'Mire Hub Switch', 'Misery Mire', ['Misery Mire - Main Lobby'], ['Mire Hub Switch Blue Barrier N', 'Mire Hub Switch Blue Barrier S']),
        create_dungeon_region(player, 'Mire Lone Shooter', 'Misery Mire', None, ['Mire Lone Shooter WS', 'Mire Lone Shooter ES']),
        create_dungeon_region(player, 'Mire Failure Bridge', 'Misery Mire', None, ['Mire Failure Bridge W', 'Mire Failure Bridge E']),
        create_dungeon_region(player, 'Mire Falling Bridge - Failure', 'Misery Mire', None,
                              ['Mire Falling Bridge W', 'Mire Falling Bridge Hook Only Path', 'Mire Falling Bridge Primary Path']),
        create_dungeon_region(player, 'Mire Falling Bridge - Primary', 'Misery Mire', None,
                              ['Mire Falling Bridge WS', 'Mire Falling Bridge Hook Path', 'Mire Falling Bridge Failure Path']),
        create_dungeon_region(player, 'Mire Falling Bridge - Chest', 'Misery Mire', ['Misery Mire - Big Chest'],
                              ['Mire Falling Bridge WN']),
        create_dungeon_region(player, 'Mire Map Spike Side', 'Misery Mire', None, ['Mire Map Spike Side EN', 'Mire Map Spike Side Drop Down', 'Mire Map Spike Side Blue Barrier']),
        create_dungeon_region(player, 'Mire Map Spot', 'Misery Mire', ['Misery Mire - Map Chest'], ['Mire Map Spot WN', 'Mire Map Spot Blue Barrier']),
        create_dungeon_region(player, 'Mire Crystal Dead End', 'Misery Mire', None, ['Mire Crystal Dead End Left Barrier', 'Mire Crystal Dead End Right Barrier', 'Mire Crystal Dead End NW']),
        create_dungeon_region(player, 'Mire Hidden Shooters', 'Misery Mire', None, ['Mire Hidden Shooters SE', 'Mire Hidden Shooters WS', 'Mire Hidden Shooters ES', 'Mire Hidden Shooters Block Path N']),
        create_dungeon_region(player, 'Mire Hidden Shooters Blocked', 'Misery Mire', None, ['Mire Hidden Shooters NE', 'Mire Hidden Shooters Block Path S']),
        create_dungeon_region(player, 'Mire Cross', 'Misery Mire', None, ['Mire Cross ES', 'Mire Cross SW']),
        create_dungeon_region(player, 'Mire Minibridge', 'Misery Mire', None, ['Mire Minibridge SE', 'Mire Minibridge NE']),
        create_dungeon_region(player, 'Mire BK Door Room', 'Misery Mire', None, ['Mire BK Door Room EN', 'Mire BK Door Room N']),
        create_dungeon_region(player, 'Mire Spikes', 'Misery Mire', ['Misery Mire - Spike Chest', 'Misery Mire - Spikes Pot Key'], ['Mire Spikes WS', 'Mire Spikes SW', 'Mire Spikes NW']),
        create_dungeon_region(player, 'Mire Ledgehop', 'Misery Mire', None, ['Mire Ledgehop SW', 'Mire Ledgehop WN', 'Mire Ledgehop NW']),
        create_dungeon_region(player, 'Mire Bent Bridge', 'Misery Mire', None, ['Mire Bent Bridge SW', 'Mire Bent Bridge W']),
        create_dungeon_region(player, 'Mire Over Bridge', 'Misery Mire', None, ['Mire Over Bridge E', 'Mire Over Bridge W']),
        create_dungeon_region(player, 'Mire Right Bridge', 'Misery Mire', ['Misery Mire - Bridge Chest'], ['Mire Right Bridge SE']),
        create_dungeon_region(player, 'Mire Left Bridge', 'Misery Mire', None, ['Mire Left Bridge S', 'Mire Left Bridge Down Stairs', 'Mire Left Bridge Hook Path']),
        create_dungeon_region(player, 'Mire Fishbone', 'Misery Mire', ['Misery Mire - Fishbone Pot Key'], ['Mire Fishbone E', 'Mire Fishbone Blue Barrier', 'Mire Fishbone Blue Barrier Bypass']),
        create_dungeon_region(player, 'Mire South Fish', 'Misery Mire', None, ['Mire South Fish Blue Barrier', 'Mire Fishbone SE']),
        create_dungeon_region(player, 'Mire Spike Barrier', 'Misery Mire', None, ['Mire Spike Barrier NE', 'Mire Spike Barrier SE', 'Mire Spike Barrier ES']),
        create_dungeon_region(player, 'Mire Square Rail', 'Misery Mire', None, ['Mire Square Rail WS', 'Mire Square Rail NW']),
        create_dungeon_region(player, 'Mire Lone Warp', 'Misery Mire', None, ['Mire Lone Warp SW', 'Mire Lone Warp Warp']),
        create_dungeon_region(player, 'Mire Wizzrobe Bypass', 'Misery Mire', None, ['Mire Wizzrobe Bypass WN', 'Mire Wizzrobe Bypass EN', 'Mire Wizzrobe Bypass NE']),
        create_dungeon_region(player, 'Mire Conveyor Crystal', 'Misery Mire', ['Misery Mire - Conveyor Crystal Key Drop'], ['Mire Conveyor to Crystal', 'Mire Conveyor Crystal WS', 'Mire Conveyor Crystal ES', 'Mire Conveyor Crystal SE']),
        create_dungeon_region(player, 'Mire Conveyor - Crystal', 'Misery Mire', None, ['Mire Conveyor Crystal Exit']),
        create_dungeon_region(player, 'Mire Tile Room', 'Misery Mire', None, ['Mire Tile Room ES', 'Mire Tile Room NW', 'Mire Tile Room SW']),
        create_dungeon_region(player, 'Mire Compass Room', 'Misery Mire', None, ['Mire Compass Room SW', 'Mire Compass Room EN', 'Mire Compass Blue Barrier']),
        create_dungeon_region(player, 'Mire Compass Chest', 'Misery Mire', ['Misery Mire - Compass Chest'], ['Mire Compass Chest Exit']),
        create_dungeon_region(player, 'Mire Neglected Room', 'Misery Mire', None, ['Mire Neglected Room SE', 'Mire Neglected Room NE']),
        create_dungeon_region(player, 'Mire Chest View', 'Misery Mire', None, ['Mire Chest View NE']),
        create_dungeon_region(player, 'Mire Conveyor Barrier', 'Misery Mire', None, ['Mire Conveyor Barrier NW', 'Mire Conveyor Barrier Up Stairs']),
        create_dungeon_region(player, 'Mire BK Chest Ledge', 'Misery Mire', ['Misery Mire - Big Key Chest'], ['Mire BK Chest Ledge WS']),
        create_dungeon_region(player, 'Mire Warping Pool', 'Misery Mire', None, ['Mire Warping Pool ES', 'Mire Warping Pool Warp']),
        create_dungeon_region(player, 'Mire Torches Top', 'Misery Mire', None, ['Mire Torches Top Down Stairs', 'Mire Torches Top SW', 'Mire Torches Top Holes']),
        create_dungeon_region(player, 'Mire Torches Bottom', 'Misery Mire', None, ['Mire Torches Bottom NW', 'Mire Torches Bottom ES', 'Mire Torches Bottom Holes']),
        create_dungeon_region(player, 'Mire Attic Hint', 'Misery Mire', None, ['Mire Attic Hint WS', 'Mire Attic Hint Hole']),
        create_dungeon_region(player, 'Mire Dark Shooters', 'Misery Mire', None, ['Mire Dark Shooters Up Stairs', 'Mire Dark Shooters SW', 'Mire Dark Shooters SE']),
        create_dungeon_region(player, 'Mire Key Rupees', 'Misery Mire', None, ['Mire Key Rupees NE']),
        create_dungeon_region(player, 'Mire Block X', 'Misery Mire', None, ['Mire Block X NW', 'Mire Block X WS']),
        create_dungeon_region(player, 'Mire Tall Dark and Roomy', 'Misery Mire', None, ['Mire Tall Dark and Roomy ES', 'Mire Tall Dark and Roomy WS', 'Mire Tall Dark and Roomy WN', 'Mire Tall Dark and Roomy to Ranged Crystal']),
        create_dungeon_region(player, 'Mire Tall Dark and Roomy - Ranged Crystal', 'Misery Mire', None, ['Mire Tall Dark and Roomy Ranged Crystal Exit']),
        create_dungeon_region(player, 'Mire Crystal Right', 'Misery Mire', None, ['Mire Crystal Right ES', 'Mire Crystal Right Orange Barrier']),
        create_dungeon_region(player, 'Mire Crystal Mid', 'Misery Mire', None, ['Mire Crystal Mid Orange Barrier', 'Mire Crystal Mid Blue Barrier', 'Mire Crystal Mid NW']),
        create_dungeon_region(player, 'Mire Crystal Left', 'Misery Mire', None, ['Mire Crystal Left Blue Barrier', 'Mire Crystal Left WS']),
        create_dungeon_region(player, 'Mire Crystal Top', 'Misery Mire', None, ['Mire Crystal Top SW']),
        create_dungeon_region(player, 'Mire Shooter Rupees', 'Misery Mire', None, ['Mire Shooter Rupees EN']),
        create_dungeon_region(player, 'Mire Falling Foes', 'Misery Mire', None, ['Mire Falling Foes ES', 'Mire Falling Foes Up Stairs']),
        create_dungeon_region(player, 'Mire Firesnake Skip', 'Misery Mire', None, ['Mire Firesnake Skip Down Stairs', 'Mire Firesnake Skip Orange Barrier']),
        create_dungeon_region(player, 'Mire Antechamber', 'Misery Mire', None, ['Mire Antechamber Orange Barrier', 'Mire Antechamber NW']),
        create_dungeon_region(player, 'Mire Boss', 'Misery Mire', None, ['Mire Boss SW', 'Misery Mire Boss']),
        create_dungeon_region(player, 'Mire Boss Spoils', 'Misery Mire', ['Misery Mire - Boss', 'Misery Mire - Prize', 'Misery Mire - Boss Kill']),

        # tr
        create_dungeon_region(player, 'TR Main Lobby', 'Turtle Rock', None, ['TR Main Lobby Gap', 'TR Main Lobby SE']),
        create_dungeon_region(player, 'TR Lobby Ledge', 'Turtle Rock', None, ['TR Lobby Ledge NE', 'TR Lobby Ledge Gap']),
        create_dungeon_region(player, 'TR Compass Room', 'Turtle Rock', ['Turtle Rock - Compass Chest'], ['TR Compass Room NW']),
        create_dungeon_region(player, 'TR Hub', 'Turtle Rock', None, ['TR Hub SW', 'TR Hub SE', 'TR Hub ES', 'TR Hub EN', 'TR Hub NW', 'TR Hub NE', 'TR Hub Path']),
        create_dungeon_region(player, 'TR Hub Ledges', 'Turtle Rock', None, ['TR Hub Ledges Path']),
        create_dungeon_region(player, 'TR Torches Ledge', 'Turtle Rock', None, ['TR Torches Ledge WS']),
        create_dungeon_region(player, 'TR Torches', 'Turtle Rock', None, ['TR Torches WN', 'TR Torches NW']),
        create_dungeon_region(player, 'TR Roller Room', 'Turtle Rock', ['Turtle Rock - Roller Room - Left', 'Turtle Rock - Roller Room - Right'], ['TR Roller Room SW']),
        create_dungeon_region(player, 'TR Tile Room', 'Turtle Rock', None, ['TR Tile Room SE', 'TR Tile Room NE']),
        create_dungeon_region(player, 'TR Refill', 'Turtle Rock', None, ['TR Refill SE']),
        create_dungeon_region(player, 'TR Pokey 1', 'Turtle Rock', ['Turtle Rock - Pokey 1 Key Drop'], ['TR Pokey 1 SW', 'TR Pokey 1 NW']),
        create_dungeon_region(player, 'TR Chain Chomps Top', 'Turtle Rock', ['Turtle Rock - Chain Chomps'], ['TR Chain Chomps Top to Crystal', 'TR Chain Chomps Down Stairs', 'TR Chain Chomps Top to Bottom Barrier - Orange']),
        create_dungeon_region(player, 'TR Chain Chomps Top - Crystal', 'Turtle Rock', None, ['TR Chain Chomps Top Crystal Exit']),
        create_dungeon_region(player, 'TR Chain Chomps Bottom', 'Turtle Rock', None, ['TR Chain Chomps SW', 'TR Chain Chomps Bottom to Top Barrier - Orange', 'TR Chain Chomps Bottom to Ranged Crystal']),
        create_dungeon_region(player, 'TR Chain Chomps Bottom - Ranged Crystal', 'Turtle Rock', None, ['TR Chain Chomps Bottom Ranged Crystal Exit']),
        create_dungeon_region(player, 'TR Pipe Pit', 'Turtle Rock', None, ['TR Pipe Pit Up Stairs', 'TR Pipe Pit WN']),
        create_dungeon_region(player, 'TR Pipe Ledge', 'Turtle Rock', None, ['TR Pipe Ledge WS', 'TR Pipe Ledge Drop Down']),
        create_dungeon_region(player, 'TR Lava Dual Pipes', 'Turtle Rock', None, ['TR Lava Dual Pipes EN', 'TR Lava Dual Pipes WN', 'TR Lava Dual Pipes SW']),
        create_dungeon_region(player, 'TR Lava Island', 'Turtle Rock', ['Turtle Rock - Big Key Chest'], ['TR Lava Island WS', 'TR Lava Island ES']),
        create_dungeon_region(player, 'TR Lava Escape', 'Turtle Rock', None, ['TR Lava Escape SE', 'TR Lava Escape NW']),
        create_dungeon_region(player, 'TR Pokey 2 Top', 'Turtle Rock', None, ['TR Pokey 2 EN', 'TR Pokey 2 Top to Bottom Barrier - Blue', 'TR Pokey 2 Top to Crystal']),
        create_dungeon_region(player, 'TR Pokey 2 Top - Crystal', 'Turtle Rock', None, ['TR Pokey 2 Top Crystal Exit']),
        create_dungeon_region(player, 'TR Pokey 2 Bottom', 'Turtle Rock', ['Turtle Rock - Pokey 2 Key Drop'], ['TR Pokey 2 ES', 'TR Pokey 2 Bottom to Top Barrier - Blue', 'TR Pokey 2 Bottom to Ranged Crystal']),
        create_dungeon_region(player, 'TR Pokey 2 Bottom - Ranged Crystal', 'Turtle Rock', None, ['TR Pokey 2 Bottom Ranged Crystal Exit']),
        create_dungeon_region(player, 'TR Twin Pokeys', 'Turtle Rock', None, ['TR Twin Pokeys NW', 'TR Twin Pokeys EN', 'TR Twin Pokeys SW']),
        create_dungeon_region(player, 'TR Hallway', 'Turtle Rock', None, ['TR Hallway NW', 'TR Hallway ES', 'TR Hallway WS']),
        create_dungeon_region(player, 'TR Dodgers', 'Turtle Rock', None, ['TR Dodgers WN', 'TR Dodgers SE', 'TR Dodgers NE']),
        create_dungeon_region(player, 'TR Big View', 'Turtle Rock', None, ['TR Big View WS']),
        create_dungeon_region(player, 'TR Big Chest', 'Turtle Rock', ['Turtle Rock - Big Chest'], ['TR Big Chest Gap', 'TR Big Chest NE']),
        create_dungeon_region(player, 'TR Big Chest Entrance', 'Turtle Rock', None, ['TR Big Chest Entrance SE', 'TR Big Chest Entrance Gap']),
        create_dungeon_region(player, 'TR Lazy Eyes', 'Turtle Rock', None, ['TR Lazy Eyes SE', 'TR Lazy Eyes ES']),
        create_dungeon_region(player, 'TR Dash Room', 'Turtle Rock', None, ['TR Dash Room SW', 'TR Dash Room ES', 'TR Dash Room NW']),
        create_dungeon_region(player, 'TR Tongue Pull', 'Turtle Rock', None, ['TR Tongue Pull WS', 'TR Tongue Pull NE']),
        create_dungeon_region(player, 'TR Rupees', 'Turtle Rock', None, ['TR Rupees SE']),
        create_dungeon_region(player, 'TR Crystaroller Bottom' , 'Turtle Rock', None, ['TR Crystaroller Bottom to Middle Barrier - Orange', 'TR Crystaroller Bottom to Ranged Crystal', 'TR Crystaroller SW']),
        create_dungeon_region(player, 'TR Crystaroller Middle', 'Turtle Rock', None, ['TR Crystaroller Middle to Bottom Barrier - Orange', 'TR Crystaroller Middle to Chest Barrier - Blue', 'TR Crystaroller Middle to Top Barrier - Orange', 'TR Crystaroller Middle to Ranged Crystal', 'TR Crystaroller Middle to Bottom Bypass']),
        create_dungeon_region(player, 'TR Crystaroller Top', 'Turtle Rock', None, ['TR Crystaroller Top to Middle Barrier - Orange', 'TR Crystaroller Down Stairs', 'TR Crystaroller Top to Crystal']),
        create_dungeon_region(player, 'TR Crystaroller Top - Crystal', 'Turtle Rock', None, ['TR Crystaroller Top Crystal Exit']),
        create_dungeon_region(player, 'TR Crystaroller Chest', 'Turtle Rock', ['Turtle Rock - Crystaroller Room'], ['TR Crystaroller Chest to Middle Barrier - Blue']),
        create_dungeon_region(player, 'TR Crystaroller Middle - Ranged Crystal', 'Turtle Rock', None, ['TR Crystaroller Middle Ranged Crystal Exit']),
        create_dungeon_region(player, 'TR Crystaroller Bottom - Ranged Crystal', 'Turtle Rock', None, ['TR Crystaroller Bottom Ranged Crystal Exit']),
        create_dungeon_region(player, 'TR Dark Ride', 'Turtle Rock', None, ['TR Dark Ride Up Stairs', 'TR Dark Ride SW', 'TR Dark Ride Path']),
        create_dungeon_region(player, 'TR Dark Ride Ledges', 'Turtle Rock', None, ['TR Dark Ride Ledges Path']),
        create_dungeon_region(player, 'TR Dash Bridge', 'Turtle Rock', None, ['TR Dash Bridge NW', 'TR Dash Bridge SW', 'TR Dash Bridge WS']),
        create_dungeon_region(player, 'TR Eye Bridge', 'Turtle Rock', ['Turtle Rock - Eye Bridge - Bottom Left', 'Turtle Rock - Eye Bridge - Bottom Right',
                                                                       'Turtle Rock - Eye Bridge - Top Left', 'Turtle Rock - Eye Bridge - Top Right'],
                                                                      ['TR Eye Bridge SW', 'TR Eye Bridge NW']),
        create_dungeon_region(player, 'TR Crystal Maze Start', 'Turtle Rock', None, ['TR Crystal Maze ES', 'TR Crystal Maze Start to Interior Barrier - Blue', 'TR Crystal Maze Start to Crystal']),
        create_dungeon_region(player, 'TR Crystal Maze Start - Crystal', 'Turtle Rock', None, ['TR Crystal Maze Start Crystal Exit']),
        create_dungeon_region(player, 'TR Crystal Maze Interior', 'Turtle Rock', None, ['TR Crystal Maze Interior to End Barrier - Blue', 'TR Crystal Maze Interior to Start Barrier - Blue', 'TR Crystal Maze Interior to Start Bypass', 'TR Crystal Maze Interior to End Bypass']),
        create_dungeon_region(player, 'TR Crystal Maze End', 'Turtle Rock', None, ['TR Crystal Maze North Stairs', 'TR Crystal Maze End to Interior Barrier - Blue', 'TR Crystal Maze End to Ranged Crystal']),
        create_dungeon_region(player, 'TR Crystal Maze End - Ranged Crystal', 'Turtle Rock', None, ['TR Crystal Maze End Ranged Crystal Exit']),
        create_dungeon_region(player, 'TR Final Abyss Balcony', 'Turtle Rock', None, ['TR Final Abyss South Stairs', 'TR Final Abyss Balcony Path']),
        create_dungeon_region(player, 'TR Final Abyss Ledge', 'Turtle Rock', None, ['TR Final Abyss NW', 'TR Final Abyss Ledge Path']),
        create_dungeon_region(player, 'TR Boss', 'Turtle Rock', None, ['TR Boss SW', 'Turtle Rock Boss']),
        create_dungeon_region(player, 'TR Boss Spoils', 'Turtle Rock', ['Turtle Rock - Boss', 'Turtle Rock - Prize', 'Turtle Rock - Boss Kill']),

        # gt
        create_dungeon_region(player, 'GT Lobby', 'Ganon\'s Tower', None, ['GT Lobby Left Down Stairs', 'GT Lobby Up Stairs', 'GT Lobby Right Down Stairs', 'GT Lobby S']),
        create_dungeon_region(player, 'GT Bob\'s Torch', 'Ganon\'s Tower', ['Ganons Tower - Bob\'s Torch'], ['GT Torch Up Stairs', 'GT Torch WN', 'GT Torch EN', 'GT Torch SW']),
        create_dungeon_region(player, 'GT Hope Room', 'Ganon\'s Tower', ['Ganons Tower - Hope Room - Left', 'Ganons Tower - Hope Room - Right'], ['GT Hope Room Up Stairs', 'GT Hope Room WN', 'GT Hope Room EN']),
        create_dungeon_region(player, 'GT Big Chest', 'Ganon\'s Tower', ['Ganons Tower - Big Chest'], ['GT Big Chest NW', 'GT Big Chest SW']),
        create_dungeon_region(player, 'GT Blocked Stairs', 'Ganon\'s Tower', None, ['GT Blocked Stairs Down Stairs', 'GT Blocked Stairs Block Path']),
        create_dungeon_region(player, 'GT Bob\'s Room', 'Ganon\'s Tower', ['Ganons Tower - Bob\'s Chest'], ['GT Bob\'s Room SE', 'GT Bob\'s Room Hole']),
        create_dungeon_region(player, 'GT Tile Room', 'Ganon\'s Tower', ['Ganons Tower - Tile Room'], ['GT Tile Room WN', 'GT Tile Room EN']),
        create_dungeon_region(player, 'GT Speed Torch', 'Ganon\'s Tower', None, ['GT Speed Torch WS', 'GT Speed Torch SE', 'GT Speed Torch North Path']),
        create_dungeon_region(player, 'GT Speed Torch Upper', 'Ganon\'s Tower', None, ['GT Speed Torch WN', 'GT Speed Torch NE', 'GT Speed Torch South Path']),
        create_dungeon_region(player, 'GT Pots n Blocks', 'Ganon\'s Tower', None, ['GT Pots n Blocks ES']),
        create_dungeon_region(player, 'GT Crystal Conveyor', 'Ganon\'s Tower', None, ['GT Crystal Conveyor NE', 'GT Crystal Conveyor to Corner Barrier - Blue', 'GT Crystal Conveyor to Ranged Crystal']),
        create_dungeon_region(player, 'GT Crystal Conveyor Corner', 'Ganon\'s Tower', None, ['GT Crystal Conveyor Corner to Barrier - Blue', 'GT Crystal Conveyor Corner to Barrier - Orange', 'GT Crystal Conveyor Corner to Ranged Crystal', 'GT Crystal Conveyor Corner to Left Bypass']),
        create_dungeon_region(player, 'GT Crystal Conveyor Left', 'Ganon\'s Tower', None, ['GT Crystal Conveyor WN', 'GT Crystal Conveyor Left to Corner Barrier - Orange']),
        create_dungeon_region(player, 'GT Crystal Conveyor - Ranged Crystal', 'Ganon\'s Tower', None, ['GT Crystal Conveyor Ranged Crystal Exit']),
        create_dungeon_region(player, 'GT Crystal Conveyor Corner - Ranged Crystal', 'Ganon\'s Tower', None, ['GT Crystal Conveyor Corner Ranged Crystal Exit']),

        create_dungeon_region(player, 'GT Compass Room', 'Ganon\'s Tower', ['Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right'],
                              ['GT Compass Room EN', 'GT Compass Room Warp']),
        create_dungeon_region(player, 'GT Invisible Bridges', 'Ganon\'s Tower', None, ['GT Invisible Bridges WS']),
        create_dungeon_region(player, 'GT Invisible Catwalk', 'Ganon\'s Tower', None, ['GT Invisible Catwalk ES', 'GT Invisible Catwalk WS', 'GT Invisible Catwalk NW', 'GT Invisible Catwalk NE']),
        create_dungeon_region(player, 'GT Conveyor Cross', 'Ganon\'s Tower', ['Ganons Tower - Conveyor Cross Pot Key'], ['GT Conveyor Cross EN', 'GT Conveyor Cross Hammer Path']),
        create_dungeon_region(player, 'GT Conveyor Cross Across Pits', 'Ganon\'s Tower', None, ['GT Conveyor Cross Hookshot Path', 'GT Conveyor Cross WN']),
        create_dungeon_region(player, 'GT Hookshot East Platform', 'Ganon\'s Tower', None, ['GT Hookshot EN', 'GT Hookshot East-Mid Path']),
        create_dungeon_region(player, 'GT Hookshot Mid Platform', 'Ganon\'s Tower', None, ['GT Hookshot Mid-East Path', 'GT Hookshot Mid-South Path', 'GT Hookshot Mid-North Path']),
        create_dungeon_region(player, 'GT Hookshot North Platform', 'Ganon\'s Tower', None, ['GT Hookshot NW', 'GT Hookshot North-Mid Path']),
        create_dungeon_region(player, 'GT Hookshot South Platform', 'Ganon\'s Tower', None, ['GT Hookshot ES', 'GT Hookshot South-Mid Path', 'GT Hookshot Platform Blue Barrier', 'GT Hookshot Platform Barrier Bypass']),
        create_dungeon_region(player, 'GT Hookshot South Entry', 'Ganon\'s Tower', None, ['GT Hookshot SW', 'GT Hookshot Entry Blue Barrier', 'GT Hookshot South Entry to Ranged Crystal']),
        create_dungeon_region(player, 'GT Hookshot South Entry - Ranged Crystal', 'Ganon\'s Tower', None, ['GT HookShot South Entry Ranged Crystal Exit']),
        create_dungeon_region(player, 'GT Map Room', 'Ganon\'s Tower', ['Ganons Tower - Map Chest'], ['GT Map Room WS']),

        create_dungeon_region(player, 'GT Double Switch Entry', 'Ganon\'s Tower', None, ['GT Double Switch NW', 'GT Double Switch Entry to Left Barrier - Orange', 'GT Double Switch Entry to Pot Corners Barrier - Orange', 'GT Double Switch Entry to Ranged Switches']),
        create_dungeon_region(player, 'GT Double Switch Entry - Ranged Switches', 'Ganon\'s Tower', None, ['GT Double Switch Entry Ranged Switches Exit']),
        create_dungeon_region(player, 'GT Double Switch Left', 'Ganon\'s Tower', None, ['GT Double Switch Left to Crystal', 'GT Double Switch Left to Entry Barrier - Orange', 'GT Double Switch Left to Entry Bypass', 'GT Double Switch Left to Pot Corners Bypass', 'GT Double Switch Left to Exit Bypass']),
        create_dungeon_region(player, 'GT Double Switch Left - Crystal', 'Ganon\'s Tower', None, ['GT Double Switch Left Crystal Exit']),
        create_dungeon_region(player, 'GT Double Switch Pot Corners', 'Ganon\'s Tower', ['Ganons Tower - Double Switch Pot Key'], ['GT Double Switch Pot Corners to Entry Barrier - Orange', 'GT Double Switch Pot Corners to Exit Barrier - Blue', 'GT Double Switch Pot Corners to Ranged Switches']),
        create_dungeon_region(player, 'GT Double Switch Pot Corners - Ranged Switches', 'Ganon\'s Tower', None, ['GT Double Switch Pot Corners Ranged Switches Exit']),
        create_dungeon_region(player, 'GT Double Switch Exit', 'Ganon\'s Tower', None, ['GT Double Switch EN', 'GT Double Switch Exit to Blue Barrier']),

        create_dungeon_region(player, 'GT Spike Crystal Left', 'Ganon\'s Tower', None, ['GT Spike Crystals WN', 'GT Spike Crystal Left to Right Barrier - Orange', 'GT Spike Crystal Left to Right Bypass']),
        create_dungeon_region(player, 'GT Spike Crystal Right', 'Ganon\'s Tower', None, ['GT Spike Crystals Warp', 'GT Spike Crystal Right to Left Barrier - Orange']),
        create_dungeon_region(player, 'GT Warp Maze - Left Section', 'Ganon\'s Tower', None, ['GT Warp Maze - Left Section Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Mid Section', 'Ganon\'s Tower', None, ['GT Warp Maze - Mid Section Left Warp', 'GT Warp Maze - Mid Section Right Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Right Section', 'Ganon\'s Tower', None, ['GT Warp Maze - Right Section Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Pit Section', 'Ganon\'s Tower', None, ['GT Warp Maze - Pit Section Warp Spot']),
        create_dungeon_region(player, 'GT Warp Maze - Pit Exit Warp Spot', 'Ganon\'s Tower', None, ['GT Warp Maze - Pit Exit Warp']),
        create_dungeon_region(player, 'GT Warp Maze Exit Section', 'Ganon\'s Tower', None, ['GT Warp Maze (Pits) ES', 'GT Warp Maze Exit Section Warp Spot']),
        create_dungeon_region(player, 'GT Firesnake Room', 'Ganon\'s Tower', None, ['GT Firesnake Room Hook Path']),
        create_dungeon_region(player, 'GT Firesnake Room Ledge', 'Ganon\'s Tower', ['Ganons Tower - Firesnake Room'], ['GT Firesnake Room SW']),
        create_dungeon_region(player, 'GT Warp Maze - Rail Choice', 'Ganon\'s Tower', None, ['GT Warp Maze (Rails) NW', 'GT Warp Maze - Rail Choice Left Warp', 'GT Warp Maze - Rail Choice Right Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Rando Rail', 'Ganon\'s Tower', None, ['GT Warp Maze (Rails) WS', 'GT Warp Maze - Rando Rail Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Main Rails', 'Ganon\'s Tower', None, ['GT Warp Maze - Main Rails Best Warp', 'GT Warp Maze - Main Rails Mid Left Warp', 'GT Warp Maze - Main Rails Mid Right Warp', 'GT Warp Maze - Main Rails Right Top Warp', 'GT Warp Maze - Main Rails Right Mid Warp']),
        create_dungeon_region(player, 'GT Warp Maze - Pot Rail', 'Ganon\'s Tower', None, ['GT Warp Maze - Pot Rail Warp']),
        create_dungeon_region(player, 'GT Petting Zoo', 'Ganon\'s Tower', None, ['GT Petting Zoo SE']),
        create_dungeon_region(player, 'GT Conveyor Star Pits', 'Ganon\'s Tower', ['Ganons Tower - Conveyor Star Pits Pot Key'], ['GT Conveyor Star Pits EN']),
        create_dungeon_region(player, 'GT Hidden Star', 'Ganon\'s Tower', None, ['GT Hidden Star ES', 'GT Hidden Star Warp']),
        create_dungeon_region(player, 'GT DMs Room', 'Ganon\'s Tower', ['Ganons Tower - DMs Room - Top Left', 'Ganons Tower - DMs Room - Top Right',
                                                                        'Ganons Tower - DMs Room - Bottom Left', 'Ganons Tower - DMs Room - Bottom Right'], ['GT DMs Room SW']),
        create_dungeon_region(player, 'GT Falling Bridge', 'Ganon\'s Tower', None, ['GT Falling Bridge WN', 'GT Falling Bridge WS']),
        create_dungeon_region(player, 'GT Randomizer Room', 'Ganon\'s Tower', ['Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right',
                                                                          'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right'], ['GT Randomizer Room ES']),
        create_dungeon_region(player, 'GT Ice Armos', 'Ganon\'s Tower', None, ['GT Ice Armos NE', 'GT Ice Armos WS']),
        create_dungeon_region(player, 'GT Big Key Room', 'Ganon\'s Tower', ['Ganons Tower - Big Key Room - Left',
                                                                            'Ganons Tower - Big Key Room - Right', 'Ganons Tower - Big Key Chest'], ['GT Big Key Room SE']),
        create_dungeon_region(player, 'GT Four Torches', 'Ganon\'s Tower', None, ['GT Four Torches Up Stairs', 'GT Four Torches NW', 'GT Four Torches ES']),
        create_dungeon_region(player, 'GT Fairy Abyss', 'Ganon\'s Tower', None, ['GT Fairy Abyss SW']),
        create_dungeon_region(player, 'GT Crystal Paths', 'Ganon\'s Tower', None, ['GT Crystal Paths Down Stairs', 'GT Crystal Paths SW']),
        create_dungeon_region(player, 'GT Mimics 1', 'Ganon\'s Tower', None, ['GT Mimics 1 NW', 'GT Mimics 1 ES']),
        create_dungeon_region(player, 'GT Mimics 2', 'Ganon\'s Tower', None, ['GT Mimics 2 WS', 'GT Mimics 2 NE']),
        create_dungeon_region(player, 'GT Dash Hall', 'Ganon\'s Tower', None, ['GT Dash Hall SE', 'GT Dash Hall NE']),
        create_dungeon_region(player, 'GT Hidden Spikes', 'Ganon\'s Tower', None, ['GT Hidden Spikes SE', 'GT Hidden Spikes EN']),
        create_dungeon_region(player, 'GT Cannonball Bridge', 'Ganon\'s Tower', None, ['GT Cannonball Bridge WN', 'GT Cannonball Bridge Up Stairs', 'GT Cannonball Bridge SE']),
        create_dungeon_region(player, 'GT Refill', 'Ganon\'s Tower', None, ['GT Refill NE']),
        create_dungeon_region(player, 'GT Gauntlet 1', 'Ganon\'s Tower', None, ['GT Gauntlet 1 Down Stairs', 'GT Gauntlet 1 WN']),
        create_dungeon_region(player, 'GT Gauntlet 2', 'Ganon\'s Tower', None, ['GT Gauntlet 2 EN', 'GT Gauntlet 2 SW']),
        create_dungeon_region(player, 'GT Gauntlet 3', 'Ganon\'s Tower', None, ['GT Gauntlet 3 NW', 'GT Gauntlet 3 SW']),
        create_dungeon_region(player, 'GT Gauntlet 4', 'Ganon\'s Tower', None, ['GT Gauntlet 4 NW', 'GT Gauntlet 4 SW']),
        create_dungeon_region(player, 'GT Gauntlet 5', 'Ganon\'s Tower', None, ['GT Gauntlet 5 NW', 'GT Gauntlet 5 WS']),
        create_dungeon_region(player, 'GT Beam Dash', 'Ganon\'s Tower', None, ['GT Beam Dash ES', 'GT Beam Dash WS']),
        create_dungeon_region(player, 'GT Lanmolas 2', 'Ganon\'s Tower', None, ['GT Lanmolas 2 ES', 'GT Lanmolas 2 NW']),
        create_dungeon_region(player, 'GT Quad Pot', 'Ganon\'s Tower', None, ['GT Quad Pot SW', 'GT Quad Pot Up Stairs']),
        create_dungeon_region(player, 'GT Wizzrobes 1', 'Ganon\'s Tower', None, ['GT Wizzrobes 1 Down Stairs', 'GT Wizzrobes 1 SW']),
        create_dungeon_region(player, 'GT Dashing Bridge', 'Ganon\'s Tower', None, ['GT Dashing Bridge NW', 'GT Dashing Bridge NE']),
        create_dungeon_region(player, 'GT Wizzrobes 2', 'Ganon\'s Tower', None, ['GT Wizzrobes 2 SE', 'GT Wizzrobes 2 NE']),
        create_dungeon_region(player, 'GT Conveyor Bridge', 'Ganon\'s Tower', None, ['GT Conveyor Bridge SE', 'GT Conveyor Bridge EN']),
        create_dungeon_region(player, 'GT Torch Cross', 'Ganon\'s Tower', None, ['GT Torch Cross WN', 'GT Torch Cross ES']),
        create_dungeon_region(player, 'GT Staredown', 'Ganon\'s Tower', None, ['GT Staredown WS', 'GT Staredown Up Ladder']),
        create_dungeon_region(player, 'GT Falling Torches', 'Ganon\'s Tower', None, ['GT Falling Torches Down Ladder', 'GT Falling Torches NE', 'GT Falling Torches Hole']),
        create_dungeon_region(player, 'GT Mini Helmasaur Room', 'Ganon\'s Tower', ['Ganons Tower - Mini Helmasaur Room - Left',
                                                                                   'Ganons Tower - Mini Helmasaur Room - Right', 'Ganons Tower - Mini Helmasaur Key Drop'], ['GT Mini Helmasaur Room SE', 'GT Mini Helmasaur Room WN']),
        create_dungeon_region(player, 'GT Bomb Conveyor', 'Ganon\'s Tower', None, ['GT Bomb Conveyor EN', 'GT Bomb Conveyor SW']),

        create_dungeon_region(player, 'GT Crystal Circles', 'Ganon\'s Tower', None, ['GT Crystal Circles NW', 'GT Crystal Circles SW', 'GT Crystal Circles Barrier - Orange', 'GT Crystal Circles to Ranged Crystal']),
        create_dungeon_region(player, 'GT Crystal Inner Circle', 'Ganon\'s Tower', ['Ganons Tower - Pre-Moldorm Chest'], ['GT Crystal Inner Circle Barrier - Orange']),
        create_dungeon_region(player, 'GT Crystal Circles - Ranged Crystal', 'Ganon\'s Tower', None, ['GT Crystal Circles Ranged Crystal Exit']),
      
        create_dungeon_region(player, 'GT Left Moldorm Ledge', 'Ganon\'s Tower', None, ['GT Left Moldorm Ledge Drop Down', 'GT Left Moldorm Ledge NW']),
        create_dungeon_region(player, 'GT Right Moldorm Ledge', 'Ganon\'s Tower', None, ['GT Right Moldorm Ledge Down Stairs', 'GT Right Moldorm Ledge Drop Down']),
        create_dungeon_region(player, 'GT Moldorm', 'Ganon\'s Tower', None, ['GT Moldorm Hole', 'GT Moldorm Gap']),
        create_dungeon_region(player, 'GT Moldorm Pit', 'Ganon\'s Tower', None, ['GT Moldorm Pit Up Stairs']),
        create_dungeon_region(player, 'GT Validation', 'Ganon\'s Tower', ['Ganons Tower - Validation Chest'], ['GT Validation Block Path']),
        create_dungeon_region(player, 'GT Validation Door', 'Ganon\'s Tower', None, ['GT Validation WS']),
        create_dungeon_region(player, 'GT Frozen Over', 'Ganon\'s Tower', None, ['GT Frozen Over ES', 'GT Frozen Over Up Stairs']),
        create_dungeon_region(player, 'GT Brightly Lit Hall', 'Ganon\'s Tower', None, ['GT Brightly Lit Hall Down Stairs', 'GT Brightly Lit Hall NW']),
        create_dungeon_region(player, 'GT Agahnim 2', 'Ganon\'s Tower', ['Agahnim 2'], ['GT Agahnim 2 SW'])
    ]

    world.initialize_regions()
    world.get_region('Hera Lobby - Crystal', player).crystal_switch = True
    world.get_region('Hera Front - Crystal', player).crystal_switch = True
    world.get_region('Hera Down Stairs Landing - Ranged Crystal', player).crystal_switch = True
    world.get_region('Hera Up Stairs Landing - Ranged Crystal', player).crystal_switch = True
    world.get_region('Hera Back - Ranged Crystal', player).crystal_switch = True
    world.get_region('Hera Basement Cage - Crystal', player).crystal_switch = True
    world.get_region('Hera Tile Room', player).crystal_switch = True  # INTERIOR not accessible (maybe with cane)
    world.get_region('Hera Beetles', player).crystal_switch = True
    world.get_region('Hera Tridorm - Crystal', player).crystal_switch = True
    world.get_region('Hera Startile Wide - Crystal', player).crystal_switch = True
    world.get_region('PoD Arena Main - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Arena Bridge - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Arena Right - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Arena Ledge - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Map Balcony - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Sexy Statue', player).crystal_switch = True
    world.get_region('PoD Bow Statue Left - Crystal', player).crystal_switch = True
    world.get_region('PoD Bow Statue Right - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Dark Pegs Landing - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Dark Pegs Right', player).crystal_switch = True
    world.get_region('PoD Dark Pegs Middle - Ranged Crystal', player).crystal_switch = True
    world.get_region('PoD Dark Pegs Left - Ranged Crystal', player).crystal_switch = True
    world.get_region('Swamp Crystal Switch Inner - Crystal', player).crystal_switch = True
    world.get_region('Swamp Crystal Switch Outer - Ranged Crystal', player).crystal_switch = True
    world.get_region('Thieves Spike Switch', player).crystal_switch = True
    world.get_region('Ice Bomb Drop', player).crystal_switch = True
    world.get_region('Ice Conveyor - Crystal', player).crystal_switch = True
    world.get_region('Ice Refill - Crystal', player).crystal_switch = True
    world.get_region('Mire Fishbone', player).crystal_switch = True
    world.get_region('Mire Conveyor - Crystal', player).crystal_switch = True
    world.get_region('Mire Tall Dark and Roomy - Ranged Crystal', player).crystal_switch = True
    world.get_region('Mire Crystal Top', player).crystal_switch = True
    world.get_region('Mire Falling Foes', player).crystal_switch = True
    world.get_region('TR Chain Chomps Top - Crystal', player).crystal_switch = True
    world.get_region('TR Chain Chomps Bottom - Ranged Crystal', player).crystal_switch = True
    world.get_region('TR Pokey 2 Top - Crystal', player).crystal_switch = True
    world.get_region('TR Pokey 2 Bottom - Ranged Crystal', player).crystal_switch = True
    world.get_region('TR Crystaroller Top - Crystal', player).crystal_switch = True
    world.get_region('TR Crystaroller Bottom - Ranged Crystal', player).crystal_switch = True
    world.get_region('TR Crystaroller Middle - Ranged Crystal', player).crystal_switch = True
    world.get_region('TR Crystal Maze Start - Crystal', player).crystal_switch = True
    world.get_region('TR Crystal Maze Interior', player).crystal_switch = True
    world.get_region('TR Crystal Maze End - Ranged Crystal', player).crystal_switch = True
    world.get_region('GT Crystal Conveyor - Ranged Crystal', player).crystal_switch = True
    world.get_region('GT Crystal Conveyor Corner - Ranged Crystal', player).crystal_switch = True
    world.get_region('GT Hookshot South Platform', player).crystal_switch = True
    world.get_region('GT Hookshot South Entry - Ranged Crystal', player).crystal_switch = True
    world.get_region('GT Double Switch Left - Crystal', player).crystal_switch = True
    world.get_region('GT Double Switch Entry - Ranged Switches', player).crystal_switch = True
    world.get_region('GT Double Switch Pot Corners - Ranged Switches', player).crystal_switch = True
    world.get_region('GT Spike Crystal Left', player).crystal_switch = True
    world.get_region('GT Crystal Paths', player).crystal_switch = True
    world.get_region('GT Hidden Spikes', player).crystal_switch = True
    world.get_region('GT Crystal Inner Circle', player).crystal_switch = True
    world.get_region('GT Crystal Circles - Ranged Crystal', player).crystal_switch = True

def create_menu_region(player, name, locations=None, exits=None):
    return _create_region(player, name, RegionType.Menu, 'Menu', locations, exits)


def create_lw_region(player, name, locations=None, exits=None, hint='Light World', terrain=Terrain.Land):
    region = _create_region(player, name, RegionType.LightWorld, hint, locations, exits)
    region.terrain = terrain
    return region


def create_dw_region(player, name, locations=None, exits=None, hint='Dark World', terrain=Terrain.Land):
    region = _create_region(player, name, RegionType.DarkWorld, hint, locations, exits)
    region.terrain = terrain
    return region


def create_cave_region(player, name, hint='Hyrule', locations=None, exits=None):
    return _create_region(player, name, RegionType.Cave, hint, locations, exits)


def create_dungeon_region(player, name, hint='Hyrule', locations=None, exits=None):
    return _create_region(player, name, RegionType.Dungeon, hint, locations, exits)

def _create_region(player, name, type, hint='Hyrule', locations=None, exits=None):
    ret = Region(name, type, hint, player)
    if locations is None:
        locations = []
    if exits is None:
        exits = []

    for exit in exits:
        ret.exits.append(Entrance(player, exit, ret))
    for location in locations:
        if location in key_drop_data:
            ko_hint = key_drop_data[location][2]
            ret.locations.append(Location(player, location, None, False, ko_hint, ret, key_drop_data[location][3]))
        else:
            address, player_address, prize, hint_text = location_table[location]
            ret.locations.append(Location(player, location, address, prize, hint_text, ret, None, player_address))
    return ret

def mark_light_dark_world_regions(world, player):
    # cross world caves may have some sections marked as both in_light_world, and in_dark_work.
    # That is ok. the bunny logic will check for this case and incorporate special rules.
    queue = collections.deque(region for region in world.get_regions(player) if region.type == RegionType.LightWorld)
    seen = set(queue)
    while queue:
        current = queue.popleft()
        current.is_light_world = True
        for exit in current.exits:
            if exit.connected_region is None or exit.connected_region.type == RegionType.DarkWorld:
                # Don't venture into the dark world
                continue
            if exit.connected_region not in seen:
                seen.add(exit.connected_region)
                queue.append(exit.connected_region)

    queue = collections.deque(region for region in world.get_regions(player) if region.type == RegionType.DarkWorld)
    seen = set(queue)
    while queue:
        current = queue.popleft()
        current.is_dark_world = True
        for exit in current.exits:
            if exit.connected_region is None or exit.connected_region.type == RegionType.LightWorld:
                # Don't venture into the light world
                continue
            if exit.connected_region not in seen:
                seen.add(exit.connected_region)
                queue.append(exit.connected_region)


def create_shops(world, player):
    world.shops[player] = []
    for region_name, (room_id, type, shopkeeper, custom, locked, inventory, sram) in shop_table.items():
        if world.mode[player] == 'inverted':
            if (not world.is_tile_swapped(0x35, player) and region_name == 'Dark Lake Hylia Shop') \
                    or (not world.is_tile_swapped(0x35, player) and region_name == 'Lake Hylia Shop'):
                locked = True
                inventory = [('Blue Potion', 160), ('Blue Shield', 50), ('Bombs (10)', 50)]
                custom = True
        region = world.get_region(region_name, player)
        shop = Shop(region, room_id, type, shopkeeper, custom, locked, sram)
        region.shop = shop
        world.shops[player].append(shop)
        for index, item in enumerate(inventory):
            shop.add_inventory(index, *item)
        if not world.shopsanity[player]:
            if region_name in shop_to_location_table.keys():
                for index, location in enumerate(shop_to_location_table[region_name]):
                    loc = world.get_location(location, player)
                    loc.skip = True
                    loc.forced_item = loc.item = ItemFactory(shop.inventory[index]['item'], player)
                    loc.item.location = loc


def adjust_locations(world, player):
    # handle pots
    world.data_tables[player].pot_secret_table = PotSecretTable()
    for location, datum in key_drop_data.items():
        loc = world.get_location(location, player)
        drop_location = 'Drop' == datum[0]
        if drop_location:
            loc.type = LocationType.Drop
            snes_address, room, sprite_idx = datum[1]
            loc.address = snes_address
            sprite = world.data_tables[player].uw_enemy_table.room_map[room][sprite_idx]
            sprite.location = loc
            if world.enemy_shuffle[player] != 'none':
                loc.note = enemy_names[sprite.kind]
        else:
            loc.type = LocationType.Pot
            pot, pot_index = next((p, i) for i, p in enumerate(vanilla_pots[datum[1]]) if p.item == PotItem.Key)
            pot = pot.copy()
            loc.address = pot_address(pot_index, datum[1])
            loc.pot = pot
            pot.location = loc
        if ((world.dropshuffle[player] == 'none' and drop_location)
           or (not drop_location and world.pottery[player] in ['none', 'cave'])):
            loc.skip = True
        else:
            key_item = loc.item
            key_item.location = None
            loc.forced_item = None
            loc.item = None
            loc.event = False
            item_dungeon = key_item.dungeon
            dungeon = world.get_dungeon(item_dungeon, player)
            if key_item.smallkey and world.keyshuffle[player] != 'universal':
                dungeon.small_keys.append(key_item)
            elif key_item.bigkey:
                dungeon.big_key = key_item
    world.pot_pool[player] = choose_pots(world, player)
    for super_tile, pot_list in vanilla_pots.items():
        for pot_index, pot_orig in enumerate(pot_list):
            if pot_orig.item == PotItem.Key:
                loc = next(location for location, datum in key_drop_data.items() if datum[1] == super_tile)
                pot = world.get_location(loc, player).pot
            else:
                pot = pot_orig.copy()
            world.data_tables[player].pot_secret_table.room_map[super_tile].append(pot)

            if valid_pot_location(pot, world.pot_pool[player], world, player):
                create_pot_location(pot, pot_index, super_tile, world, player)
    if world.shopsanity[player]:
        index = 0
        for shop, location_list in shop_to_location_table.items():
            for location in location_list:
                loc = world.get_location(location, player)
                loc.address = 0x400000 + index
                loc.type = LocationType.Shop
                # player address? it is in the shop table
                index += 1
    setup_enemy_locations(world, player)
    # disable forced prize locations
    if world.prizeshuffle[player] != 'none':
        for l in [name for name, data in location_table.items() if data[2]]:
            location = world.get_location_unsafe(l, player)
            if location:
                location.prize = False
    # unreal events:
    for l in ['Ganon', 'Zelda Pickup', 'Zelda Drop Off'] + list(location_events):
        location = world.get_location_unsafe(l, player)
        if location:
            location.type = LocationType.Logical
            location.real = False
            if l not in ['Ganon', 'Agahnim 1', 'Agahnim 2']:
                location.skip = True


def valid_pot_location(pot, pot_set, world, player):
    if world.pottery[player] == 'lottery':
        return True
    if world.pottery[player] == 'nonempty' and pot.item != PotItem.Nothing:
        return True
    if world.pottery[player] in ['reduced', 'clustered'] and pot in pot_set:
        return True
    if world.pottery[player] == 'dungeon' and world.get_region(pot.room, player).type == RegionType.Dungeon:
        return True
    if world.pottery[player] in ['cave', 'cavekeys'] and world.get_region(pot.room, player).type == RegionType.Cave:
        return True
    return False


def create_pot_location(pot, pot_index, super_tile, world, player):
    if (pot.item not in [PotItem.Key, PotItem.Hole]
       and (pot.item != PotItem.Switch or (world.potshuffle[player]
                                           and world.pottery[player] not in ['none', 'cave', 'keys', 'cavekeys']))):
        address = pot_address(pot_index, super_tile)
        region = pot.room
        parent = world.get_region(region, player)
        descriptor = 'Large Block' if pot.flags & PotFlags.Block else f'Pot #{pot_index+1}'
        hint_text = ('under a block' if pot.flags & PotFlags.Block else 'in a pot')
        modifier = parent.hint_text not in {'a storyteller', 'fairies deep in a cave', 'a spiky hint',
                                            'a bounty of five items', 'the sick kid', 'Sahasrahla'}
        hint_text = f'{hint_text} {"in" if modifier else "near"} {parent.hint_text}'
        pot_location = Location(player, f'{pot.room} {descriptor}', address, hint_text=hint_text,
                                parent=parent)
        world.dynamic_locations.append(pot_location)
        pot_location.pot = pot
        pot.location = pot_location

        pot_location.type = LocationType.Pot
        parent.locations.append(pot_location)


def pot_address(pot_index, super_tile):
    return 0x7f6018 + super_tile * 2 + (pot_index << 24)


# bonk location: record id, OW flag bitmask, aga required, default item, region, hint text
bonk_prize_table = {
    'Lost Woods Hideout Tree':          (0x00, 0x10, False, '', 'Lost Woods East Area',           'in a tree'),
    'Death Mountain Bonk Rocks':        (0x01, 0x10, False, '', 'East Death Mountain (Top East)', 'encased in stone'),
    'Mountain Pass Pull Tree':          (0x02, 0x10, False, '', 'Mountain Pass Area',             'in a tree'),
    'Mountain Pass Southeast Tree':     (0x03, 0x08, False, '', 'Mountain Pass Area',             'in a tree'),
    'Lost Woods Pass West Tree':        (0x04, 0x10, False, '', 'Lost Woods Pass West Area',      'in a tree'),
    'Kakariko Portal Tree':             (0x05, 0x08, False, '', 'Lost Woods Pass East Top Area',  'in a tree'),
    'Fortune Bonk Rocks':               (0x06, 0x10, False, '', 'Kakariko Fortune Area',          'encased in stone'),
    'Kakariko Pond Tree':               (0x07, 0x10, True,  '', 'Kakariko Pond Area',             'in a tree'),
    'Bonk Rocks Tree':                  (0x08, 0x10, True,  '', 'Bonk Rock Ledge',                'in a tree'),
    'Sanctuary Tree':                   (0x09, 0x08, False, '', 'Sanctuary Area',                 'in a tree'),
    'River Bend West Tree':             (0x0a, 0x10, True,  '', 'River Bend Area',                'in a tree'),
    'River Bend East Tree':             (0x0b, 0x08, False, '', 'River Bend East Bank',           'in a tree'),
    'Blinds Hideout Tree':              (0x0c, 0x10, False, '', 'Kakariko Village',               'in a tree'),
    'Kakariko Welcome Tree':            (0x0d, 0x08, False, '', 'Kakariko Village',               'in a tree'),
    'Forgotten Forest Southwest Tree':  (0x0e, 0x10, False, '', 'Forgotten Forest Area',          'in a tree'),
    'Forgotten Forest Central Tree':    (0x0f, 0x08, False, '', 'Forgotten Forest Area',          'in a tree'),
    #'Forgotten Forest Southeast Tree':  (0x10, 0x04, False, '', 'Forgotten Forest Area',          'in a tree'),
    'Hyrule Castle Tree':               (0x10, 0x10, False, '', 'Hyrule Castle Courtyard',        'in a tree'),
    'Wooden Bridge Tree':               (0x11, 0x10, False, '', 'Wooden Bridge Area',             'in a tree'),
    'Eastern Palace Tree':              (0x12, 0x10, True,  '', 'Eastern Palace Area',            'in a tree'),
    'Flute Boy South Tree':             (0x13, 0x10, True,  '', 'Flute Boy Area',                 'in a tree'),
    'Flute Boy East Tree':              (0x14, 0x08, True,  '', 'Flute Boy Area',                 'in a tree'),
    'Central Bonk Rocks Tree':          (0x15, 0x10, False, '', 'Central Bonk Rocks Area',        'in a tree'),
    'Tree Line Tree 2':                 (0x16, 0x10, True,  '', 'Tree Line Area',                 'in a tree'),
    'Tree Line Tree 4':                 (0x17, 0x08, True,  '', 'Tree Line Area',                 'in a tree'),
    'Flute Boy Approach South Tree':    (0x18, 0x10, False, '', 'Flute Boy Approach Area',        'in a tree'),
    'Flute Boy Approach North Tree':    (0x19, 0x08, False, '', 'Flute Boy Approach Area',        'in a tree'),
    'Dark Lumberjack Tree':             (0x1a, 0x10, False, '', 'Dark Lumberjack Area',           'in a tree'),
    'Dark Fortune Bonk Rocks (Drop 1)': (0x1b, 0x10, False, '', 'Dark Fortune Area',              'encased in stone'),
    'Dark Fortune Bonk Rocks (Drop 2)': (0x1c, 0x08, False, '', 'Dark Fortune Area',              'encased in stone'),
    'Dark Graveyard West Bonk Rocks':   (0x1d, 0x10, False, '', 'Dark Graveyard Area',            'encased in stone'),
    'Dark Graveyard North Bonk Rocks':  (0x1e, 0x08, False, '', 'Dark Graveyard North',           'encased in stone'),
    'Dark Graveyard Tomb Bonk Rocks':   (0x1f, 0x04, False, '', 'Dark Graveyard North',           'encased in stone'),
    'Qirn Jump West Tree':              (0x20, 0x10, False, '', 'Qirn Jump Area',                 'in a tree'),
    'Qirn Jump East Tree':              (0x21, 0x08, False, '', 'Qirn Jump East Bank',            'in a tree'),
    'Dark Witch Tree':                  (0x22, 0x10, False, '', 'Dark Witch Area',                'in a tree'),
    'Pyramid Tree':                     (0x23, 0x10, False, '', 'Pyramid Area',                   'in a tree'),
    'Palace of Darkness Tree':          (0x24, 0x10, False, '', 'Palace of Darkness Area',        'in a tree'),
    'Dark Tree Line Tree 2':            (0x25, 0x10, False, '', 'Dark Tree Line Area',            'in a tree'),
    'Dark Tree Line Tree 3':            (0x26, 0x08, False, '', 'Dark Tree Line Area',            'in a tree'),
    'Dark Tree Line Tree 4':            (0x27, 0x04, False, '', 'Dark Tree Line Area',            'in a tree'),
    'Hype Cave Statue':                 (0x28, 0x10, False, '', 'Hype Cave Area',                 'encased in stone'),
    'Cold Fairy Statue':                (0x29, 0x02, False, '', 'Good Bee Cave (back)',           'encased in stone')
}

bonk_table_by_location_id = {0x2ABB00+(data[0]*6)+3: name for name, data in bonk_prize_table.items()}
bonk_table_by_location = {y: x for x, y in bonk_table_by_location_id.items()}


# (room_id, type, shopkeeper, custom, locked, [items])
# item = (item, price, max=0, replacement=None, replacement_price=0)
_basic_shop_defaults = [('Red Potion', 150), ('Small Heart', 10), ('Bombs (10)', 50)]
_dark_world_shop_defaults = [('Red Potion', 150), ('Blue Shield', 50), ('Bombs (10)', 50)]
shop_table = {
    'Dark Death Mountain Shop': (0x0112, ShopType.Shop, 0xC1, False, False, _basic_shop_defaults, 0),
    'Red Shield Shop': (0x0110, ShopType.Shop, 0xC1, False, False,
                        [('Red Shield', 500), ('Bee', 10), ('Arrows (10)', 30)], 3),
    'Dark Lake Hylia Shop': (0x010F, ShopType.Shop, 0xC1, False, False, _dark_world_shop_defaults, 6),
    'Dark Lumberjack Shop': (0x010F, ShopType.Shop, 0xC1, False, False, _dark_world_shop_defaults, 9),
    'Village of Outcasts Shop': (0x010F, ShopType.Shop, 0xC1, False, False, _dark_world_shop_defaults, 12),
    'Dark Potion Shop': (0x010F, ShopType.Shop, 0xC1, False, False, _dark_world_shop_defaults, 15),
    'Paradox Shop': (0x00FF, ShopType.Shop, 0xA0, False, False, _basic_shop_defaults, 18),
    'Kakariko Shop': (0x011F, ShopType.Shop, 0xA0, False, False, _basic_shop_defaults, 21),
    'Lake Hylia Shop': (0x0112, ShopType.Shop, 0xA0, False, False, _basic_shop_defaults, 24),
    'Potion Shop': (0x0109, ShopType.Shop, 0xFF, False, True,
                    [('Red Potion', 120), ('Green Potion', 60), ('Blue Potion', 160)], 27),
    'Capacity Upgrade': (0x0115, ShopType.UpgradeShop, 0x04, True, True,
                         [('Bomb Upgrade (+5)', 100, 7), ('Arrow Upgrade (+5)', 100, 7)], 30)
}


shop_to_location_table = {
    'Dark Death Mountain Shop': ['Dark Death Mountain Shop - Left', 'Dark Death Mountain Shop - Middle', 'Dark Death Mountain Shop - Right'],
    'Red Shield Shop': ['Red Shield Shop - Left', 'Red Shield Shop - Middle', 'Red Shield Shop - Right'],
    'Dark Lake Hylia Shop': ['Dark Lake Hylia Shop - Left', 'Dark Lake Hylia Shop - Middle', 'Dark Lake Hylia Shop - Right'],
    'Dark Lumberjack Shop': ['Dark Lumberjack Shop - Left', 'Dark Lumberjack Shop - Middle', 'Dark Lumberjack Shop - Right'],
    'Village of Outcasts Shop': ['Village of Outcasts Shop - Left', 'Village of Outcasts Shop - Middle', 'Village of Outcasts Shop - Right'],
    'Dark Potion Shop': ['Dark Potion Shop - Left', 'Dark Potion Shop - Middle', 'Dark Potion Shop - Right'],
    'Paradox Shop': ['Paradox Shop - Left', 'Paradox Shop - Middle', 'Paradox Shop - Right'],
    'Kakariko Shop': ['Kakariko Shop - Left', 'Kakariko Shop - Middle', 'Kakariko Shop - Right'],
    'Lake Hylia Shop': ['Lake Hylia Shop - Left', 'Lake Hylia Shop - Middle', 'Lake Hylia Shop - Right'],
    'Potion Shop': ['Potion Shop - Left', 'Potion Shop - Middle', 'Potion Shop - Right'],
    'Capacity Upgrade': ['Capacity Upgrade - Left', 'Capacity Upgrade - Right'],
}

retro_shops = {
    'Old Man Sword Cave': ['Old Man Sword Cave Item 1'],
    'Take-Any #1': ['Take-Any #1 Item 1', 'Take-Any #1 Item 2'],
    'Take-Any #2': ['Take-Any #2 Item 1', 'Take-Any #2 Item 2'],
    'Take-Any #3': ['Take-Any #3 Item 1', 'Take-Any #3 Item 2'],
    'Take-Any #4': ['Take-Any #4 Item 1', 'Take-Any #4 Item 2'],
}

flat_normal_shops = [loc_name for name, location_list in shop_to_location_table.items() for loc_name in location_list]
flat_retro_shops = [loc_name for name, location_list in retro_shops.items() for loc_name in location_list]
shop_table_by_location_id = {0x400000+cnt: x for cnt, x in enumerate(flat_normal_shops)}
shop_table_by_location_id = {**shop_table_by_location_id, **{0x400020+cnt: x for cnt, x in enumerate(flat_retro_shops)}}
shop_table_by_location = {y: x for x, y in shop_table_by_location_id.items()}


location_events = {
    'Agahnim 1': 'Beat Agahnim 1',
    'Agahnim 2': 'Beat Agahnim 2',
    'Eastern Palace - Boss Kill': 'Beat Boss',
    'Desert Palace - Boss Kill': 'Beat Boss',
    'Tower of Hera - Boss Kill': 'Beat Boss',
    'Palace of Darkness - Boss Kill': 'Beat Boss',
    'Swamp Palace - Boss Kill': 'Beat Boss',
    'Skull Woods - Boss Kill': 'Beat Boss',
    'Thieves\' Town - Boss Kill': 'Beat Boss',
    'Ice Palace - Boss Kill': 'Beat Boss',
    'Misery Mire - Boss Kill': 'Beat Boss',
    'Turtle Rock - Boss Kill': 'Beat Boss',
    'Lost Old Man': 'Escort Old Man',
    'Old Man Drop Off': 'Return Old Man',
    'Floodgate': 'Open Floodgate',
    'Big Bomb': 'Pick Up Big Bomb',
    'Pyramid Crack': 'Detonate Big Bomb',
    'Frog': 'Get Frog',
    'Missing Smith': 'Return Smith',
    'Dark Blacksmith Ruins': 'Pick Up Purple Chest',
    'Middle Aged Man': 'Deliver Purple Chest',
    'Trench 1 Switch': 'Trench 1 Filled',
    'Trench 2 Switch': 'Trench 2 Filled',
    'Swamp Drain': 'Drained Swamp',
    'Turtle Medallion Pad': 'Turtle Opened',
    'Attic Cracked Floor': 'Shining Light',
    'Suspicious Maiden': 'Maiden Rescued',
    'Revealing Light': 'Maiden Unmasked',
    'Ice Block Drop': 'Convenient Block',
    'Skull Star Tile': 'Hidden Pits',
    'Zelda Pickup': None,
    'Zelda Drop Off': None
}


flooded_keys_reverse = {
    'Swamp Palace - Trench 1 Pot Key': 'Trench 1 Switch',
    'Swamp Palace - Trench 2 Pot Key': 'Trench 2 Switch'
}


location_table = {'Mushroom': (0x180013, 0x186df8, False, 'in the woods'),
                  'Bottle Merchant': (0x2eb18, 0x186df9, False, 'with a merchant'),
                  'Flute Spot': (0x18014a, 0x186dfd, False, 'underground'),
                  'Sunken Treasure': (0x180145, 0x186e14, False, 'underwater'),
                  'Purple Chest': (0x33d68, 0x186e19, False, 'from a box'),
                  "Blind's Hideout - Top": (0xeb0f, 0x186da3, False, 'in a basement'),
                  "Blind's Hideout - Left": (0xeb12, 0x186da6, False, 'in a basement'),
                  "Blind's Hideout - Right": (0xeb15, 0x186da9, False, 'in a basement'),
                  "Blind's Hideout - Far Left": (0xeb18, 0x186dac, False, 'in a basement'),
                  "Blind's Hideout - Far Right": (0xeb1b, 0x186daf, False, 'in a basement'),
                  "Link's Uncle": (0x2df45, 0x186e1f, False, 'with your uncle'),
                  'Secret Passage': (0xe971, 0x186c05, False, 'near your uncle'),
                  'King Zora': (0xee1c3, 0x186e20, False, 'at a high price'),
                  "Zora's Ledge": (0x180149, 0x186e18, False, 'near Zora'),
                  'Waterfall Fairy - Left': (0xe9b0, 0x186c44, False, 'near a fairy'),
                  'Waterfall Fairy - Right': (0xe9d1, 0x186c65, False, 'near a fairy'),
                  "King's Tomb": (0xe97a, 0x186c0e, False, 'alone in a cave'),
                  'Floodgate Chest': (0xe98c, 0x186c20, False, 'in the dam'),
                  "Link's House": (0xe9bc, 0x186c50, False, 'in your home'),
                  'Kakariko Tavern': (0xe9ce, 0x186c62, False, 'in the bar'),
                  'Chicken House': (0xe9e9, 0x186c7d, False, 'near poultry'),
                  "Aginah's Cave": (0xe9f2, 0x186c86, False, 'with Aginah'),
                  "Sahasrahla's Hut - Left": (0xea82, 0x186d16, False, 'near the elder'),
                  "Sahasrahla's Hut - Middle": (0xea85, 0x186d19, False, 'near the elder'),
                  "Sahasrahla's Hut - Right": (0xea88, 0x186d1c, False, 'near the elder'),
                  'Sahasrahla': (0x2f1fc, 0x186e25, False, 'with the elder'),
                  'Kakariko Well - Top': (0xea8e, 0x186d22, False, 'in a well'),
                  'Kakariko Well - Left': (0xea91, 0x186d25, False, 'in a well'),
                  'Kakariko Well - Middle': (0xea94, 0x186d28, False, 'in a well'),
                  'Kakariko Well - Right': (0xea97, 0x186d2b, False, 'in a well'),
                  'Kakariko Well - Bottom': (0xea9a, 0x186d2e, False, 'in a well'),
                  'Blacksmith': (0x18002a, 0x186e26, False, 'with the smith'),
                  'Magic Bat': (0x180015, 0x186e1e, False, 'with the bat'),
                  'Sick Kid': (0x339cf, 0x186e27, False, 'with the sick'),
                  'Hobo': (0x33e7d, 0x186e28, False, 'with the hobo'),
                  'Lost Woods Hideout': (0x180000, 0x186e08, False, 'near a thief'),
                  'Lumberjack Tree': (0x180001, 0x186e09, False, 'in a hole'),
                  'Cave 45': (0x180003, 0x186e0b, False, 'alone in a cave'),
                  'Graveyard Cave': (0x180004, 0x186e0c, False, 'alone in a cave'),
                  'Checkerboard Cave': (0x180005, 0x186e0d, False, 'alone in a cave'),
                  'Mini Moldorm Cave - Far Left': (0xeb42, 0x186dd6, False, 'near Moldorms'),
                  'Mini Moldorm Cave - Left': (0xeb45, 0x186dd9, False, 'near Moldorms'),
                  'Mini Moldorm Cave - Right': (0xeb48, 0x186ddc, False, 'near Moldorms'),
                  'Mini Moldorm Cave - Far Right': (0xeb4b, 0x186ddf, False, 'near Moldorms'),
                  'Mini Moldorm Cave - Generous Guy': (0x180010, 0x186e1a, False, 'near Moldorms'),
                  'Ice Rod Cave': (0xeb4e, 0x186de2, False, 'in a frozen cave'),
                  'Bonk Rock Cave': (0xeb3f, 0x186dd3, False, 'alone in a cave'),
                  'Library': (0x180012, 0x186e1c, False, 'near books'),
                  'Potion Shop': (0x180014, 0x186e1d, False, 'near potions'),
                  'Lake Hylia Island': (0x180144, 0x186e13, False, 'on an island'),
                  'Maze Race': (0x180142, 0x186e11, False, 'at the race'),
                  'Desert Ledge': (0x180143, 0x186e12, False, 'in the desert'),
                  'Desert Palace - Big Chest': (0xe98f, 0x186c23, False, 'in Desert Palace'),
                  'Desert Palace - Torch': (0x180160, 0x186e22, False, 'in Desert Palace'),
                  'Desert Palace - Map Chest': (0xe9b6, 0x186c4a, False, 'in Desert Palace'),
                  'Desert Palace - Compass Chest': (0xe9cb, 0x186c5f, False, 'in Desert Palace'),
                  'Desert Palace - Big Key Chest': (0xe9c2, 0x186c56, False, 'in Desert Palace'),
                  'Desert Palace - Boss': (0x180151, 0x186dff, False, 'with Lanmolas'),
                  'Eastern Palace - Compass Chest': (0xe977, 0x186c0b, False, 'in Eastern Palace'),
                  'Eastern Palace - Big Chest': (0xe97d, 0x186c11, False, 'in Eastern Palace'),
                  'Eastern Palace - Cannonball Chest': (0xe9b3, 0x186c47, False, 'in Eastern Palace'),
                  'Eastern Palace - Big Key Chest': (0xe9b9, 0x186c4d, False, 'in Eastern Palace'),
                  'Eastern Palace - Map Chest': (0xe9f5, 0x186c89, False, 'in Eastern Palace'),
                  'Eastern Palace - Boss': (0x180150, 0x186dfe, False, 'with the Armos'),
                  'Master Sword Pedestal': (0x289b0, 0x186e29, False, 'at the pedestal'),
                  'Hyrule Castle - Boomerang Chest': (0xe974, 0x186c08, False, 'in Hyrule Castle'),
                  'Hyrule Castle - Map Chest': (0xeb0c, 0x186da0, False, 'in Hyrule Castle'),
                  "Hyrule Castle - Zelda's Chest": (0xeb09, 0x186d9d, False, 'in Hyrule Castle'),
                  'Sewers - Dark Cross': (0xe96e, 0x186c02, False, 'in the sewers'),
                  'Sewers - Secret Room - Left': (0xeb5d, 0x186df1, False, 'in the sewers'),
                  'Sewers - Secret Room - Middle': (0xeb60, 0x186df4, False, 'in the sewers'),
                  'Sewers - Secret Room - Right': (0xeb63, 0x186df7, False, 'in the sewers'),
                  'Sanctuary': (0xea79, 0x186d0d, False, 'in Sanctuary'),
                  'Castle Tower - Room 03': (0xeab5, 0x186d49, False, 'in Castle Tower'),
                  'Castle Tower - Dark Maze': (0xeab2, 0x186d46, False, 'in Castle Tower'),
                  'Old Man': (0xf69fa, 0x186e24, False, 'with the old man'),
                  'Spectacle Rock Cave': (0x180002, 0x186e0a, False, 'alone in a cave'),
                  'Paradox Cave Lower - Far Left': (0xeb2a, 0x186dbe, False, 'in a cave with seven chests'),
                  'Paradox Cave Lower - Left': (0xeb2d, 0x186dc1, False, 'in a cave with seven chests'),
                  'Paradox Cave Lower - Right': (0xeb30, 0x186dc4, False, 'in a cave with seven chests'),
                  'Paradox Cave Lower - Far Right': (0xeb33, 0x186dc7, False, 'in a cave with seven chests'),
                  'Paradox Cave Lower - Middle': (0xeb36, 0x186dca, False, 'in a cave with seven chests'),
                  'Paradox Cave Upper - Left': (0xeb39, 0x186dcd, False, 'in a cave with seven chests'),
                  'Paradox Cave Upper - Right': (0xeb3c, 0x186dd0, False, 'in a cave with seven chests'),
                  'Spiral Cave': (0xe9bf, 0x186c53, False, 'in Spiral Cave'),
                  'Ether Tablet': (0x180016, 0x186dfb, False, 'at a monolith'),
                  'Spectacle Rock': (0x180140, 0x186e0f, False, 'atop a rock'),
                  'Tower of Hera - Basement Cage': (0x180162, 0x186dfa, False, 'in Tower of Hera'),
                  'Tower of Hera - Map Chest': (0xe9ad, 0x186c41, False, 'in Tower of Hera'),
                  'Tower of Hera - Big Key Chest': (0xe9e6, 0x186c7a, False, 'in Tower of Hera'),
                  'Tower of Hera - Compass Chest': (0xe9fb, 0x186c8f, False, 'in Tower of Hera'),
                  'Tower of Hera - Big Chest': (0xe9f8, 0x186c8c, False, 'in Tower of Hera'),
                  'Tower of Hera - Boss': (0x180152, 0x186e00, False, 'with Moldorm'),
                  'Pyramid': (0x180147, 0x186e16, False, 'on the Pyramid'),
                  'Catfish': (0xee185, 0x186e21, False, 'with a catfish'),
                  'Stumpy': (0x330c7, 0x186e2a, False, 'with tree boy'),
                  'Digging Game': (0x180148, 0x186e17, False, 'underground'),
                  'Bombos Tablet': (0x180017, 0x186dfc, False, 'at a monolith'),
                  'Hype Cave - Top': (0xeb1e, 0x186db2, False, 'near a bat-like man'),
                  'Hype Cave - Middle Right': (0xeb21, 0x186db5, False, 'near a bat-like man'),
                  'Hype Cave - Middle Left': (0xeb24, 0x186db8, False, 'near a bat-like man'),
                  'Hype Cave - Bottom': (0xeb27, 0x186dbb, False, 'near a bat-like man'),
                  'Hype Cave - Generous Guy': (0x180011, 0x186e1b, False, 'with a bat-like man'),
                  'Peg Cave': (0x180006, 0x186e0e, False, 'alone in a cave'),
                  'Pyramid Fairy - Left': (0xe980, 0x186c14, False, 'near a fairy'),
                  'Pyramid Fairy - Right': (0xe983, 0x186c17, False, 'near a fairy'),
                  'Brewery': (0xe9ec, 0x186c80, False, 'alone in a home'),
                  'C-Shaped House': (0xe9ef, 0x186c83, False, 'alone in a home'),
                  'Chest Game': (0xeda8, 0x186e2b, False, 'as a game reward'),
                  'Bumper Cave Ledge': (0x180146, 0x186e15, False, 'on a ledge'),
                  'Mire Shed - Left': (0xea73, 0x186d07, False, 'near sparks'),
                  'Mire Shed - Right': (0xea76, 0x186d0a, False, 'near sparks'),
                  'Superbunny Cave - Top': (0xea7c, 0x186d10, False, 'in a connection'),
                  'Superbunny Cave - Bottom': (0xea7f, 0x186d13, False, 'in a connection'),
                  'Spike Cave': (0xea8b, 0x186d1f, False, 'beyond spikes'),
                  'Hookshot Cave - Top Right': (0xeb51, 0x186de5, False, 'across pits'),
                  'Hookshot Cave - Top Left': (0xeb54, 0x186de8, False, 'across pits'),
                  'Hookshot Cave - Bottom Right': (0xeb5a, 0x186dee, False, 'across pits'),
                  'Hookshot Cave - Bottom Left': (0xeb57, 0x186deb, False, 'across pits'),
                  'Floating Island': (0x180141, 0x186e10, False, 'on an island'),
                  'Mimic Cave': (0xe9c5, 0x186c59, False, 'in a cave of mimicry'),
                  'Swamp Palace - Entrance': (0xea9d, 0x186d31, False, 'in Swamp Palace'),
                  'Swamp Palace - Map Chest': (0xe986, 0x186c1a, False, 'in Swamp Palace'),
                  'Swamp Palace - Big Chest': (0xe989, 0x186c1d, False, 'in Swamp Palace'),
                  'Swamp Palace - Compass Chest': (0xeaa0, 0x186d34, False, 'in Swamp Palace'),
                  'Swamp Palace - Big Key Chest': (0xeaa6, 0x186d3a, False, 'in Swamp Palace'),
                  'Swamp Palace - West Chest': (0xeaa3, 0x186d37, False, 'in Swamp Palace'),
                  'Swamp Palace - Flooded Room - Left': (0xeaa9, 0x186d3d, False, 'in Swamp Palace'),
                  'Swamp Palace - Flooded Room - Right': (0xeaac, 0x186d40, False, 'in Swamp Palace'),
                  'Swamp Palace - Waterfall Room': (0xeaaf, 0x186d43, False, 'in Swamp Palace'),
                  'Swamp Palace - Boss': (0x180154, 0x186e02, False, 'with Arrghus'),
                  "Thieves' Town - Big Key Chest": (0xea04, 0x186c98, False, "in Thieves Town"),
                  "Thieves' Town - Map Chest": (0xea01, 0x186c95, False, "in Thieves Town"),
                  "Thieves' Town - Compass Chest": (0xea07, 0x186c9b, False, "in Thieves Town"),
                  "Thieves' Town - Ambush Chest": (0xea0a, 0x186c9e, False, "in Thieves Town"),
                  "Thieves' Town - Attic": (0xea0d, 0x186ca1, False, "in Thieves Town"),
                  "Thieves' Town - Big Chest": (0xea10, 0x186ca4, False, "in Thieves Town"),
                  "Thieves' Town - Blind's Cell": (0xea13, 0x186ca7, False, "in Thieves Town"),
                  "Thieves' Town - Boss": (0x180156, 0x186e04, False, 'with Blind'),
                  'Skull Woods - Compass Chest': (0xe992, 0x186c26, False, 'in Skull Woods'),
                  'Skull Woods - Map Chest': (0xe99b, 0x186c2f, False, 'in Skull Woods'),
                  'Skull Woods - Big Chest': (0xe998, 0x186c2c, False, 'in Skull Woods'),
                  'Skull Woods - Pot Prison': (0xe9a1, 0x186c35, False, 'in Skull Woods'),
                  'Skull Woods - Pinball Room': (0xe9c8, 0x186c5c, False, 'in Skull Woods'),
                  'Skull Woods - Big Key Chest': (0xe99e, 0x186c32, False, 'in Skull Woods'),
                  'Skull Woods - Bridge Room': (0xe9fe, 0x186c92, False, 'near Mothula'),
                  'Skull Woods - Boss': (0x180155, 0x186e03, False, 'with Mothula'),
                  'Ice Palace - Compass Chest': (0xe9d4, 0x186c68, False, 'in Ice Palace'),
                  'Ice Palace - Freezor Chest': (0xe995, 0x186c29, False, 'in Ice Palace'),
                  'Ice Palace - Big Chest': (0xe9aa, 0x186c3e, False, 'in Ice Palace'),
                  'Ice Palace - Iced T Room': (0xe9e3, 0x186c77, False, 'in Ice Palace'),
                  'Ice Palace - Spike Room': (0xe9e0, 0x186c74, False, 'in Ice Palace'),
                  'Ice Palace - Big Key Chest': (0xe9a4, 0x186c38, False, 'in Ice Palace'),
                  'Ice Palace - Map Chest': (0xe9dd, 0x186c71, False, 'in Ice Palace'),
                  'Ice Palace - Boss': (0x180157, 0x186e05, False, 'with Kholdstare'),
                  'Misery Mire - Big Chest': (0xea67, 0x186cfb, False, 'in Misery Mire'),
                  'Misery Mire - Map Chest': (0xea6a, 0x186cfe, False, 'in Misery Mire'),
                  'Misery Mire - Main Lobby': (0xea5e, 0x186cf2, False, 'in Misery Mire'),
                  'Misery Mire - Bridge Chest': (0xea61, 0x186cf5, False, 'in Misery Mire'),
                  'Misery Mire - Spike Chest': (0xe9da, 0x186c6e, False, 'in Misery Mire'),
                  'Misery Mire - Compass Chest': (0xea64, 0x186cf8, False, 'in Misery Mire'),
                  'Misery Mire - Big Key Chest': (0xea6d, 0x186d01, False, 'in Misery Mire'),
                  'Misery Mire - Boss': (0x180158, 0x186e06, False, 'with Vitreous'),
                  'Turtle Rock - Compass Chest': (0xea22, 0x186cb6, False, 'in Turtle Rock'),
                  'Turtle Rock - Roller Room - Left': (0xea1c, 0x186cb0, False, 'in Turtle Rock'),
                  'Turtle Rock - Roller Room - Right': (0xea1f, 0x186cb3, False, 'in Turtle Rock'),
                  'Turtle Rock - Chain Chomps': (0xea16, 0x186caa, False, 'in Turtle Rock'),
                  'Turtle Rock - Big Key Chest': (0xea25, 0x186cb9, False, 'in Turtle Rock'),
                  'Turtle Rock - Big Chest': (0xea19, 0x186cad, False, 'in Turtle Rock'),
                  'Turtle Rock - Crystaroller Room': (0xea34, 0x186cc8, False, 'in Turtle Rock'),
                  'Turtle Rock - Eye Bridge - Bottom Left': (0xea31, 0x186cc5, False, 'in Turtle Rock'),
                  'Turtle Rock - Eye Bridge - Bottom Right': (0xea2e, 0x186cc2, False, 'in Turtle Rock'),
                  'Turtle Rock - Eye Bridge - Top Left': (0xea2b, 0x186cbf, False, 'in Turtle Rock'),
                  'Turtle Rock - Eye Bridge - Top Right': (0xea28, 0x186cbc, False, 'in Turtle Rock'),
                  'Turtle Rock - Boss': (0x180159, 0x186e07, False, 'with Trinexx'),
                  'Palace of Darkness - Shooter Room': (0xea5b, 0x186cef, False, 'in Palace of Darkness'),
                  'Palace of Darkness - The Arena - Bridge': (0xea3d, 0x186cd1, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Stalfos Basement': (0xea49, 0x186cdd, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Big Key Chest': (0xea37, 0x186ccb, False, 'in Palace of Darkness'),
                  'Palace of Darkness - The Arena - Ledge': (0xea3a, 0x186cce, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Map Chest': (0xea52, 0x186ce6, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Compass Chest': (0xea43, 0x186cd7, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Dark Basement - Left': (0xea4c, 0x186ce0, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Dark Basement - Right': (0xea4f, 0x186ce3, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Dark Maze - Top': (0xea55, 0x186ce9, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Dark Maze - Bottom': (0xea58, 0x186cec, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Big Chest': (0xea40, 0x186cd4, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Harmless Hellway': (0xea46, 0x186cda, False, 'in Palace of Darkness'),
                  'Palace of Darkness - Boss': (0x180153, 0x186e01, False, 'with Helmasaur King'),
                  "Ganons Tower - Bob's Torch": (0x180161, 0x186e23, False, "in Ganon's Tower"),
                  'Ganons Tower - Hope Room - Left': (0xead9, 0x186d6d, False, "in Ganon's Tower"),
                  'Ganons Tower - Hope Room - Right': (0xeadc, 0x186d70, False, "in Ganon's Tower"),
                  'Ganons Tower - Tile Room': (0xeae2, 0x186d76, False, "in Ganon's Tower"),
                  'Ganons Tower - Compass Room - Top Left': (0xeae5, 0x186d79, False, "in Ganon's Tower"),
                  'Ganons Tower - Compass Room - Top Right': (0xeae8, 0x186d7c, False, "in Ganon's Tower"),
                  'Ganons Tower - Compass Room - Bottom Left': (0xeaeb, 0x186d7f, False, "in Ganon's Tower"),
                  'Ganons Tower - Compass Room - Bottom Right': (0xeaee, 0x186d82, False, "in Ganon's Tower"),
                  'Ganons Tower - DMs Room - Top Left': (0xeab8, 0x186d4c, False, "in Ganon's Tower"),
                  'Ganons Tower - DMs Room - Top Right': (0xeabb, 0x186d4f, False, "in Ganon's Tower"),
                  'Ganons Tower - DMs Room - Bottom Left': (0xeabe, 0x186d52, False, "in Ganon's Tower"),
                  'Ganons Tower - DMs Room - Bottom Right': (0xeac1, 0x186d55, False, "in Ganon's Tower"),
                  'Ganons Tower - Map Chest': (0xead3, 0x186d67, False, "in Ganon's Tower"),
                  'Ganons Tower - Firesnake Room': (0xead0, 0x186d64, False, "in Ganon's Tower"),
                  'Ganons Tower - Randomizer Room - Top Left': (0xeac4, 0x186d58, False, "in Ganon's Tower"),
                  'Ganons Tower - Randomizer Room - Top Right': (0xeac7, 0x186d5b, False, "in Ganon's Tower"),
                  'Ganons Tower - Randomizer Room - Bottom Left': (0xeaca, 0x186d5e, False, "in Ganon's Tower"),
                  'Ganons Tower - Randomizer Room - Bottom Right': (0xeacd, 0x186d61, False, "in Ganon's Tower"),
                  "Ganons Tower - Bob's Chest": (0xeadf, 0x186d73, False, "in Ganon's Tower"),
                  'Ganons Tower - Big Chest': (0xead6, 0x186d6a, False, "in Ganon's Tower"),
                  'Ganons Tower - Big Key Room - Left': (0xeaf4, 0x186d88, False, "in Ganon's Tower"),
                  'Ganons Tower - Big Key Room - Right': (0xeaf7, 0x186d8b, False, "in Ganon's Tower"),
                  'Ganons Tower - Big Key Chest': (0xeaf1, 0x186d85, False, "in Ganon's Tower"),
                  'Ganons Tower - Mini Helmasaur Room - Left': (0xeafd, 0x186d91, False, "atop Ganon's Tower"),
                  'Ganons Tower - Mini Helmasaur Room - Right': (0xeb00, 0x186d94, False, "atop Ganon's Tower"),
                  'Ganons Tower - Pre-Moldorm Chest': (0xeb03, 0x186d97, False, "atop Ganon's Tower"),
                  'Ganons Tower - Validation Chest': (0xeb06, 0x186d9a, False, "atop Ganon's Tower"),
                  'Ganon': (None, None, False, 'from me'),
                  'Agahnim 1': (None, None, False, 'from Ganon\'s wizardry form'),
                  'Agahnim 2': (None, None, False, 'from Ganon\'s wizardry form'),
                  'Eastern Palace - Boss Kill': (None, None, False, None),
                  'Desert Palace - Boss Kill': (None, None, False, None),
                  'Tower of Hera - Boss Kill': (None, None, False, None),
                  'Palace of Darkness - Boss Kill': (None, None, False, None),
                  'Swamp Palace - Boss Kill': (None, None, False, None),
                  'Thieves\' Town - Boss Kill': (None, None, False, None),
                  'Skull Woods - Boss Kill': (None, None, False, None),
                  'Ice Palace - Boss Kill': (None, None, False, None),
                  'Misery Mire - Boss Kill': (None, None, False, None),
                  'Turtle Rock - Boss Kill': (None, None, False, None),
                  'Lost Old Man': (None, None, False, None),
                  'Old Man Drop Off': (None, None, False, None),
                  'Floodgate': (None, None, False, None),
                  'Frog': (None, None, False, None),
                  'Missing Smith': (None, None, False, None),
                  'Dark Blacksmith Ruins': (None, None, False, None),
                  'Big Bomb': (None, None, False, None),
                  'Pyramid Crack': (None, None, False, None),
                  'Middle Aged Man': (None, None, False, None),
                  'Trench 1 Switch': (None, None, False, None),
                  'Trench 2 Switch': (None, None, False, None),
                  'Swamp Drain': (None, None, False, None),
                  'Turtle Medallion Pad': (None, None, False, None),
                  'Attic Cracked Floor': (None, None, False, None),
                  'Suspicious Maiden': (None, None, False, None),
                  'Revealing Light': (None, None, False, None),
                  'Ice Block Drop': (None, None, False, None),
                  'Skull Star Tile': (None, None, False, None),
                  'Zelda Pickup': (None, None, False, None),
                  'Zelda Drop Off': (None, None, False, None),
                  'Eastern Palace - Prize': (0xC6FE, 0x186E2C, True, 'with the Armos'),
                  'Desert Palace - Prize': (0xC6FF, 0x186E2D, True, 'with Lanmolas'),
                  'Tower of Hera - Prize': (0xC706, 0x186E2E, True, 'with Moldorm'),
                  'Palace of Darkness - Prize': (0xC702, 0x186E2F, True, 'with Helmasaur King'),
                  'Swamp Palace - Prize': (0xC701, 0x186E30, True, 'with Arrghus'),
                  'Skull Woods - Prize': (0xC704, 0x186E31, True, 'with Mothula'),
                  'Thieves\' Town - Prize': (0xC707, 0x186E32, True, 'with Blind'),
                  'Ice Palace - Prize': (0xC705, 0x186E33, True, 'with Kholdstare'),
                  'Misery Mire - Prize': (0xC703, 0x186E34, True, 'with Vitreous'),
                  'Turtle Rock - Prize': (0xC708, 0x186E35, True, 'with Trinexx'),
                  'Kakariko Shop - Left': (None, None, False, 'for sale in Kakariko'),
                  'Kakariko Shop - Middle': (None, None, False, 'for sale in Kakariko'),
                  'Kakariko Shop - Right': (None, None, False, 'for sale in Kakariko'),
                  'Lake Hylia Shop - Left': (None, None, False, 'for sale near the lake'),
                  'Lake Hylia Shop - Middle': (None, None, False, 'for sale near the lake'),
                  'Lake Hylia Shop - Right': (None, None, False, 'for sale near the lake'),
                  'Paradox Shop - Left': (None, None, False, 'for sale near seven chests'),
                  'Paradox Shop - Middle': (None, None, False, 'for sale near seven chests'),
                  'Paradox Shop - Right': (None, None, False, 'for sale near seven chests'),
                  'Capacity Upgrade - Left': (None, None, False, 'for sale near the queen'),
                  'Capacity Upgrade - Right': (None, None, False, 'for sale near the queen'),
                  'Village of Outcasts Shop - Left': (None, None, False, 'for sale near outcasts'),
                  'Village of Outcasts Shop - Middle': (None, None, False, 'for sale near outcasts'),
                  'Village of Outcasts Shop - Right': (None, None, False, 'for sale near outcasts'),
                  'Dark Lumberjack Shop - Left': (None, None, False, 'for sale in the far north'),
                  'Dark Lumberjack Shop - Middle': (None, None, False, 'for sale in the far north'),
                  'Dark Lumberjack Shop - Right': (None, None, False, 'for sale in the far north'),
                  'Dark Lake Hylia Shop - Left': (None, None, False, 'for sale near the dark lake'),
                  'Dark Lake Hylia Shop - Middle': (None, None, False, 'for sale near the dark lake'),
                  'Dark Lake Hylia Shop - Right': (None, None, False, 'for sale near the dark lake'),
                  'Dark Potion Shop - Left': (None, None, False, 'for sale near a catfish'),
                  'Dark Potion Shop - Middle': (None, None, False, 'for sale near a catfish'),
                  'Dark Potion Shop - Right': (None, None, False, 'for sale near a catfish'),
                  'Dark Death Mountain Shop - Left': (None, None, False, 'for sale on the dark mountain'),
                  'Dark Death Mountain Shop - Middle': (None, None, False, 'for sale on the dark mountain'),
                  'Dark Death Mountain Shop - Right': (None, None, False, 'for sale on the dark mountain'),
                  'Red Shield Shop - Left': (None, None, False, 'for sale as a curiosity'),
                  'Red Shield Shop - Middle': (None, None, False, 'for sale as a curiosity'),
                  'Red Shield Shop - Right': (None, None, False, 'for sale as a curiosity'),
                  'Potion Shop - Left': (None, None, False, 'for sale near potions'),
                  'Potion Shop - Middle': (None, None, False, 'for sale near potions'),
                  'Potion Shop - Right': (None, None, False, 'for sale near potions'),
                  }
lookup_id_to_name = {data[0]: name for name, data in location_table.items() if type(data[0]) == int}
lookup_id_to_name.update(shop_table_by_location_id)
lookup_id_to_name.update(bonk_table_by_location_id)
lookup_name_to_id = {name: data[0] for name, data in location_table.items() if type(data[0]) == int}
lookup_name_to_id.update(shop_table_by_location)
lookup_name_to_id.update(bonk_table_by_location)
