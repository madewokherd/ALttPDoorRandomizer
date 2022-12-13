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
    yield 'Dark World Hammer Peg Cave'
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

    yield ('Bat Cave River Clip Spot', 'Light World', 'Bat Cave Ledge')
    yield ('Light World DMA Clip Spot', 'Light World', 'Death Mountain (West Bottom)')
    yield ('Hera Ascent', 'Death Mountain (West Bottom)', 'Death Mountain (Top)')
    yield ('Death Mountain Return Ledge Clip Spot', 'Light World', 'Death Mountain Return Ledge')
    yield ('Death Mountain Entrance Clip Spot', 'Light World', 'Death Mountain Entrance')
    yield ('Death Mountain Glitched Bridge', 'Death Mountain (West Bottom)', 'East Death Mountain (Top)')
    yield ('Zora Descent Clip Spot', 'East Death Mountain (Top)', 'Zoras Domain')
    yield ('Desert Northern Cliffs', 'Light World', 'Desert Northern Cliffs')
    yield ('Desert Ledge Dropdown', 'Desert Northern Cliffs', 'Desert Ledge')
    yield ('Desert Palace Entrance Dropdown', 'Desert Northern Cliffs', 'Desert Palace Entrance (North) Spot')
    yield ('Lake Hylia Island Clip Spot', 'Light World', 'Lake Hylia Island')
    yield ('Death Mountain Descent', 'Death Mountain (West Bottom)', 'Light World')
    yield ('Kings Grave Clip Spot', 'Death Mountain (West Bottom)', 'Kings Grave Area')

    if not inverted:
        yield ('Graveyard Ledge Clip Spot', 'Death Mountain (West Bottom)', 'Graveyard Ledge')
        yield ('Desert Ledge (Northeast) Dropdown', 'Desert Northern Cliffs', 'Desert Checkerboard Ledge')
        yield ('Spectacle Rock Clip Spot', 'Death Mountain (Top)', 'Spectacle Rock')
        yield ('Bombos Tablet Clip Spot', 'Light World', 'Bombos Tablet Ledge')
        yield ('Floating Island Clip Spot', 'East Death Mountain (Top)', 'Death Mountain Floating Island')
        yield ('Cave 45 Clip Spot', 'Light World', 'Cave 45 Ledge')


def get_boots_clip_exits_dw(inverted):
    """
    Special Dark World region exits that require boots clips.
    """

    yield ('Dark World DMA Clip Spot', 'West Dark World', 'Dark Death Mountain (West Bottom)')
    yield ('Bumper Cave Ledge Clip Spot', 'West Dark World', 'Bumper Cave Ledge')
    yield ('Bumper Cave Entrance Clip Spot', 'West Dark World', 'Bumper Cave Entrance')
    yield ('Catfish Descent', 'Dark Death Mountain (Top)', 'Catfish Area')
    yield ('Hammer Pegs River Clip Spot', 'East Dark World', 'Hammer Peg Area')
    yield ('Dark Lake Hylia Ledge Clip Spot', 'East Dark World', 'Southeast Dark World')
    yield ('Dark Desert Cliffs Clip Spot', 'South Dark World', 'Dark Desert')
    yield ('DW Floating Island Clip Spot', 'Dark Death Mountain (East Bottom)', 'Death Mountain Floating Island (Dark World)')

    if not inverted:
        yield ('Dark Death Mountain Descent', 'Dark Death Mountain (West Bottom)', 'West Dark World')
        yield ('Ganons Tower Ascent', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain (Top)')  # This only gets you to the GT entrance
        yield ('Dark Death Mountain Glitched Bridge', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain (Top)')
        yield ('Turtle Rock (Top) Clip Spot', 'Dark Death Mountain (Top)', 'Turtle Rock (Top)')
    else:
        yield ('Dark Desert Teleporter Clip Spot', 'Dark Desert', 'Dark Desert Ledge')


def get_glitched_speed_drops_dw(inverted = False):
    """
    Dark World drop-down ledges that require glitched speed.
    """
    yield ('Dark Death Mountain Ledge Clip Spot', 'Dark Death Mountain (Top)', 'Dark Death Mountain Ledge')


def get_mirror_clip_spots_dw():
    """
    Out of bounds transitions using the mirror
    """
    yield ('Dark Death Mountain Bunny Descent Mirror Spot', 'Dark Death Mountain (West Bottom)', 'West Dark World')
    yield ('Dark Death Mountain Bunny Mirror To East Jump', 'Dark Death Mountain (West Bottom)', 'Dark Death Mountain (East Bottom)')
    yield ('Desert East Mirror Clip', 'Dark Desert', 'Desert Palace Mouth')


def get_mirror_offset_spots_dw():
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Dark Death Mountain Offset Mirror', 'Dark Death Mountain (West Bottom)', 'East Dark World')


def get_mirror_offset_spots_lw(player):
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """
    yield ('Death Mountain Offset Mirror', 'Death Mountain (West Bottom)', 'Light World')
    yield ('Death Mountain Offset Mirror (Houlihan Exit)', 'Death Mountain (West Bottom)', 'Hyrule Castle Ledge', lambda state: state.has_Mirror(player) and state.can_boots_clip_dw(player) and state.has_Pearl(player))


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
        add_alternate_rule(world.get_entrance('Dark Death Mountain Ledge Clip Spot', player), lambda state: state.has_Mirror(player))

    # Mirror clip spots.
    if world.mode[player] != 'inverted':
        set_owg_rules(player, world, get_mirror_clip_spots_dw(), lambda state: state.has_Mirror(player))
        set_owg_rules(player, world, get_mirror_offset_spots_dw(), lambda state: state.has_Mirror(player) and state.can_boots_clip_lw(player))
    else:
        set_owg_rules(player, world, get_mirror_offset_spots_lw(player), lambda state: state.has_Mirror(player) and state.can_boots_clip_dw(player))

    # Regions that require the boots and some other stuff.
    if world.mode[player] != 'inverted':
        world.get_entrance('Turtle Rock Teleporter', player).access_rule = lambda state: (state.can_boots_clip_lw(player) or state.can_lift_heavy_rocks(player)) and state.has('Hammer', player)
        add_alternate_rule(world.get_entrance('Waterfall Fairy Access', player), lambda state: state.has_Pearl(player) or state.has_Boots(player)) # assumes access to Waterwalk ability (boots case)
    else:
        add_alternate_rule(world.get_entrance('Waterfall Fairy Access', player), lambda state: state.has_Pearl(player))

    world.get_entrance('Dark Desert Teleporter', player).access_rule = lambda state: (state.can_flute(player) or state.can_boots_clip_dw(player)) and state.can_lift_heavy_rocks(player)
    add_alternate_rule(world.get_entrance('Dark Witch Rock (North)', player), lambda state: state.can_boots_clip_dw(player))
    add_alternate_rule(world.get_entrance('East Dark World Broken Bridge Pass', player), lambda state: state.can_boots_clip_dw(player))
    add_alternate_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.can_boots_clip_lw(player)) # assumes access to Waterwalk ability


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
