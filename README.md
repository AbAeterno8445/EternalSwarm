# Infinity Swarm
"Incremental" game project.
Assets taken from Terraria (https://terraria.org/), owned by Re-Logic; I do not claim ownership to any of these.

The basic idea for the game is that you begin as a newborn alien swarm on an unknown planet, and must conquer it.
You begin with a piece of terrain, and may capture areas surrounding it, gradually expanding the reach of your swarm.

## Installation
The project uses pygame, version 1.9.4. If future versions are backwards compatible, this should cause no problem.

The requirements.txt file is given, you may install it with pip using:

`pip install -r requirements.txt`

## Gameplay
Run the main.py file to start the game.

**DISCLAIMER:** Game is currently heavily unbalanced for testing purposes.

### Interface: Main screen
This is the screen you see when you boot up the game.
The main screen contains three panels.
On the left you will see the materials panel, which displays the materials obtained by you.

The bottom panel contains many buttons, aka shortcuts, that lead you to a different feature.

The middle panel, or main panel, displays the currently selected feature.
The game always begins displaying terrain information.

### Main panel: Terrain
The terrain feature displays a map with the terrain of the planet.
This map is divided as a grid where each tile represents a capturable piece of terrain.

Scattered around the whole map are different "biomes", called regions, which determine which kind of creatures will appear
naturally within it. For example "Tundra", "Desert", "Wooded Grasslands", etc.

The piece of terrain in the middle of the map always begins as yours.
You may select surrounding pieces of terrain to then attempt to capture and claim them as yours, thus expanding your swarm.

### Main panel: Buildings
Not currently implemented.
This feature is where you are supposed to buy and upgrade buildings to then use in the capturing process.

### Main panel: Saving and Loading
In the "Save" feature, you may write a name for your savefile and then create it.
If a savefile with the same name already exists, it will be overwritten.
Clicking on an existing savefile button will set the save name to that file's name (makes overwriting easier).

In the "Load" feature, you can click on an existing savefile and load it.
Some relevant information is displayed on selection.

Savefiles use the ".issf" (Infinity Swarm Save File) extension, for *uniqueness* purposes.

### Interface: Level information screen
On the terrain panel, selecting a tile adjacent to an owned tile will let you attempt to capture it.
This sends you to a screen where information on the selected level is displayed.

### Gameplay: Battle for terrain
In this game, you must place buildings on your side of the battlefield, which will create units that
advance on a straight line towards the enemy.
This means you must pay attention to the row you place your buildings in.
The objective is to destroy all enemy buildings.

The game begins paused so you can place your buildings before beginning.
To unpause, press **P**.

You start with some energy and health.
Energy is used to place buildings and you gain some per second.
To place a building, click on a tile owned by you and select the building you want to place.

You can sell a building by selecting it and pressing **DEL**, which will return 40% of its value.

Once the game is unpaused, buildings will begin spawning units, and these will fight whichever enemy unit/building they
encounter.
If an enemy unit escapes through your side of the battlefield, you will lose health.