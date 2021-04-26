import random
from BaseClasses import OWEdge, WorldType, Direction, Terrain
from OWEdges import OWEdgeGroups

__version__ = '0.1.1.0-u'

def link_overworld(world, player):
    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname, player)
    for exitname, destname in temporary_mandatory_connections:
        connect_two_way(world, exitname, destname, player)

    connect_custom(world, player)

    # if we do not shuffle, set default connections
    if world.owShuffle[player] == 'vanilla':
        for exitname, destname in default_connections:
            connect_two_way(world, exitname, destname, player)
    else:
        remaining_edges = []
        for exitname, destname in default_connections:
            remaining_edges.append(exitname)
            remaining_edges.append(destname)
        
        if world.mode[player] == 'standard':
            for exitname, destname in standard_connections:
                connect_two_way(world, exitname, destname, player)
                remaining_edges.remove(exitname)
                remaining_edges.remove(destname)

        #TODO: Remove, just for testing
        for exitname, destname in test_connections:
            connect_two_way(world, exitname, destname, player)
            remaining_edges.remove(exitname)
            remaining_edges.remove(destname)
        
        if world.owShuffle[player] == 'full':
            if world.owKeepSimilar[player]:
                #TODO: remove edges from list that are already placed, Std and Plando
                # shuffle edges in groups that connect the same pair of tiles
                for grouping in (OWEdgeGroups, None):
                    if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                        groups = list(grouping.values())
                        random.shuffle(groups)
                        for (forward_edge_sets, back_edge_sets) in groups:
                            assert len(forward_edge_sets) == len(back_edge_sets)
                            random.shuffle(back_edge_sets)
                        
                            for (forward_set, back_set) in zip(forward_edge_sets, back_edge_sets):
                                assert len(forward_set) == len(back_set)
                                for (forward_edge, back_edge) in zip(forward_set, back_set):
                                    connect_two_way(world, forward_edge, back_edge, player)
                                    remaining_edges.remove(forward_edge)
                                    remaining_edges.remove(back_edge)
                
                assert len(remaining_edges) == 0, remaining_edges
            else:
                connect_remaining(world, remaining_edges, player)
        else:
            raise NotImplementedError('Shuffling not supported yet')


def connect_custom(world, player):
    if hasattr(world, 'custom_overworld') and world.custom_overworld[player]:
        for exit_name, region_name in world.custom_overworld[player]:
            # doesn't actually change addresses
            connect_simple(world, exit_name, region_name, player)
    # this needs to remove custom connections from the pool


def connect_simple(world, exitname, regionname, player):
    world.get_entrance(exitname, player).connect(world.get_region(regionname, player))

def connect_two_way(world, entrancename, exitname, player):
    entrance = world.get_entrance(entrancename, player)
    exit = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    entrance.connect(exit.parent_region)
    exit.connect(entrance.parent_region)
    x = world.check_for_owedge(entrancename, player)
    y = world.check_for_owedge(exitname, player)
    if x is not None and y is not None:
        x.dest = y
        y.dest = x
    elif x is None:
        logging.getLogger('').error('%s is not a valid edge.', entrancename)
    elif y is None:
        logging.getLogger('').error('%s is not a valid edge.', exitname)

    world.spoiler.set_overworld(exitname, entrancename, 'both', player)

def connect_edges(world, edges, targets, player):
    """This works inplace"""
    random.shuffle(edges)
    random.shuffle(targets)
    while edges:
        edge = edges.pop()
        target = targets.pop()
        connect_two_way(world, edge, target, player)

def connect_remaining(world, edges, player):
    lw_edges = list()
    dw_edges = list()
    for edgename in edges:
        edge = world.check_for_owedge(edgename, player)
        if edge.worldType == WorldType.Dark:
            dw_edges.append(edge)
        else:
            lw_edges.append(edge)
    
    land_edges = list()
    water_edges = list()
    for edge in lw_edges:
        if edge.terrain == Terrain.Land:
            land_edges.append(edge)
        else:
            water_edges.append(edge)

    north_edges = list()
    south_edges = list()
    west_edges = list()
    east_edges = list()
    for edge in land_edges:
        if edge.direction == Direction.North:
            north_edges.append(edge.name)
        elif edge.direction == Direction.South:
            south_edges.append(edge.name)
        elif edge.direction == Direction.West:
            west_edges.append(edge.name)
        else:
            east_edges.append(edge.name)

    #lw land edges
    connect_edges(world, north_edges, south_edges, player)
    connect_edges(world, west_edges, east_edges, player)

    north_edges = list()
    south_edges = list()
    west_edges = list()
    east_edges = list()
    for edge in water_edges:
        if edge.direction == Direction.North:
            north_edges.append(edge.name)
        elif edge.direction == Direction.South:
            south_edges.append(edge.name)
        elif edge.direction == Direction.West:
            west_edges.append(edge.name)
        else:
            east_edges.append(edge.name)

    #lw water edges
    connect_edges(world, north_edges, south_edges, player)
    connect_edges(world, west_edges, east_edges, player)

    land_edges = list()
    water_edges = list()
    for edge in dw_edges:
        if edge.terrain == Terrain.Land:
            land_edges.append(edge)
        else:
            water_edges.append(edge)
    
    north_edges = list()
    south_edges = list()
    west_edges = list()
    east_edges = list()
    for edge in land_edges:
        if edge.direction == Direction.North:
            north_edges.append(edge.name)
        elif edge.direction == Direction.South:
            south_edges.append(edge.name)
        elif edge.direction == Direction.West:
            west_edges.append(edge.name)
        else:
            east_edges.append(edge.name)
    
    #dw land edges
    connect_edges(world, north_edges, south_edges, player)
    connect_edges(world, west_edges, east_edges, player)

    north_edges = list()
    south_edges = list()
    west_edges = list()
    east_edges = list()
    for edge in water_edges:
        if edge.direction == Direction.North:
            north_edges.append(edge.name)
        elif edge.direction == Direction.South:
            south_edges.append(edge.name)
        elif edge.direction == Direction.West:
            west_edges.append(edge.name)
        else:
            east_edges.append(edge.name)
    
    #dw water edges
    connect_edges(world, north_edges, south_edges, player)
    connect_edges(world, west_edges, east_edges, player)

test_connections = [
                    #('Links House ES', 'Octoballoon WS'),
                    #('Links House NE', 'Lost Woods Pass SW')
                    ]

temporary_mandatory_connections = [
                         # Special OW Areas
                         ('Lost Woods NW', 'Master Sword Meadow SC'),
                         ('Zora Approach NE', 'Zoras Domain SW'),
                         ('Stone Bridge WC', 'Hobo EC'),
                        ]

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Flute Spot 1', 'West Death Mountain (Bottom)'),
                         ('Flute Spot 2', 'Potion Shop Area'),
                         ('Flute Spot 3', 'Kakariko Area'),
                         ('Flute Spot 4', 'Links House Area'),
                         ('Flute Spot 5', 'Eastern Nook Area'),
                         ('Flute Spot 6', 'Desert Palace Teleporter Ledge'),
                         ('Flute Spot 7', 'Dam Area'),
                         ('Flute Spot 8', 'Octoballoon Area'),

                         # Whirlpool Connections
                         ('C Whirlpool', 'Useless Fairy Water'),
                         ('Useless Fairy Whirlpool', 'C Whirlpool Area'),
                         ('Lake Hylia Whirlpool', 'Zora Approach Area'),
                         ('Zora Whirlpool', 'Lake Hylia Water'),
                         ('Kakariko Pond Whirlpool', 'Octoballoon Water'),
                         ('Octoballoon Whirlpool', 'Kakariko Pond Area'),
                         ('Qirn Jump Whirlpool', 'Southeast DW Water'),
                         ('Southeast DW Whirlpool', 'Qirn Jump Water'),

                         # Intra-tile OW Connections
                         ('Death Mountain Entrance Rock', 'Death Mountain Entrance'),
                         ('Death Mountain Entrance Drop', 'DM Ascent Area'),
                         ('Death Mountain Return Drop', 'DM Ascent Area'),
                         ('Bonk Rock Ledge Drop', 'Sanctuary Area'),
                         ('Kings Grave Outer Rocks', 'Kings Grave Area'),
                         ('Kings Grave Inner Rocks', 'Graveyard Area'),
                         ('Graveyard Ledge Drop', 'Graveyard Area'),
                         ('Useless Fairy Water Drop', 'Useless Fairy Water'),
                         ('Useless Fairy East Water Drop', 'Useless Fairy Water'),
                         ('Useless Fairy West Pier', 'Useless Fairy Area'),
                         ('Useless Fairy East Pier', 'Useless Fairy East Bank'),
                         ('Potion Shop Water Drop', 'Potion Shop Water'),
                         ('Potion Shop Northeast Water Drop', 'Potion Shop Water'),
                         ('Potion Shop Rock (South)', 'Potion Shop Northeast'),
                         ('Potion Shop Rock (North)', 'Potion Shop Area'),
                         ('Zora Warning Water Drop', 'Zora Warning Water'),
                         ('Bat Cave Ledge Peg', 'Bat Cave Ledge'),
                         ('Hyrule Castle Main Gate (South)', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Main Gate (North)', 'Hyrule Castle Area'),
                         ('Hyrule Castle Ledge Drop', 'Hyrule Castle Area'),
                         ('Hyrule Castle Ledge Courtyard Drop', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Inner East Rock', 'Hyrule Castle East Entry'),
                         ('Hyrule Castle Outer East Rock', 'Hyrule Castle Area'),
                         ('Wooden Bridge Water Drop', 'Wooden Bridge Water'),
                         ('Maze Race Ledge Drop', 'Maze Race Area'),
                         ('Cave 45 Ledge Drop', 'Cave 45 Area'),
                         ('C Whirlpool Rock (Bottom)', 'C Whirlpool Outer Area'),
                         ('C Whirlpool Rock (Top)', 'C Whirlpool Area'),
                         ('Desert Palace Statue Move', 'Desert Palace Stairs'),
                         ('Desert Ledge Drop', 'Desert Area'),
                         ('Desert Ledge Outer Rocks', 'Desert Palace Entrance (North) Spot'),
                         ('Desert Ledge Inner Rocks', 'Desert Ledge'),
                         ('Checkerboard Ledge Drop', 'Desert Area'),
                         ('Desert Mouth Drop', 'Desert Area'),
                         ('Desert Teleporter Drop', 'Desert Area'),
                         ('Bombos Tablet Drop', 'Desert Area'),
                         ('Purple Chest Ledge Drop', 'Purple Chest Area'),
                         ('Purple Chest Rocks (North)', 'Purple Chest Southeast'),
                         ('Purple Chest Rocks (South)', 'Purple Chest Area'),
                         ('Lake Hylia Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia South Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Northeast Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Central Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Island Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Central Island Pier', 'Lake Hylia Central Island'),
                         ('Lake Hylia West Pier', 'Lake Hylia Area'),
                         ('Lake Hylia East Pier', 'Lake Hylia Northeast Bank'),
                         ('Octoballoon Water Drop', 'Octoballoon Water'),
                         ('Octoballoon Waterfall Water Drop', 'Octoballoon Water'),
                         ('Octoballoon Pier', 'Octoballoon Area'),

                         ('West Death Mountain Drop', 'West Death Mountain (Bottom)'),
                         ('Spectacle Rock Drop', 'West Death Mountain (Top)'),
                         ('DM Hammer Bridge (West)', 'East Death Mountain (Top West)'),
                         ('DM Hammer Bridge (East)', 'East Death Mountain (Top East)'),
                         ('East Death Mountain Spiral Drop', 'Spiral Cave Ledge'),
                         ('East Death Mountain Fairy Drop', 'Fairy Ascension Ledge'),
                         ('Spiral Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Ledge Drop', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Plateau Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Rocks', 'Fairy Ascension Plateau'),
                         ('DM Broken Bridge (West)', 'East Death Mountain (Bottom)'),
                         ('DM Broken Bridge (East)', 'East Death Mountain (Bottom Left)'),
                         
                         ('Skull Woods Bush Rock (West)', 'Skull Woods Forest'),
                         ('Skull Woods Bush Rock (East)', 'Skull Woods Portal Entry'),
                         ('Skull Woods Forgotten Bush (West)', 'Skull Woods Forgotten Path (Northeast)'),
                         ('Skull Woods Forgotten Bush (East)', 'Skull Woods Forgotten Path (Southwest)'),
                         ('Bumper Cave Entrance Rock', 'Bumper Cave Entrance'),
                         ('Bumper Cave Ledge Drop', 'Bumper Cave Area'),
                         ('Bumper Cave Entrance Drop', 'Bumper Cave Area'),
                         ('Skull Woods Pass Bush Row (West)', 'Skull Woods Pass East Top Area'),
                         ('Skull Woods Pass Bush Row (East)', 'Skull Woods Pass West Area'),
                         ('Skull Woods Pass Rock (Top)', 'Skull Woods Pass East Bottom Area'),
                         ('Skull Woods Pass Rock (Bottom)', 'Skull Woods Pass East Top Area'),
                         ('Qirn Jump Water Drop', 'Qirn Jump Water'),
                         ('Qirn Jump East Water Drop', 'Qirn Jump Water'),
                         ('Qirn Jump Pier', 'Qirn Jump East Bank'),
                         ('Dark Witch Water Drop', 'Dark Witch Water'),
                         ('Dark Witch Northeast Water Drop', 'Dark Witch Water'),
                         ('Dark Witch Rock (North)', 'Dark Witch Area'),
                         ('Dark Witch Rock (South)', 'Dark Witch Northeast'),
                         ('Catfish Approach Water Drop', 'Catfish Approach Water'),
                         ('Village of Outcasts Pegs', 'Dark Grassy Lawn'),
                         ('Grassy Lawn Pegs', 'Village of Outcasts Area'),
                         ('Peg Area Rocks (West)', 'Hammer Peg Area'),
                         ('Peg Area Rocks (East)', 'Hammer Peg Entry'),
                         ('Pyramid Exit Drop', 'Pyramid Area'),
                         ('Broken Bridge Hammer Rock (South)', 'Broken Bridge Northeast'),
                         ('Broken Bridge Hammer Rock (North)', 'Broken Bridge Area'),
                         ('Broken Bridge Hookshot Gap', 'Broken Bridge West'),
                         ('Broken Bridge Water Drop', 'Broken Bridge Water'),
                         ('Broken Bridge Northeast Water Drop', 'Broken Bridge Water'),
                         ('Broken Bridge West Water Drop', 'Broken Bridge Water'),
                         ('Dig Game To Ledge Drop', 'Dig Game Ledge'),
                         ('Dig Game Ledge Drop', 'Dig Game Area'),
                         ('Frog Ledge Drop', 'Archery Game Area'),
                         ('Archery Game Rock', 'Frog Area'),
                         ('Dark C Whirlpool Rock (Bottom)', 'Dark C Whirlpool Outer Area'),
                         ('Dark C Whirlpool Rock (Top)', 'Dark C Whirlpool Area'),
                         ('Hammer Bridge Pegs (North)', 'Hammer Bridge South Area'),
                         ('Hammer Bridge Pegs (South)', 'Hammer Bridge North Area'),
                         ('Hammer Bridge Water Drop', 'Hammer Bridge Water'),
                         ('Hammer Bridge Pier', 'Hammer Bridge North Area'),
                         ('Dark Lake Hylia Water Drop', 'Dark Lake Hylia Water'),
                         ('Dark Lake Hylia Northeast Water Drop', 'Dark Lake Hylia Water'),
                         ('Dark Lake Hylia Southwest Water Drop', 'Dark Lake Hylia Water'),
                         ('Dark Lake Hylia Southeast Water Drop', 'Dark Lake Hylia Water'),
                         ('Dark Lake Hylia Northeast Pier', 'Dark Lake Hylia Northeast Bank'),
                         ('Southeast DW Water Drop', 'Southeast DW Water'),
                         ('Southeast DW Waterfall Water Drop', 'Southeast DW Water'),
                         ('Southeast DW Pier', 'Southeast DW Area'),

                         ('Dark Death Mountain Drop (West)', 'Dark Death Mountain (West Bottom)'),
                         ('Dark Death Mountain Drop (East)', 'Dark Death Mountain (East Bottom)'),
                         ('Floating Island Drop', 'Dark Death Mountain (Top East)'),
                         ('Turtle Rock Ledge Drop', 'Turtle Rock Area'),
                         
                         # Portal Connections
                         ('Kakariko Teleporter (Hammer)', 'Skull Woods Pass East Top Area'),
                         ('Kakariko Teleporter (Rock)', 'Skull Woods Pass East Top Area'),
                         ('Top of Pyramid', 'Pyramid Area'),
                         ('Top of Pyramid (Inner)', 'Pyramid Area'),
                         ('East Hyrule Teleporter', 'Palace of Darkness Nook Area'),
                         ('South Hyrule Teleporter', 'Dark C Whirlpool Area'),
                         ('Desert Teleporter', 'Misery Mire Area'),
                         ('Lake Hylia Teleporter', 'Ice Palace Area'),
                         ('West Death Mountain Teleporter', 'Dark Death Mountain (West Bottom)'),
                         ('East Death Mountain Teleporter', 'Dark Death Mountain (East Bottom)'),
                         ('Turtle Rock Teleporter', 'Turtle Rock Ledge'),

                         # Mirror Connections
                         ('Lost Woods Mirror Spot', 'Lost Woods Area'),
                         ('Lost Woods Entry Mirror Spot', 'Lost Woods Area'),
                         ('Lost Woods Pedestal Mirror Spot', 'Lost Woods Area'),
                         ('Lost Woods Southwest Mirror Spot', 'Lost Woods Area'),
                         ('Lost Woods Northeast Mirror Spot', 'Lost Woods Area'),
                         ('Lumberjack Mirror Spot', 'Lumberjack Area'),
                         ('DM Ascent Mirror Spot', 'DM Ascent Area'),
                         ('DM Ascent Entrance Mirror Spot', 'Death Mountain Entrance'),
                         ('DM Ascent Ledge Mirror Spot', 'Death Mountain Return Ledge'),
                         ('Lost Woods Pass West Mirror Spot', 'Lost Woods Pass West Area'),
                         ('Lost Woods Pass East Top Mirror Spot', 'Lost Woods Pass East Top Area'),
                         ('Lost Woods East Bottom Mirror Spot', 'Lost Woods Pass East Bottom Area'),
                         ('Kakariko Fortune Mirror Spot', 'Kakariko Fortune Area'),
                         ('Kakariko Pond Mirror Spot', 'Kakariko Pond Area'),
                         ('Forgotton Forest Mirror Spot', 'Forgotten Forest Area'),
                         ('Bonk Rock Ledge Mirror Spot', 'Bonk Rock Ledge'),
                         ('Graveyard Ledge Mirror Spot', 'Graveyard Ledge'),
                         ('Kings Grave Mirror Spot', 'Kings Grave Area'),
                         ('Useless Fairy Mirror Spot', 'Useless Fairy Area'),
                         ('Useless Fairy East Mirror Spot', 'Useless Fairy East Bank'),
                         ('Potion Shop Mirror Spot', 'Potion Shop Area'),
                         ('Potion Shop Northeast Mirror Spot', 'Potion Shop Northeast'),
                         ('Zora Warning Mirror Spot', 'Zora Warning Area'),
                         ('Zora Approach Mirror Spot', 'Zora Approach Area'),
                         ('Kakariko Mirror Spot', 'Kakariko Area'),
                         ('Kakariko Grass Mirror Spot', 'Kakariko Area'),
                         ('Blacksmith Mirror Spot', 'Blacksmith Area'),
                         ('Blacksmith Entry Mirror Spot', 'Blacksmith Area'),
                         ('Bat Cave Ledge Mirror Spot', 'Bat Cave Ledge'),
                         ('HC Ledge Mirror Spot', 'Hyrule Castle Ledge'),
                         ('HC Courtyard Mirror Spot', 'Hyrule Castle Courtyard'),
                         ('HC Area Mirror Spot', 'Hyrule Castle Area'),
                         ('HC Area South Mirror Spot', 'Hyrule Castle Area'),
                         ('HC East Entry Mirror Spot', 'Hyrule Castle East Entry'),
                         ('Wooden Bridge Mirror Spot', 'Wooden Bridge Area'),
                         ('Wooden Bridge Northeast Mirror Spot', 'Wooden Bridge Area'),
                         ('Wooden Bridge West Mirror Spot', 'Wooden Bridge Area'),
                         ('Sand Dune Mirror Spot', 'Sand Dune Area'),
                         ('Eastern Palace Mirror Spot', 'Eastern Palace Area'),
                         ('Eastern Nook Mirror Spot', 'Eastern Nook Area'),
                         ('Maze Race Mirror Spot', 'Maze Race Ledge'),
                         ('Maze Race Ledge Mirror Spot', 'Maze Race Ledge'),
                         ('Kakariko Suburb Mirror Spot', 'Kakariko Suburb Area'),
                         ('Kakariko Suburb South Mirror Spot', 'Kakariko Suburb Area'),
                         ('Flute Boy Mirror Spot', 'Flute Boy Area'),
                         ('Flute Boy Pass Mirror Spot', 'Flute Boy Pass'),
                         ('Cave 45 Mirror Spot', 'Cave 45 Ledge'),
                         ('C Whirlpool Mirror Spot', 'C Whirlpool Area'),
                         ('C Whirlpool Outer Mirror Spot', 'C Whirlpool Outer Area'),
                         ('Central Bonk Rock Mirror Spot', 'Central Bonk Rock Area'),
                         ('Links House Mirror Spot', 'Links House Area'),
                         ('Stone Bridge Mirror Spot', 'Stone Bridge Area'),
                         ('Stone Bridge South Mirror Spot', 'Stone Bridge Area'),
                         ('Hobo Mirror Spot', 'Stone Bridge Water'),
                         ('Tree Line Mirror Spot', 'Tree Line Area'),
                         ('Desert Ledge Mirror Spot', 'Desert Ledge'),
                         ('Checkerboard Mirror Spot', 'Desert Checkerboard Ledge'),
                         ('DP Stairs Mirror Spot', 'Desert Palace Stairs'),
                         ('DP Entrance (North) Mirror Spot', 'Desert Palace Entrance (North) Spot'),
                         ('Bombos Tablet Mirror Spot', 'Purple Chest Ledge'),
                         ('Purple Chest Mirror Spot', 'Purple Chest Area'),
                         ('Dam Mirror Spot', 'Dam Area'),
                         ('Statues Mirror Spot', 'Statues Area'),
                         ('South Pass Mirror Spot', 'South Pass Area'),
                         ('Lake Hylia Mirror Spot', 'Lake Hylia Area'),
                         ('Lake Hylia Northeast Mirror Spot', 'Lake Hylia Northeast Bank'),
                         ('South Shore Mirror Spot', 'Lake Hylia South Shore'),
                         ('South Shore East Mirror Spot', 'Lake Hylia South Shore'),
                         ('Lake Hylia Island Mirror Spot', 'Lake Hylia Island'),
                         ('Lake Hylia Central Island Mirror Spot', 'Lake Hylia Central Island'),
                         ('Octoballoon Mirror Spot', 'Octoballoon Area'),
                         ('Ice Rod Cave Mirror Spot', 'Ice Rod Cave Area'),
                         ('Spectacle Rock Mirror Spot', 'Spectacle Rock Ledge'),
                         ('West Death Mountain (Top) Mirror Spot', 'West Death Mountain (Top)'),
                         ('East Death Mountain (Top West) Mirror Spot', 'East Death Mountain (Top West)'),
                         ('East Death Mountain (Top East) Mirror Spot', 'East Death Mountain (Top East)'),
                         ('Spiral Cave Mirror Spot', 'Spiral Cave Ledge'),
                         ('Mimic Cave Mirror Spot', 'Mimic Cave Ledge'),
                         ('Isolated Ledge Mirror Spot', 'Fairy Ascension Ledge'),
                         ('Fairy Ascension Mirror Spot', 'Fairy Ascension Plateau'),
                         ('Death Mountain Bridge Mirror Spot', 'East Death Mountain (Bottom Left)'),
                         ('Floating Island Mirror Spot', 'Death Mountain Floating Island (Light World)'),
                         ('TR Pegs Area Mirror Spot', 'Death Mountain TR Pegs')
                         ]

standard_connections = [('Hyrule Castle SW', 'Central Bonk Rock NW'),
                        ('Hyrule Castle SE', 'Links House NE'),
                        ('Central Bonk Rock EN', 'Links House WN'),
                        ('Central Bonk Rock EC', 'Links House WC'),
                        ('Central Bonk Rock ES', 'Links House WS')
                        ]

# non shuffled overworld
default_connections = [('Lost Woods SW', 'Lost Woods Pass NW'),
                        ('Lost Woods SC', 'Lost Woods Pass NE'),
                        ('Lost Woods SE', 'Kakariko Fortune NE'),
                        ('Lost Woods EN', 'Lumberjack WN'),
                        ('Lumberjack SW', 'DM Ascent NW'),
                        ('DM Ascent SE', 'Kakariko Pond NE'),
                        ('Lost Woods Pass SW', 'Kakariko NW'),
                        ('Lost Woods Pass SE', 'Kakariko NC'),
                        ('Kakariko Fortune SC', 'Kakariko NE'),
                        ('Kakariko Fortune EN', 'Kakariko Pond WN'),
                        ('Kakariko Fortune ES', 'Kakariko Pond WS'),
                        ('Kakariko Pond SW', 'Forgotten Forest NW'),
                        ('Kakariko Pond SE', 'Forgotten Forest NE'),
                        ('Kakariko Pond EN', 'Sanctuary WN'),
                        ('Kakariko Pond ES', 'Sanctuary WS'),
                        ('Forgotten Forest ES', 'Hyrule Castle WN'),
                        ('Sanctuary EC', 'Graveyard WC'),
                        ('Graveyard EC', 'Useless Fairy WC'),
                        ('Useless Fairy SW', 'Wooden Bridge NW'),
                        ('Useless Fairy SC', 'Wooden Bridge NC'),
                        ('Useless Fairy SE', 'Wooden Bridge NE'),
                        ('Useless Fairy EN', 'Potion Shop WN'),
                        ('Useless Fairy EC', 'Potion Shop WC'),
                        ('Useless Fairy ES', 'Potion Shop WS'),
                        ('Potion Shop EN', 'Zora Warning WN'),
                        ('Potion Shop EC', 'Zora Warning WC'),
                        ('Zora Warning NE', 'Zora Approach SE'),
                        ('Kakariko SE', 'Kakariko Suburb NE'),
                        ('Kakariko ES', 'Blacksmith WS'),
                        ('Hyrule Castle SW', 'Central Bonk Rock NW'),
                        ('Hyrule Castle SE', 'Links House NE'),
                        ('Hyrule Castle ES', 'Sand Dune WN'),
                        ('Wooden Bridge SW', 'Sand Dune NW'),
                        ('Sand Dune SC', 'Stone Bridge NC'),
                        ('Eastern Palace SW', 'Tree Line NW'),
                        ('Eastern Palace SE', 'Eastern Nook NE'),
                        ('Maze Race ES', 'Kakariko Suburb WS'),
                        ('Kakariko Suburb ES', 'Flute Boy WS'),
                        ('Flute Boy SW', 'Cave 45 NW'),
                        ('Flute Boy SC', 'Cave 45 NC'),
                        ('Cave 45 EC', 'C Whirlpool WC'),
                        ('C Whirlpool NW', 'Central Bonk Rock SW'),
                        ('C Whirlpool SC', 'Dam NC'),
                        ('C Whirlpool EN', 'Statues WN'),
                        ('C Whirlpool EC', 'Statues WC'),
                        ('C Whirlpool ES', 'Statues WS'),
                        ('Central Bonk Rock EN', 'Links House WN'),
                        ('Central Bonk Rock EC', 'Links House WC'),
                        ('Central Bonk Rock ES', 'Links House WS'),
                        ('Links House SC', 'Statues NC'),
                        ('Links House ES', 'Stone Bridge WS'),
                        ('Stone Bridge SC', 'Lake Hylia NW'),
                        ('Stone Bridge EN', 'Tree Line WN'),
                        ('Stone Bridge EC', 'Tree Line WC'),
                        ('Tree Line SC', 'Lake Hylia NC'),
                        ('Tree Line SE', 'Lake Hylia NE'),
                        ('Desert EC', 'Purple Chest WC'),
                        ('Desert ES', 'Purple Chest WS'),
                        ('Purple Chest EC', 'Dam WC'),
                        ('Purple Chest ES', 'Dam WS'),
                        ('Dam EC', 'South Pass WC'),
                        ('Statues SC', 'South Pass NC'),
                        ('South Pass ES', 'Lake Hylia WS'),
                        ('Lake Hylia EC', 'Octoballoon WC'),
                        ('Lake Hylia ES', 'Octoballoon WS'),
                        ('Octoballoon NW', 'Ice Rod Cave SW'),
                        ('Octoballoon NE', 'Ice Rod Cave SE'),
                        ('West Death Mountain EN', 'East Death Mountain WN'),
                        ('West Death Mountain ES', 'East Death Mountain WS'),
                        ('East Death Mountain EN', 'Death Mountain TR Pegs WN'),

                        ('Skull Woods SW', 'Skull Woods Pass NW'),
                        ('Skull Woods SC', 'Skull Woods Pass NE'),
                        ('Skull Woods SE', 'Dark Fortune NE'),
                        ('Skull Woods EN', 'Dark Lumberjack WN'),
                        ('Dark Lumberjack SW', 'Bumper Cave NW'),
                        ('Bumper Cave SE', 'Outcast Pond NE'),
                        ('Skull Woods Pass SW', 'Village of Outcasts NW'),
                        ('Skull Woods Pass SE', 'Village of Outcasts NC'),
                        ('Dark Fortune SC', 'Village of Outcasts NE'),
                        ('Dark Fortune EN', 'Outcast Pond WN'),
                        ('Dark Fortune ES', 'Outcast Pond WS'),
                        ('Outcast Pond SW', 'Shield Shop NW'),
                        ('Outcast Pond SE', 'Shield Shop NE'),
                        ('Outcast Pond EN', 'Dark Chapel WN'),
                        ('Outcast Pond ES', 'Dark Chapel WS'),
                        ('Dark Chapel EC', 'Dark Graveyard WC'),
                        ('Dark Graveyard ES', 'Qirn Jump WC'),
                        ('Qirn Jump SW', 'Broken Bridge NW'),
                        ('Qirn Jump SC', 'Broken Bridge NC'),
                        ('Qirn Jump SE', 'Broken Bridge NE'),
                        ('Qirn Jump EN', 'Dark Witch WN'),
                        ('Qirn Jump EC', 'Dark Witch WC'),
                        ('Qirn Jump ES', 'Dark Witch WS'),
                        ('Dark Witch EN', 'Catfish Approach WN'),
                        ('Dark Witch EC', 'Catfish Approach WC'),
                        ('Catfish Approach NE', 'Catfish SE'),
                        ('Village of Outcasts SE', 'Frog NE'),
                        ('Village of Outcasts ES', 'Hammer Pegs WS'),
                        ('Pyramid SW', 'Dark Bonk Rock NW'),
                        ('Pyramid SE', 'Big Bomb Shop NE'),
                        ('Pyramid ES', 'Dark Dune WN'),
                        ('Broken Bridge SW', 'Dark Dune NW'),
                        ('Dark Dune SC', 'Hammer Bridge NC'),
                        ('Palace of Darkness SW', 'Dark Tree Line NW'),
                        ('Palace of Darkness SE', 'Palace of Darkness Nook NE'),
                        ('Dig Game EC', 'Frog WC'),
                        ('Dig Game ES', 'Frog WS'),
                        ('Frog ES', 'Stumpy WS'),
                        ('Stumpy SW', 'Circle of Bushes NW'),
                        ('Stumpy SC', 'Circle of Bushes NC'),
                        ('Circle of Bushes EC', 'Dark C Whirlpool WC'),
                        ('Dark C Whirlpool NW', 'Dark Bonk Rock SW'),
                        ('Dark C Whirlpool SC', 'Swamp Palace NC'),
                        ('Dark C Whirlpool EN', 'Hype Cave WN'),
                        ('Dark C Whirlpool EC', 'Hype Cave WC'),
                        ('Dark C Whirlpool ES', 'Hype Cave WS'),
                        ('Dark Bonk Rock EN', 'Big Bomb Shop WN'),
                        ('Dark Bonk Rock EC', 'Big Bomb Shop WC'),
                        ('Dark Bonk Rock ES', 'Big Bomb Shop WS'),
                        ('Big Bomb Shop SC', 'Hype Cave NC'),
                        ('Big Bomb Shop ES', 'Hammer Bridge WS'),
                        ('Hammer Bridge SC', 'Dark Lake Hylia NW'),
                        ('Hammer Bridge EN', 'Dark Tree Line WN'),
                        ('Hammer Bridge EC', 'Dark Tree Line WC'),
                        ('Dark Tree Line SC', 'Dark Lake Hylia NC'),
                        ('Dark Tree Line SE', 'Dark Lake Hylia NE'),
                        ('Dark Purple Chest EC', 'Swamp Palace WC'),
                        ('Dark Purple Chest ES', 'Swamp Palace WS'),
                        ('Swamp Palace EC', 'Dark South Pass WC'),
                        ('Hype Cave SC', 'Dark South Pass NC'),
                        ('Dark South Pass ES', 'Dark Lake Hylia WS'),
                        ('Dark Lake Hylia EC', 'Southeast DW WC'),
                        ('Dark Lake Hylia ES', 'Southeast DW WS'),
                        ('Southeast DW NW', 'Dark Shopping Mall SW'),
                        ('Southeast DW NE', 'Dark Shopping Mall SE'),
                        ('West Dark Death Mountain EN', 'East Dark Death Mountain WN'),
                        ('West Dark Death Mountain ES', 'East Dark Death Mountain WS'),
                        ('East Dark Death Mountain EN', 'Turtle Rock WN')
                        ]
