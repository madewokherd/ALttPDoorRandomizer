"""
Helper functions to deliver entrance/exit/region sets to OWG rules.
"""

from BaseClasses import Entrance


def get_sword_required_superbunny_mirror_regions():
    """
    Cave regions that superbunny can get through - but only with a sword.
    """
    yield 'Spiral Cave (Top)'

def get_boots_required_superbunny_mirror_regions():
    """
    Cave regions that superbunny can get through - but only with boots.
    """
    yield 'Two Brothers House'

def get_boots_required_superbunny_mirror_locations():
    """
    Cave locations that superbunny can access - but only with boots.
    """
    yield 'Sahasrahla\'s Hut - Left'
    yield 'Sahasrahla\'s Hut - Middle'
    yield 'Sahasrahla\'s Hut - Right'


def get_invalid_mirror_bunny_entrances():
    """
    Entrances that can't be superbunny-mirrored into.
    """
    yield 'Skull Woods Final Section'
    yield 'Hype Cave'
    yield 'Bonk Fairy (Dark)'
    yield 'Thieves Town'
    yield 'Hammer Peg Cave'
    yield 'Brewery'
    yield 'Hookshot Cave'
    yield 'Dark Lake Hylia Ledge Fairy'
    yield 'Dark Lake Hylia Ledge Spike Cave'
    yield 'Palace of Darkness'
    yield 'Misery Mire'
    yield 'Turtle Rock'
    yield 'Bonk Rock Cave'
    yield 'Bonk Fairy (Light)'
    yield '50 Rupee Cave'
    yield '20 Rupee Cave'
    yield 'Checkerboard Cave'
    yield 'Light Hype Fairy'
    yield 'Waterfall of Wishing'
    yield 'Light World Bomb Hut'
    yield 'Mini Moldorm Cave'
    yield 'Ice Rod Cave'
    yield 'Sanctuary Grave'
    yield 'Kings Grave'
    yield 'Sanctuary Grave'
    yield 'Hyrule Castle Secret Entrance Drop'
    yield 'Skull Woods Second Section Hole'
    yield 'Skull Woods First Section Hole (North)'


def get_superbunny_accessible_locations():
    """
    Interior locations that can be accessed with superbunny state.
    """

    yield 'Waterfall of Wishing - Left'
    yield 'Waterfall of Wishing - Right'
    yield 'King\'s Tomb'
    yield 'Floodgate'
    yield 'Floodgate Chest'
    yield 'Cave 45'
    yield 'Bonk Rock Cave'
    yield 'Brewery'
    yield 'C-Shaped House'
    yield 'Chest Game'
    yield 'Mire Shed - Left'
    yield 'Mire Shed - Right'
    yield 'Secret Passage'
    yield 'Ice Rod Cave'
    yield 'Pyramid Fairy - Left'
    yield 'Pyramid Fairy - Right'
    yield 'Superbunny Cave - Top'
    yield 'Superbunny Cave - Bottom'
    yield 'Blind\'s Hideout - Left'
    yield 'Blind\'s Hideout - Right'
    yield 'Blind\'s Hideout - Far Left'
    yield 'Blind\'s Hideout - Far Right'
    yield 'Kakariko Well - Left'
    yield 'Kakariko Well - Middle'
    yield 'Kakariko Well - Right'
    yield 'Kakariko Well - Bottom'
    yield 'Kakariko Tavern'
    yield 'Library'
    yield 'Spiral Cave'
    for location in get_boots_required_superbunny_mirror_locations():
        yield location


def get_non_mandatory_exits(inverted):
    """
    Entrances that can be reached with full equipment using overworld glitches and don't need to be an exit.
    The following are still be mandatory exits:

    Open:
    Turtle Rock Isolated Ledge Entrance
    Skull Woods Second Section Door (West) (or Skull Woods Final Section)

    Inverted:
    Two Brothers House (West)
    Desert Palace Entrance (East)
    """

    yield 'Bumper Cave (Top)'
    yield 'Death Mountain Return Cave (West)'
    yield 'Hookshot Cave Back Entrance'

    if inverted:
        yield 'Desert Palace Entrance (North)'
        yield 'Desert Palace Entrance (West)'
        yield 'Agahnims Tower'
        yield 'Hyrule Castle Entrance (West)'
        yield 'Hyrule Castle Entrance (East)'
    else:
        yield 'Dark Death Mountain Ledge (West)'
        yield 'Dark Death Mountain Ledge (East)'
        yield 'Mimic Cave'
        yield 'Desert Palace Entrance (East)'


def get_boots_clip_exits_lw(inverted = False):
    """
    Special Light World region exits that require boots clips.
    """

    yield ('Lumberjack DMA Clip', 'Lumberjack Area', 'West Death Mountain (Bottom)')
    yield ('Spectacle Rock Clip', 'West Death Mountain (Top)', 'Spectacle Rock Ledge')
    yield ('Hera Ascent Clip', 'West Death Mountain (Bottom)', 'West Death Mountain (Top)')
    yield ('Death Mountain Glitched Bridge Clip', 'West Death Mountain (Bottom)', 'East Death Mountain (Top East)')
    yield ('Sanctuary DMD Clip', 'West Death Mountain (Bottom)', 'Sanctuary Area')
    yield ('Graveyard Ledge Clip', 'West Death Mountain (Bottom)', 'Graveyard Ledge')
    yield ('Kings Grave Clip', 'West Death Mountain (Bottom)', 'Kings Grave Area')
    yield ('Floating Island Clip', 'East Death Mountain (Top East)', 'Death Mountain Floating Island')
    yield ('Zora DMD Clip', 'Death Mountain TR Pegs Area', 'Zoras Domain')
    yield ('TR Pegs Ledge Clip', 'Death Mountain TR Pegs Area', 'Death Mountain TR Pegs Ledge')
    yield ('Mountain Pass Ledge Clip', 'Mountain Pass Area', 'Mountain Pass Ledge')
    yield ('Mountain Pass Entry Clip', 'Kakariko Pond Area', 'Mountain Pass Entry')
    yield ('Bat Cave River Clip', 'Blacksmith Area', 'Blacksmith Ledge')
    yield ('Desert Keep Clip', 'Maze Race Area', 'Desert Ledge Keep')
    yield ('Desert Ledge Clip', 'Maze Race Area', 'Desert Ledge')
    yield ('Stone Bridge To Cliff Clip', 'Stone Bridge South Area', 'Central Cliffs')
    yield ('Bombos Tablet Clip', 'Desert Area', 'Bombos Tablet Ledge')
    yield ('Desert Teleporter Clip', 'Desert Area', 'Desert Teleporter Ledge')
    yield ('Cave 45 Clip', 'Flute Boy Approach Area', 'Cave 45 Ledge')
    yield ('Desert Northern Cliffs Clip', 'Flute Boy Approach Area', 'Desert Northern Cliffs')


def get_boots_clip_exits_dw(inverted):
    """
    Special Dark World region exits that require boots clips.
    """

    yield ('Dark World DMA Clip', 'Dark Lumberjack Area', 'West Dark Death Mountain (Bottom)')
    yield ('Dark Death Mountain Descent', 'West Dark Death Mountain (Bottom)', 'Dark Chapel Area')
    yield ('Ganons Tower Ascent', 'West Dark Death Mountain (Bottom)', 'GT Stairs')  # This only gets you to the GT entrance
    yield ('Dark Death Mountain Glitched Bridge', 'West Dark Death Mountain (Bottom)', 'East Dark Death Mountain (Top)')
    yield ('DW Floating Island Clip', 'East Dark Death Mountain (Bottom)', 'Dark Death Mountain Floating Island')
    yield ('Turtle Rock (Top) Clip', 'Turtle Rock Area', 'Turtle Rock Ledge')
    yield ('Catfish DMD', 'Turtle Rock Area', 'Catfish Area')
    yield ('Bumper Cave Ledge Clip', 'Bumper Cave Area', 'Bumper Cave Ledge')
    yield ('Bumper Cave Entry Clip', 'Outcast Pond Area', 'Bumper Cave Entry')
    yield ('Broken Bridge Hammer Rock Skip Clip', 'Qirn Jump East Bank', 'Broken Bridge Area')
    yield ('Dark Witch Rock Skip Clip', 'Dark Witch Area', 'Dark Witch Northeast')
    yield ('Hammer Pegs River Clip', 'Dark Dunes Area', 'Hammer Pegs Area')
    yield ('Hammer Bridge To Cliff Clip', 'Hammer Bridge South Area', 'Dark Central Cliffs')
    yield ('Mire Cliffs Clip', 'Stumpy Approach Area', 'Mire Northern Cliffs')
    yield ('Dark Lake Hylia Ledge Clip', 'Darkness Nook Area', 'Shopping Mall Area')
    yield ('Mire Teleporter Clip', 'Mire Area', 'Mire Teleporter Ledge')


def get_glitched_speed_drops_dw(inverted = False):
    """
    Dark World drop-down ledges that require glitched speed.
    """
    yield ('Dark Death Mountain Ledge Clip', 'East Dark Death Mountain (Top)', 'Dark Death Mountain Ledge')


def get_mirror_clip_spots_dw():
    """
    Out of bounds transitions using the mirror
    """
    yield ('Bunny DMD Mirror Spot', 'West Dark Death Mountain (Bottom)', 'Qirn Jump Area')
    yield ('Dark Death Mountain Bunny Mirror To East Jump', 'West Dark Death Mountain (Bottom)', 'East Dark Death Mountain (Bottom)')
    yield ('Desert East Mirror Clip', 'Mire Area', 'Desert Mouth')


def get_mirror_offset_spots_dw():
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Dark Death Mountain Offset Mirror', 'West Dark Death Mountain (Bottom)', 'Pyramid Area')


def get_mirror_offset_spots_lw(player):
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Death Mountain Offset Mirror', 'West Death Mountain (Bottom)', 'Hyrule Castle Area')
    yield ('Death Mountain Uncle Offset Mirror', 'West Death Mountain (Bottom)', 'Hyrule Castle Courtyard Northeast')
    yield ('Death Mountain Castle Ledge Offset Mirror', 'West Death Mountain (Bottom)', 'Hyrule Castle Ledge')


def create_owg_connections(world, player):
    """
    Add OWG transitions to player's world without logic
    """
    create_no_logic_connections(player, world, get_boots_clip_exits_lw(world.mode[player] == 'inverted'))
    create_no_logic_connections(player, world, get_boots_clip_exits_dw(world.mode[player] == 'inverted'))

    # Glitched speed drops.
    create_no_logic_connections(player, world, get_glitched_speed_drops_dw(world.mode[player] == 'inverted'))

    # Mirror clip spots.
    if world.mode[player] != 'inverted':
        create_no_logic_connections(player, world, get_mirror_clip_spots_dw())
        create_no_logic_connections(player, world, get_mirror_offset_spots_dw())
    else:
        create_no_logic_connections(player, world, get_mirror_offset_spots_lw(player))


def overworld_glitches_rules(world, player):
    # Boots-accessible locations.
    set_owg_rules(player, world, get_boots_clip_exits_lw(world.mode[player] == 'inverted'), lambda state: state.can_boots_clip_lw(player))
    set_owg_rules(player, world, get_boots_clip_exits_dw(world.mode[player] == 'inverted'), lambda state: state.can_boots_clip_dw(player))

    # Glitched speed drops.
    set_owg_rules(player, world, get_glitched_speed_drops_dw(world.mode[player] == 'inverted'), lambda state: state.can_get_glitched_speed_dw(player))
    # Dark Death Mountain Ledge Clip Spot also accessible with mirror.
    if world.mode[player] != 'inverted':
        add_alternate_rule(world.get_entrance('Dark Death Mountain Ledge Clip', player), lambda state: state.has_Mirror(player))

    # Mirror clip spots.
    if world.mode[player] != 'inverted':
        set_owg_rules(player, world, get_mirror_clip_spots_dw(), lambda state: state.has_Mirror(player))
        set_owg_rules(player, world, get_mirror_offset_spots_dw(), lambda state: state.has_Mirror(player) and state.can_boots_clip_lw(player))
    else:
        set_owg_rules(player, world, get_mirror_offset_spots_lw(player), lambda state: state.has_Mirror(player) and state.can_boots_clip_dw(player))

    # Regions that require the boots and some other stuff.
    if world.mode[player] != 'inverted':
        add_alternate_rule(world.get_entrance('Zora Waterfall Approach', player), lambda state: state.has_Pearl(player) or state.has_Boots(player)) # assumes access to Waterwalk ability (boots case)
    else:
        add_alternate_rule(world.get_entrance('Zora Waterfall Approach', player), lambda state: state.has_Pearl(player))

    add_alternate_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.can_boots_clip_lw(player)) # assumes access to Waterwalk ability,


def add_alternate_rule(entrance, rule):
    old_rule = entrance.access_rule
    entrance.access_rule = lambda state: old_rule(state) or rule(state)


def create_no_logic_connections(player, world, connections):
    for entrance, parent_region, target_region, *rule_override in connections:
        parent = world.get_region(parent_region, player)
        target = world.get_region(target_region, player)
        connection = Entrance(player, entrance, parent)
        parent.exits.append(connection)
        connection.connect(target)


def set_owg_rules(player, world, connections, default_rule):
    for entrance, parent_region, target_region, *rule_override in connections:
        connection = world.get_entrance(entrance, player)
        rule = rule_override[0] if len(rule_override) > 0 else default_rule
        connection.access_rule = rule
