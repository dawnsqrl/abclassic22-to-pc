# `com.rovio.abclassic22` to PC

A save file translator from _Rovio Classics: Angry Birds_
(2022) to _Angry Birds Classic_ PC.

## Background

**tl;dr.** The recently re-released _Rovio Classics: Angry
Birds_ does not contain all levels from its predecessor.
This translator helps to transfer existing game progress to
the PC version, where more later episodes could be found.

The original _Angry Birds Classic_ mobile game used Rovio
Account to sync game progress to the cloud. However, the
system was abruptly closed down on March 18, 2022, over 4
years after the game received its last content update.
This wiped all legacy save data from the server, so they
could not be retrieved by any means after that point. (I
lost all my progress since 2014: 2109 stars and 36 golden
eggs.)

The shutdown was soon followed by the re-release of the
title, _Rovio Classics: Angry Birds_ (_RC:AB_). It featured
a subset of the original episodes and still used a cloud
save system, but this time I had to sling from scratch.

It took me around 2 weeks to 3-star all available levels
on _RC:AB_ once again (1117 stars and 28 golden eggs), but
I need to continue playing on the PC version for the
remaining episodes (it is currently unknown whether they
will be ported to _RC:AB_ anymore). This translator is thus
for the very purpose of preserving my progress as I resume
on a different platform.

## Usage

1. Download or clone the translator scripts.

2. On Android, a local copy of _RC:AB_ save file can be
found at the following path, where `[uuid]` is a
36-character UUID string. Copy `getGameState` to the same
directory as the scripts.

   ```text
   /storage/emulated/0/Android/data/com.rovio.abclassic22/files/RC[uuid]/getGameState
   ```

3. Run the scripts. Two files `highscores.lua` and
`settings.lua` will be generated in the current directory.

   ```bash
   python translate.py
   ```

4. **(Optional)** _RC:AB_ does not come with any powerup
item except for the Mighty Eagle. If full powerup
availability is desired on PC, run the scripts with a
`--no-grind` flag.

   ```bash
   python translate.py --no-grind
   ```

5. On Windows, copy `highscores.lua` and `settings.lua` to
the following directory for _Angry Birds Classic_ PC to
load upon next start.

   ```text
   %APPDATA%\Rovio\Angry Birds
   ```

## Limitations

This translator is developed based on the save data
structure and content from version _RC:AB_ 1.2.1479 and
_Angry Birds Classic_ PC 5.0.1.

_RC:AB_ stores a much more limited set of information in
its save file than _Angry Birds Classic_ PC, so not all
values could be deduced from `getGameState`. Below is a
list of transferable data implemented in this translator.

* Level completion status, used bird count[^1], numeric
score, star[^2]
* Level Mighty Eagle numeric score, percentage score[^3]
* Golden Egg level score, star, unlock status, open
status[^4]
* Encountered birds through tutorial
* Last viewed page in each episode's selection screen
* Whether Hal has been released from cage (Level 6-4)

Below is a non-exhaustive list of **_not_** transferable
data; they will either be automatically updated or reset
after game launch.

* Episode completion status, full 3-star status
* Cumulative level numeric score, star, feather
* Achievement status
* Main menu background theme
* Mighty Eagle cooldown duration, last used level
* Number of destroyed blocks (per material), launched birds
* Whether Secret Cake has been obtained (Level 18-15)

This translator is **_not_** capable of merging converted
data into another existing instance of _Angry Birds
Classic_ PC save file.

[^1]: Since _RC:AB_ does not keep track of this data, all
completed non-minigame levels are assumed to have 1 bird
used (0 otherwise).

[^2]: _Angry Birds Classic_ PC dynamically calculates level
star based on score, so the actual number of stars shown
in-game may change due to differently set thresholds.

[^3]: Since _RC:AB_ only stores a _Total Destruction_ flag
while its precise score threshold remains unknown, this
percentage is set to either 100 or 0.

[^4]: Unlocked but not completed Golden Egg levels are
assumed to be not opened (they will glow in the selection
screen).

## Attributions

Credits to _Angry Birds Series Modding Hub_ Discord server
for providing the AES encryption key used in _Angry Birds
Classic_ PC save files.
