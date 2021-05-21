import random
from BaseClasses import OWEdge, WorldType, Direction, Terrain
from OWEdges import OWEdgeGroups, parallel_links, IsParallel

__version__ = '0.1.3.0u'

def link_overworld(world, player):
    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname, player)
    for exitname, destname in temporary_mandatory_connections:
        connect_two_way(world, exitname, destname, player)
    
    if world.mode[player] != 'inverted':
        for exitname, regionname in open_connections:
            connect_simple(world, exitname, regionname, player)
    else:
        for exitname, regionname in inverted_connections:
            connect_simple(world, exitname, regionname, player)

    connected_edges = []

    connect_custom(world, connected_edges, player)

    # if we do not shuffle, set default connections
    if world.owShuffle[player] == 'vanilla':
        for exitname, destname in default_connections:
            connect_two_way(world, exitname, destname, player)
    else:
        if world.owKeepSimilar[player] and world.owShuffle[player] == 'parallel':
            for exitname, destname in parallelsimilar_connections:
                connect_two_way(world, exitname, destname, player)
                connected_edges.append(exitname)
                connected_edges.append(destname)

        #TODO: Remove, just for testing
        for exitname, destname in test_connections:
            connect_two_way(world, exitname, destname, player)
            connected_edges.append(exitname)
            connected_edges.append(destname)
        
        trimmed_groups = remove_reserved(world, OWEdgeGroups, connected_edges, player)
        
        if world.owShuffle[player] == 'full':
            #predefined shuffle groups get reorganized here
            if world.owKeepSimilar[player]:
                if world.mode[player] == 'standard':
                    #tuple stays (A,B,C,D,_,F)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (std, region, axis, terrain, _, count) = group
                                new_grouping[(std, region, axis, terrain, count)] = ([], [])
                            
                            for group in grouping.keys():
                                (std, region, axis, terrain, _, count) = group
                                (forward_edges, back_edges) = grouping[group]
                                (exist_forward_edges, exist_back_edges) = new_grouping[(std, region, axis, terrain, count)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(std, region, axis, terrain, count)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
                else:
                    #tuple goes to (_,B,C,D,_,F)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (_, region, axis, terrain, _, count) = group
                                new_grouping[(region, axis, terrain, count)] = ([], [])
                            
                            for group in grouping.keys():
                                (_, region, axis, terrain, _, count) = group
                                (forward_edges, back_edges) = grouping[group]
                                (exist_forward_edges, exist_back_edges) = new_grouping[(region, axis, terrain, count)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(region, axis, terrain, count)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
            else:
                if world.mode[player] == 'standard':
                    #tuple stays (A,B,C,D,_,_)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (std, region, axis, terrain, _, _) = group
                                new_grouping[(std, region, axis, terrain)] = ([], [])
                            
                            for group in grouping.keys():
                                (std, region, axis, terrain, _, _) = group
                                (forward_edges, back_edges) = grouping[group]
                                forward_edges = [[i] for l in forward_edges for i in l]
                                back_edges = [[i] for l in back_edges for i in l]
                                
                                (exist_forward_edges, exist_back_edges) = new_grouping[(std, region, axis, terrain)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(std, region, axis, terrain)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
                else:
                    #tuple goes to (_,B,C,D,_,_)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (_, region, axis, terrain, _, _) = group
                                new_grouping[(region, axis, terrain)] = ([], [])
                            
                            for group in grouping.keys():
                                (_, region, axis, terrain, _, _) = group
                                (forward_edges, back_edges) = grouping[group]
                                forward_edges = [[i] for l in forward_edges for i in l]
                                back_edges = [[i] for l in back_edges for i in l]
                                
                                (exist_forward_edges, exist_back_edges) = new_grouping[(region, axis, terrain)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(region, axis, terrain)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
        elif world.owShuffle[player] == 'parallel':
            #predefined shuffle groups get reorganized here
            if world.owKeepSimilar[player]:
                if world.mode[player] == 'standard':
                    #tuple stays (A,B,C,D,E,F)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            groups = list(grouping.values())
                else:
                    #tuple goes to (_,B,C,D,E,F)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (_, region, axis, terrain, parallel, count) = group
                                new_grouping[(region, axis, terrain, parallel, count)] = ([], [])
                            
                            for group in grouping.keys():
                                (_, region, axis, terrain, parallel, count) = group
                                (forward_edges, back_edges) = grouping[group]
                                (exist_forward_edges, exist_back_edges) = new_grouping[(region, axis, terrain, parallel, count)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(region, axis, terrain, parallel, count)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
            else:
                if world.mode[player] == 'standard':
                    #tuple stays (A,B,C,D,E,_)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (std, region, axis, terrain, parallel, _) = group
                                new_grouping[(std, region, axis, terrain, parallel)] = ([], [])
                            
                            for group in grouping.keys():
                                (std, region, axis, terrain, parallel, _) = group
                                (forward_edges, back_edges) = grouping[group]
                                forward_edges = [[i] for l in forward_edges for i in l]
                                back_edges = [[i] for l in back_edges for i in l]
                                
                                (exist_forward_edges, exist_back_edges) = new_grouping[(std, region, axis, terrain, parallel)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(std, region, axis, terrain, parallel)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
                else:
                    #tuple goes to (_,B,C,D,E,_)
                    for grouping in (trimmed_groups, None):
                        if grouping is not None: #TODO: Figure out why ^ has to be a tuple for this to work
                            new_grouping = {}

                            for group in grouping.keys():
                                (_, region, axis, terrain, parallel, _) = group
                                new_grouping[(region, axis, terrain, parallel)] = ([], [])
                            
                            for group in grouping.keys():
                                (_, region, axis, terrain, parallel, _) = group
                                (forward_edges, back_edges) = grouping[group]
                                forward_edges = [[i] for l in forward_edges for i in l]
                                back_edges = [[i] for l in back_edges for i in l]
                                
                                (exist_forward_edges, exist_back_edges) = new_grouping[(region, axis, terrain, parallel)]
                                exist_forward_edges.extend(forward_edges)
                                exist_back_edges.extend(back_edges)
                                new_grouping[(region, axis, terrain, parallel)] = (exist_forward_edges, exist_back_edges)

                            groups = list(new_grouping.values())
        else:
            raise NotImplementedError('Shuffling not supported yet')
        
        #all shuffling occurs here
        random.shuffle(groups)
        for (forward_edge_sets, back_edge_sets) in groups:
            assert len(forward_edge_sets) == len(back_edge_sets)
            random.shuffle(back_edge_sets)
            for (forward_set, back_set) in zip(forward_edge_sets, back_edge_sets):
                assert len(forward_set) == len(back_set)
                for (forward_edge, back_edge) in zip(forward_set, back_set):
                    connect_two_way(world, forward_edge, back_edge, player)
                    connected_edges.append(forward_edge)
                    connected_edges.append(back_edge)
                    if world.owShuffle[player] == 'parallel' and forward_edge in parallel_links.keys():
                        connect_two_way(world, parallel_links[forward_edge], parallel_links[back_edge], player)
                        connected_edges.append(parallel_links[forward_edge])
                        connected_edges.append(parallel_links[back_edge])
                        
        assert len(connected_edges) == len(default_connections) * 2, connected_edges

def connect_custom(world, connected_edges, player):
    if hasattr(world, 'custom_overworld') and world.custom_overworld[player]:
        for edgename1, edgename2 in world.custom_overworld[player]:
            connect_two_way(world, edgename1, edgename2, player)
            connected_edges.append(edgename1)
            connected_edges.append(edgename2)

def connect_simple(world, exitname, regionname, player):
    world.get_entrance(exitname, player).connect(world.get_region(regionname, player))

def connect_two_way(world, edgename1, edgename2, player):
    edge1 = world.get_entrance(edgename1, player)
    edge2 = world.get_entrance(edgename2, player)

    # if these were already connected somewhere, remove the backreference
    if edge1.connected_region is not None:
        edge1.connected_region.entrances.remove(edge1)
    if edge2.connected_region is not None:
        edge2.connected_region.entrances.remove(edge2)

    edge1.connect(edge2.parent_region)
    edge2.connect(edge1.parent_region)
    x = world.check_for_owedge(edgename1, player)
    y = world.check_for_owedge(edgename2, player)
    if x is None:
        logging.getLogger('').error('%s is not a valid edge.', edgename1)
    elif y is None:
        logging.getLogger('').error('%s is not a valid edge.', edgename2)
    else:
        x.dest = y
        y.dest = x

    if world.owShuffle[player] != 'vanilla':
        world.spoiler.set_overworld(edgename2, edgename1, 'both', player)

def remove_reserved(world, groupedlist, connected_edges, player):
    new_grouping = {}
    for group in groupedlist.keys():
        new_grouping[group] = ([], [])

    for group in groupedlist.keys():
        (std, region, axis, terrain, parallel, count) = group
        (forward_edges, back_edges) = groupedlist[group]

        for edge in connected_edges:
            forward_edges = list(list(filter((edge).__ne__, i)) for i in forward_edges)
            back_edges = list(list(filter((edge).__ne__, i)) for i in back_edges)
        
        if world.owShuffle[player] == 'parallel' and region == WorldType.Dark:
            for edge in parallel_links:
                forward_edges = list(list(filter((parallel_links[edge]).__ne__, i)) for i in forward_edges)
                back_edges = list(list(filter((parallel_links[edge]).__ne__, i)) for i in back_edges)

        forward_edges = list(filter(([]).__ne__, forward_edges))
        back_edges = list(filter(([]).__ne__, back_edges))

        #TODO: Remove edges set in connect_custom. The lists above can be left with invalid counts if connect_custom removes entries, they need to get put into their appropriate group

        (exist_forward_edges, exist_back_edges) = new_grouping[group]
        exist_forward_edges.extend(forward_edges)
        exist_back_edges.extend(back_edges)
        if len(exist_forward_edges) > 0:
            new_grouping[group] = (exist_forward_edges, exist_back_edges)

    return new_grouping

test_connections = [
                    #('Links House ES', 'Octoballoon WS'),
                    #('Links House NE', 'Lost Woods Pass SW')
                    ]

temporary_mandatory_connections = [
                         # Special OW Areas
                         ('Lost Woods NW', 'Master Sword Meadow SC'),
                         ('Zora Waterfall NE', 'Zoras Domain SW'),
                         ('Stone Bridge WC', 'Hobo EC'),
                        ]

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [ # Whirlpool Connections
                         ('C Whirlpool', 'River Bend Water'),
                         ('River Bend Whirlpool', 'C Whirlpool Water'),
                         ('Lake Hylia Whirlpool', 'Zora Waterfall Water'),
                         ('Zora Whirlpool', 'Lake Hylia Water'),
                         ('Kakariko Pond Whirlpool', 'Octoballoon Water'),
                         ('Octoballoon Whirlpool', 'Kakariko Pond Area'),
                         ('Qirn Jump Whirlpool', 'Bomber Corner Water'),
                         ('Bomber Corner Whirlpool', 'Qirn Jump Water'),

                         # Intra-tile OW Connections
                         ('Lost Woods Bush (West)', 'Lost Woods East Area'),
                         ('Lost Woods Bush (East)', 'Lost Woods West Area'),
                         ('West Death Mountain Drop', 'West Death Mountain (Bottom)'),
                         ('Spectacle Rock Drop', 'West Death Mountain (Top)'),
                         ('Spectacle Rock Leave', 'West Death Mountain (Top)'),
                         ('Spectacle Rock Approach', 'Spectacle Rock Ledge'),
                         ('DM Hammer Bridge (West)', 'East Death Mountain (Top West)'),
                         ('DM Hammer Bridge (East)', 'East Death Mountain (Top East)'),
                         ('Floating Island Bridge (West)', 'East Death Mountain (Top East)'),
                         ('Floating Island Bridge (East)', 'Death Mountain Floating Island'),
                         ('East Death Mountain Spiral Ledge Drop', 'Spiral Cave Ledge'),
                         ('East Death Mountain Fairy Ledge Drop', 'Fairy Ascension Ledge'),
                         ('East Death Mountain Mimic Ledge Drop', 'Mimic Cave Ledge'),
                         ('Spiral Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Mimic Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Ledge Drop', 'Fairy Ascension Plateau'),
                         ('Fairy Ascension Plateau Ledge Drop', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Rocks (North)', 'East Death Mountain (Bottom)'),
                         ('Fairy Ascension Rocks (South)', 'Fairy Ascension Plateau'),
                         ('DM Broken Bridge (West)', 'East Death Mountain (Bottom)'),
                         ('DM Broken Bridge (East)', 'East Death Mountain (Bottom Left)'),
                         ('TR Pegs Ledge Entry', 'Death Mountain TR Pegs Ledge'),
                         ('TR Pegs Ledge Drop', 'Death Mountain TR Pegs'),
                         ('Death Mountain Entrance Rock', 'Death Mountain Entrance'),
                         ('Death Mountain Entrance Drop', 'Mountain Entry Area'),
                         ('Death Mountain Return Drop', 'Mountain Entry Area'),
                         ('Zora Waterfall Landing', 'Zora Waterfall Area'),
                         ('Zora Waterfall Water Drop', 'Zora Waterfall Water'),
                         ('Zora Waterfall Water Entry', 'Zora Waterfall Water'),
                         ('Waterfall of Wishing Cave Entry', 'Waterfall of Wishing Cave'),
                         ('Bonk Rock Ledge Drop', 'Sanctuary Area'),
                         ('Graveyard Ledge Drop', 'Graveyard Area'),
                         ('Graveyard Ladder (Top)', 'Graveyard Area'),
                         ('Graveyard Ladder (Bottom)', 'Graveyard Ledge'),
                         ('Kings Grave Outer Rocks', 'Kings Grave Area'),
                         ('Kings Grave Inner Rocks', 'Graveyard Area'),
                         ('River Bend Water Drop', 'River Bend Water'),
                         ('River Bend East Water Drop', 'River Bend Water'),
                         ('River Bend West Pier', 'River Bend Area'),
                         ('River Bend East Pier', 'River Bend East Bank'),
                         ('Potion Shop Water Drop', 'Potion Shop Water'),
                         ('Potion Shop Northeast Water Drop', 'Potion Shop Water'),
                         ('Potion Shop Rock (South)', 'Potion Shop Northeast'),
                         ('Potion Shop Rock (North)', 'Potion Shop Area'),
                         ('Zora Approach Water Drop', 'Zora Approach Water'),
                         ('Kakariko Southwest Bush (North)', 'Kakariko Southwest'),
                         ('Kakariko Southwest Bush (South)', 'Kakariko Area'),
                         ('Kakariko Yard Bush (South)', 'Kakariko Grass Yard'),
                         ('Kakariko Yard Bush (North)', 'Kakariko Area'),
                         ('Hyrule Castle Courtyard Bush (North)', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Courtyard Bush (South)', 'Hyrule Castle Courtyard Northeast'),
                         ('Hyrule Castle Main Gate (South)', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Main Gate (North)', 'Hyrule Castle Area'),
                         ('Hyrule Castle Ledge Drop', 'Hyrule Castle Area'),
                         ('Hyrule Castle Ledge Courtyard Drop', 'Hyrule Castle Courtyard'),
                         ('Hyrule Castle Inner East Rock', 'Hyrule Castle East Entry'),
                         ('Hyrule Castle Outer East Rock', 'Hyrule Castle Area'),
                         ('Wooden Bridge Bush (South)', 'Wooden Bridge Northeast'),
                         ('Wooden Bridge Bush (North)', 'Wooden Bridge Area'),
                         ('Wooden Bridge Water Drop', 'Wooden Bridge Water'),
                         ('Wooden Bridge Northeast Water Drop', 'Wooden Bridge Water'),
                         ('Bat Cave Ledge Peg', 'Bat Cave Ledge'),
                         ('Maze Race Game', 'Maze Race Prize'),
                         ('Maze Race Ledge Drop', 'Maze Race Area'),
                         ('Desert Palace Statue Move', 'Desert Palace Stairs'),
                         ('Desert Ledge Drop', 'Desert Area'),
                         ('Desert Ledge Outer Rocks', 'Desert Palace Entrance (North) Spot'),
                         ('Desert Ledge Inner Rocks', 'Desert Ledge'),
                         ('Checkerboard Ledge Drop', 'Desert Area'),
                         ('Checkerboard Ledge Approach', 'Desert Checkerboard Ledge'),
                         ('Checkerboard Ledge Leave', 'Desert Area'),
                         ('Desert Mouth Drop', 'Desert Area'),
                         ('Desert Teleporter Drop', 'Desert Area'),
                         ('Bombos Tablet Drop', 'Desert Area'),
                         ('Flute Boy Bush (North)', 'Flute Boy Approach Area'),
                         ('Flute Boy Bush (South)', 'Flute Boy Bush Entry'),
                         ('Cave 45 Ledge Drop', 'Flute Boy Approach Area'),
                         ('Cave 45 Inverted Leave', 'Flute Boy Approach Area'),
                         ('Cave 45 Inverted Approach', 'Cave 45 Ledge'),
                         ('C Whirlpool Water Entry', 'C Whirlpool Water'),
                         ('C Whirlpool Landing', 'C Whirlpool Area'),
                         ('C Whirlpool Rock (Bottom)', 'C Whirlpool Outer Area'),
                         ('C Whirlpool Rock (Top)', 'C Whirlpool Area'),
                         ('Statues Water Entry', 'Statues Water'),
                         ('Statues Landing', 'Statues Area'),
                         ('Lake Hylia Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia South Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Northeast Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Central Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Island Water Drop', 'Lake Hylia Water'),
                         ('Lake Hylia Central Island Pier', 'Lake Hylia Central Island'),
                         ('Lake Hylia Island Pier', 'Lake Hylia Island'),
                         ('Lake Hylia West Pier', 'Lake Hylia Area'),
                         ('Lake Hylia East Pier', 'Lake Hylia Northeast Bank'),
                         ('Desert Pass Ledge Drop', 'Desert Pass Area'),
                         ('Desert Pass Ladder (North)', 'Desert Pass Area'),
                         ('Desert Pass Ladder (South)', 'Desert Pass Ledge'),
                         ('Desert Pass Rocks (North)', 'Desert Pass Southeast'),
                         ('Desert Pass Rocks (South)', 'Desert Pass Area'),
                         ('Octoballoon Water Drop', 'Octoballoon Water'),
                         ('Octoballoon Waterfall Water Drop', 'Octoballoon Water'),
                         ('Octoballoon Pier', 'Octoballoon Area'),

                         ('Skull Woods Bush Rock (West)', 'Skull Woods Forest'),
                         ('Skull Woods Bush Rock (East)', 'Skull Woods Portal Entry'),
                         ('Skull Woods Forgotten Bush (West)', 'Skull Woods Forgotten Path (Northeast)'),
                         ('Skull Woods Forgotten Bush (East)', 'Skull Woods Forgotten Path (Southwest)'),
                         ('Dark Death Mountain Drop (West)', 'West Dark Death Mountain (Bottom)'),
                         ('Dark Death Mountain Ladder (North)', 'West Dark Death Mountain (Bottom)'),
                         ('Dark Death Mountain Ladder (South)', 'West Dark Death Mountain (Top)'),
                         ('GT Entry Approach', 'GT Approach'),
                         ('GT Entry Leave', 'West Dark Death Mountain (Top)'),
                         ('Floating Island Drop', 'East Dark Death Mountain (Top)'),
                         ('Dark Death Mountain Drop (East)', 'East Dark Death Mountain (Bottom)'),
                         ('Turtle Rock Ledge Drop', 'Turtle Rock Area'),
                         ('Turtle Rock Tail Ledge Drop', 'Turtle Rock Ledge'),
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
                         ('Shield Shop Fence (Outer) Ledge Drop', 'Shield Shop Fence'),
                         ('Shield Shop Fence (Inner) Ledge Drop', 'Shield Shop Area'),
                         ('Pyramid Exit Ledge Drop', 'Pyramid Area'),
                         ('Broken Bridge Hammer Rock (South)', 'Broken Bridge Northeast'),
                         ('Broken Bridge Hammer Rock (North)', 'Broken Bridge Area'),
                         ('Broken Bridge Hookshot Gap', 'Broken Bridge West'),
                         ('Broken Bridge Water Drop', 'Broken Bridge Water'),
                         ('Broken Bridge Northeast Water Drop', 'Broken Bridge Water'),
                         ('Broken Bridge West Water Drop', 'Broken Bridge Water'),
                         ('Peg Area Rocks (West)', 'Hammer Peg Area'),
                         ('Peg Area Rocks (East)', 'Hammer Peg Entry'),
                         ('Dig Game To Ledge Drop', 'Dig Game Ledge'),
                         ('Dig Game Ledge Drop', 'Dig Game Area'),
                         ('Frog Ledge Drop', 'Archery Game Area'),
                         ('Archery Game Rock', 'Frog Area'),
                         ('Hammer Bridge Pegs (North)', 'Hammer Bridge South Area'),
                         ('Hammer Bridge Pegs (South)', 'Hammer Bridge North Area'),
                         ('Hammer Bridge Water Drop', 'Hammer Bridge Water'),
                         ('Hammer Bridge Pier', 'Hammer Bridge North Area'),
                         ('Misery Mire Teleporter Ledge Drop', 'Misery Mire Area'),
                         ('Stumpy Approach Bush (North)', 'Stumpy Approach Area'),
                         ('Stumpy Approach Bush (South)', 'Stumpy Approach Bush Entry'),
                         ('Dark C Whirlpool Water Entry', 'Dark C Whirlpool Water'),
                         ('Dark C Whirlpool Landing', 'Dark C Whirlpool Area'),
                         ('Dark C Whirlpool Rock (Bottom)', 'Dark C Whirlpool Outer Area'),
                         ('Dark C Whirlpool Rock (Top)', 'Dark C Whirlpool Area'),
                         ('Hype Cave Water Entry', 'Hype Cave Water'),
                         ('Hype Cave Landing', 'Hype Cave Area'),
                         ('Ice Lake Water Drop', 'Ice Lake Water'),
                         ('Ice Lake Northeast Water Drop', 'Ice Lake Water'),
                         ('Ice Lake Southwest Water Drop', 'Ice Lake Water'),
                         ('Ice Lake Southeast Water Drop', 'Ice Lake Water'),
                         ('Ice Lake Moat Water Drop', 'Ice Lake Water'),
                         ('Ice Lake Northeast Pier', 'Ice Lake Northeast Bank'),
                         ('Ice Palace Approach', 'Ice Palace Area'),
                         ('Ice Palace Leave', 'Ice Lake Moat'),
                         ('Bomber Corner Water Drop', 'Bomber Corner Water'),
                         ('Bomber Corner Waterfall Water Drop', 'Bomber Corner Water'),
                         ('Bomber Corner Pier', 'Bomber Corner Area'),
                         
                         # OWG Connections
                         ('Sand Dunes Ledge Drop', 'Sand Dunes Area'),
                         ('Stone Bridge East Ledge Drop', 'Stone Bridge Area'),
                         ('Tree Line Ledge Drop', 'Tree Line Area'),
                         ('Eastern Palace Ledge Drop', 'Eastern Palace Area'),
                         
                         ('Links House Cliff Ledge Drop', 'Links House Area'),
                         ('Central Bonk Rocks Cliff Ledge Drop', 'Central Bonk Rocks Area'),
                         ('Stone Bridge Cliff Ledge Drop', 'Stone Bridge Area'),
                         ('Lake Hylia Area Cliff Ledge Drop', 'Lake Hylia Area'),
                         ('C Whirlpool Cliff Ledge Drop', 'C Whirlpool Area'),
                         ('C Whirlpool Outer Cliff Ledge Drop', 'C Whirlpool Outer Area'),
                         ('South Teleporter Cliff Ledge Drop', 'Dark C Whirlpool Area'),
                         ('Statues Cliff Ledge Drop', 'Statues Area'),
                         ('Lake Hylia Island FAWT Ledge Drop', 'Lake Hylia Island'),
                         ('Stone Bridge EC Cliff Water Drop', 'Stone Bridge Water'), #fake flipper
                         ('Tree Line WC Cliff Water Drop', 'Tree Line Water'), #fake flipper
                         
                         ('Desert Boss Cliff Ledge Drop', 'Desert Palace Entrance (North) Spot'),
                         ('Checkerboard Cliff Ledge Drop', 'Desert Checkerboard Ledge'),
                         ('Suburb Cliff Ledge Drop', 'Kakariko Suburb Area'),
                         ('Cave 45 Cliff Ledge Drop', 'Cave 45 Ledge'),
                         ('Desert Pass Cliff Ledge Drop', 'Desert Pass Area'),
                         ('Desert Pass Southeast Cliff Ledge Drop', 'Desert Pass Southeast'),
                         ('Desert C Whirlpool Cliff Ledge Drop', 'C Whirlpool Outer Area'),
                         ('Dam Cliff Ledge Drop', 'Dam Area'),

                         ('Dark Dunes Ledge Drop', 'Dark Dunes Area'),
                         ('Hammer Bridge North Ledge Drop', 'Hammer Bridge North Area'),
                         ('Dark Tree Line Ledge Drop', 'Dark Tree Line Area'),
                         ('Palace of Darkness Ledge Drop', 'Palace of Darkness Area'),

                         ('Mire Cliff Ledge Drop', 'Misery Mire Area'),
                         ('Archery Game Cliff Ledge Drop', 'Archery Game Area'),
                         ('Stumpy Approach Cliff Ledge Drop', 'Stumpy Approach Area'),
                         ('Swamp Nook Cliff Ledge Drop', 'Swamp Nook Area'),
                         ('Mire C Whirlpool Cliff Ledge Drop', 'Dark C Whirlpool Outer Area'),
                         ('Swamp Cliff Ledge Drop', 'Swamp Area'),

                         ('Bomb Shop Cliff Ledge Drop', 'Big Bomb Shop Area'),
                         ('Dark Bonk Rocks Cliff Ledge Drop', 'Dark Bonk Rocks Area'),
                         ('Hammer Bridge South Cliff Ledge Drop', 'Hammer Bridge South Area'),
                         ('Ice Lake Area Cliff Ledge Drop', 'Ice Lake Area'),
                         ('Ice Lake Northeast Pier Bomb Jump', 'Ice Lake Northeast Bank'),
                         ('Dark C Whirlpool Cliff Ledge Drop', 'Dark C Whirlpool Area'),
                         ('Dark C Whirlpool Outer Cliff Ledge Drop', 'Dark C Whirlpool Outer Area'),
                         ('Dark South Teleporter Cliff Ledge Drop', 'Dark Central Cliffs'), #TODO:inverted only, add glove requirement
                         ('Hype Cliff Ledge Drop', 'Hype Cave Area'),
                         ('Ice Palace Island FAWT Ledge Drop', 'Ice Lake Moat'),
                         ('Hammer Bridge EC Cliff Water Drop', 'Hammer Bridge Water'), #fake flipper
                         ('Dark Tree Line WC Cliff Water Drop', 'Dark Tree Line Water'), #fake flipper
                         
                         # Portal Connections
                         ('Kakariko Teleporter (Hammer)', 'Skull Woods Pass East Top Area'),
                         ('Kakariko Teleporter (Rock)', 'Skull Woods Pass East Top Area'),
                         ('Top of Pyramid', 'Pyramid Area'),
                         ('Top of Pyramid (Inner)', 'Pyramid Area'),
                         ('East Hyrule Teleporter', 'Palace of Darkness Nook Area'),
                         ('South Hyrule Teleporter', 'Dark C Whirlpool Area'),
                         ('Desert Teleporter', 'Misery Mire Teleporter Ledge'),
                         ('Lake Hylia Teleporter', 'Ice Palace Area'),
                         ('West Death Mountain Teleporter', 'West Dark Death Mountain (Bottom)'),
                         ('East Death Mountain Teleporter', 'East Dark Death Mountain (Bottom)'),
                         ('TR Pegs Teleporter', 'Turtle Rock Ledge'),
                         
                         ('Post Aga Inverted Teleporter', 'Hyrule Castle Area'),
                         ('Ice Palace Teleporter', 'Lake Hylia Central Island'),
                         ('Misery Mire Teleporter', 'Desert Palace Teleporter Ledge'),
                         ('East Dark World Teleporter', 'Eastern Nook Area'),
                         ('South Dark World Teleporter', 'C Whirlpool Area'),
                         ('West Dark World Teleporter (Hammer)', 'Lost Woods Pass East Top Area'),
                         ('West Dark World Teleporter (Rock)', 'Lost Woods Pass East Bottom Area'),
                         ('Dark Death Mountain Teleporter (West)', 'West Death Mountain (Bottom)'),
                         ('Dark Death Mountain Teleporter (East)', 'East Death Mountain (Bottom)'),
                         ('Turtle Rock Teleporter', 'Death Mountain TR Pegs Ledge'),

                         # Mirror Connections
                         ('Lost Woods East Mirror Spot', 'Lost Woods East Area'),
                         ('Lost Woods Entry Mirror Spot', 'Lost Woods West Area'),
                         ('Lost Woods Pedestal Mirror Spot', 'Lost Woods West Area'),
                         ('Lost Woods Southwest Mirror Spot', 'Lost Woods West Area'),
                         ('Lost Woods East (Forgotten) Mirror Spot', 'Lost Woods East Area'),
                         ('Lost Woods West (Forgotten) Mirror Spot', 'Lost Woods West Area'),
                         ('Lumberjack Mirror Spot', 'Lumberjack Area'),
                         ('Mountain Entry Mirror Spot', 'Mountain Entry Area'),
                         ('Mountain Entry Entrance Mirror Spot', 'Death Mountain Entrance'),
                         ('Mountain Entry Ledge Mirror Spot', 'Death Mountain Return Ledge'),
                         ('Lost Woods Pass West Mirror Spot', 'Lost Woods Pass West Area'),
                         ('Lost Woods Pass East Top Mirror Spot', 'Lost Woods Pass East Top Area'),
                         ('Lost Woods East Bottom Mirror Spot', 'Lost Woods Pass East Bottom Area'),
                         ('Kakariko Fortune Mirror Spot', 'Kakariko Fortune Area'),
                         ('Kakariko Pond Mirror Spot', 'Kakariko Pond Area'),
                         ('Forgotton Forest Mirror Spot', 'Forgotten Forest Area'),
                         ('Bonk Rock Ledge Mirror Spot', 'Bonk Rock Ledge'),
                         ('Graveyard Ledge Mirror Spot', 'Graveyard Ledge'),
                         ('Kings Grave Mirror Spot', 'Kings Grave Area'),
                         ('River Bend Mirror Spot', 'River Bend Area'),
                         ('River Bend East Mirror Spot', 'River Bend East Bank'),
                         ('Potion Shop Mirror Spot', 'Potion Shop Area'),
                         ('Potion Shop Northeast Mirror Spot', 'Potion Shop Northeast'),
                         ('Zora Approach Mirror Spot', 'Zora Approach Area'),
                         ('Zora Waterfall Mirror Spot', 'Zora Waterfall Area'),
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
                         ('Sand Dunes Mirror Spot', 'Sand Dunes Area'),
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
                         ('Central Bonk Rocks Mirror Spot', 'Central Bonk Rocks Area'),
                         ('Links House Mirror Spot', 'Links House Area'),
                         ('Stone Bridge Mirror Spot', 'Stone Bridge Area'),
                         ('Stone Bridge South Mirror Spot', 'Stone Bridge Area'),
                         ('Hobo Mirror Spot', 'Stone Bridge Water'),
                         ('Tree Line Mirror Spot', 'Tree Line Area'),
                         ('Desert Ledge Mirror Spot', 'Desert Ledge'),
                         ('Checkerboard Mirror Spot', 'Desert Checkerboard Ledge'),
                         ('DP Stairs Mirror Spot', 'Desert Palace Stairs'),
                         ('DP Entrance (North) Mirror Spot', 'Desert Palace Entrance (North) Spot'),
                         ('Bombos Tablet Ledge Mirror Spot', 'Bombos Tablet Ledge'),
                         ('Desert Pass Ledge Mirror Spot', 'Desert Pass Ledge'),
                         ('Desert Pass Mirror Spot', 'Desert Pass Area'),
                         ('Dam Mirror Spot', 'Dam Area'),
                         ('Statues Mirror Spot', 'Statues Area'),
                         ('South Pass Mirror Spot', 'South Pass Area'),
                         ('Lake Hylia Mirror Spot', 'Lake Hylia Area'),
                         ('Lake Hylia Northeast Mirror Spot', 'Lake Hylia Northeast Bank'),
                         ('South Shore Mirror Spot', 'Lake Hylia South Shore'),
                         ('South Shore East Mirror Spot', 'Lake Hylia South Shore'),
                         ('Lake Hylia Island Mirror Spot', 'Lake Hylia Island'),
                         ('Lake Hylia Central Island Mirror Spot', 'Lake Hylia Central Island'),
                         ('Lake Hylia Water Mirror Spot', 'Lake Hylia Water'),
                         ('Octoballoon Mirror Spot', 'Octoballoon Area'),
                         ('Ice Cave Mirror Spot', 'Ice Cave Area'),
                         ('Spectacle Rock Mirror Spot', 'Spectacle Rock Ledge'),
                         ('West Death Mountain (Top) Mirror Spot', 'West Death Mountain (Top)'),
                         ('East Death Mountain (Top West) Mirror Spot', 'East Death Mountain (Top West)'),
                         ('East Death Mountain (Top East) Mirror Spot', 'East Death Mountain (Top East)'),
                         ('Spiral Cave Mirror Spot', 'Spiral Cave Ledge'),
                         ('Mimic Cave Mirror Spot', 'Mimic Cave Ledge'),
                         ('Isolated Ledge Mirror Spot', 'Fairy Ascension Ledge'),
                         ('Fairy Ascension Mirror Spot', 'Fairy Ascension Plateau'),
                         ('Death Mountain Bridge Mirror Spot', 'East Death Mountain (Bottom Left)'),
                         ('Floating Island Mirror Spot', 'Death Mountain Floating Island'),
                         ('TR Pegs Area Mirror Spot', 'Death Mountain TR Pegs')

                         #TODO: Inverted Mirror Spots
                         ]

standard_connections = [('Hyrule Castle SW', 'Central Bonk Rocks NW'),
                        ('Hyrule Castle SE', 'Links House NE'),
                        ('Central Bonk Rocks EN', 'Links House WN'),
                        ('Central Bonk Rocks EC', 'Links House WC'),
                        ('Central Bonk Rocks ES', 'Links House WS')
                        ]

open_connections = [('Flute Spot 1', 'West Death Mountain (Bottom)'),
                         ('Flute Spot 2', 'Potion Shop Area'),
                         ('Flute Spot 3', 'Kakariko Area'),
                         ('Flute Spot 4', 'Links House Area'),
                         ('Flute Spot 5', 'Eastern Nook Area'),
                         ('Flute Spot 6', 'Desert Palace Teleporter Ledge'),
                         ('Flute Spot 7', 'Dam Area'),
                         ('Flute Spot 8', 'Octoballoon Area')
                         ]

inverted_connections = [('Flute Spot 1', 'West Dark Death Mountain (Bottom)'),
                         ('Flute Spot 2', 'Dark Witch Area'),
                         ('Flute Spot 3', 'Village of Outcasts Area'),
                         ('Flute Spot 4', 'Big Bomb Shop Area'),
                         ('Flute Spot 5', 'Palace of Darkness Nook Area'),
                         ('Flute Spot 6', 'Misery Mire Teleporter Ledge'),
                         ('Flute Spot 7', 'Swamp Area'),
                         ('Flute Spot 8', 'Bomber Corner Area')
                         ]

parallelsimilar_connections = [('Maze Race ES', 'Kakariko Suburb WS'),
                                ('Dig Game EC', 'Frog WC'),
                                ('Dig Game ES', 'Frog WS')
                                ]

# non shuffled overworld
default_connections = [('Lost Woods SW', 'Lost Woods Pass NW'),
                        ('Lost Woods SC', 'Lost Woods Pass NE'),
                        ('Lost Woods SE', 'Kakariko Fortune NE'),
                        ('Lost Woods EN', 'Lumberjack WN'),
                        ('Lumberjack SW', 'Mountain Entry NW'),
                        ('Mountain Entry SE', 'Kakariko Pond NE'),
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
                        ('Graveyard EC', 'River Bend WC'),
                        ('River Bend SW', 'Wooden Bridge NW'),
                        ('River Bend SC', 'Wooden Bridge NC'),
                        ('River Bend SE', 'Wooden Bridge NE'),
                        ('River Bend EN', 'Potion Shop WN'),
                        ('River Bend EC', 'Potion Shop WC'),
                        ('River Bend ES', 'Potion Shop WS'),
                        ('Potion Shop EN', 'Zora Approach WN'),
                        ('Potion Shop EC', 'Zora Approach WC'),
                        ('Zora Approach NE', 'Zora Waterfall SE'),
                        ('Kakariko SE', 'Kakariko Suburb NE'),
                        ('Kakariko ES', 'Blacksmith WS'),
                        ('Hyrule Castle SW', 'Central Bonk Rocks NW'),
                        ('Hyrule Castle SE', 'Links House NE'),
                        ('Hyrule Castle ES', 'Sand Dunes WN'),
                        ('Wooden Bridge SW', 'Sand Dunes NW'),
                        ('Sand Dunes SC', 'Stone Bridge NC'),
                        ('Eastern Palace SW', 'Tree Line NW'),
                        ('Eastern Palace SE', 'Eastern Nook NE'),
                        ('Maze Race ES', 'Kakariko Suburb WS'),
                        ('Kakariko Suburb ES', 'Flute Boy WS'),
                        ('Flute Boy SW', 'Flute Boy Approach NW'),
                        ('Flute Boy SC', 'Flute Boy Approach NC'),
                        ('Flute Boy Approach EC', 'C Whirlpool WC'),
                        ('C Whirlpool NW', 'Central Bonk Rocks SW'),
                        ('C Whirlpool SC', 'Dam NC'),
                        ('C Whirlpool EN', 'Statues WN'),
                        ('C Whirlpool EC', 'Statues WC'),
                        ('C Whirlpool ES', 'Statues WS'),
                        ('Central Bonk Rocks EN', 'Links House WN'),
                        ('Central Bonk Rocks EC', 'Links House WC'),
                        ('Central Bonk Rocks ES', 'Links House WS'),
                        ('Links House SC', 'Statues NC'),
                        ('Links House ES', 'Stone Bridge WS'),
                        ('Stone Bridge SC', 'Lake Hylia NW'),
                        ('Stone Bridge EN', 'Tree Line WN'),
                        ('Stone Bridge EC', 'Tree Line WC'),
                        ('Tree Line SC', 'Lake Hylia NC'),
                        ('Tree Line SE', 'Lake Hylia NE'),
                        ('Desert EC', 'Desert Pass WC'),
                        ('Desert ES', 'Desert Pass WS'),
                        ('Desert Pass EC', 'Dam WC'),
                        ('Desert Pass ES', 'Dam WS'),
                        ('Dam EC', 'South Pass WC'),
                        ('Statues SC', 'South Pass NC'),
                        ('South Pass ES', 'Lake Hylia WS'),
                        ('Lake Hylia EC', 'Octoballoon WC'),
                        ('Lake Hylia ES', 'Octoballoon WS'),
                        ('Octoballoon NW', 'Ice Cave SW'),
                        ('Octoballoon NE', 'Ice Cave SE'),
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
                        ('Pyramid SW', 'Dark Bonk Rocks NW'),
                        ('Pyramid SE', 'Big Bomb Shop NE'),
                        ('Pyramid ES', 'Dark Dunes WN'),
                        ('Broken Bridge SW', 'Dark Dunes NW'),
                        ('Dark Dunes SC', 'Hammer Bridge NC'),
                        ('Palace of Darkness SW', 'Dark Tree Line NW'),
                        ('Palace of Darkness SE', 'Palace of Darkness Nook NE'),
                        ('Dig Game EC', 'Frog WC'),
                        ('Dig Game ES', 'Frog WS'),
                        ('Frog ES', 'Stumpy WS'),
                        ('Stumpy SW', 'Stumpy Approach NW'),
                        ('Stumpy SC', 'Stumpy Approach NC'),
                        ('Stumpy Approach EC', 'Dark C Whirlpool WC'),
                        ('Dark C Whirlpool NW', 'Dark Bonk Rocks SW'),
                        ('Dark C Whirlpool SC', 'Swamp NC'),
                        ('Dark C Whirlpool EN', 'Hype Cave WN'),
                        ('Dark C Whirlpool EC', 'Hype Cave WC'),
                        ('Dark C Whirlpool ES', 'Hype Cave WS'),
                        ('Dark Bonk Rocks EN', 'Big Bomb Shop WN'),
                        ('Dark Bonk Rocks EC', 'Big Bomb Shop WC'),
                        ('Dark Bonk Rocks ES', 'Big Bomb Shop WS'),
                        ('Big Bomb Shop SC', 'Hype Cave NC'),
                        ('Big Bomb Shop ES', 'Hammer Bridge WS'),
                        ('Hammer Bridge SC', 'Ice Lake NW'),
                        ('Hammer Bridge EN', 'Dark Tree Line WN'),
                        ('Hammer Bridge EC', 'Dark Tree Line WC'),
                        ('Dark Tree Line SC', 'Ice Lake NC'),
                        ('Dark Tree Line SE', 'Ice Lake NE'),
                        ('Swamp Nook EC', 'Swamp WC'),
                        ('Swamp Nook ES', 'Swamp WS'),
                        ('Swamp EC', 'Dark South Pass WC'),
                        ('Hype Cave SC', 'Dark South Pass NC'),
                        ('Dark South Pass ES', 'Ice Lake WS'),
                        ('Ice Lake EC', 'Bomber Corner WC'),
                        ('Ice Lake ES', 'Bomber Corner WS'),
                        ('Bomber Corner NW', 'Shopping Mall SW'),
                        ('Bomber Corner NE', 'Shopping Mall SE'),
                        ('West Dark Death Mountain EN', 'East Dark Death Mountain WN'),
                        ('West Dark Death Mountain ES', 'East Dark Death Mountain WS'),
                        ('East Dark Death Mountain EN', 'Turtle Rock WN')
                        ]
