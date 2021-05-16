# Overworld Randomizer

This is a overworld randomizer for _The Legend of Zelda: A Link to the Past_ for the SNES
based on the Door Randomizer found at [Aerinon's Github Project.](https://github.com/Aerinon/ALttPDoorRandomizer)
See https://alttpr.com/ for more details on the normal randomizer.

### Trackers & Guides

This is a very new mode of LTTPR so the tools and info is very limited. - There is an [OW Rando Cheat Sheet](https://zelda.codemann8.com/images/shared/ow-rando-reference-sheet.png) that shows all the transitions that exist and are candidates for shuffle.
- There is OW tracking capability within CodeTracker, an [EmoTracker](https://emotracker.net) package for LTTPR.
- There is an [OW OWG Reference Sheet](https://zelda.codemann8.com/images/shared/ow-owg-reference-sheet.png) that shows all the in-logic places where boots/mirror clips and fake flippers are expected from the player.

# Known Issues
(Updated 2021-05-16)

### If you want to playtest this, know these things:
- Big Red Bomb may require bomb duping as ledge drops may be in the way of your path to the Pyramid Fairy crack
- Do NOT grab the Frogsmith until you have seen the Blacksmith location. Doing so may prevent you from continuing in your save file.
- Inverted regions/rules/logic is NOT implemented yet. Generation should fail 100%.
- If you fake flipper, beware of transitioning south. You could end up at the top of the waterfall in the southeast of either world. If you mistakenly drop down, it is important to NOT make any other movements and S+Q immediately or there will be a hardlock. Falling from the waterfall is avoidable but it is super easy to do as it is super close to the transition.

### Known bugs:
- ~~Camera unlocks, this is a known issue and will eventually be fixed at a later time~~ _(Fixed with 0.1.1.2)_
- ~~When generating, there is a message about one location that remains unfilled. You will find a Nothing item at that location.~~ _(Fixed with 0.1.1.0)_
- There may be an issue with progression being front-loaded in the seed in some scenarios, due to an unsophisticated shuffle algorithm that could make varying-sized parts of each world unreachable

# Feedback and Bug Reports

All feedback and dev conversation happens in the #ow-rando channel on the [ALTTP Randomizer discord](https://discordapp.com/invite/alttprandomizer).

# Installation from source

See these instructions.

https://github.com/codemann8/ALttPDoorRandomizer/blob/OverworldShuffle/docs/BUILDING.md

When installing platform specific dependencies, don't forget to run the appropriate command from the bottom of the page! Those will install missing pip dependencies.

Running the MultiServer and MultiClient for multiworld should run resources/ci/common/local_install.py for those dependencies as well.

To use the CLI, run ```DungeonRandomizer.py```.

Alternatively, run ```Gui.py``` for a simple graphical user interface.

# Settings

Only extra settings are found here. All door and entrance randomizer settings are supported. See their [readme](https://github.com/Aerinon/ALttPDoorRandomizer/blob/master/README.md)

## Overworld Layout Shuffle (--ow_shuffle)

### Vanilla

OW is not shuffled.

### Parallel

OW Transitions are shuffled, but both worlds will have a matching layout.

### Full

OW Transitions are shuffled within each world separately.

## Keep Similar Edges Together (--ow_keepsimilar)

This keeps similar edge transitions together. ie. The 2 west edges of Potion Shop will be paired to another set of two similar edges


# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--ow_shuffle <mode>     
```

For specifying the overworld layout shuffle you want as above. (default: vanilla)

```
--ow_keepsimilar     
```

This keeps similar edge transitions paired together with other pairs of transitions
