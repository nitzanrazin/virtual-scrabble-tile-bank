# virtual-scrabble-tile-bank
Virtual tile bank for playing Hebrew Scrabble (שבץ נא) in several remote locations, each using their own physical copy of the game.

## Purpose
This script allows playing a game of Hebrew Scrabble (שבץ נא) in multiple remote locations. It is assumed that in each location, there is a physical copy of the game board and tiles.
This script should be used in addition to a group chat or similar solution for sharing the board state after each turn, and a video chat service for communication between the players during the game.
When using this script to play remote Scrabble, all the tiles at each location should be placed face up, to allow finding specific tiles for
1. a player taking tiles matching the ones drawn for them by the virtual tile bank
2. placing tiles on the game board following a remote players turn, to update the local board.

Thus, each player has more information about the tile bank and the tiles other players have than in a regular Scrabble game with
face down tiles in the tile bank.<sup>[1](#footnote1)</sup>

This script is a virtual tile bank, from which tiles can be drawn for each of the players.
A list of the drawn tiles is sent to an email address provided for the player, so it can be kept secret from other players (as much as possible, yet local players could observe the player taking the tiles from the face-up local tile bank).
The virtual tile bank program should be run by one of the players (the designated "tile bank manager"), which is responsible for filling the amount of tiles needed and the player that requires them.
During the game, each location should use a game board, on which local players place tiles during their turn.
Tiles placed by remote players on a different board are placed on all game boards by local players after each turn (updating all players
about changes to the board after each turn can be done by sharing a picture of the board to a group chat).


## Instructions for playing a game of Scrabble using the virtual tile bank

1. Before starting the game, choose the tile distribution and tile scores.

    There are several different versions of the Hebrew Scrabble game, each with slightly different tile numbers and scores for the different letters.
Decide how many tiles of each type to put in the tile bank (pick a game version or freely set the amounts), and how many points each tile is worth.

2. At each location, set up:
    1. A board game, and the game tiles face-up
    2. A video chat connection
    3. A means by which to share the state of the board after each turn, for example taking a picture and sending it to a group chat

## Instructions for running the tile bank
### Before the game starts:
1. Set up a gmail account for sending the drawn tile lists
It is highly recommended to set up a specialized account and not use a personal account for this, since 
sending messages from Python code code requires lowering the account security, and since the password to this account
will be saved to a plain text file, to be used by the virtual scrabble bank. 

    Turn "Allow less secures apps" to ON: https://myaccount.google.com/lesssecureapps?pli=1

2. Decide which tile distribution to use (if not all game sets used are the same, may decide to use the minimal amount available from each type, for example)
3. Set up the game settings: enter the gmail account details, and set the tile distribution
4. Enter player data (name and email)

### During the game:
1. To decide the order of play, draw one tile for each of the players.
This is a good opportunity to verify everyone receives the emails. The drawn tiles are shown in the text box at the bottom of the window,
but can be hidden by clicking the "הסתר היסטוריה" button. It can be shown by clicking "הצג היסטוריה" (which can help the tile bank manager overcome an issue of a player not receiving an email).

    After drawing tiles, the combobox for selection of the player for which to draw tiles advances to the next player automatically,
so at this point it would be convenient to re-order the player list by drag and drop.
Click "התחל משחק חדש" to return all tiles to the tile bank and start the game.

2. Draw 7 tiles for each player

3. Start the game, after each player's turn the tile bank manager should fill in the amount of tiles the player needs to draw from the bank,
and click "הגרל" to draw the tiles and send a list of the drawn tiles to the players email.

4. The status bar at the bottom of the virtual tile bank GUI is updated to show the amount of tiles drawn, for which player, and the amount of tiles left in the bank.

5. In the case of a mistake in the tile drawing (for example, too many tiles drawn for a player, or tiles drawn for the wrong player), the last draw can be undone by clicking "בטל".

## Requirements
* Pmw

install by: pip install Pmw
This package is used to create tooltips

<a name="footnote1">[1]</a>: For the (unrealistic) case of
<img src="https://render.githubusercontent.com/render/math?math=N=\infty">
tile bank tiles at each location, this information reduces to zero and the game is identical to regular Scrabble.
Being a physicist, I still suggest using it for
<img src="https://render.githubusercontent.com/render/math?math=N=2">
(the case of 2 remote locations, with one game set in each).
