import logging
from collections import defaultdict, OrderedDict
import RaceRandom as random
from BaseClasses import CollectionState, RegionType
from OverworldShuffle import build_accessible_region_list
from DoorShuffle import find_inaccessible_regions
from OWEdges import OWTileRegions
from Utils import stack_size3a

entrance_pool = list()
exit_pool = list()
entrance_exits = list()
ignore_pool = True
suppress_spoiler = True

def link_entrances(world, player):
    invFlag = world.mode[player] == 'inverted'

    global entrance_pool, exit_pool, ignore_pool, suppress_spoiler, entrance_exits
    entrance_exits = list()
    ignore_pool = False
    suppress_spoiler = True
    links_house = False
    entrance_pool = Entrance_Pool_Base.copy()
    exit_pool = Exit_Pool_Base.copy()
    drop_connections = default_drop_connections.copy()
    dropexit_connections = default_dropexit_connections.copy()

    Dungeon_Exits = LW_Dungeon_Exits + DW_Mid_Dungeon_Exits + DW_Late_Dungeon_Exits
    Cave_Exits = Cave_Exits_Base.copy()
    Old_Man_House = Old_Man_House_Base.copy()
    Cave_Three_Exits = Cave_Three_Exits_Base.copy()

    from OverworldShuffle import build_sectors
    if not world.owsectors[player] and world.shuffle[player] != 'vanilla':
        world.owsectors[player] = build_sectors(world, player)

    # modifications to lists
    if not world.is_tile_swapped(0x1b, player):
        drop_connections.append(tuple(('Pyramid Hole', 'Pyramid')))
        dropexit_connections.append(tuple(('Pyramid Entrance', 'Pyramid Exit')))
    else:
        entrance_pool.remove('Pyramid Hole')
        entrance_pool.append('Inverted Pyramid Hole')
        entrance_pool.remove('Pyramid Entrance')
        entrance_pool.append('Inverted Pyramid Entrance')
        drop_connections.append(tuple(('Inverted Pyramid Hole', 'Pyramid')))
        dropexit_connections.append(tuple(('Inverted Pyramid Entrance', 'Pyramid Exit')))
        
    unbias_some_entrances(Dungeon_Exits, Cave_Exits, Old_Man_House, Cave_Three_Exits)
    Cave_Exits.extend(Cave_Exits_Directional)

    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname, player)

    connect_simple(world, 'Tavern North', 'Tavern', player)
    
    suppress_spoiler = False
    connect_custom(world, player)
    suppress_spoiler = True

    # if we do not shuffle, set default connections
    if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
        for entrancename, exitname in (default_connections + default_pot_connections +
               default_takeany_connections + drop_connections + default_item_connections + default_shop_connections):
            connect_logical(world, entrancename, exitname, player, exitname.endswith(' Exit'))
        for entrancename, exitname in default_connector_connections + dropexit_connections:
            connect_logical(world, entrancename, exitname, player, True)
        if invFlag:
            world.get_entrance('Dark Sanctuary Hint Exit', player).connect(world.get_entrance('Dark Sanctuary Hint', player).parent_region)
        if world.is_bombshop_start(player):
            world.get_entrance('Big Bomb Shop Exit', player).connect(world.get_entrance('Big Bomb Shop', player).parent_region)
        
        ignore_pool = False

        # dungeon entrance shuffle
        if world.shuffle[player] == 'vanilla':
            for entrancename, exitname in default_dungeon_connections:
                connect_logical(world, entrancename, exitname, player, True)
            for entrancename, exitname in default_skulldrop_connections:
                connect_logical(world, entrancename, exitname, player, False)
            
            if world.is_atgt_swapped(player):
                for entrancename, exitname in inverted_default_dungeon_connections:
                    connect_logical(world, entrancename, exitname, player, True)
            else:
                for entrancename, exitname in open_default_dungeon_connections:
                    connect_logical(world, entrancename, exitname, player, True)
        elif world.shuffle[player] == 'dungeonssimple':
            suppress_spoiler = False
            simple_shuffle_dungeons(world, player)
        elif world.shuffle[player] == 'dungeonsfull':
            suppress_spoiler = False
            full_shuffle_dungeons(world, Dungeon_Exits, player)
    elif world.shuffle[player] == 'simple':
        suppress_spoiler = False
        simple_shuffle_dungeons(world, player)

        # shuffle dropdowns
        scramble_holes(world, player)

        # list modification
        lw_wdm_entrances = ['Old Man Cave (West)', 'Death Mountain Return Cave (West)',
                            'Old Man Cave (East)', 'Old Man House (Bottom)', 'Old Man House (Top)',
                            'Death Mountain Return Cave (East)', 'Spectacle Rock Cave',
                            'Spectacle Rock Cave Peak', 'Spectacle Rock Cave (Bottom)']
        lw_edm_entrances = ['Paradox Cave (Bottom)', 'Paradox Cave (Middle)', 'Paradox Cave (Top)', 'Spiral Cave',
                            'Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave (Top)', 'Spiral Cave (Bottom)']
        ddm_entrances = ['Dark Death Mountain Fairy', 'Spike Cave']
        
        caves = list(Cave_Exits)
        three_exit_caves = list(Cave_Three_Exits)

        Two_Door_Caves_Directional = [('Bumper Cave (Bottom)', 'Bumper Cave (Top)')]
        Two_Door_Caves = [('Elder House (East)', 'Elder House (West)'),
                          ('Superbunny Cave (Bottom)', 'Superbunny Cave (Top)')]
        if not world.is_tile_swapped(0x05, player):
            Two_Door_Caves_Directional.append(tuple({'Hookshot Cave', 'Hookshot Cave Back Entrance'}))
        else:
            Two_Door_Caves.append(tuple({'Hookshot Cave', 'Hookshot Cave Back Entrance'}))
        if not world.is_tile_swapped(0x28, player):
            Two_Door_Caves.append(tuple({'Two Brothers House (East)', 'Two Brothers House (West)'}))
        else:
            Two_Door_Caves_Directional.append(tuple({'Two Brothers House (East)', 'Two Brothers House (West)'}))
        
        # shuffle all 2 entrance caves as pairs as a start
        # start with the ones that need to be directed
        two_door_caves = list(Two_Door_Caves_Directional)
        random.shuffle(two_door_caves)
        random.shuffle(caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)

        # shuffle remaining 2 entrance cave pairs
        two_door_caves = list(Two_Door_Caves)
        random.shuffle(two_door_caves)
        while two_door_caves:
            entrance1, entrance2 = two_door_caves.pop()
            exit1, exit2 = caves.pop()
            connect_two_way(world, entrance1, exit1, player)
            connect_two_way(world, entrance2, exit2, player)
        
        # shuffle LW DM entrances
        caves.extend(list(Old_Man_House))
        caves.extend(list(three_exit_caves))

        candidates = [e for e in lw_wdm_entrances if e != 'Old Man House (Bottom)']
        random.shuffle(candidates)
        old_man_exit = candidates.pop()
        lw_wdm_entrances.remove(old_man_exit)
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)

        if 0x03 in world.owswaps[player][0] == 0x05 in world.owswaps[player][0]: # if WDM and EDM are in same world
            candidates = lw_wdm_entrances + lw_edm_entrances
            random.shuffle(candidates)
            old_man_entrance = candidates.pop()
            if old_man_entrance in lw_wdm_entrances:
                lw_wdm_entrances.remove(old_man_entrance)
            elif old_man_entrance in lw_edm_entrances:
                lw_edm_entrances.remove(old_man_entrance)
        else:
            random.shuffle(lw_wdm_entrances)
            old_man_entrance = lw_wdm_entrances.pop()
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)
        
        # connect remaining LW DM entrances
        if 0x03 in world.owswaps[player][0] == 0x05 in world.owswaps[player][0]: # if WDM and EDM are in same world
            connect_caves(world, lw_wdm_entrances + lw_edm_entrances, [], caves, player)
        else:
            # place Old Man House in WDM if not flipped
            if not world.is_tile_swapped(0x03, player):
                connect_caves(world, lw_wdm_entrances, [], list(Old_Man_House), player)
            else:
                connect_caves(world, lw_edm_entrances, [], list(Old_Man_House), player)
            caves.remove(Old_Man_House[0])

            i = 0
            c = 0
            while i != len(lw_wdm_entrances):
                random.shuffle(caves)
                i = 0
                c = 0
                while i < len(lw_wdm_entrances):
                    i += len(caves[c])
                    c += 1
            
            connect_caves(world, lw_wdm_entrances, [], caves[0:c], player)
            connect_caves(world, lw_edm_entrances, [], caves[c:], player)

        if invFlag:
            # place dark sanc
            place_dark_sanc(world, player)
        
        # place links house
        links_house = place_links_house(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)

        # junk fill inaccessible regions
        # TODO: Should be obsolete someday when OWR rebalances the shuffle to prevent unreachable regions
        junk_fill_inaccessible(world, player)
    
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'restricted':
        suppress_spoiler = False
        simple_shuffle_dungeons(world, player)

        # shuffle holes
        scramble_holes(world, player)

        # place dark sanc
        if invFlag:
            place_dark_sanc(world, player)
        
        # place links house
        links_house = place_links_house(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)

        # determine pools
        lw_entrances = list()
        dw_entrances = list()
        caves = list(Cave_Exits + Cave_Three_Exits + Old_Man_House)
        for e in entrance_pool:
            if world.mode[player] == 'standard' and e == 'Bonk Fairy (Light)':
                continue
            region = world.get_entrance(e, player).parent_region
            if region.type == RegionType.LightWorld:
                lw_entrances.append(e)
            else:
                dw_entrances.append(e)
        
        # place connectors in inaccessible regions
        connect_inaccessible_regions(world, lw_entrances, dw_entrances, caves, player)
        
        # place old man, has limited options
        place_old_man(world, lw_entrances if not invFlag else dw_entrances, player)
        
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # shuffle connectors
        lw_entrances = [e for e in lw_entrances if e in entrance_pool]
        dw_entrances = [e for e in dw_entrances if e in entrance_pool]
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'full':
        suppress_spoiler = False
        skull_woods_shuffle(world, player)

        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House)
        
        if world.mode[player] == 'standard':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            caves.append(tuple(random.sample(['Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 2)))
        else:
            caves.append(tuple(random.sample(['Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 3)))
        
        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
        else:
            caves.append('Ganons Tower Exit')

        # place dark sanc
        if invFlag:
            place_dark_sanc(world, player, list(zip(*drop_connections + dropexit_connections))[0])
        
        # place links house
        links_house = place_links_house(world, player, list(zip(*drop_connections + dropexit_connections))[0])

        # determine pools
        lw_entrances = list()
        dw_entrances = list()
        for e in entrance_pool:
            if world.mode[player] == 'standard' and e == 'Bonk Fairy (Light)':
                continue
            if e not in list(zip(*drop_connections + dropexit_connections))[0]:
                region = world.get_entrance(e, player).parent_region
                if region.type == RegionType.LightWorld:
                    lw_entrances.append(e)
                else:
                    dw_entrances.append(e)
        
        # place connectors in inaccessible regions
        connect_inaccessible_regions(world, lw_entrances, dw_entrances, caves, player, list(zip(*drop_connections + dropexit_connections))[0])
        
        # place old man, has limited options
        place_old_man(world, lw_entrances if not invFlag else dw_entrances, player, list(zip(*drop_connections + dropexit_connections))[0])
        
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = [e for e in entrance_pool if e not in list(zip(*drop_connections + dropexit_connections))[0]]
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in bomb_shop_doors if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # shuffle connectors
        lw_entrances = [e for e in lw_entrances if e in entrance_pool]
        dw_entrances = [e for e in dw_entrances if e in entrance_pool]
        connect_caves(world, lw_entrances, dw_entrances, caves, player)

        # shuffle holes
        scramble_holes(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)

        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'lite':
        for entrancename, exitname in (default_connections +
               ([] if world.shopsanity[player] else default_shop_connections) +
               ([] if world.pottery[player] not in ['none', 'keys', 'dungeon'] else default_pot_connections) +
               ([] if world.take_any[player] == 'fixed' else default_takeany_connections)):
            connect_logical(world, entrancename, exitname, player, False)
        if invFlag:
            world.get_entrance('Dark Sanctuary Hint Exit', player).connect(world.get_entrance('Dark Sanctuary Hint', player).parent_region)
        
        suppress_spoiler = False
        
        # shuffle dungeons
        skull_woods_shuffle(world, player)

        # build dungeon lists
        lw_dungeons = LW_Dungeon_Exits.copy()
        dw_dungeons = DW_Late_Dungeon_Exits.copy()

        if world.mode[player] == 'standard':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            lw_dungeons.append(tuple(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')))
        else:
            lw_dungeons.append(tuple(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)', 'Hyrule Castle Exit (South)')))

        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
        else:
            dw_dungeons.append('Ganons Tower Exit')
        
        unbias_dungeons(lw_dungeons)
        unbias_dungeons(dw_dungeons)
        
        # shuffle dropdowns
        scramble_holes(world, player)

        # place links house
        links_house = place_links_house(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)

        # determine pools
        Cave_Base = list(Cave_Exits + Cave_Three_Exits + Old_Man_House)
        lw_entrances = list()
        dw_entrances = list()
        for e in entrance_pool:
            region = world.get_entrance(e, player).parent_region
            if region.type == RegionType.LightWorld:
                lw_entrances.append(e)
            else:
                dw_entrances.append(e)
        
        # place connectors in inaccessible regions
        caves = Cave_Base + (dw_dungeons if not invFlag else lw_dungeons)
        connector_entrances = [e for e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] if e in (dw_entrances if not invFlag else lw_entrances)]
        connect_inaccessible_regions(world, [], connector_entrances, caves, player)
        if invFlag:
            lw_dungeons = [e for e in lw_dungeons if e in caves]
        else:
            dw_dungeons = [e for e in dw_dungeons if e in caves]
        
        caves = [e for e in caves if e not in (dw_dungeons if not invFlag else lw_dungeons)] + (lw_dungeons if not invFlag else dw_dungeons)
        connector_entrances = [e for e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] if e in (lw_entrances if not invFlag else dw_entrances)]
        connect_inaccessible_regions(world, connector_entrances, [], caves, player)
        if not invFlag:
            lw_dungeons = [e for e in lw_dungeons if e in caves]
        else:
            dw_dungeons = [e for e in dw_dungeons if e in caves]
        
        caves = [e for e in caves if e not in (lw_dungeons if not invFlag else dw_dungeons)] + DW_Mid_Dungeon_Exits
        
        # place old man, has limited options
        lw_entrances = [e for e in lw_entrances if e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] and e in entrance_pool]
        dw_entrances = [e for e in dw_entrances if e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] and e in entrance_pool]
        place_old_man(world, lw_entrances if not invFlag else dw_entrances, player)
        
        # shuffle remaining connectors
        lw_entrances = [e for e in lw_entrances if e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] and e in entrance_pool]
        dw_entrances = [e for e in dw_entrances if e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] and e in entrance_pool]
        connect_caves(world, lw_entrances, [], lw_dungeons, player)
        connect_caves(world, [], dw_entrances, dw_dungeons, player)
        connect_caves(world, lw_entrances, dw_entrances, caves, player)
        
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'lean':
        for entrancename, exitname in (default_connections +
               ([] if world.shopsanity[player] else default_shop_connections) +
               ([] if world.pottery[player] not in ['none', 'keys', 'dungeon'] else default_pot_connections) +
               ([] if world.take_any[player] == 'fixed' else default_takeany_connections)):
            connect_logical(world, entrancename, exitname, player, False)
        if invFlag:
            world.get_entrance('Dark Sanctuary Hint Exit', player).connect(world.get_entrance('Dark Sanctuary Hint', player).parent_region)
        
        suppress_spoiler = False
        
        # shuffle dungeons
        skull_woods_shuffle(world, player)

        if world.mode[player] == 'standard':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            Dungeon_Exits.append(tuple(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)')))
        else:
            Dungeon_Exits.append(tuple(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)', 'Hyrule Castle Exit (South)')))

        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
        else:
            Dungeon_Exits.append('Ganons Tower Exit')
        
        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House)

        # shuffle dropdowns
        scramble_holes(world, player)

        # place links house
        links_house = place_links_house(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)

        # place connectors in inaccessible regions
        connector_entrances = [e for e in list(zip(*default_connector_connections + default_dungeon_connections + open_default_dungeon_connections))[0] if e in entrance_pool]
        connect_inaccessible_regions(world, connector_entrances, [], caves, player)

        # place old man, has limited options
        connector_entrances = [e for e in connector_entrances if e in entrance_pool]
        place_old_man(world, list(connector_entrances), player)
        
        # shuffle remaining connectors
        connector_entrances = [e for e in connector_entrances if e in entrance_pool]
        connect_caves(world, connector_entrances, [], caves, player)
        
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'crossed':
        suppress_spoiler = False
        skull_woods_shuffle(world, player)

        caves = list(Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House)
        
        if world.mode[player] == 'standard':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            caves.append(tuple(random.sample(['Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 2)))
        else:
            caves.append(tuple(random.sample(['Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'], 3)))
        
        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
        else:
            caves.append('Ganons Tower Exit')

        # shuffle holes
        scramble_holes(world, player)

        # place dark sanc
        if invFlag:
            place_dark_sanc(world, player)
        
        # place links house
        links_house = place_links_house(world, player)
        
        # place blacksmith, has limited options
        place_blacksmith(world, links_house, player)
        
        # place connectors in inaccessible regions
        pool = list(entrance_pool)
        if world.mode[player] == 'standard' and 'Bonk Fairy (Light)' in pool:
            pool.remove('Bonk Fairy (Light)')
        connect_inaccessible_regions(world, pool, [], caves, player)
        
        # place old man, has limited options
        pool = [e for e in pool if e in entrance_pool]
        place_old_man(world, pool, player)
    
        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            bomb_shop = random.choice(bomb_shop_doors)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # shuffle connectors
        pool = [e for e in pool if e in entrance_pool]
        connect_caves(world, pool, [], caves, player)

        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    elif world.shuffle[player] == 'insanity':
        # beware ye who enter here
        suppress_spoiler = False

        # list preparation
        caves = Cave_Exits + Dungeon_Exits + Cave_Three_Exits + Old_Man_House + \
            ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)',
             'Kakariko Well Exit', 'Bat Cave Exit', 'North Fairy Cave Exit', 'Lost Woods Hideout Exit', 'Lumberjack Tree Exit', 'Sanctuary Exit']

        hole_entrances = ['Kakariko Well Drop', 'Bat Cave Drop', 'North Fairy Cave Drop', 'Lost Woods Hideout Drop', 'Lumberjack Tree Tree', 'Sanctuary Grave',
                          'Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole']

        hole_targets = ['Kakariko Well (top)', 'Bat Cave (right)', 'North Fairy Cave', 'Lost Woods Hideout (top)', 'Lumberjack Tree (top)', 'Sewer Drop', 'Skull Back Drop',
                        'Skull Left Drop', 'Skull Pinball', 'Skull Pot Circle']

        if world.mode[player] == 'standard':
            connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
            connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance', player)
            connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit', player)
            caves.append(('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))
        else:
            hole_entrances.append('Hyrule Castle Secret Entrance Drop')
            hole_targets.append('Hyrule Castle Secret Entrance')
            caves.append('Hyrule Castle Secret Entrance Exit')
            caves.append(('Hyrule Castle Exit (South)', 'Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)'))

        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
            connect_two_way(world, 'Pyramid Entrance' if not world.is_tile_swapped(0x1b, player) else 'Inverted Pyramid Entrance', 'Pyramid Exit', player)
            connect_entrance(world, 'Pyramid Hole' if not world.is_tile_swapped(0x1b, player) else 'Inverted Pyramid Hole', 'Pyramid', player)
        else:
            caves.extend(['Ganons Tower Exit', 'Pyramid Exit'])
            hole_entrances.append('Pyramid Hole' if not world.is_tile_swapped(0x1b, player) else 'Inverted Pyramid Hole')
            hole_targets.append('Pyramid')

        # shuffle holes
        random.shuffle(hole_entrances)
        random.shuffle(hole_targets)
        for hole in hole_entrances:
            connect_entrance(world, hole, hole_targets.pop(), player)

        # place dark sanc
        if invFlag:
            place_dark_sanc(world, player)

        # place links house
        links_house = place_links_house(world, player)

        # place blacksmith, place sanc exit first for additional blacksmith candidates
        doors = list(entrance_pool)
        random.shuffle(doors)
        door = doors.pop()
        connect_entrance(world, door, 'Sanctuary Exit', player, False)
        doors = [e for e in doors if e not in entrance_exits]
        door = doors.pop()
        connect_exit(world, 'Sanctuary Exit', door, player, False)
        caves.remove('Sanctuary Exit')
        place_blacksmith(world, links_house, player)

        # place connectors in inaccessible regions
        pool = list(entrance_pool)
        if world.mode[player] == 'standard' and 'Bonk Fairy (Light)' in pool:
            pool.remove('Bonk Fairy (Light)')
        connect_inaccessible_regions(world, pool, [], caves, player)
        
        # place old man, has limited options
        pool = [e for e in pool if e in entrance_pool]
        place_old_man(world, pool, player)
        caves.append('Old Man Cave Exit (West)')

        # place bomb shop, has limited options
        if not world.is_bombshop_start(player):
            bomb_shop_doors = list(entrance_pool)
            if world.logic[player] in ['noglitches', 'minorglitches'] or world.is_tile_swapped(0x1b, player):
                bomb_shop_doors = [e for e in entrance_pool if e not in ['Pyramid Fairy']]
            if world.is_tile_swapped(0x03, player):
                bomb_shop_doors = [x for x in bomb_shop_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
            random.shuffle(bomb_shop_doors)
            bomb_shop = bomb_shop_doors.pop()
            pool.remove(bomb_shop)
            connect_entrance(world, bomb_shop, 'Big Bomb Shop', player)
            
        # shuffle connectors
        doors = list(entrance_pool)
        if world.mode[player] == 'standard' and 'Bonk Fairy (Light)' in doors:
            doors.remove('Bonk Fairy (Light)')
        exit_doors = [e for e in entrance_pool if e not in entrance_exits]
        random.shuffle(doors)
        random.shuffle(exit_doors)
        for cave in caves:
            if isinstance(cave, str):
                cave = (cave,)
            for exit in cave:
                connect_exit(world, exit, exit_doors.pop(), player, False)
                connect_entrance(world, doors.pop(), exit, player, False)

        # place remaining doors
        connect_doors(world, list(entrance_pool), list(exit_pool), player)
    else:
        raise NotImplementedError('Shuffling not supported yet')
    
    # ensure Houlihan exits where Links House does
    # TODO: Plando should overrule this
    if not links_house:
        for links_house in world.get_entrance('Links House Exit' if not world.is_bombshop_start(player) else 'Big Bomb Shop Exit', player).connected_region.exits:
            if links_house.connected_region and links_house.connected_region.name == ('Links House' if not world.is_bombshop_start(player) else 'Big Bomb Shop'):
                links_house = links_house.name
                break
    connect_exit(world, 'Chris Houlihan Room Exit', links_house, player)
    ignore_pool = True

    # check for swamp palace fix
    if not (world.get_entrance('Dam', player).connected_region.name in ['Dam', 'Swamp Portal'] and world.get_entrance('Swamp Palace', player).connected_region.name in ['Dam', 'Swamp Portal']):
        world.swamp_patch_required[player] = True

    # check for potion shop location
    if world.get_entrance('Potion Shop', player).connected_region.name != 'Potion Shop':
        world.powder_patch_required[player] = True

    # check for ganon location
    if world.get_entrance('Pyramid Hole' if not world.is_tile_swapped(0x1b, player) else 'Inverted Pyramid Hole', player).connected_region.name != 'Pyramid':
        world.ganon_at_pyramid[player] = False

    # check for Ganon's Tower location
    if world.get_entrance('Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', player).connected_region.name != 'Ganons Tower Portal':
        world.ganonstower_vanilla[player] = False


def connect_custom(world, player):
    if hasattr(world, 'custom_entrances') and world.custom_entrances[player]:
        for exit_name, region_name in world.custom_entrances[player]:
            # doesn't actually change addresses
            connect_simple(world, exit_name, region_name, player)
    # this needs to remove custom connections from the pool


def connect_simple(world, exitname, regionname, player):
    world.get_entrance(exitname, player).connect(world.get_region(regionname, player))


def connect_logical(world, entrancename, exitname, player, isTwoWay = False):
    if not ignore_pool:
        logging.getLogger('').debug('Connecting %s -> %s', entrancename, exitname)
        assert entrancename in entrance_pool, 'Entrance not in pool: ' + entrancename
        assert exitname in exit_pool, 'Exit not in pool: ' + exitname
    
    try:
        region = world.get_region(exitname, player)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname, player)
        region = exit.parent_region

    connect_simple(world, entrancename, region.name, player)
    if isTwoWay:
        region = world.get_entrance(entrancename, player).parent_region
        connect_simple(world, exitname, region.name, player)
    
    if not ignore_pool:
        entrance_pool.remove(entrancename)
        exit_pool.remove(exitname)


def connect_entrance(world, entrancename, exitname, player, mark_two_way=True):
    if not ignore_pool:
        logging.getLogger('').debug('Connecting %s -> %s', entrancename, exitname)
        assert entrancename in entrance_pool, f'Entrance not in pool: {entrancename}'
        if mark_two_way:
            assert exitname in exit_pool, f'Exit not in pool: {exitname}'
    
    entrance = world.get_entrance(entrancename, player)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname, player)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname, player)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0]

    entrance.connect(region, addresses, target)

    if not ignore_pool:
        entrance_pool.remove(entrancename)
        if mark_two_way:
            exit_pool.remove(exitname)
    
    if not suppress_spoiler:
        world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance', player)


def connect_exit(world, exitname, entrancename, player, mark_two_way=True):
    if not (ignore_pool or exitname == 'Chris Houlihan Room Exit'):
        logging.getLogger('').debug('Connecting %s -> %s', exitname, entrancename)
        if mark_two_way:
            assert entrancename in entrance_pool, 'Entrance not in pool: ' + entrancename
        assert exitname in exit_pool, 'Exit not in pool: ' + exitname
    
    entrance = world.get_entrance(entrancename, player)
    exit = world.get_entrance(exitname, player)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    
    if not (ignore_pool or exitname == 'Chris Houlihan Room Exit'):
        if mark_two_way:
            entrance_pool.remove(entrancename)
        elif world.shuffle[player] == 'insanity':
            entrance_exits.append(entrancename)
        exit_pool.remove(exitname)
    
    if not suppress_spoiler:
        world.spoiler.set_entrance(entrance.name, exit.name, 'exit', player)


def connect_two_way(world, entrancename, exitname, player):
    if not ignore_pool:
        logging.getLogger('').debug('Connecting %s <-> %s', entrancename, exitname)
        assert entrancename in entrance_pool, 'Entrance not in pool: ' + entrancename
        assert exitname in exit_pool, 'Exit not in pool: ' + exitname
    
    entrance = world.get_entrance(entrancename, player)
    exit = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    entrance.connect(exit.parent_region, door_addresses[entrance.name][0], exit_ids[exit.name][0])
    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    
    if not ignore_pool:
        entrance_pool.remove(entrancename)
        exit_pool.remove(exitname)
        if world.shuffle[player] == 'insanity':
            entrance_exits.append(entrancename)
    
    if not suppress_spoiler:
        world.spoiler.set_entrance(entrance.name, exit.name, 'both', player)


def connect_random(world, exitlist, targetlist, player, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target, player)
        else:
            connect_entrance(world, exit, target, player)


def connect_mandatory_exits(world, entrances, caves, must_be_exits, player, must_deplete_mustexits=True):
    # Keeps track of entrances that cannot be used to access each exit / cave
    invalid_cave_connections = defaultdict(set)

    # if world.logic[player] in ['owglitches', 'hybridglitches', 'nologic']:
    #     import OverworldGlitchRules
    #     for entrance in OverworldGlitchRules.get_non_mandatory_exits(world, player):
    #         if entrance in must_be_exits:
    #             must_be_exits.remove(entrance)
    #             entrances.append(entrance)

    # for insanity use only
    def extract_reachable_exit(cavelist):
        candidate = None
        for cave in cavelist:
            if isinstance(cave, tuple) and len(cave) > 1:
                # special handling: TRock has two entries that we should consider entrance only
                # ToDo this should be handled in a more sensible manner
                if cave[0] in ['Turtle Rock Exit (Front)', 'Spectacle Rock Cave Exit (Peak)'] and len(cave) == 2:
                    continue
                candidate = cave
                break
        if candidate is None:
            raise RuntimeError('No suitable cave.')
        return candidate

    """This works inplace"""
    random.shuffle(entrances)
    random.shuffle(caves)
    
    used_caves = []
    required_entrances = 0  # Number of entrances reserved for used_caves
    skip_remaining = False
    while must_be_exits and not skip_remaining:
        exit = must_be_exits.pop()

        # find multi exit cave
        # * this is a mess, but it ensures a loose assignment possibility when the cave/entrance pool is plentiful,
        # *   but can also find and prepare for solutions when the cave/entrance pool is limiting
        # * however, this probably could be better implemented
        cave = None
        if world.shuffle[player] == 'insanity':
            cave = extract_reachable_exit(caves)
        else:
            if must_deplete_mustexits:
                cave_surplus = sum(0 if isinstance(x, str) else len(x) - 1 for x in caves) - (len(must_be_exits) + 1)
                if cave_surplus < 0:
                    raise RuntimeError('Not enough multi-entrance caves left to connect unreachable regions!')
                if len(entrances) < len(must_be_exits) + 1:
                    raise RuntimeError('Not enough entrances left to connect unreachable regions!')
                if cave_surplus > len(must_be_exits):
                    for candidate in caves:
                        if not isinstance(candidate, str) and (candidate in used_caves or len(candidate) < len(entrances) - required_entrances - 1):
                            cave = candidate
                            break
                if len(must_be_exits) == 0: # if assigning last must exit
                    for candidate in caves:
                        if not isinstance(candidate, str) and (candidate in used_caves or len(candidate) <= len(entrances) - required_entrances - 1):
                            cave = candidate
                            break
                if cave is None and cave_surplus <= 1: # if options are limited
                    # attempt to find use caves already used
                    for candidate in caves:
                        if not isinstance(candidate, str) and candidate in used_caves:
                            cave = candidate
                            break
                    if cave is None:
                        # attempt to find caves with exact number of exits
                        for candidate in caves:
                            if not isinstance(candidate, str) and (len(entrances) - required_entrances - 1) - len(candidate) == 0:
                                cave = candidate
                                break
                    if cave is None:
                        # attempt to find caves with one left over exit
                        for candidate in caves:
                            if not isinstance(candidate, str) and (len(entrances) - required_entrances - 1) - len(candidate) == 1:
                                cave = candidate
                                break
            
            if cave is None:
                for candidate in caves:
                    if not isinstance(candidate, str) and (candidate in used_caves or len(candidate) < len(entrances) - required_entrances - 1):
                        cave = candidate
                        break
            if cave is None and must_deplete_mustexits:
                for candidate in caves:
                    if not isinstance(candidate, str) and (candidate in used_caves or len(candidate) <= len(entrances) - required_entrances - 1):
                        cave = candidate
                        break

        inaccessible_entrances = list()
        for region_name in world.inaccessible_regions[player]:
            region = world.get_region(region_name, player)
            if region.type in [RegionType.LightWorld, RegionType.DarkWorld]:
                for x in region.exits:
                    if not x.connected_region and x.name in entrance_pool:
                        inaccessible_entrances.append(x.name)

        if cave is None:
            if must_deplete_mustexits:
                raise RuntimeError('No more caves left. Should not happen!')
            else:
                must_be_exits.append(exit)
                skip_remaining = True
                continue

        # all caves are sorted so that the last exit is always reachable
        if world.shuffle[player] == 'insanity':
            connect_exit(world, cave[-1], exit, player, False)
            entrance = next(e for e in entrances[::-1] if e not in entrance_exits + inaccessible_entrances + list(invalid_cave_connections[tuple(cave)]))
            entrances.remove(entrance)
            connect_entrance(world, entrance, cave[-1], player, False)
        else:
            connect_two_way(world, exit, cave[-1], player)
        
        if len(cave) == 2:
            entrance = next(e for e in entrances[::-1] if e not in inaccessible_entrances and e not in invalid_cave_connections[tuple(cave)])
            entrances.remove(entrance)
            if world.shuffle[player] == 'insanity':
                connect_entrance(world, entrance, cave[0], player, False)
                entrance = next(e for e in entrances[::-1] if e not in entrance_exits + inaccessible_entrances + list(invalid_cave_connections[tuple(cave)]))
                entrances.remove(entrance)
                connect_exit(world, cave[0], entrance, player, False)
            else:
                connect_two_way(world, entrance, cave[0], player)
            if cave in used_caves:
                required_entrances -= 2
                used_caves.remove(cave)
        elif cave[-1] == 'Spectacle Rock Cave Exit': # Spectacle rock only has one exit
            cave_entrances = []
            for cave_exit in cave[:-1]:
                entrance = next(e for e in entrances[::-1] if e not in inaccessible_entrances)
                cave_entrances.append(entrance)
                entrances.remove(entrance)
                if world.shuffle[player] == 'insanity':
                    connect_entrance(world, entrance, cave_exit, player, False)
                    entrance = next(e for e in entrances[::-1] if e not in entrance_exits + inaccessible_entrances)
                    cave_entrances.append(entrance)
                    entrances.remove(entrance)
                    connect_exit(world, cave_exit, entrance, player, False)
                else:
                    connect_two_way(world, entrance, cave_exit, player)
        else: # save for later so we can connect to multiple exits
            if cave in used_caves:
                required_entrances -= 1
                used_caves.remove(cave)
            else:
                required_entrances += len(cave)-1
            caves.append(cave[0:-1])
            random.shuffle(caves)
            used_caves.append(cave[0:-1])
            invalid_cave_connections[tuple(cave[0:-1])] = invalid_cave_connections[tuple(cave)].union(inaccessible_entrances).union(entrance_exits)
        caves.remove(cave)

        find_inaccessible_regions(world, player)
        
    for cave in used_caves:
        if cave in caves: # check if we placed multiple entrances from this 3 or 4 exit 
            for cave_exit in cave:
                entrance = next(e for e in entrances[::-1] if e not in inaccessible_entrances and e not in invalid_cave_connections[tuple(cave)])
                invalid_cave_connections[tuple(cave)] = set()
                entrances.remove(entrance)
                if world.shuffle[player] == 'insanity':
                    connect_entrance(world, entrance, cave_exit, player, False)
                    entrance = next(e for e in entrances[::-1] if e not in entrance_exits + inaccessible_entrances + list(invalid_cave_connections[tuple(cave)]))
                    entrances.remove(entrance)
                    connect_exit(world, cave_exit, entrance, player, False)
                else:
                    connect_two_way(world, entrance, cave_exit, player)
            caves.remove(cave)


def connect_caves(world, lw_entrances, dw_entrances, caves, player):
    """This works inplace"""
    random.shuffle(lw_entrances)
    random.shuffle(dw_entrances)
    random.shuffle(caves)
    while caves:
        # connect highest exit count caves first, prevent issue where we have 2 or 3 exits accross worlds left to fill
        cave_candidate = (None, 0)
        for i, cave in enumerate(caves):
            if isinstance(cave, str):
                cave = (cave,)
            if len(cave) > cave_candidate[1]:
                cave_candidate = (i, len(cave))
        cave = caves.pop(cave_candidate[0])

        target = lw_entrances if random.randint(0, 1) == 0 else dw_entrances
        if isinstance(cave, str):
            cave = (cave,)

        # check if we can still fit the cave into our target group
        if len(target) < len(cave):
            # need to use other set
            target = lw_entrances if target is dw_entrances else dw_entrances

        for exit in cave:
            connect_two_way(world, target.pop(), exit, player)


def connect_doors(world, doors, targets, player):
    """This works inplace"""
    random.shuffle(doors)
    random.shuffle(targets)
    placing = min(len(doors), len(targets))
    for door, target in zip(doors, targets):
        connect_entrance(world, door, target, player)
    doors[:] = doors[placing:]
    targets[:] = targets[placing:]


def scramble_holes(world, player):
    invFlag = world.mode[player] == 'inverted'

    hole_entrances = [('Kakariko Well Cave', 'Kakariko Well Drop'),
                      ('Bat Cave Cave', 'Bat Cave Drop'),
                      ('North Fairy Cave', 'North Fairy Cave Drop'),
                      ('Lost Woods Hideout Stump', 'Lost Woods Hideout Drop'),
                      ('Lumberjack Tree Cave', 'Lumberjack Tree Tree'),
                      ('Sanctuary', 'Sanctuary Grave')]

    hole_targets = [('Kakariko Well Exit', 'Kakariko Well (top)'),
                    ('Bat Cave Exit', 'Bat Cave (right)'),
                    ('North Fairy Cave Exit', 'North Fairy Cave'),
                    ('Lost Woods Hideout Exit', 'Lost Woods Hideout (top)'),
                    ('Lumberjack Tree Exit', 'Lumberjack Tree (top)')]

    # force uncle cave
    if world.mode[player] == 'standard':
        connect_two_way(world, 'Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit', player)
        connect_entrance(world, 'Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance', player)
    else:
        hole_entrances.append(('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Drop'))
        hole_targets.append(('Hyrule Castle Secret Entrance Exit', 'Hyrule Castle Secret Entrance'))
    
    if world.shuffle_ganon[player]:
        hole_entrances.append(('Pyramid Entrance', 'Pyramid Hole') if not world.is_tile_swapped(0x1b, player) else ('Inverted Pyramid Entrance', 'Inverted Pyramid Hole'))
        hole_targets.append(('Pyramid Exit', 'Pyramid'))

    # shuffle sanctuary hole in same world as other HC entrances
    if world.shuffle[player] not in ['lean', 'crossed']:
        drop_owid_map = { #                         owid, is_light_world
            'Lost Woods Hideout Stump':             (0x00, True),
            'Lumberjack Tree Cave':                 (0x02, True),
            'Sanctuary':                            (0x13, True),
            'North Fairy Cave':                     (0x15, True),
            'Kakariko Well Cave':                   (0x18, True),
            'Hyrule Castle Secret Entrance Stairs': (0x1b, True),
            'Bat Cave Cave':                        (0x22, True),
            'Inverted Pyramid Entrance':            (0x1b, True),
            'Pyramid Entrance':                     (0x5b, False)
        }

        region = world.get_entrance('Hyrule Castle Exit (South)', player).parent_region
        if len(region.entrances) > 0:
            hc_in_lw = region.entrances[0].parent_region.type == (RegionType.LightWorld if not invFlag else RegionType.DarkWorld)
        elif world.shuffle[player] == 'lite':
            hc_in_lw = not invFlag
        else:
            # checks if drop candidates exist in LW
            drop_owids = [ 0x00, 0x02, 0x13, 0x15, 0x18, 0x1b, 0x22 ]
            hc_in_lw = any([not world.is_tile_swapped(owid, player) for owid in drop_owids])

        candidate_drops = list()
        for door, drop in hole_entrances:
            if hc_in_lw == (drop_owid_map[door][1] == (not world.is_tile_swapped(drop_owid_map[door][0], player))):
                candidate_drops.append(tuple((door, drop)))
        
        random.shuffle(candidate_drops)
        door, drop = candidate_drops.pop()
        hole_entrances.remove((door, drop))
        connect_two_way(world, door, 'Sanctuary Exit', player)
        connect_entrance(world, drop, 'Sewer Drop', player)
    else:
        hole_targets.append(('Sanctuary Exit', 'Sewer Drop'))

    # place pyramid hole
    if not world.shuffle_ganon[player]:
        exit, target = ('Pyramid Exit', 'Pyramid')
        if not world.is_tile_swapped(0x1b, player):
            connect_two_way(world, 'Pyramid Entrance', exit, player)
            connect_entrance(world, 'Pyramid Hole', target, player)
        else:
            connect_two_way(world, 'Inverted Pyramid Entrance', exit, player)
            connect_entrance(world, 'Inverted Pyramid Hole', target, player)

    # shuffle the rest
    random.shuffle(hole_entrances)
    random.shuffle(hole_targets)
    for entrance, drop in hole_entrances:
        exit, target = hole_targets.pop()
        connect_two_way(world, entrance, exit, player)
        connect_entrance(world, drop, target, player)


def skull_woods_shuffle(world, player):
    connect_random(world, ['Skull Woods First Section Hole (East)', 'Skull Woods First Section Hole (West)', 'Skull Woods First Section Hole (North)', 'Skull Woods Second Section Hole'],
                   ['Skull Left Drop', 'Skull Pinball', 'Skull Pot Circle', 'Skull Back Drop'], player)
    connect_random(world, ['Skull Woods First Section Door', 'Skull Woods Second Section Door (East)', 'Skull Woods Second Section Door (West)'],
                   ['Skull Woods First Section Exit', 'Skull Woods Second Section Exit (East)', 'Skull Woods Second Section Exit (West)'], player, True)


def simple_shuffle_dungeons(world, player):
    invFlag = world.mode[player] == 'inverted'

    skull_woods_shuffle(world, player)

    dungeon_entrances = ['Eastern Palace', 'Tower of Hera', 'Thieves Town', 'Skull Woods Final Section', 'Palace of Darkness', 'Ice Palace', 'Misery Mire', 'Swamp Palace']
    dungeon_exits = ['Eastern Palace Exit', 'Tower of Hera Exit', 'Agahnims Tower Exit', 'Thieves Town Exit', 'Skull Woods Final Section Exit', 'Palace of Darkness Exit', 'Ice Palace Exit', 'Misery Mire Exit', 'Swamp Palace Exit']

    if not invFlag:
        if not world.shuffle_ganon[player]:
            connect_two_way(world, 'Ganons Tower', 'Ganons Tower Exit', player)
        else:
            dungeon_entrances.append('Ganons Tower')
            dungeon_exits.append('Ganons Tower Exit')
        random.shuffle(dungeon_exits)
        at_door = dungeon_exits.pop()
    else:
        dungeon_entrances.append('Ganons Tower')
        if not world.shuffle_ganon[player]:
            at_door = 'Ganons Tower Exit'
        else:
            dungeon_exits.append('Ganons Tower Exit')
            random.shuffle(dungeon_exits)
            at_door = dungeon_exits.pop()

    # shuffle single-entrance dungeons
    connect_random(world, dungeon_entrances, dungeon_exits, player, True)

    # shuffle multi-entrance dungeons
    multi_dungeons = ['Desert Palace', 'Turtle Rock']
    if world.mode[player] == 'standard' or (world.mode[player] == 'inverted' and not world.shuffle_ganon):
        hc_target = 'Hyrule Castle'
        random.shuffle(multi_dungeons)
    else:
        multi_dungeons.append('Hyrule Castle')
        
        dungeon_owid_map = { # owid, is_lw_dungeon
            'Hyrule Castle': (0x1b, True),
            'Desert Palace': (0x30, True),
            'Turtle Rock':   (0x47, False)
        }
        
        # checks if drop candidates exist in LW
        drop_owids = [ 0x00, 0x02, 0x13, 0x15, 0x18, 0x1b, 0x22 ]
        drops_in_light_world = any([not world.is_tile_swapped(owid, player) for owid in drop_owids])
        
        # placing HC in guaranteed same-world as available dropdowns
        if not drops_in_light_world or not invFlag:
            candidate_dungeons = list()
            for d in multi_dungeons:
                if not drops_in_light_world and dungeon_owid_map[d][1] == world.is_tile_swapped(dungeon_owid_map[d][0], player):
                    # only adding DW candidates
                    candidate_dungeons.append(d)
                elif not invFlag and dungeon_owid_map[d][1] == (not world.is_tile_swapped(dungeon_owid_map[d][0], player)):
                    # only adding LW candidates
                    candidate_dungeons.append(d)
            random.shuffle(candidate_dungeons)
            hc_target = candidate_dungeons.pop()
            multi_dungeons.remove(hc_target)
            random.shuffle(multi_dungeons)
        else:
            random.shuffle(multi_dungeons)
            hc_target = multi_dungeons.pop()

    dp_target = multi_dungeons.pop()
    tr_target = multi_dungeons.pop()
    
    if hc_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)', player)
        connect_two_way(world, 'Agahnims Tower', at_door, player)
    elif hc_target == 'Desert Palace':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Hyrule Castle Exit (South)', player)
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Hyrule Castle Exit (East)', player)
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Hyrule Castle Exit (West)', player)
        connect_two_way(world, 'Desert Palace Entrance (North)', at_door, player)
    elif hc_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Hyrule Castle Exit (South)', player)
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Hyrule Castle Exit (West)', player)
        if not world.is_tile_swapped(0x45, player):
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Hyrule Castle Exit (East)', player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', at_door, player)
        else:
            connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', at_door, player)
            connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Hyrule Castle Exit (East)', player)
   
    if dp_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Desert Palace Exit (South)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Desert Palace Exit (East)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Desert Palace Exit (West)', player)
        connect_two_way(world, 'Agahnims Tower', 'Desert Palace Exit (North)', player)
    elif dp_target == 'Desert Palace':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Desert Palace Exit (South)', player)
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Desert Palace Exit (East)', player)
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Desert Palace Exit (West)', player)
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Desert Palace Exit (North)', player)
    elif dp_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Desert Palace Exit (South)', player)
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Desert Palace Exit (East)', player)
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Desert Palace Exit (West)', player)
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Desert Palace Exit (North)', player)
        
    if tr_target == 'Hyrule Castle':
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Turtle Rock Exit (Front)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (East)', 'Turtle Rock Ledge Exit (East)', player)
        connect_two_way(world, 'Hyrule Castle Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
        connect_two_way(world, 'Agahnims Tower', 'Turtle Rock Isolated Ledge Exit', player)
    elif tr_target == 'Desert Palace':
        connect_two_way(world, 'Desert Palace Entrance (South)', 'Turtle Rock Exit (Front)', player)
        connect_two_way(world, 'Desert Palace Entrance (North)', 'Turtle Rock Ledge Exit (East)', player)
        connect_two_way(world, 'Desert Palace Entrance (West)', 'Turtle Rock Ledge Exit (West)', player)
        connect_two_way(world, 'Desert Palace Entrance (East)', 'Turtle Rock Isolated Ledge Exit', player)
    elif tr_target == 'Turtle Rock':
        connect_two_way(world, 'Turtle Rock', 'Turtle Rock Exit (Front)', player)
        connect_two_way(world, 'Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit', player)
        connect_two_way(world, 'Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)', player)
        connect_two_way(world, 'Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)', player)


def full_shuffle_dungeons(world, Dungeon_Exits, player):
    invFlag = world.mode[player] == 'inverted'

    skull_woods_shuffle(world, player)

    dungeon_exits = list(Dungeon_Exits)

    if world.mode[player] == 'standard':
        # must connect front of hyrule castle to do escape
        connect_two_way(world, 'Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)', player)
    
    if not world.shuffle_ganon[player]:
        connect_two_way(world, 'Ganons Tower' if not world.is_atgt_swapped(player) else 'Agahnims Tower', 'Ganons Tower Exit', player)
    else:
        dungeon_exits.append('Ganons Tower Exit')

    # determine LW and DW entrances
    #                   owid: (entrances, is_light_world)
    dungeon_owid_map = {0x03: ({'Tower of Hera'}, True),
                        0x1e: ({'Eastern Palace'}, True),
                        0x1b: ({'Hyrule Castle Entrance (South)',
                                'Hyrule Castle Entrance (West)',
                                'Hyrule Castle Entrance (East)',
                                'Agahnims Tower'}, True),
                        0x30: ({'Desert Palace Entrance (South)',
                                'Desert Palace Entrance (West)',
                                'Desert Palace Entrance (East)',
                                'Desert Palace Entrance (North)'}, True),
                        0x40: ({'Skull Woods Final Section'}, False),
                        0x43: ({'Ganons Tower'}, False),
                        0x45: ({'Dark Death Mountain Ledge (West)',
                                'Dark Death Mountain Ledge (East)',
                                'Turtle Rock Isolated Ledge Entrance'}, False),
                        0x47: ({'Turtle Rock'}, False),
                        0x58: ({'Thieves Town'}, False),
                        0x5e: ({'Palace of Darkness'}, False),
                        0x70: ({'Misery Mire'}, False),
                        0x75: ({'Ice Palace'}, False),
                        0x7b: ({'Swamp Palace'}, False)
    }

    lw_entrances = list()
    dw_entrances = list()
    for owid in dungeon_owid_map.keys():
        if dungeon_owid_map[owid][1] == (not world.is_tile_swapped(owid, player)):
            lw_entrances.extend([e for e in dungeon_owid_map[owid][0] if e in entrance_pool])
        else:
            dw_entrances.extend([e for e in dungeon_owid_map[owid][0] if e in entrance_pool])
    
    # determine must-exit entrances
    find_inaccessible_regions(world, player)

    lw_must_exit = list()
    dw_must_exit = list()
    lw_related = list()
    dw_related = list()
    if not world.is_tile_swapped(0x45, player):
        dw_entrances.remove('Turtle Rock Isolated Ledge Entrance')
        dw_must_exit.append('Turtle Rock Isolated Ledge Entrance')
        if 'Dark Death Mountain Ledge' in world.inaccessible_regions[player]:
            ledge = ['Dark Death Mountain Ledge (West)', 'Dark Death Mountain Ledge (East)']
            dw_entrances = [e for e in dw_entrances if e not in ledge]
            random.shuffle(ledge)
            dw_must_exit.append(ledge.pop())
            dw_related.extend(ledge)
    if not world.is_tile_swapped(0x30, player):
        if 'Desert Mouth' in world.inaccessible_regions[player]:
            lw_entrances.remove('Desert Palace Entrance (East)')
            lw_must_exit.append('Desert Palace Entrance (East)')
    else:
        dw_entrances.remove('Desert Palace Entrance (East)')
        dw_must_exit.append('Desert Palace Entrance (East)')
        if 'Desert Ledge' in world.inaccessible_regions[player]:
            ledge = ['Desert Palace Entrance (West)', 'Desert Palace Entrance (North)']
            dw_entrances = [e for e in dw_entrances if e not in ledge]
            random.shuffle(ledge)
            dw_must_exit.append(ledge.pop())
            dw_related.extend(ledge)
    if not world.is_tile_swapped(0x1b, player):
        if 'Hyrule Castle Ledge' in world.inaccessible_regions[player]:
            ledge = ['Hyrule Castle Entrance (West)', 'Hyrule Castle Entrance (East)', 'Agahnims Tower']
            lw_entrances = [e for e in lw_entrances if e not in ledge]
            random.shuffle(ledge)
            lw_must_exit.append(ledge.pop())
            lw_related.extend(ledge)
    random.shuffle(lw_must_exit)
    random.shuffle(dw_must_exit)
    
    # place HC first, needs to be same world as Sanc drop
    hyrule_castle_exits = ('Hyrule Castle Exit (West)', 'Hyrule Castle Exit (East)', 'Hyrule Castle Exit (South)')
    hyrule_castle_exits = list([tuple(e for e in hyrule_castle_exits if e in exit_pool)])
    hyrule_castle_exits.extend([e for e in dungeon_exits if isinstance(e, str)])
    dungeon_exits = [e for e in dungeon_exits if not isinstance(e, str)]
    if not world.is_tile_swapped(0x13, player):
        connect_mandatory_exits(world, lw_entrances, hyrule_castle_exits, lw_must_exit, player, False)
        dungeon_exits.extend([e for e in hyrule_castle_exits if isinstance(e, str)])
        hyrule_castle_exits = [e for e in hyrule_castle_exits if not isinstance(e, str)]
        connect_caves(world, lw_entrances, [], hyrule_castle_exits, player)
    else:
        connect_mandatory_exits(world, dw_entrances, hyrule_castle_exits, dw_must_exit, player, False)
        dungeon_exits.extend([e for e in hyrule_castle_exits if isinstance(e, str)])
        hyrule_castle_exits = [e for e in hyrule_castle_exits if not isinstance(e, str)]
        connect_caves(world, [], dw_entrances, hyrule_castle_exits, player)
    
    # connect any remaining must-exit entrances
    dungeon_exits.extend(hyrule_castle_exits)
    connect_mandatory_exits(world, lw_entrances, dungeon_exits, lw_must_exit, player)
    connect_mandatory_exits(world, dw_entrances, dungeon_exits, dw_must_exit, player)

    # shuffle the remaining entrances
    lw_entrances = lw_entrances + lw_related
    dw_entrances = dw_entrances + dw_related
    connect_caves(world, lw_entrances, dw_entrances, dungeon_exits, player)


def place_links_house(world, player, ignore_list=[]):
    invFlag = world.mode[player] == 'inverted'
    if world.mode[player] == 'standard' or not world.shufflelinks[player]:
        links_house = 'Links House' if not world.is_bombshop_start(player) else 'Big Bomb Shop'
    else:
        if invFlag:
            for dark_sanc in world.get_entrance('Dark Sanctuary Hint Exit', player).connected_region.exits:
                if dark_sanc.connected_region and dark_sanc.connected_region.name == 'Dark Sanctuary Hint':
                    dark_sanc = dark_sanc.name
                    break
        
        if invFlag and isinstance(dark_sanc, str):
            links_house_doors = [i for i in get_distant_entrances(world, dark_sanc, player) if i in entrance_pool]
        else:
            links_house_doors = [i for i in get_starting_entrances(world, player, world.shuffle[player] != 'insanity') if i in entrance_pool]
        if world.is_bombshop_start(player) and world.is_tile_swapped(0x03, player):
            links_house_doors = [x for x in links_house_doors if x not in ['Spectacle Rock Cave', 'Spectacle Rock Cave (Bottom)']]
        if world.shuffle[player] in ['lite', 'lean']:
            links_house_doors = [e for e in links_house_doors if e in list(zip(*(default_item_connections +
               (default_shop_connections if world.shopsanity[player] else []) +
               (default_pot_connections if world.pottery[player] not in ['none', 'keys', 'dungeon'] else []) +
               (default_takeany_connections if world.take_any[player] == 'fixed' else []))))[0]]
        
        #TODO: Need to improve Links House placement to choose a better sector or eliminate entrances that are after ledge drops
        links_house_doors = [e for e in links_house_doors if e not in ignore_list]
        assert len(links_house_doors), 'No valid candidates to place Links House'
        links_house = random.choice(links_house_doors)
    if not world.is_bombshop_start(player):
        connect_two_way(world, links_house, 'Links House Exit', player)
    else:
        connect_entrance(world, links_house, 'Big Bomb Shop', player)
        world.get_entrance('Big Bomb Shop Exit', player).connect(world.get_entrance(links_house, player).parent_region)
    return links_house


def place_dark_sanc(world, player, ignore_list=[]):
    if not world.shufflelinks[player]:
        sanc_doors = [i for i in get_distant_entrances(world, 'Big Bomb Shop' if world.is_bombshop_start(player) else 'Links House', player) if i in entrance_pool]
    else:
        sanc_doors = [i for i in get_starting_entrances(world, player, world.shuffle[player] != 'insanity') if i in entrance_pool]
    if world.shuffle[player] in ['lite', 'lean']:
        sanc_doors = [e for e in sanc_doors if e in list(zip(*(default_item_connections + (default_shop_connections if world.shopsanity[player] else []))))[0]]
    
    sanc_doors = [e for e in sanc_doors if e not in ignore_list]
    assert len(sanc_doors), 'No valid candidates to place Dark Chapel'
    sanc_door = random.choice(sanc_doors)
    connect_entrance(world, sanc_door, 'Dark Sanctuary Hint', player)
    world.get_entrance('Dark Sanctuary Hint Exit', player).connect(world.get_entrance(sanc_door, player).parent_region)
    return sanc_door


def place_blacksmith(world, links_house, player):
    invFlag = world.mode[player] == 'inverted'
    
    assumed_inventory = list()
    if world.logic[player] in ['noglitches', 'minorglitches'] and (world.is_tile_swapped(0x29, player) == invFlag):
        assumed_inventory.append('Titans Mitts')
    
    links_region = world.get_entrance(links_house, player).parent_region.name
    blacksmith_doors = list(build_accessible_entrance_list(world, links_region, player, assumed_inventory, False, True, True))
    
    if invFlag:
        dark_sanc = world.get_entrance('Dark Sanctuary Hint Exit', player).connected_region.name
        blacksmith_doors = list(OrderedDict.fromkeys(blacksmith_doors + list(build_accessible_entrance_list(world, dark_sanc, player, assumed_inventory, False, True, True))))
    elif world.doorShuffle[player] == 'vanilla' or world.intensity[player] < 3:
        sanc_region = world.get_entrance('Sanctuary Exit', player).connected_region.name
        blacksmith_doors = list(OrderedDict.fromkeys(blacksmith_doors + list(build_accessible_entrance_list(world, sanc_region, player, assumed_inventory, False, True, True))))
    if world.shuffle[player] in ['lite', 'lean']:
        blacksmith_doors = [e for e in blacksmith_doors if e in list(zip(*(default_item_connections +
           (default_shop_connections if world.shopsanity[player] else []) +
           (default_pot_connections if world.pottery[player] not in ['none', 'keys', 'dungeon'] else []) +
           (default_takeany_connections if world.take_any[player] == 'fixed' else []))))[0]]
    
    assert len(blacksmith_doors), 'No valid candidates to place Blacksmiths Hut'
    blacksmith_hut = random.choice(blacksmith_doors)
    connect_entrance(world, blacksmith_hut, 'Blacksmiths Hut', player)
    return blacksmith_hut


def place_old_man(world, pool, player, ignore_list=[]):
    # exit has to come from specific set of doors, the entrance is free to move about
    if not world.is_tile_swapped(0x03, player):
        region_name = 'West Death Mountain (Top)'
    else:
        region_name = 'West Dark Death Mountain (Top)'
    old_man_entrances = list(build_accessible_entrance_list(world, region_name, player, [], False, True, True, True))
    old_man_entrances = [e for e in old_man_entrances if e != 'Old Man House (Bottom)' and e not in ignore_list]
    if world.shuffle[player] in ['lite', 'lean']:
        old_man_entrances = [e for e in old_man_entrances if e in pool]
    assert len(old_man_entrances), 'No available entrances left to place Old Man Cave'
    random.shuffle(old_man_entrances)
    old_man_exit = None
    while not old_man_exit:
        old_man_exit = old_man_entrances.pop()
        if 'West Death Mountain (Bottom)' not in build_accessible_region_list(world, world.get_entrance(old_man_exit, player).parent_region.name, player, True, True):
            old_man_exit = None
    
    old_man_entrances = [e for e in pool if e in entrance_pool and e not in ignore_list and e not in entrance_exits + [old_man_exit]]
    random.shuffle(old_man_entrances)
    old_man_entrance = old_man_entrances.pop()
    if world.shuffle[player] != 'insanity':
        connect_two_way(world, old_man_exit, 'Old Man Cave Exit (East)', player)
        connect_two_way(world, old_man_entrance, 'Old Man Cave Exit (West)', player)
    else:
        # skip assigning connections to West Entrance/Exit
        connect_exit(world, 'Old Man Cave Exit (East)', old_man_exit, player, False)
        connect_entrance(world, old_man_entrance, 'Old Man Cave Exit (East)', player, False)


def junk_fill_inaccessible(world, player):
    from Main import copy_world_premature
    find_inaccessible_regions(world, player)

    for p in range(1, world.players + 1):
        world.key_logic[p] = {}
    base_world = copy_world_premature(world, player)
    base_world.override_bomb_check = True
    
    # remove regions that have a dungeon entrance
    accessible_regions = list()
    for region_name in world.inaccessible_regions[player]:
        region = world.get_region(region_name, player)
        for exit in region.exits:
            if exit.connected_region and exit.connected_region.type == RegionType.Dungeon:
                accessible_regions.append(region_name)
                break
    for region_name in accessible_regions.copy():
        accessible_regions = list(OrderedDict.fromkeys(accessible_regions + list(build_accessible_region_list(base_world, region_name, player, False, True, False, False))))
    world.inaccessible_regions[player] = [r for r in world.inaccessible_regions[player] if r not in accessible_regions]
    
    # get inaccessible entrances
    inaccessible_entrances = list()
    for region_name in world.inaccessible_regions[player]:
        region = world.get_region(region_name, player)
        if region.type in [RegionType.LightWorld, RegionType.DarkWorld]:
            for exit in region.exits:
                if not exit.connected_region and exit.name in entrance_pool:
                    inaccessible_entrances.append(exit.name)

    junk_locations = [e for e in list(zip(*(default_connections +
                       ([] if world.pottery[player] not in ['none', 'keys', 'dungeon'] else default_pot_connections) +
                       ([] if world.take_any[player] == 'fixed' else default_takeany_connections))))[1] if e in exit_pool]
    random.shuffle(junk_locations)
    for entrance in inaccessible_entrances:
        connect_entrance(world, entrance, junk_locations.pop(), player)


def connect_inaccessible_regions(world, lw_entrances, dw_entrances, caves, player, ignore_list=[]):
    def find_inacessible_ow_regions():
        nonlocal inaccessible_regions
        find_inaccessible_regions(world, player)
        inaccessible_regions = list(world.inaccessible_regions[player])
        
        # find OW regions that don't have a multi-entrance dungeon exit connected
        glitch_regions = ['Central Cliffs', 'Eastern Cliff', 'Desert Northern Cliffs', 'Hyrule Castle Water',
                          'Dark Central Cliffs', 'Darkness Cliff', 'Mire Northern Cliffs', 'Pyramid Water']
        multi_dungeon_exits = {
            'Hyrule Castle South Portal', 'Hyrule Castle West Portal', 'Hyrule Castle East Portal', 'Sanctuary Portal',
            'Desert South Portal', 'Desert West Portal',
            'Skull 2 East Portal', 'Skull 2 West Portal',
            'Turtle Rock Main Portal', 'Turtle Rock Lazy Eyes Portal', 'Turtle Rock Eye Bridge Portal'
        }
        for region_name in world.inaccessible_regions[player]:
            if (world.logic[player] in ['noglitches', 'minorglitches'] and region_name in glitch_regions) \
                    or (region_name == 'Pyramid Exit Ledge' and (world.shuffle[player] not in ['district', 'insanity'] or world.is_tile_swapped(0x1b, player))) \
                    or (region_name == 'Spiral Mimic Ledge Extend' and not world.is_tile_swapped(0x05, player)):
                # removing irrelevant and resolved regions
                inaccessible_regions.remove(region_name)
                continue
            region = world.get_region(region_name, player)
            if region.type not in [RegionType.LightWorld, RegionType.DarkWorld]:
                inaccessible_regions.remove(region_name)
                continue
            if world.shuffle[player] != 'insanity':
                for exit in region.exits:
                    # because dungeon regions haven't been connected yet, the inaccessibility check won't be able to know it's reachable yet
                    if exit.connected_region and exit.connected_region.name in multi_dungeon_exits:
                        resolved_regions.append(region_name)
                        break

    inaccessible_regions = list()
    resolved_regions = list()
    find_inacessible_ow_regions()

    # keep track of neighboring regions for later consolidation
    must_exit_links = OrderedDict()
    for region_name in inaccessible_regions:
        region = world.get_region(region_name, player)
        must_exit_links[region_name] = [x.connected_region.name for x in region.exits if x.connected_region and x.connected_region.name in inaccessible_regions]

    # group neighboring regions together, separated by one-ways
    def consolidate_group(region):
        processed_regions.append(region)
        must_exit_links_copy.pop(region)
        region_group.append(region)
        for dest_region in must_exit_links[region]:
            if region in must_exit_links[dest_region]:
                if dest_region not in processed_regions:
                    consolidate_group(dest_region)
            else:
                one_ways.append(tuple((region, dest_region)))

    processed_regions = list()
    must_exit_candidates = list()
    one_ways = list()
    must_exit_links_copy = must_exit_links.copy()
    while len(must_exit_links_copy):
        region_group = list()
        region_name = next(iter(must_exit_links_copy))
        consolidate_group(region_name)
        must_exit_candidates.append(region_group)

    # get available entrances in each group
    for regions in must_exit_candidates:
        entrances = list()
        for region_name in regions:
            region = world.get_region(region_name, player)
            entrances = entrances + [x.name for x in region.exits if x.spot_type == 'Entrance' and not x.connected_region]
        entrances = [e for e in entrances if e in entrance_pool and e not in ignore_list]
        must_exit_candidates[must_exit_candidates.index(regions)] = tuple((regions, entrances))

    # necessary for circular relations between region groups, it will pick the last group
    # and fill one of those entrances, and we don't want it to bias the same group
    random.shuffle(must_exit_candidates)

    # remove must exit candidates that would be made accessible thru other region groups
    def find_group(region):
        for group in must_exit_candidates:
            regions, _ = group
            if region in regions:
                return group
        raise Exception(f'Could not find region group for {region}')

    def cascade_ignore(group):
        nonlocal ignored_regions
        regions, _ = group
        ignored_regions = ignored_regions + regions
        for from_region, to_region in one_ways:
            if from_region in regions and to_region not in ignored_regions:
                cascade_ignore(find_group(to_region))

    def process_group(group):
        nonlocal processed_regions, ignored_regions
        regions, entrances = group
        must_exit_candidates_copy.remove(group)
        processed_regions = processed_regions + regions
        if regions[0] not in ignored_regions:
            for from_region, to_region in one_ways:
                if to_region in regions and from_region not in ignored_regions + processed_regions:
                    process_group(find_group(from_region)) # process the parent region group
            if regions[0] not in ignored_regions:
                # this is the top level region
                if any(r in resolved_regions for r in regions):
                    cascade_ignore(group)
                else:
                    if len(entrances):
                        # we will fulfill must exit here and cascade access to children
                        must_exit_regions.append(group)
                        cascade_ignore(group)
                    else:
                        ignored_regions = ignored_regions + regions

    processed_regions = list()
    ignored_regions = list()
    must_exit_regions = list()
    must_exit_candidates_copy = must_exit_candidates.copy()
    while len(must_exit_candidates_copy):
        region_group = next(iter(must_exit_candidates_copy))
        process_group(region_group)

    # connect must exits
    random.shuffle(must_exit_regions)
    must_exits_lw = list()
    must_exits_dw = list()
    for regions, entrances in must_exit_regions:
        region = world.get_region(regions[0], player)
        if region.type == RegionType.LightWorld:
            must_exits_lw.append(random.choice(entrances))
        else:
            must_exits_dw.append(random.choice(entrances))
    if world.shuffle[player] in ['lean', 'crossed', 'insanity']: # cross world
        pool = [e for e in lw_entrances + dw_entrances if e in entrance_pool and e not in must_exits_lw + must_exits_dw]
        connect_mandatory_exits(world, pool, caves, must_exits_lw + must_exits_dw, player)
    else:
        pool = [e for e in lw_entrances if e in entrance_pool and e not in must_exits_lw]
        if len(pool):
            connect_mandatory_exits(world, pool, caves, must_exits_lw, player)
        pool = [e for e in dw_entrances if e in entrance_pool and e not in must_exits_dw]
        if len(pool):
            connect_mandatory_exits(world, pool, caves, must_exits_dw, player)

    # check accessibility afterwards
    resolved_regions = list()
    find_inacessible_ow_regions()
    inaccessible_regions = [e for e in inaccessible_regions if e not in resolved_regions]
    # TODO: Instead of line above, this should cascade from the resolved regions down to regions it can access
    if len(inaccessible_regions) > 0:
        logging.getLogger('').debug(f'Could not resolve inaccessible regions: [{", ".join(inaccessible_regions)}]')
        logging.getLogger('').debug(f'^ This is most often a false positive because Dungeon regions aren\'t connected yet')


def unbias_some_entrances(Dungeon_Exits, Cave_Exits, Old_Man_House, Cave_Three_Exits):
    def shuffle_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = random.sample(item, len(item))

    def tuplize_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = tuple(item)

    shuffle_lists_in_list(Dungeon_Exits)
    shuffle_lists_in_list(Cave_Exits)
    shuffle_lists_in_list(Old_Man_House)
    shuffle_lists_in_list(Cave_Three_Exits)

    # paradox fixup
    if Cave_Three_Exits[1][0] == "Paradox Cave Exit (Bottom)":
        i = random.randint(1,2)
        Cave_Three_Exits[1][0] = Cave_Three_Exits[1][i]
        Cave_Three_Exits[1][i] = "Paradox Cave Exit (Bottom)"

    # TR fixup
    tr_fixup = False
    for i, item in enumerate(Dungeon_Exits[-1]):
        if 'Turtle Rock Ledge Exit (East)' == item:
            tr_fixup = True
            if 0 != i:
                Dungeon_Exits[-1][i] = Dungeon_Exits[-1][0]
                Dungeon_Exits[-1][0] = 'Turtle Rock Ledge Exit (East)'
            break

    if not tr_fixup: raise RuntimeError("TR entrance shuffle fixup didn't happen")

    tuplize_lists_in_list(Dungeon_Exits)
    tuplize_lists_in_list(Cave_Exits)
    tuplize_lists_in_list(Old_Man_House)
    tuplize_lists_in_list(Cave_Three_Exits)


def unbias_dungeons(Dungeon_Exits):
    def shuffle_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = random.sample(item, len(item))

    def tuplize_lists_in_list(ls):
        for i, item in enumerate(ls):
            if isinstance(item, list):
                ls[i] = tuple(item)

    shuffle_lists_in_list(Dungeon_Exits)

    # TR fixup
    for i, item in enumerate(Dungeon_Exits[-1]):
        if 'Turtle Rock Ledge Exit (East)' == item:
            if 0 != i:
                Dungeon_Exits[-1][i] = Dungeon_Exits[-1][0]
                Dungeon_Exits[-1][0] = 'Turtle Rock Ledge Exit (East)'
            break

    tuplize_lists_in_list(Dungeon_Exits)


def build_accessible_entrance_list(world, start_region, player, assumed_inventory=[], cross_world=False, region_rules=True, exit_rules=True, include_one_ways=False):
    from Main import copy_world_premature
    from Items import ItemFactory
    from OverworldShuffle import one_way_ledges
    
    for p in range(1, world.players + 1):
        world.key_logic[p] = {}
    base_world = copy_world_premature(world, player)
    base_world.override_bomb_check = True
    
    connect_simple(base_world, 'Links House S&Q', start_region, player)
    blank_state = CollectionState(base_world)
    if base_world.mode[player] == 'standard':
        blank_state.collect(ItemFactory('Zelda Delivered', player), True)
    for item in assumed_inventory:
        blank_state.collect(ItemFactory(item, player), True)

    explored_regions = list(build_accessible_region_list(base_world, start_region, player, False, cross_world, region_rules, False))

    if include_one_ways:
        new_regions = list()
        for region_name in explored_regions:
            if region_name in one_way_ledges:
                for ledge in one_way_ledges[region_name]:
                    if ledge not in explored_regions + new_regions:
                        new_regions.append(ledge)
        explored_regions.extend(new_regions)
    
    entrances = list()
    for region_name in explored_regions:
        region = base_world.get_region(region_name, player)
        for exit in region.exits:
            if exit.name in entrance_pool and (not exit_rules or exit.access_rule(blank_state)):
                entrances.append(exit.name)

    return entrances
    

def get_starting_entrances(world, player, force_starting_world=True):
    invFlag = world.mode[player] == 'inverted'

    # find largest walkable sector
    sector = None
    invalid_sectors = list()
    entrances = list()
    while not len(entrances):
        while (sector is None):
            sector = max(world.owsectors[player], key=lambda x: len(x) - (0 if x not in invalid_sectors else 1000))
            if not ((world.owCrossed[player] == 'polar' and world.owMixed[player]) or world.owCrossed[player] not in ['none', 'polar']) \
                    and world.get_region(next(iter(next(iter(sector)))), player).type != (RegionType.LightWorld if not invFlag else RegionType.DarkWorld):
                invalid_sectors.append(sector)
                sector = None
        regions = max(sector, key=lambda x: len(x))
        
        # get entrances from list of regions
        entrances = list()
        for region_name in regions:
            if world.shuffle[player] == 'simple' and region_name in OWTileRegions.keys() and OWTileRegions[region_name] in [0x03, 0x05, 0x07]:
                continue
            region = world.get_region(region_name, player)
            if not force_starting_world or region.type == (RegionType.LightWorld if not invFlag else RegionType.DarkWorld):
                for exit in region.exits:
                    if not exit.connected_region and exit.spot_type == 'Entrance':
                        entrances.append(exit.name)
        
        invalid_sectors.append(sector)
        sector = None
    
    return entrances


def get_distant_entrances(world, start_entrance, player):
    from OverworldShuffle import one_way_ledges
    
    # get walkable sector in which initial entrance was placed
    start_region = world.get_entrance(start_entrance, player).parent_region.name
    regions = next(s for s in world.owsectors[player] if any(start_region in w for w in s))
    regions = next(w for w in regions if start_region in w)
    
    # eliminate regions surrounding the initial entrance until less than half of the candidate regions remain
    explored_regions = list({start_region})
    was_progress = True
    while was_progress and len(explored_regions) < len(regions) / 2:
        was_progress = False
        new_regions = list()
        for region_name in explored_regions:
            if region_name in one_way_ledges:
                for ledge in one_way_ledges[region_name]:
                    if ledge not in explored_regions + new_regions:
                        new_regions.append(ledge)
                        was_progress = True
            region = world.get_region(region_name, player)
            for exit in region.exits:
                if exit.connected_region and region.type == exit.connected_region.type and exit.connected_region.name in regions and exit.connected_region.name not in explored_regions + new_regions:
                    new_regions.append(exit.connected_region.name)
                    was_progress = True
        explored_regions.extend(new_regions)

    # get entrances from remaining regions
    candidates = list()
    for region_name in [r for r in regions if r not in explored_regions]:
        if region_name in OWTileRegions.keys() and OWTileRegions[region_name] in [0x03, 0x05, 0x07]:
            continue
        region = world.get_region(region_name, player)
        for exit in region.exits:
            if not exit.connected_region and exit.spot_type == 'Entrance':
                candidates.append(exit.name)
    
    return candidates


def can_reach(world, entrance_name, region_name, player):
    from Main import copy_world_premature
    from Items import ItemFactory
    
    for p in range(1, world.players + 1):
        world.key_logic[p] = {}
    base_world = copy_world_premature(world, player)
    base_world.override_bomb_check = True
    
    entrance = world.get_entrance(entrance_name, player)
    connect_simple(base_world, 'Links House S&Q', entrance.parent_region.name, player)
    blank_state = CollectionState(base_world)
    if base_world.mode[player] == 'standard':
        blank_state.collect(ItemFactory('Zelda Delivered', player), True)

    find_inaccessible_regions(world, player)
    return region_name not in world.inaccessible_regions[player]


LW_Dungeon_Exits = [('Desert Palace Exit (South)', 'Desert Palace Exit (West)', 'Desert Palace Exit (East)'),
    'Desert Palace Exit (North)',
    'Eastern Palace Exit',
    'Tower of Hera Exit',
    'Agahnims Tower Exit']

DW_Late_Dungeon_Exits = ['Ice Palace Exit',
    'Misery Mire Exit',
    ('Turtle Rock Ledge Exit (East)', 'Turtle Rock Exit (Front)',  'Turtle Rock Ledge Exit (West)', 'Turtle Rock Isolated Ledge Exit')]

DW_Mid_Dungeon_Exits = ['Thieves Town Exit',
    'Skull Woods Final Section Exit',
    'Palace of Darkness Exit',
    'Swamp Palace Exit']

Cave_Exits_Base = [('Elder House Exit (East)', 'Elder House Exit (West)'),
                   ('Two Brothers House Exit (East)', 'Two Brothers House Exit (West)'),
                   ('Death Mountain Return Cave Exit (West)', 'Death Mountain Return Cave Exit (East)'),
                   ('Fairy Ascension Cave Exit (Bottom)', 'Fairy Ascension Cave Exit (Top)'),
                   ('Bumper Cave Exit (Top)', 'Bumper Cave Exit (Bottom)'),
                   ('Hookshot Cave Back Exit', 'Hookshot Cave Front Exit')]

Cave_Exits_Directional = [('Superbunny Cave Exit (Bottom)', 'Superbunny Cave Exit (Top)'),
                          ('Spiral Cave Exit (Top)', 'Spiral Cave Exit')]

Cave_Three_Exits_Base = [('Spectacle Rock Cave Exit (Peak)', 'Spectacle Rock Cave Exit (Top)', 'Spectacle Rock Cave Exit'),
                         ('Paradox Cave Exit (Top)', 'Paradox Cave Exit (Middle)', 'Paradox Cave Exit (Bottom)')]

Old_Man_House_Base = [('Old Man House Exit (Bottom)', 'Old Man House Exit (Top)')]


Entrance_Pool_Base = ['Links House',
                    'Desert Palace Entrance (South)',
                    'Desert Palace Entrance (West)',
                    'Desert Palace Entrance (East)',
                    'Desert Palace Entrance (North)',
                    'Eastern Palace',
                    'Tower of Hera',
                    'Hyrule Castle Entrance (South)',
                    'Hyrule Castle Entrance (West)',
                    'Hyrule Castle Entrance (East)',
                    'Agahnims Tower',
                    'Thieves Town',
                    'Skull Woods First Section Door',
                    'Skull Woods Second Section Door (East)',
                    'Skull Woods Second Section Door (West)',
                    'Skull Woods Final Section',
                    'Ice Palace',
                    'Misery Mire',
                    'Palace of Darkness',
                    'Swamp Palace',
                    'Turtle Rock',
                    'Dark Death Mountain Ledge (West)',
                    'Dark Death Mountain Ledge (East)',
                    'Turtle Rock Isolated Ledge Entrance',
                    'Hyrule Castle Secret Entrance Stairs',
                    'Kakariko Well Cave',
                    'Bat Cave Cave',
                    'Elder House (East)',
                    'Elder House (West)',
                    'North Fairy Cave',
                    'Lost Woods Hideout Stump',
                    'Lumberjack Tree Cave',
                    'Two Brothers House (East)',
                    'Two Brothers House (West)',
                    'Sanctuary',
                    'Old Man Cave (East)',
                    'Old Man Cave (West)',
                    'Old Man House (Bottom)',
                    'Old Man House (Top)',
                    'Death Mountain Return Cave (West)',
                    'Death Mountain Return Cave (East)',
                    'Spectacle Rock Cave (Bottom)',
                    'Spectacle Rock Cave',
                    'Spectacle Rock Cave Peak',
                    'Paradox Cave (Bottom)',
                    'Paradox Cave (Middle)',
                    'Paradox Cave (Top)',
                    'Fairy Ascension Cave (Bottom)',
                    'Fairy Ascension Cave (Top)',
                    'Spiral Cave (Bottom)',
                    'Spiral Cave',
                    'Bumper Cave (Top)',
                    'Bumper Cave (Bottom)',
                    'Superbunny Cave (Top)',
                    'Superbunny Cave (Bottom)',
                    'Hookshot Cave',
                    'Hookshot Cave Back Entrance',
                    'Ganons Tower',
                    'Pyramid Entrance',
                    'Waterfall of Wishing',
                    'Dam',
                    'Blinds Hideout',
                    'Lumberjack House',
                    'Bonk Fairy (Light)',
                    'Bonk Fairy (Dark)',
                    'Lake Hylia Fairy',
                    'Light Hype Fairy',
                    'Desert Fairy',
                    'Dark Lake Hylia Fairy',
                    'Dark Lake Hylia Ledge Fairy',
                    'Mire Fairy',
                    'Dark Death Mountain Fairy',
                    'Fortune Teller (Light)',
                    'Lake Hylia Fortune Teller',
                    'Kings Grave',
                    'Chicken House',
                    'Aginahs Cave',
                    'Sahasrahlas Hut',
                    'Lake Hylia Shop',
                    'Dark Death Mountain Shop',
                    'Capacity Upgrade',
                    'Blacksmiths Hut',
                    'Sick Kids House',
                    'Lost Woods Gamble',
                    'Snitch Lady (East)',
                    'Snitch Lady (West)',
                    'Bush Covered House',
                    'Tavern (Front)',
                    'Light World Bomb Hut',
                    'Kakariko Shop',
                    'Cave 45',
                    'Graveyard Cave',
                    'Checkerboard Cave',
                    'Mini Moldorm Cave',
                    'Long Fairy Cave',
                    'Good Bee Cave',
                    '20 Rupee Cave',
                    '50 Rupee Cave',
                    'Ice Rod Cave',
                    'Bonk Rock Cave',
                    'Library',
                    'Kakariko Gamble Game',
                    'Potion Shop',
                    'Hookshot Fairy',
                    'Pyramid Fairy',
                    'East Dark World Hint',
                    'Palace of Darkness Hint',
                    'Big Bomb Shop',
                    'Dark World Shop',
                    'Dark Lake Hylia Shop',
                    'Dark Lumberjack Shop',
                    'Dark Potion Shop',
                    'Dark Lake Hylia Ledge Spike Cave',
                    'Dark Lake Hylia Ledge Hint',
                    'Hype Cave',
                    'Brewery',
                    'C-Shaped House',
                    'Chest Game',
                    'Hammer Peg Cave',
                    'Red Shield Shop',
                    'Dark Sanctuary Hint',
                    'Fortune Teller (Dark)',
                    'Archery Game',
                    'Mire Shed',
                    'Mire Hint',
                    'Spike Cave',
                    'Mimic Cave',
                    'Kakariko Well Drop',
                    'Hyrule Castle Secret Entrance Drop',
                    'Bat Cave Drop',
                    'North Fairy Cave Drop',
                    'Lost Woods Hideout Drop',
                    'Lumberjack Tree Tree',
                    'Sanctuary Grave',
                    'Skull Woods Second Section Hole',
                    'Skull Woods First Section Hole (West)',
                    'Skull Woods First Section Hole (East)',
                    'Skull Woods First Section Hole (North)',
                    'Pyramid Hole']

Exit_Pool_Base = ['Links House Exit',
                'Desert Palace Exit (South)',
                'Desert Palace Exit (West)',
                'Desert Palace Exit (East)',
                'Desert Palace Exit (North)',
                'Eastern Palace Exit',
                'Tower of Hera Exit',
                'Hyrule Castle Exit (South)',
                'Hyrule Castle Exit (West)',
                'Hyrule Castle Exit (East)',
                'Agahnims Tower Exit',
                'Thieves Town Exit',
                'Skull Woods First Section Exit',
                'Skull Woods Second Section Exit (East)',
                'Skull Woods Second Section Exit (West)',
                'Skull Woods Final Section Exit',
                'Ice Palace Exit',
                'Misery Mire Exit',
                'Palace of Darkness Exit',
                'Swamp Palace Exit',
                'Turtle Rock Exit (Front)',
                'Turtle Rock Ledge Exit (West)',
                'Turtle Rock Ledge Exit (East)',
                'Turtle Rock Isolated Ledge Exit',
                'Hyrule Castle Secret Entrance Exit',
                'Kakariko Well Exit',
                'Bat Cave Exit',
                'Elder House Exit (East)',
                'Elder House Exit (West)',
                'North Fairy Cave Exit',
                'Lost Woods Hideout Exit',
                'Lumberjack Tree Exit',
                'Two Brothers House Exit (East)',
                'Two Brothers House Exit (West)',
                'Sanctuary Exit',
                'Old Man Cave Exit (East)',
                'Old Man Cave Exit (West)',
                'Old Man House Exit (Bottom)',
                'Old Man House Exit (Top)',
                'Death Mountain Return Cave Exit (West)',
                'Death Mountain Return Cave Exit (East)',
                'Spectacle Rock Cave Exit',
                'Spectacle Rock Cave Exit (Top)',
                'Spectacle Rock Cave Exit (Peak)',
                'Paradox Cave Exit (Bottom)',
                'Paradox Cave Exit (Middle)',
                'Paradox Cave Exit (Top)',
                'Fairy Ascension Cave Exit (Bottom)',
                'Fairy Ascension Cave Exit (Top)',
                'Spiral Cave Exit',
                'Spiral Cave Exit (Top)',
                'Bumper Cave Exit (Top)',
                'Bumper Cave Exit (Bottom)',
                'Superbunny Cave Exit (Top)',
                'Superbunny Cave Exit (Bottom)',
                'Hookshot Cave Front Exit',
                'Hookshot Cave Back Exit',
                'Ganons Tower Exit',
                'Pyramid Exit',
                'Waterfall of Wishing',
                'Dam',
                'Blinds Hideout',
                'Lumberjack House',
                'Bonk Fairy (Light)',
                'Bonk Fairy (Dark)',
                'Lake Hylia Healer Fairy',
                'Light Hype Fairy',
                'Desert Healer Fairy',
                'Dark Lake Hylia Healer Fairy',
                'Dark Lake Hylia Ledge Healer Fairy',
                'Mire Healer Fairy',
                'Dark Death Mountain Healer Fairy',
                'Fortune Teller (Light)',
                'Lake Hylia Fortune Teller',
                'Kings Grave',
                'Chicken House',
                'Aginahs Cave',
                'Sahasrahlas Hut',
                'Lake Hylia Shop',
                'Dark Death Mountain Shop',
                'Capacity Upgrade',
                'Blacksmiths Hut',
                'Sick Kids House',
                'Lost Woods Gamble',
                'Snitch Lady (East)',
                'Snitch Lady (West)',
                'Bush Covered House',
                'Tavern (Front)',
                'Light World Bomb Hut',
                'Kakariko Shop',
                'Cave 45',
                'Graveyard Cave',
                'Checkerboard Cave',
                'Mini Moldorm Cave',
                'Long Fairy Cave',
                'Good Bee Cave',
                '20 Rupee Cave',
                '50 Rupee Cave',
                'Ice Rod Cave',
                'Bonk Rock Cave',
                'Library',
                'Kakariko Gamble Game',
                'Potion Shop',
                'Hookshot Fairy',
                'Pyramid Fairy',
                'East Dark World Hint',
                'Palace of Darkness Hint',
                'Big Bomb Shop',
                'Village of Outcasts Shop',
                'Dark Lake Hylia Shop',
                'Dark Lumberjack Shop',
                'Dark Potion Shop',
                'Dark Lake Hylia Ledge Spike Cave',
                'Dark Lake Hylia Ledge Hint',
                'Hype Cave',
                'Brewery',
                'C-Shaped House',
                'Chest Game',
                'Hammer Peg Cave',
                'Red Shield Shop',
                'Dark Sanctuary Hint',
                'Fortune Teller (Dark)',
                'Archery Game',
                'Mire Shed',
                'Mire Hint',
                'Spike Cave',
                'Mimic Cave',
                'Kakariko Well (top)',
                'Hyrule Castle Secret Entrance',
                'Bat Cave (right)',
                'North Fairy Cave',
                'Lost Woods Hideout (top)',
                'Lumberjack Tree (top)',
                'Sewer Drop',
                'Skull Back Drop',
                'Skull Left Drop',
                'Skull Pinball',
                'Skull Pot Circle',
                'Pyramid']

# these are connections that cannot be shuffled and always exist.
# They link together underworld regions
mandatory_connections = [
                         ('Lost Woods Hideout (top to bottom)', 'Lost Woods Hideout (bottom)'),
                         ('Lumberjack Tree (top to bottom)', 'Lumberjack Tree (bottom)'),
                         ('Death Mountain Return Cave E', 'Death Mountain Return Cave (right)'),
                         ('Death Mountain Return Cave W', 'Death Mountain Return Cave (left)'),
                         ('Old Man Cave Dropdown', 'Old Man Cave (West)'),
                         ('Old Man Cave W', 'Old Man Cave (West)'),
                         ('Old Man Cave E', 'Old Man Cave (East)'),
                         ('Spectacle Rock Cave Drop', 'Spectacle Rock Cave Pool'),
                         ('Spectacle Rock Cave Peak Drop', 'Spectacle Rock Cave Pool'),
                         ('Spectacle Rock Cave West Edge', 'Spectacle Rock Cave (Bottom)'),
                         ('Spectacle Rock Cave East Edge', 'Spectacle Rock Cave Pool'),
                         ('Old Man House Front to Back', 'Old Man House Back'),
                         ('Old Man House Back to Front', 'Old Man House'),
                         ('Spiral Cave (top to bottom)', 'Spiral Cave (Bottom)'),
                         ('Paradox Shop', 'Paradox Shop'),
                         ('Paradox Cave Push Block Reverse', 'Paradox Cave Chest Area'),
                         ('Paradox Cave Push Block', 'Paradox Cave Front'),
                         ('Paradox Cave Chest Area NE', 'Paradox Cave Bomb Area'),
                         ('Paradox Cave Bomb Jump', 'Paradox Cave'),
                         ('Paradox Cave Drop', 'Paradox Cave Chest Area'),
                         ('Fairy Ascension Cave Climb', 'Fairy Ascension Cave (Top)'),
                         ('Fairy Ascension Cave Pots', 'Fairy Ascension Cave (Bottom)'),
                         ('Fairy Ascension Cave Drop', 'Fairy Ascension Cave (Drop)'),
                         ('Sewer Drop', 'Sewers Rat Path'),
                         ('Kakariko Well (top to bottom)', 'Kakariko Well (bottom)'),
                         ('Kakariko Well (top to back)', 'Kakariko Well (back)'),
                         ('Blinds Hideout N', 'Blinds Hideout (Top)'),
                         ('Bat Cave Door', 'Bat Cave (left)'),
                         ('Good Bee Cave Front to Back', 'Good Bee Cave (back)'),
                         ('Good Bee Cave Back to Front', 'Good Bee Cave'),
                         ('Capacity Upgrade East', 'Capacity Fairy Pool'),
                         ('Capacity Fairy Pool West', 'Capacity Upgrade'),
                         ('Bonk Fairy (Dark) Pool', 'Bonk Fairy Pool'),
                         ('Bonk Fairy (Light) Pool', 'Bonk Fairy Pool'),

                         ('Hookshot Cave Front to Middle', 'Hookshot Cave (Middle)'),
                         ('Hookshot Cave Middle to Front', 'Hookshot Cave (Front)'),
                         ('Hookshot Cave Middle to Back', 'Hookshot Cave (Back)'),
                         ('Hookshot Cave Back to Middle', 'Hookshot Cave (Middle)'),
                         ('Hookshot Cave Back to Fairy', 'Hookshot Cave (Fairy Pool)'),
                         ('Hookshot Cave Fairy to Back', 'Hookshot Cave (Back)'),
                         ('Hookshot Cave Bonk Path', 'Hookshot Cave (Bonk Islands)'),
                         ('Hookshot Cave Hook Path', 'Hookshot Cave (Hook Islands)'),
                         ('Superbunny Cave Climb', 'Superbunny Cave (Top)'),
                         ('Bumper Cave Bottom to Top', 'Bumper Cave (top)'),
                         ('Bumper Cave Top To Bottom', 'Bumper Cave (bottom)'),
                         ('Missing Smith', 'Missing Smith'),
                         ('Ganon Drop', 'Bottom of Pyramid')
                    ]

# non-shuffled entrance links
default_connections = [('Lost Woods Gamble', 'Lost Woods Gamble'),
                       ('Fortune Teller (Light)', 'Fortune Teller (Light)'),
                       ('Bush Covered House', 'Bush Covered House'),
                       ('Kakariko Gamble Game', 'Kakariko Gamble Game'),
                       ('Bonk Fairy (Light)', 'Bonk Fairy (Light)'),
                       ('Lake Hylia Fairy', 'Lake Hylia Healer Fairy'),
                       ('Long Fairy Cave', 'Long Fairy Cave'),
                       ('Lake Hylia Fortune Teller', 'Lake Hylia Fortune Teller'),
                       ('Good Bee Cave', 'Good Bee Cave'),
                       
                       ('Fortune Teller (Dark)', 'Fortune Teller (Dark)'),
                       ('Dark Sanctuary Hint', 'Dark Sanctuary Hint'),
                       ('Archery Game', 'Archery Game'),
                       ('Dark Lake Hylia Fairy', 'Dark Lake Hylia Healer Fairy'),
                       ('East Dark World Hint', 'East Dark World Hint'),
                       ('Mire Fairy', 'Mire Healer Fairy'),
                       ('Dark Lake Hylia Ledge Hint', 'Dark Lake Hylia Ledge Hint')
                    ]

default_takeany_connections = [('Light Hype Fairy', 'Light Hype Fairy'),
                               ('Desert Fairy', 'Desert Healer Fairy'),
                               ('Dark Death Mountain Fairy', 'Dark Death Mountain Healer Fairy'),
                               ('Bonk Fairy (Dark)', 'Bonk Fairy (Dark)'),
                               ('Dark Lake Hylia Ledge Fairy', 'Dark Lake Hylia Ledge Healer Fairy')
                            ]

default_pot_connections = [('Lumberjack House', 'Lumberjack House'),
                           ('Hookshot Fairy', 'Hookshot Fairy'),
                           ('Snitch Lady (East)', 'Snitch Lady (East)'),
                           ('Snitch Lady (West)', 'Snitch Lady (West)'),
                           ('Light World Bomb Hut', 'Light World Bomb Hut'),
                           ('Tavern (Front)', 'Tavern (Front)'),
                           ('20 Rupee Cave', '20 Rupee Cave'),
                           ('50 Rupee Cave', '50 Rupee Cave'),
                           ('Palace of Darkness Hint', 'Palace of Darkness Hint'),
                           ('Mire Hint', 'Mire Hint'),
                           ('Dark Lake Hylia Ledge Spike Cave', 'Dark Lake Hylia Ledge Spike Cave')
                        ]

default_connector_connections = [('Death Mountain Return Cave (West)', 'Death Mountain Return Cave Exit (West)'),
                                 ('Death Mountain Return Cave (East)', 'Death Mountain Return Cave Exit (East)'),
                                 ('Spectacle Rock Cave Peak', 'Spectacle Rock Cave Exit (Peak)'),
                                 ('Spectacle Rock Cave (Bottom)', 'Spectacle Rock Cave Exit'),
                                 ('Spectacle Rock Cave', 'Spectacle Rock Cave Exit (Top)'),
                                 ('Old Man Cave (East)', 'Old Man Cave Exit (East)'),
                                 ('Old Man Cave (West)', 'Old Man Cave Exit (West)'),
                                 ('Old Man House (Bottom)', 'Old Man House Exit (Bottom)'),
                                 ('Old Man House (Top)', 'Old Man House Exit (Top)'),
                                 ('Spiral Cave', 'Spiral Cave Exit (Top)'),
                                 ('Spiral Cave (Bottom)', 'Spiral Cave Exit'),
                                 ('Fairy Ascension Cave (Top)', 'Fairy Ascension Cave Exit (Top)'),
                                 ('Fairy Ascension Cave (Bottom)', 'Fairy Ascension Cave Exit (Bottom)'),
                                 ('Paradox Cave (Bottom)', 'Paradox Cave Exit (Bottom)'),
                                 ('Paradox Cave (Middle)', 'Paradox Cave Exit (Middle)'),
                                 ('Paradox Cave (Top)', 'Paradox Cave Exit (Top)'),
                                 ('Elder House (West)', 'Elder House Exit (West)'),
                                 ('Elder House (East)', 'Elder House Exit (East)'),
                                 ('Two Brothers House (West)', 'Two Brothers House Exit (West)'),
                                 ('Two Brothers House (East)', 'Two Brothers House Exit (East)'),
                                 ('Hookshot Cave Back Entrance', 'Hookshot Cave Back Exit'),
                                 ('Hookshot Cave', 'Hookshot Cave Front Exit'),
                                 ('Superbunny Cave (Top)', 'Superbunny Cave Exit (Top)'),
                                 ('Superbunny Cave (Bottom)', 'Superbunny Cave Exit (Bottom)'),
                                 ('Bumper Cave (Bottom)', 'Bumper Cave Exit (Bottom)'),
                                 ('Bumper Cave (Top)', 'Bumper Cave Exit (Top)')
                            ]

default_item_connections = [('Mimic Cave', 'Mimic Cave'),
                            ('Waterfall of Wishing', 'Waterfall of Wishing'),
                            ('Bonk Rock Cave', 'Bonk Rock Cave'),
                            ('Graveyard Cave', 'Graveyard Cave'),
                            ('Kings Grave', 'Kings Grave'),
                            ('Potion Shop', 'Potion Shop'),
                            ('Blinds Hideout', 'Blinds Hideout'),
                            ('Chicken House', 'Chicken House'),
                            ('Sick Kids House', 'Sick Kids House'),
                            ('Sahasrahlas Hut', 'Sahasrahlas Hut'),
                            ('Blacksmiths Hut', 'Blacksmiths Hut'),
                            ('Library', 'Library'),
                            ('Links House', 'Links House Exit'),
                            ('Checkerboard Cave', 'Checkerboard Cave'),
                            ('Aginahs Cave', 'Aginahs Cave'),
                            ('Cave 45', 'Cave 45'),
                            ('Mini Moldorm Cave', 'Mini Moldorm Cave'),
                            ('Ice Rod Cave', 'Ice Rod Cave'),
                            ('Dam', 'Dam'),
                            ('Spike Cave', 'Spike Cave'),
                            ('Chest Game', 'Chest Game'),
                            ('C-Shaped House', 'C-Shaped House'),
                            ('Brewery', 'Brewery'),
                            ('Pyramid Fairy', 'Pyramid Fairy'),
                            ('Hammer Peg Cave', 'Hammer Peg Cave'),
                            ('Big Bomb Shop', 'Big Bomb Shop'),
                            ('Mire Shed', 'Mire Shed'),
                            ('Hype Cave', 'Hype Cave')
                        ]

default_shop_connections = [('Kakariko Shop', 'Kakariko Shop'),
                            ('Lake Hylia Shop', 'Lake Hylia Shop'),
                            ('Capacity Upgrade', 'Capacity Upgrade'),
                            ('Dark Lumberjack Shop', 'Dark Lumberjack Shop'),
                            ('Dark Death Mountain Shop', 'Dark Death Mountain Shop'),
                            ('Dark Potion Shop', 'Dark Potion Shop'),
                            ('Dark World Shop', 'Village of Outcasts Shop'),
                            ('Red Shield Shop', 'Red Shield Shop'),
                            ('Dark Lake Hylia Shop', 'Dark Lake Hylia Shop')
                        ]

default_drop_connections = [('Lost Woods Hideout Drop', 'Lost Woods Hideout (top)'),
                            ('Lumberjack Tree Tree', 'Lumberjack Tree (top)'),
                            ('Sanctuary Grave', 'Sewer Drop'),
                            ('North Fairy Cave Drop', 'North Fairy Cave'),
                            ('Kakariko Well Drop', 'Kakariko Well (top)'),
                            ('Hyrule Castle Secret Entrance Drop', 'Hyrule Castle Secret Entrance'),
                            ('Bat Cave Drop', 'Bat Cave (right)'),
                            #('Pyramid Hole', 'Pyramid') # this is dynamically added because of Inverted/OW Mixed
                        ]

default_dropexit_connections = [('Lost Woods Hideout Stump', 'Lost Woods Hideout Exit'),
                                ('Lumberjack Tree Cave', 'Lumberjack Tree Exit'),
                                ('Sanctuary', 'Sanctuary Exit'),
                                ('North Fairy Cave', 'North Fairy Cave Exit'),
                                ('Kakariko Well Cave', 'Kakariko Well Exit'),
                                ('Hyrule Castle Secret Entrance Stairs', 'Hyrule Castle Secret Entrance Exit'),
                                ('Bat Cave Cave', 'Bat Cave Exit'),
                                #('Pyramid Entrance', 'Pyramid Exit') # this is dynamically added because of Inverted/OW Mixed
                            ]

# non shuffled dungeons
default_dungeon_connections = [('Desert Palace Entrance (South)', 'Desert Palace Exit (South)'),
                               ('Desert Palace Entrance (West)', 'Desert Palace Exit (West)'),
                               ('Desert Palace Entrance (North)', 'Desert Palace Exit (North)'),
                               ('Desert Palace Entrance (East)', 'Desert Palace Exit (East)'),
                               
                               ('Eastern Palace', 'Eastern Palace Exit'),
                               ('Tower of Hera', 'Tower of Hera Exit'),

                               ('Hyrule Castle Entrance (South)', 'Hyrule Castle Exit (South)'),
                               ('Hyrule Castle Entrance (West)', 'Hyrule Castle Exit (West)'),
                               ('Hyrule Castle Entrance (East)', 'Hyrule Castle Exit (East)'),

                               ('Thieves Town', 'Thieves Town Exit'),
                               ('Skull Woods First Section Door', 'Skull Woods First Section Exit'),
                               ('Skull Woods Second Section Door (East)', 'Skull Woods Second Section Exit (East)'),
                               ('Skull Woods Second Section Door (West)', 'Skull Woods Second Section Exit (West)'),
                               ('Skull Woods Final Section', 'Skull Woods Final Section Exit'),
                               ('Ice Palace', 'Ice Palace Exit'),
                               ('Misery Mire', 'Misery Mire Exit'),
                               ('Palace of Darkness', 'Palace of Darkness Exit'),
                               ('Swamp Palace', 'Swamp Palace Exit'), # requires additional patch for flooding moat if moved

                               ('Turtle Rock', 'Turtle Rock Exit (Front)'),
                               ('Dark Death Mountain Ledge (West)', 'Turtle Rock Ledge Exit (West)'),
                               ('Dark Death Mountain Ledge (East)', 'Turtle Rock Ledge Exit (East)'),
                               ('Turtle Rock Isolated Ledge Entrance', 'Turtle Rock Isolated Ledge Exit')
                            ]

default_skulldrop_connections = [('Skull Woods First Section Hole (East)', 'Skull Pinball'),
                                 ('Skull Woods First Section Hole (West)', 'Skull Left Drop'),
                                 ('Skull Woods First Section Hole (North)', 'Skull Pot Circle'),
                                 ('Skull Woods Second Section Hole', 'Skull Back Drop')
                                ]

open_default_dungeon_connections = [('Ganons Tower', 'Ganons Tower Exit'),
                                    ('Agahnims Tower', 'Agahnims Tower Exit')
                                ]

inverted_default_dungeon_connections = [('Ganons Tower', 'Agahnims Tower Exit'),
                                        ('Agahnims Tower', 'Ganons Tower Exit')
                                    ]
# format:
# Key=Name
# addr = (door_index, exitdata, ow_flag) # multiexit
#       | ([addr], None)  # holes
# exitdata = (room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2)

# ToDo somehow merge this with creation of the locations
door_addresses = {'Links House':                            (0x00, (0x0104, 0x2c, 0x0506, 0x0a9a, 0x0832, 0x0ae8, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfe, 0x0816, 0x0000), 0x00),
                  'Desert Palace Entrance (South)':         (0x08, (0x0084, 0x30, 0x0314, 0x0c56, 0x00a6, 0x0ca8, 0x0128, 0x0cc3, 0x0133, 0x0a, 0xfa, 0x0000, 0x0000), 0x00),
                  'Desert Palace Entrance (West)':          (0x0A, (0x0083, 0x30, 0x0280, 0x0c46, 0x0003, 0x0c98, 0x0088, 0x0cb3, 0x0090, 0x0a, 0xfd, 0x0000, 0x0000), 0x00),
                  'Desert Palace Entrance (North)':         (0x0B, (0x0063, 0x30, 0x0016, 0x0c00, 0x00a2, 0x0c28, 0x0128, 0x0c6d, 0x012f, 0x00, 0x0e, 0x0000, 0x0000), 0x00),
                  'Desert Palace Entrance (East)':          (0x09, (0x0085, 0x30, 0x02a8, 0x0c4a, 0x0142, 0x0c98, 0x01c8, 0x0cb7, 0x01cf, 0x06, 0xfe, 0x0000, 0x0000), 0x00),
                  'Eastern Palace':                         (0x07, (0x00c9, 0x1e, 0x005a, 0x0600, 0x0ed6, 0x0618, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000), 0x00),
                  'Tower of Hera':                          (0x32, (0x0077, 0x03, 0x0050, 0x0014, 0x087c, 0x0068, 0x08f0, 0x0083, 0x08fb, 0x0a, 0xf4, 0x0000, 0x0000), 0x00),
                  'Hyrule Castle Entrance (South)':         (0x03, (0x0061, 0x1b, 0x0530, 0x0692, 0x0784, 0x06cc, 0x07f8, 0x06ff, 0x0803, 0x0e, 0xfa, 0x0000, 0x87be), 0x00),
                  'Hyrule Castle Entrance (West)':          (0x02, (0x0060, 0x1b, 0x0016, 0x0600, 0x06ae, 0x0604, 0x0728, 0x066d, 0x0733, 0x00, 0x02, 0x0000, 0x8124), 0x00),
                  'Hyrule Castle Entrance (East)':          (0x04, (0x0062, 0x1b, 0x004a, 0x0600, 0x0856, 0x0604, 0x08c8, 0x066d, 0x08d3, 0x00, 0xfa, 0x0000, 0x8158), 0x00),
                  'Inverted Pyramid Entrance':              (0x35, (0x0010, 0x1b, 0x000e, 0x0600, 0x0676, 0x0604, 0x06e8, 0x066d, 0x06f3, 0x00, 0x0a, 0x0000, 0x811c), 0x00),
                  'Agahnims Tower':                         (0x23, (0x00e0, 0x1b, 0x0032, 0x0600, 0x0784, 0x0634, 0x07f8, 0x066d, 0x0803, 0x00, 0x0a, 0x0000, 0x82be), 0x40),
                  'Thieves Town':                           (0x33, (0x00db, 0x58, 0x0b2e, 0x075a, 0x0176, 0x07a8, 0x01f8, 0x07c7, 0x0203, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Skull Woods First Section Door':         (0x29, (0x0058, 0x40, 0x0f4c, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0xfe, 0x0000, 0x0000), 0x00),
                  'Skull Woods Second Section Door (East)': (0x28, (0x0057, 0x40, 0x0eb8, 0x01e6, 0x01c2, 0x0238, 0x0248, 0x0253, 0x024f, 0x0a, 0xfe, 0x0000, 0x0000), 0x00),
                  'Skull Woods Second Section Door (West)': (0x27, (0x0056, 0x40, 0x0c8e, 0x01a6, 0x0062, 0x01f8, 0x00e8, 0x0213, 0x00ef, 0x0a, 0x0e, 0x0000, 0x0000), 0x00),
                  'Skull Woods Final Section':              (0x2A, (0x0059, 0x40, 0x0282, 0x0066, 0x0016, 0x00b8, 0x0098, 0x00d3, 0x00a3, 0x0a, 0xfa, 0x0000, 0x0000), 0x20),
                  'Ice Palace':                             (0x2C, (0x000e, 0x75, 0x0bc6, 0x0d6a, 0x0c3e, 0x0db8, 0x0cb8, 0x0dd7, 0x0cc3, 0x06, 0xf2, 0x0000, 0x0000), 0x00),
                  'Misery Mire':                            (0x26, (0x0098, 0x70, 0x0414, 0x0c79, 0x00a6, 0x0cc7, 0x0128, 0x0ce6, 0x0133, 0x07, 0xfa, 0x0000, 0x0000), 0x20),
                  'Palace of Darkness':                     (0x25, (0x004a, 0x5e, 0x005a, 0x0600, 0x0ed6, 0x0628, 0x0f50, 0x066d, 0x0f5b, 0x00, 0xfa, 0x0000, 0x0000), 0x20),
                  'Swamp Palace':                           (0x24, (0x0028, 0x7b, 0x049e, 0x0e8c, 0x06f2, 0x0ed8, 0x0778, 0x0ef9, 0x077f, 0x04, 0xfe, 0x0000, 0x0000), 0x00),
                  'Turtle Rock':                            (0x34, (0x00d6, 0x47, 0x0712, 0x00da, 0x0e96, 0x0128, 0x0f08, 0x0147, 0x0f13, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Dark Death Mountain Ledge (West)':       (0x14, (0x0023, 0x45, 0x07ca, 0x0103, 0x0c46, 0x0157, 0x0cb8, 0x0172, 0x0cc3, 0x0b, 0x0a, 0x0000, 0x0000), 0x00),
                  'Dark Death Mountain Ledge (East)':       (0x18, (0x0024, 0x45, 0x07e0, 0x0103, 0x0d00, 0x0157, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Turtle Rock Isolated Ledge Entrance':    (0x17, (0x00d5, 0x45, 0x0ad4, 0x0164, 0x0ca6, 0x01b8, 0x0d18, 0x01d3, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000), 0x00),
                  'Hyrule Castle Secret Entrance Stairs':   (0x31, (0x0055, 0x1b, 0x044a, 0x067a, 0x0854, 0x06c8, 0x08c8, 0x06e7, 0x08d3, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Kakariko Well Cave':                     (0x38, (0x002f, 0x18, 0x0386, 0x0665, 0x0032, 0x06b7, 0x00b8, 0x06d2, 0x00bf, 0x0b, 0xfe, 0x0000, 0x0000), 0x00),
                  'Bat Cave Cave':                          (0x10, (0x00e3, 0x22, 0x0412, 0x087a, 0x048e, 0x08c8, 0x0508, 0x08e7, 0x0513, 0x06, 0x02, 0x0000, 0x0000), 0x00),
                  'Elder House (East)':                     (0x0D, (0x00f3, 0x18, 0x02c4, 0x064a, 0x0222, 0x0698, 0x02a8, 0x06b7, 0x02af, 0x06, 0xfe, 0x05d4, 0x0000), 0x00),
                  'Elder House (West)':                     (0x0C, (0x00f2, 0x18, 0x02bc, 0x064c, 0x01e2, 0x0698, 0x0268, 0x06b9, 0x026f, 0x04, 0xfe, 0x05cc, 0x0000), 0x00),
                  'North Fairy Cave':                       (0x37, (0x0008, 0x15, 0x0088, 0x0400, 0x0a36, 0x0448, 0x0aa8, 0x046f, 0x0ab3, 0x00, 0x0a, 0x0000, 0x0000), 0x00),
                  'Lost Woods Hideout Stump':               (0x2B, (0x00e1, 0x00, 0x0f4e, 0x01f6, 0x0262, 0x0248, 0x02e8, 0x0263, 0x02ef, 0x0a, 0x0e, 0x0000, 0x0000), 0x00),
                  'Lumberjack Tree Cave':                   (0x11, (0x00e2, 0x02, 0x0118, 0x0015, 0x04c6, 0x0067, 0x0548, 0x0082, 0x0553, 0x0b, 0xfa, 0x0000, 0x0000), 0x00),
                  'Two Brothers House (East)':              (0x0F, (0x00f5, 0x29, 0x0880, 0x0b07, 0x0200, 0x0b58, 0x0238, 0x0b74, 0x028d, 0x09, 0x00, 0x0b86, 0x0000), 0x00),
                  'Two Brothers House (West)':              (0x0E, (0x00f4, 0x28, 0x08a0, 0x0b06, 0x0100, 0x0b58, 0x01b8, 0x0b73, 0x018d, 0x0a, 0x00, 0x0bb6, 0x0000), 0x00),
                  'Sanctuary':                              (0x01, (0x0012, 0x13, 0x001c, 0x0400, 0x06de, 0x0414, 0x0758, 0x046d, 0x0763, 0x00, 0x02, 0x0000, 0x01aa), 0x00),
                  'Old Man Cave (West)':                    (0x05, (0x00f0, 0x0a, 0x03a0, 0x0264, 0x0500, 0x02b8, 0x05a8, 0x02d3, 0x058d, 0x0a, 0x00, 0x0000, 0x0000), 0x00),
                  'Old Man Cave (East)':                    (0x06, (0x00f1, 0x03, 0x1402, 0x0294, 0x0604, 0x02e8, 0x0678, 0x0303, 0x0683, 0x0a, 0xfc, 0x0000, 0x0000), 0x00),
                  'Old Man House (Bottom)':                 (0x2F, (0x00e4, 0x03, 0x181a, 0x031e, 0x06b4, 0x03a7, 0x0728, 0x038d, 0x0733, 0x00, 0x0c, 0x0000, 0x0000), 0x00),
                  'Old Man House (Top)':                    (0x30, (0x00e5, 0x03, 0x10c6, 0x0224, 0x0814, 0x0278, 0x0888, 0x0293, 0x0893, 0x0a, 0x0c, 0x0000, 0x0000), 0x00),
                  'Death Mountain Return Cave (East)':      (0x2E, (0x00e7, 0x03, 0x0d82, 0x01c4, 0x0600, 0x0218, 0x0648, 0x0233, 0x067f, 0x0a, 0x00, 0x0000, 0x0000), 0x00),
                  'Death Mountain Return Cave (West)':      (0x2D, (0x00e6, 0x0a, 0x00a0, 0x0205, 0x0500, 0x0257, 0x05b8, 0x0272, 0x058d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Spectacle Rock Cave Peak':               (0x22, (0x00ea, 0x03, 0x092c, 0x0133, 0x0754, 0x0187, 0x07c8, 0x01a2, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000), 0x00),
                  'Spectacle Rock Cave':                    (0x21, (0x00fa, 0x03, 0x0eac, 0x01e3, 0x0754, 0x0237, 0x07c8, 0x0252, 0x07d3, 0x0b, 0xfc, 0x0000, 0x0000), 0x00),
                  'Spectacle Rock Cave (Bottom)':           (0x20, (0x00f9, 0x03, 0x0d9c, 0x01c3, 0x06d4, 0x0217, 0x0748, 0x0232, 0x0753, 0x0b, 0xfc, 0x0000, 0x0000), 0x00),
                  'Paradox Cave (Bottom)':                  (0x1D, (0x00ff, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0237, 0x0da8, 0x0252, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Paradox Cave (Middle)':                  (0x1E, (0x00ef, 0x05, 0x17e0, 0x0304, 0x0d00, 0x0358, 0x0dc8, 0x0373, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000), 0x00),
                  'Paradox Cave (Top)':                     (0x1F, (0x00df, 0x05, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Fairy Ascension Cave (Bottom)':          (0x19, (0x00fd, 0x05, 0x0dd4, 0x01c4, 0x0ca6, 0x0218, 0x0d18, 0x0233, 0x0d23, 0x0a, 0xfa, 0x0000, 0x0000), 0x00),
                  'Fairy Ascension Cave (Top)':             (0x1A, (0x00ed, 0x05, 0x0ad4, 0x0163, 0x0ca6, 0x01b7, 0x0d18, 0x01d2, 0x0d23, 0x0b, 0xfa, 0x0000, 0x0000), 0x00),
                  'Spiral Cave':                            (0x1C, (0x00ee, 0x05, 0x07c8, 0x0108, 0x0c46, 0x0158, 0x0cb8, 0x0177, 0x0cc3, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Spiral Cave (Bottom)':                   (0x1B, (0x00fe, 0x05, 0x0cca, 0x01a3, 0x0c56, 0x01f7, 0x0cc8, 0x0212, 0x0cd3, 0x0b, 0xfa, 0x0000, 0x0000), 0x00),
                  'Bumper Cave (Bottom)':                   (0x15, (0x00fb, 0x4a, 0x03a0, 0x0263, 0x0500, 0x02b7, 0x05a8, 0x02d2, 0x058d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Bumper Cave (Top)':                      (0x16, (0x00eb, 0x4a, 0x00a0, 0x020a, 0x0500, 0x0258, 0x05b8, 0x0277, 0x058d, 0x06, 0x00, 0x0000, 0x0000), 0x00),
                  'Superbunny Cave (Top)':                  (0x13, (0x00e8, 0x45, 0x0460, 0x0093, 0x0d00, 0x00e7, 0x0db8, 0x0102, 0x0d7d, 0x0b, 0x00, 0x0000, 0x0000), 0x00),
                  'Superbunny Cave (Bottom)':               (0x12, (0x00f8, 0x45, 0x0ee0, 0x01e4, 0x0d00, 0x0238, 0x0d78, 0x0253, 0x0d7d, 0x0a, 0x00, 0x0000, 0x0000), 0x00),
                  'Hookshot Cave':                          (0x39, (0x003c, 0x45, 0x04da, 0x00a3, 0x0cd6, 0x0107, 0x0d48, 0x0112, 0x0d53, 0x0b, 0xfa, 0x0000, 0x0000), 0x20),
                  'Hookshot Cave Back Entrance':            (0x3A, (0x002c, 0x45, 0x004c, 0x0000, 0x0c56, 0x0038, 0x0cc8, 0x006f, 0x0cd3, 0x00, 0x0a, 0x0000, 0x0000), 0x00),
                  'Ganons Tower':                           (0x36, (0x000c, 0x43, 0x0052, 0x0000, 0x0884, 0x0028, 0x08f8, 0x006f, 0x0903, 0x00, 0xfc, 0x0000, 0x0000), 0x20),
                  'Pyramid Entrance':                       (0x35, (0x0010, 0x5b, 0x0b0e, 0x075a, 0x0674, 0x07a8, 0x06e8, 0x07c7, 0x06f3, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Skull Woods First Section Hole (West)':  ([0xDB84D, 0xDB84E], None),
                  'Skull Woods First Section Hole (East)':  ([0xDB84F, 0xDB850], None),
                  'Skull Woods First Section Hole (North)': ([0xDB84C], None),
                  'Skull Woods Second Section Hole':        ([0xDB851, 0xDB852], None),
                  'Pyramid Hole':                           ([0xDB854, 0xDB855, 0xDB856], None),
                  'Inverted Pyramid Hole':                  ([0xDB854, 0xDB855, 0xDB856, 0x180340], None),
                  'Waterfall of Wishing':                   (0x5B, (0x0114, 0x0f, 0x0080, 0x0200, 0x0e00, 0x0207, 0x0e60, 0x026f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Dam':                                    (0x4D, (0x010b, 0x3b, 0x04a0, 0x0e8a, 0x06fa, 0x0ed8, 0x0778, 0x0ef7, 0x077f, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Blinds Hideout':                         (0x60, (0x0119, 0x18, 0x02b2, 0x064a, 0x0186, 0x0697, 0x0208, 0x06b7, 0x0213, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Hyrule Castle Secret Entrance Drop':     ([0xDB858], None),
                  'Bonk Fairy (Light)':                     (0x76, (0x0126, 0x2b, 0x00a0, 0x0a0a, 0x0700, 0x0a67, 0x0788, 0x0a77, 0x0785, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Lake Hylia Fairy':                       (0x5D, (0x0115, 0x2e, 0x0016, 0x0a00, 0x0cb6, 0x0a37, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Light Hype Fairy':                       (0x6B, (0x0115, 0x34, 0x00a0, 0x0c04, 0x0900, 0x0c58, 0x0988, 0x0c73, 0x0985, 0x0a, 0xf6, 0x0000, 0x0000), 0x02),
                  'Desert Fairy':                           (0x71, (0x0115, 0x3a, 0x0000, 0x0e00, 0x0400, 0x0e26, 0x0468, 0x0e6d, 0x0485, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Kings Grave':                            (0x5A, (0x0113, 0x14, 0x0320, 0x0456, 0x0900, 0x04a6, 0x0998, 0x04c3, 0x097d, 0x0a, 0xf6, 0x0000, 0x0000), 0x20),
                  'Tavern North':                           (0x42, (0x0103, 0x18, 0x1440, 0x08a7, 0x0206, 0x091b, 0x0288, 0x0914, 0x0293, 0xf7, 0x09, 0xFFFF, 0x0000), 0x00),
                  'Chicken House':                          (0x4A, (0x0108, 0x18, 0x1120, 0x0837, 0x0106, 0x0888, 0x0188, 0x08a4, 0x0193, 0x07, 0xf9, 0x1530, 0x0000), 0x00),
                  'Aginahs Cave':                           (0x70, (0x010a, 0x30, 0x0656, 0x0cc6, 0x02aa, 0x0d18, 0x0328, 0x0d33, 0x032f, 0x08, 0xf8, 0x0000, 0x0000), 0x00),
                  'Sahasrahlas Hut':                        (0x44, (0x0105, 0x1e, 0x0610, 0x06d4, 0x0c76, 0x0727, 0x0cf0, 0x0743, 0x0cfb, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Lake Hylia Shop':                        (0x57, (0x0112, 0x35, 0x0022, 0x0c00, 0x0b1a, 0x0c26, 0x0b98, 0x0c6d, 0x0b9f, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Capacity Upgrade':                       (0x5C, (0x0115, 0x35, 0x0a46, 0x0d36, 0x0c2a, 0x0d88, 0x0ca8, 0x0da3, 0x0caf, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Kakariko Well Drop':                     ([0xDB85C, 0xDB85D], None),
                  'Blacksmiths Hut':                        (0x63, (0x0121, 0x22, 0x010c, 0x081a, 0x0466, 0x0868, 0x04d8, 0x0887, 0x04e3, 0x06, 0xfa, 0x041A, 0x0000), 0x00),
                  'Bat Cave Drop':                          ([0xDB859, 0xDB85A], None),
                  'Sick Kids House':                        (0x3F, (0x0102, 0x18, 0x10be, 0x0826, 0x01f6, 0x0877, 0x0278, 0x0893, 0x0283, 0x08, 0xf8, 0x14CE, 0x0000), 0x00),
                  'North Fairy Cave Drop':                  ([0xDB857], None),
                  'Lost Woods Gamble':                      (0x3B, (0x0100, 0x00, 0x004e, 0x0000, 0x0272, 0x0008, 0x02f0, 0x006f, 0x02f7, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Fortune Teller (Light)':                 (0x64, (0x0122, 0x11, 0x060e, 0x04b4, 0x027d, 0x0508, 0x02f8, 0x0523, 0x0302, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Snitch Lady (East)':                     (0x3D, (0x0101, 0x18, 0x0ad8, 0x074a, 0x02c6, 0x0798, 0x0348, 0x07b7, 0x0353, 0x06, 0xfa, 0x0DE8, 0x0000), 0x00),
                  'Snitch Lady (West)':                     (0x3E, (0x0101, 0x18, 0x0788, 0x0706, 0x0046, 0x0758, 0x00c8, 0x0773, 0x00d3, 0x08, 0xf8, 0x0B98, 0x0000), 0x00),
                  'Bush Covered House':                     (0x43, (0x0103, 0x18, 0x1156, 0x081a, 0x02b6, 0x0868, 0x0338, 0x0887, 0x0343, 0x06, 0xfa, 0x1466, 0x0000), 0x00),
                  'Tavern (Front)':                         (0x41, (0x0103, 0x18, 0x1842, 0x0916, 0x0206, 0x0967, 0x0288, 0x0983, 0x0293, 0x08, 0xf8, 0x1C50, 0x0000), 0x00),
                  'Light World Bomb Hut':                   (0x49, (0x0107, 0x18, 0x1800, 0x0916, 0x0000, 0x0967, 0x0068, 0x0983, 0x008d, 0x08, 0xf8, 0x9C0C, 0x0000), 0x02),
                  'Kakariko Shop':                          (0x45, (0x011f, 0x18, 0x16a8, 0x08e7, 0x0136, 0x0937, 0x01b8, 0x0954, 0x01c3, 0x07, 0xf9, 0x1AB6, 0x0000), 0x00),
                  'Lost Woods Hideout Drop':                ([0xDB853], None),
                  'Lumberjack Tree Tree':                   ([0xDB85B], None),
                  'Cave 45':                                (0x50, (0x011b, 0x32, 0x0680, 0x0cc9, 0x0400, 0x0d16, 0x0438, 0x0d36, 0x0485, 0x07, 0xf9, 0x0000, 0x0000), 0x00),
                  'Graveyard Cave':                         (0x51, (0x011b, 0x14, 0x0016, 0x0400, 0x08a2, 0x0446, 0x0918, 0x046d, 0x091f, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Checkerboard Cave':                      (0x7D, (0x0126, 0x30, 0x00c8, 0x0c0a, 0x024a, 0x0c67, 0x02c8, 0x0c77, 0x02cf, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Mini Moldorm Cave':                      (0x7C, (0x0123, 0x35, 0x1480, 0x0e96, 0x0a00, 0x0ee8, 0x0a68, 0x0f03, 0x0a85, 0x08, 0xf8, 0x0000, 0x0000), 0x02),
                  'Long Fairy Cave':                        (0x54, (0x011e, 0x2f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Good Bee Cave':                          (0x6A, (0x0120, 0x37, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  '20 Rupee Cave':                          (0x7A, (0x0125, 0x37, 0x0200, 0x0c23, 0x0e00, 0x0c86, 0x0e68, 0x0c92, 0x0e7d, 0x0d, 0xf3, 0x0000, 0x0000), 0x20),
                  '50 Rupee Cave':                          (0x78, (0x0124, 0x3a, 0x0790, 0x0eea, 0x047a, 0x0f47, 0x04f8, 0x0f57, 0x04ff, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Ice Rod Cave':                           (0x7F, (0x0120, 0x37, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000), 0x02),
                  'Bonk Rock Cave':                         (0x79, (0x0124, 0x13, 0x0280, 0x044a, 0x0600, 0x04a7, 0x0638, 0x04b7, 0x067d, 0x06, 0xfa, 0x0000, 0x0000), 0x20),
                  'Library':                                (0x48, (0x0107, 0x29, 0x0100, 0x0a14, 0x0200, 0x0a67, 0x0278, 0x0a83, 0x0285, 0x0a, 0xf6, 0x040E, 0x0000), 0x00),
                  'Potion Shop':                            (0x4B, (0x0109, 0x16, 0x070a, 0x04e6, 0x0c56, 0x0538, 0x0cc8, 0x0553, 0x0cd3, 0x08, 0xf8, 0x0A98, 0x0000), 0x00),
                  'Sanctuary Grave':                        ([0xDB85E], None),
                  'Hookshot Fairy':                         (0x4F, (0x010c, 0x05, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0d78, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000), 0x00),
                  'Pyramid Fairy':                          (0x62, (0x0116, 0x5b, 0x0b1e, 0x0754, 0x06fa, 0x07a7, 0x0778, 0x07c3, 0x077f, 0x0a, 0xf6, 0x0000, 0x0000), 0x02),
                  'East Dark World Hint':                   (0x68, (0x010e, 0x6f, 0x06a0, 0x0aca, 0x0f00, 0x0b18, 0x0fa8, 0x0b37, 0x0f85, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Palace of Darkness Hint':                (0x67, (0x011a, 0x5e, 0x0c24, 0x0794, 0x0d12, 0x07e8, 0x0d90, 0x0803, 0x0d97, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Dark Lake Hylia Fairy':                  (0x6C, (0x0115, 0x6e, 0x0016, 0x0a00, 0x0cb6, 0x0a36, 0x0d28, 0x0a6d, 0x0d33, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Dark Lake Hylia Ledge Fairy':            (0x80, (0x0115, 0x77, 0x0080, 0x0c00, 0x0e00, 0x0c37, 0x0e48, 0x0c6f, 0x0e7d, 0x00, 0x00, 0x0000, 0x0000), 0x02),
                  'Dark Lake Hylia Ledge Spike Cave':       (0x7B, (0x0125, 0x77, 0x0200, 0x0c27, 0x0e00, 0x0c86, 0x0e68, 0x0c96, 0x0e7d, 0x09, 0xf7, 0x0000, 0x0000), 0x20),
                  'Dark Lake Hylia Ledge Hint':             (0x69, (0x010e, 0x77, 0x0084, 0x0c00, 0x0e26, 0x0c36, 0x0e98, 0x0c6f, 0x0ea3, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Hype Cave':                              (0x3C, (0x011e, 0x74, 0x00a0, 0x0c0a, 0x0900, 0x0c58, 0x0988, 0x0c77, 0x097d, 0x06, 0xfa, 0x0000, 0x0000), 0x02),
                  'Bonk Fairy (Dark)':                      (0x77, (0x0126, 0x6b, 0x00a0, 0x0a05, 0x0700, 0x0a66, 0x0788, 0x0a72, 0x0785, 0x0b, 0xf5, 0x0000, 0x0000), 0x20),
                  'Brewery':                                (0x47, (0x0106, 0x58, 0x16a8, 0x08e4, 0x013e, 0x0938, 0x01b8, 0x0953, 0x01c3, 0x0a, 0xf6, 0x1AB6, 0x0000), 0x02),
                  'C-Shaped House':                         (0x53, (0x011c, 0x58, 0x09d8, 0x0744, 0x02ce, 0x0797, 0x0348, 0x07b3, 0x0353, 0x0a, 0xf6, 0x0DE8, 0x0000), 0x00),
                  'Chest Game':                             (0x46, (0x0106, 0x58, 0x078a, 0x0705, 0x004e, 0x0758, 0x00c8, 0x0774, 0x00d3, 0x09, 0xf7, 0x0B98, 0x0000), 0x00),
                  'Hammer Peg Cave':                        (0x7E, (0x0127, 0x62, 0x0894, 0x091e, 0x0492, 0x09a6, 0x0508, 0x098b, 0x050f, 0x00, 0x00, 0x0000, 0x0000), 0x20),
                  'Red Shield Shop':                        (0x74, (0x0110, 0x5a, 0x079a, 0x06e8, 0x04d6, 0x0738, 0x0548, 0x0755, 0x0553, 0x08, 0xf8, 0x0AA8, 0x0000), 0x00),
                  'Dark Sanctuary Hint':                    (0x59, (0x0112, 0x53, 0x001e, 0x0400, 0x06e2, 0x0446, 0x0758, 0x046d, 0x075f, 0x00, 0x00, 0x0000, 0x0000), 0x00),
                  'Fortune Teller (Dark)':                  (0x65, (0x0122, 0x51, 0x0610, 0x04b4, 0x027e, 0x0507, 0x02f8, 0x0523, 0x0303, 0x0a, 0xf6, 0x091E, 0x0000), 0x00),
                  'Dark World Shop':                        (0x5F, (0x010f, 0x58, 0x1058, 0x0814, 0x02be, 0x0868, 0x0338, 0x0883, 0x0343, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Dark Lumberjack Shop':                   (0x56, (0x010f, 0x42, 0x041c, 0x0074, 0x04e2, 0x00c7, 0x0558, 0x00e3, 0x055f, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Dark Potion Shop':                       (0x6E, (0x010f, 0x56, 0x080e, 0x04f4, 0x0c66, 0x0548, 0x0cd8, 0x0563, 0x0ce3, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Archery Game':                           (0x58, (0x0111, 0x69, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000), 0x00),
                  'Mire Shed':                              (0x5E, (0x010d, 0x70, 0x0384, 0x0c69, 0x001e, 0x0cb6, 0x0098, 0x0cd6, 0x00a3, 0x07, 0xf9, 0x0000, 0x0000), 0x00),
                  'Mire Hint':                              (0x61, (0x0114, 0x70, 0x0654, 0x0cc5, 0x02aa, 0x0d16, 0x0328, 0x0d32, 0x032f, 0x09, 0xf7, 0x0000, 0x0000), 0x00),
                  'Mire Fairy':                             (0x55, (0x0115, 0x70, 0x03a8, 0x0c6a, 0x013a, 0x0cb7, 0x01b8, 0x0cd7, 0x01bf, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Spike Cave':                             (0x40, (0x0117, 0x43, 0x0ed4, 0x01e4, 0x08aa, 0x0236, 0x0928, 0x0253, 0x092f, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Dark Death Mountain Shop':               (0x6D, (0x0112, 0x45, 0x0ee0, 0x01e3, 0x0d00, 0x0236, 0x0daa, 0x0252, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000), 0x00),
                  'Dark Death Mountain Fairy':              (0x6F, (0x0115, 0x43, 0x1400, 0x0294, 0x0600, 0x02e8, 0x0678, 0x0303, 0x0685, 0x0a, 0xf6, 0x0000, 0x0000), 0x00),
                  'Mimic Cave':                             (0x4E, (0x010c, 0x05, 0x07e0, 0x0103, 0x0d00, 0x0156, 0x0d78, 0x0172, 0x0d7d, 0x0b, 0xf5, 0x0000, 0x0000), 0x00),
                  'Big Bomb Shop':                          (0x52, (0x011c, 0x6c, 0x0506, 0x0a9a, 0x0832, 0x0ae7, 0x08b8, 0x0b07, 0x08bf, 0x06, 0xfa, 0x0816, 0x0000), 0x00),
                  'Dark Lake Hylia Shop':                   (0x73, (0x010f, 0x75, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Lumberjack House':                       (0x75, (0x011f, 0x02, 0x049c, 0x0088, 0x04e6, 0x00d8, 0x0558, 0x00f7, 0x0563, 0x08, 0xf8, 0x07AA, 0x0000), 0x00),
                  'Lake Hylia Fortune Teller':              (0x72, (0x0122, 0x35, 0x0380, 0x0c6a, 0x0a00, 0x0cb8, 0x0a58, 0x0cd7, 0x0a85, 0x06, 0xfa, 0x0000, 0x0000), 0x00),
                  'Kakariko Gamble Game':                   (0x66, (0x0118, 0x29, 0x069e, 0x0ac4, 0x02ea, 0x0b18, 0x0368, 0x0b33, 0x036f, 0x0a, 0xf6, 0x09AC, 0x0000), 0x00)}

# format:
# Key=Name
# value = entrance #
#        | (entrance #, exit #)
exit_ids = {'Links House Exit': (0x01, 0x00),
            'Chris Houlihan Room Exit': (None, 0x3D),
            'Desert Palace Exit (South)': (0x09, 0x0A),
            'Desert Palace Exit (West)': (0x0B, 0x0C),
            'Desert Palace Exit (East)': (0x0A, 0x0B),
            'Desert Palace Exit (North)': (0x0C, 0x0D),
            'Eastern Palace Exit': (0x08, 0x09),
            'Tower of Hera Exit': (0x33, 0x2D),
            'Hyrule Castle Exit (South)': (0x04, 0x03),
            'Hyrule Castle Exit (West)': (0x03, 0x02),
            'Hyrule Castle Exit (East)': (0x05, 0x04),
            'Agahnims Tower Exit': (0x24, 0x25),
            'Thieves Town Exit': (0x34, 0x35),
            'Skull Woods First Section Exit': (0x2A, 0x2B),
            'Skull Woods Second Section Exit (East)': (0x29, 0x2A),
            'Skull Woods Second Section Exit (West)': (0x28, 0x29),
            'Skull Woods Final Section Exit': (0x2B, 0x2C),
            'Ice Palace Exit': (0x2D, 0x2E),
            'Misery Mire Exit': (0x27, 0x28),
            'Palace of Darkness Exit': (0x26, 0x27),
            'Swamp Palace Exit': (0x25, 0x26),
            'Turtle Rock Exit (Front)': (0x35, 0x34),
            'Turtle Rock Ledge Exit (West)': (0x15, 0x16),
            'Turtle Rock Ledge Exit (East)': (0x19, 0x1A),
            'Turtle Rock Isolated Ledge Exit': (0x18, 0x19),
            'Hyrule Castle Secret Entrance Exit': (0x32, 0x33),
            'Kakariko Well Exit': (0x39, 0x3A),
            'Bat Cave Exit': (0x11, 0x12),
            'Elder House Exit (East)': (0x0E, 0x0F),
            'Elder House Exit (West)': (0x0D, 0x0E),
            'North Fairy Cave Exit': (0x38, 0x39),
            'Lost Woods Hideout Exit': (0x2C, 0x36),
            'Lumberjack Tree Exit': (0x12, 0x13),
            'Two Brothers House Exit (East)': (0x10, 0x11),
            'Two Brothers House Exit (West)': (0x0F, 0x10),
            'Sanctuary Exit': (0x02, 0x01),
            'Old Man Cave Exit (East)': (0x07, 0x08),
            'Old Man Cave Exit (West)': (0x06, 0x07),
            'Old Man House Exit (Bottom)': (0x30, 0x31),
            'Old Man House Exit (Top)': (0x31, 0x32),
            'Death Mountain Return Cave Exit (West)': (0x2E, 0x2F),
            'Death Mountain Return Cave Exit (East)': (0x2F, 0x30),
            'Spectacle Rock Cave Exit': (0x21, 0x22),
            'Spectacle Rock Cave Exit (Top)': (0x22, 0x23),
            'Spectacle Rock Cave Exit (Peak)': (0x23, 0x24),
            'Paradox Cave Exit (Bottom)': (0x1E, 0x1F),
            'Paradox Cave Exit (Middle)': (0x1F, 0x20),
            'Paradox Cave Exit (Top)': (0x20, 0x21),
            'Fairy Ascension Cave Exit (Bottom)': (0x1A, 0x1B),
            'Fairy Ascension Cave Exit (Top)': (0x1B, 0x1C),
            'Spiral Cave Exit': (0x1C, 0x1D),
            'Spiral Cave Exit (Top)': (0x1D, 0x1E),
            'Bumper Cave Exit (Top)': (0x17, 0x18),
            'Bumper Cave Exit (Bottom)': (0x16, 0x17),
            'Superbunny Cave Exit (Top)': (0x14, 0x15),
            'Superbunny Cave Exit (Bottom)': (0x13, 0x14),
            'Hookshot Cave Front Exit': (0x3A, 0x3B),
            'Hookshot Cave Back Exit': (0x3B, 0x3C),
            'Ganons Tower Exit': (0x37, 0x38),
            'Pyramid Exit': (0x36, 0x37),
            'Waterfall of Wishing': 0x5C,
            'Dam': 0x4E,
            'Blinds Hideout': 0x61,
            'Lumberjack House': 0x6B,
            'Bonk Fairy (Light)': 0x71,
            'Bonk Fairy (Dark)': 0x71,
            'Lake Hylia Healer Fairy': 0x5E,
            'Light Hype Fairy': 0x5E,
            'Desert Healer Fairy': 0x5E,
            'Dark Lake Hylia Healer Fairy': 0x5E,
            'Dark Lake Hylia Ledge Healer Fairy': 0x5E,
            'Mire Healer Fairy': 0x5E,
            'Dark Death Mountain Healer Fairy': 0x5E,
            'Fortune Teller (Light)': 0x65,
            'Lake Hylia Fortune Teller': 0x65,
            'Kings Grave': 0x5B,
            'Tavern': 0x43,
            'Chicken House': 0x4B,
            'Aginahs Cave': 0x4D,
            'Sahasrahlas Hut': 0x45,
            'Lake Hylia Shop': 0x58,
            'Dark Death Mountain Shop': 0x58,
            'Capacity Upgrade': 0x5D,
            'Blacksmiths Hut': 0x64,
            'Sick Kids House': 0x40,
            'Lost Woods Gamble': 0x3C,
            'Snitch Lady (East)': 0x3E,
            'Snitch Lady (West)': 0x3F,
            'Bush Covered House': 0x44,
            'Tavern (Front)': 0x42,
            'Light World Bomb Hut': 0x4A,
            'Kakariko Shop': 0x46,
            'Cave 45': 0x51,
            'Graveyard Cave': 0x52,
            'Checkerboard Cave': 0x72,
            'Mini Moldorm Cave': 0x6C,
            'Long Fairy Cave': 0x55,
            'Good Bee Cave': 0x56,
            '20 Rupee Cave': 0x6F,
            '50 Rupee Cave': 0x6D,
            'Ice Rod Cave': 0x84,
            'Bonk Rock Cave': 0x6E,
            'Library': 0x49,
            'Kakariko Gamble Game': 0x67,
            'Potion Shop': 0x4C,
            'Hookshot Fairy': 0x50,
            'Pyramid Fairy': 0x63,
            'East Dark World Hint': 0x69,
            'Palace of Darkness Hint': 0x68,
            'Big Bomb Shop': 0x53,
            'Village of Outcasts Shop': 0x60,
            'Dark Lake Hylia Shop': 0x60,
            'Dark Lumberjack Shop': 0x60,
            'Dark Potion Shop': 0x60,
            'Dark Lake Hylia Ledge Spike Cave': 0x70,
            'Dark Lake Hylia Ledge Hint': 0x6A,
            'Hype Cave': 0x3D,
            'Brewery': 0x48,
            'C-Shaped House': 0x54,
            'Chest Game': 0x47,
            'Hammer Peg Cave': 0x83,
            'Red Shield Shop': 0x57,
            'Dark Sanctuary Hint': 0x5A,
            'Fortune Teller (Dark)': 0x66,
            'Archery Game': 0x59,
            'Mire Shed': 0x5F,
            'Mire Hint': 0x62,
            'Spike Cave': 0x41,
            'Mimic Cave': 0x4F,
            'Kakariko Well (top)': 0x80,
            'Hyrule Castle Secret Entrance': 0x7D,
            'Bat Cave (right)': 0x7E,
            'North Fairy Cave': 0x7C,
            'Lost Woods Hideout (top)': 0x7A,
            'Lumberjack Tree (top)': 0x7F,
            'Sewer Drop': 0x81,
            'Skull Back Drop': 0x79,
            'Skull Left Drop': 0x77,
            'Skull Pinball': 0x78,
            'Skull Pot Circle': 0x76,
            'Pyramid': 0x7B}

ow_prize_table = {'Links House': (0x8b1, 0xb2d),
                  'Desert Palace Entrance (South)': (0x108, 0xd70), 'Desert Palace Entrance (West)': (0x031, 0xca0),
                  'Desert Palace Entrance (North)': (0x0e1, 0xba0), 'Desert Palace Entrance (East)': (0x191, 0xca0),
                  'Eastern Palace': (0xf31, 0x620), 'Tower of Hera': (0x8D0, 0x080),
                  'Hyrule Castle Entrance (South)': (0x820, 0x730), 'Hyrule Castle Entrance (West)': (0x740, 0x5D0),
                  'Hyrule Castle Entrance (East)': (0x8f0, 0x5D0), 'Inverted Pyramid Entrance': (0x6C0, 0x5D0),
                  'Agahnims Tower': (0x820, 0x5D0),
                  'Thieves Town': (0x1d0, 0x780), 'Skull Woods First Section Door': (0x240, 0x280),
                  'Skull Woods Second Section Door (East)': (0x1a0, 0x240),
                  'Skull Woods Second Section Door (West)': (0x0c0, 0x1c0), 'Skull Woods Final Section': (0x082, 0x0b0),
                  'Ice Palace': (0xca0, 0xda0),
                  'Misery Mire': (0x100, 0xca0),
                  'Palace of Darkness': (0xf40, 0x620), 'Swamp Palace': (0x759, 0xED0),
                  'Turtle Rock': (0xf11, 0x103),
                  'Dark Death Mountain Ledge (West)': (0xb80, 0x180),
                  'Dark Death Mountain Ledge (East)': (0xc80, 0x180),
                  'Turtle Rock Isolated Ledge Entrance': (0xc00, 0x240),
                  'Hyrule Castle Secret Entrance Stairs': (0x8D0, 0x700),
                  'Kakariko Well Cave': (0x060, 0x680),
                  'Bat Cave Cave': (0x540, 0x8f0),
                  'Elder House (East)': (0x2b0, 0x6a0),
                  'Elder House (West)': (0x230, 0x6a0),
                  'North Fairy Cave': (0xa80, 0x440),
                  'Lost Woods Hideout Stump': (0x240, 0x280),
                  'Lumberjack Tree Cave': (0x4e0, 0x004),
                  'Two Brothers House (East)': (0x200, 0x0b60),
                  'Two Brothers House (West)': (0x180, 0x0b60),
                  'Sanctuary': (0x720, 0x4a0),
                  'Old Man Cave (West)': (0x580, 0x2c0),
                  'Old Man Cave (East)': (0x620, 0x2c0),
                  'Old Man House (Bottom)': (0x720, 0x320),
                  'Old Man House (Top)': (0x820, 0x220),
                  'Death Mountain Return Cave (East)': (0x600, 0x220),
                  'Death Mountain Return Cave (West)': (0x500, 0x1c0),
                  'Spectacle Rock Cave Peak': (0x720, 0x0a0),
                  'Spectacle Rock Cave': (0x790, 0x1a0),
                  'Spectacle Rock Cave (Bottom)': (0x710, 0x0a0),
                  'Paradox Cave (Bottom)': (0xd80, 0x180),
                  'Paradox Cave (Middle)': (0xd80, 0x380),
                  'Paradox Cave (Top)': (0xd80, 0x020),
                  'Fairy Ascension Cave (Bottom)': (0xcc8, 0x2a0),
                  'Fairy Ascension Cave (Top)': (0xc00, 0x240),
                  'Spiral Cave': (0xb80, 0x180),
                  'Spiral Cave (Bottom)': (0xb80, 0x2c0),
                  'Bumper Cave (Bottom)': (0x580, 0x2c0),
                  'Bumper Cave (Top)': (0x500, 0x1c0),
                  'Superbunny Cave (Top)': (0xd80, 0x020),
                  'Superbunny Cave (Bottom)': (0xd00, 0x180),
                  'Hookshot Cave': (0xc80, 0x0c0),
                  'Hookshot Cave Back Entrance': (0xcf0, 0x004),
                  'Ganons Tower': (0x8D0, 0x080),
                  'Pyramid Entrance': (0x640, 0x7c0),
                  'Skull Woods First Section Hole (West)': None,
                  'Skull Woods First Section Hole (East)': None,
                  'Skull Woods First Section Hole (North)': None,
                  'Skull Woods Second Section Hole': None,
                  'Pyramid Hole': None,
                  'Inverted Pyramid Hole': None,
                  'Waterfall of Wishing': (0xe80, 0x280),
                  'Dam': (0x759, 0xED0),
                  'Blinds Hideout': (0x190, 0x6c0),
                  'Hyrule Castle Secret Entrance Drop': None,
                  'Bonk Fairy (Light)': (0x740, 0xa80),
                  'Lake Hylia Fairy': (0xd40, 0x9f0),
                  'Light Hype Fairy': (0x940, 0xc80),
                  'Desert Fairy': (0x420, 0xe00),
                  'Kings Grave': (0x920, 0x520),
                  'Tavern North': (0x270, 0x900),
                  'Chicken House': (0x120, 0x880),
                  'Aginahs Cave': (0x2e0, 0xd00),
                  'Sahasrahlas Hut': (0xcf0, 0x6c0),
                  'Lake Hylia Shop': (0xbc0, 0xc00),
                  'Capacity Upgrade': (0xca0, 0xda0),
                  'Kakariko Well Drop': None,
                  'Blacksmiths Hut': (0x4a0, 0x880),
                  'Bat Cave Drop': None,
                  'Sick Kids House': (0x220, 0x880),
                  'North Fairy Cave Drop': None,
                  'Lost Woods Gamble': (0x240, 0x080),
                  'Fortune Teller (Light)': (0x2c0, 0x4c0),
                  'Snitch Lady (East)': (0x310, 0x7a0),
                  'Snitch Lady (West)': (0x080, 0x7a0),
                  'Bush Covered House': (0x2e0, 0x880),
                  'Tavern (Front)': (0x270, 0x980),
                  'Light World Bomb Hut': (0x070, 0x980),
                  'Kakariko Shop': (0x170, 0x980),
                  'Lost Woods Hideout Drop': None,
                  'Lumberjack Tree Tree': None,
                  'Cave 45': (0x440, 0xca0), 'Graveyard Cave': (0x8f0, 0x430),
                  'Checkerboard Cave': (0x260, 0xc00),
                  'Mini Moldorm Cave': (0xa40, 0xe80),
                  'Long Fairy Cave': (0xf60, 0xb00),
                  'Good Bee Cave': (0xec0, 0xc00),
                  '20 Rupee Cave': (0xe80, 0xca0),
                  '50 Rupee Cave': (0x4d0, 0xed0),
                  'Ice Rod Cave': (0xe00, 0xc00),
                  'Bonk Rock Cave': (0x5f0, 0x460),
                  'Library': (0x270, 0xaa0),
                  'Potion Shop': (0xc80, 0x4c0),
                  'Sanctuary Grave': None,
                  'Hookshot Fairy': (0xd00, 0x180),
                  'Pyramid Fairy': (0x740, 0x740),
                  'East Dark World Hint': (0xf60, 0xb00),
                  'Palace of Darkness Hint': (0xd60, 0x7c0),
                  'Dark Lake Hylia Fairy': (0xd40, 0x9f0),
                  'Dark Lake Hylia Ledge Fairy': (0xe00, 0xc00),
                  'Dark Lake Hylia Ledge Spike Cave': (0xe80, 0xca0),
                  'Dark Lake Hylia Ledge Hint': (0xec0, 0xc00),
                  'Hype Cave': (0x940, 0xc80),
                  'Bonk Fairy (Dark)': (0x740, 0xa80),
                  'Brewery': (0x170, 0x980), 'C-Shaped House': (0x310, 0x7a0), 'Chest Game': (0x080, 0x7a0),
                  'Hammer Peg Cave': (0x4c0, 0x940),
                  'Red Shield Shop': (0x500, 0x680),
                  'Dark Sanctuary Hint': (0x720, 0x4a0),
                  'Fortune Teller (Dark)': (0x2c0, 0x4c0),
                  'Dark World Shop': (0x2e0, 0x880),
                  'Dark Lumberjack Shop': (0x4e0, 0x0d0),
                  'Dark Potion Shop': (0xc80, 0x4c0),
                  'Archery Game': (0x2f0, 0xaf0),
                  'Mire Shed': (0x060, 0xc90),
                  'Mire Hint': (0x2e0, 0xd00),
                  'Mire Fairy': (0x1c0, 0xc90),
                  'Spike Cave': (0x860, 0x180),
                  'Dark Death Mountain Shop': (0xd80, 0x180),
                  'Dark Death Mountain Fairy': (0x620, 0x2c0),
                  'Mimic Cave': (0xc80, 0x180),
                  'Big Bomb Shop': (0x8b1, 0xb2d),
                  'Dark Lake Hylia Shop': (0xa40, 0xc40),
                  'Lumberjack House': (0x4e0, 0x0d0),
                  'Lake Hylia Fortune Teller': (0xa40, 0xc40),
                  'Kakariko Gamble Game': (0x2f0, 0xaf0)}
