import argparse
import os
from mapping import *
from convert import *
from encrypt import *

# Handle input arguments
parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument('--no-grind', action='store_true', help='activate powerups in output save files')
do_activate_powerups = parser.parse_args().no_grind

# Test for output file
if os.path.isfile('highscores.lua') or os.path.isfile('settings.lua'):
    print('Output save file (highscores.lua / settings.lua) already exists')
    while True:
        response = input('Overwrite? [y/n] ')
        if re.match('^[Yy]$', response) is not None:
            break
        elif re.match('^[Nn]$', response) is not None:
            exit(0)

# Read save data
try:
    save_file = open('getGameState', encoding='utf-8', errors='ignore')
except FileNotFoundError as exception:
    raise Exception('Input save file (getGameState) is not found') from exception
save_raw = save_file.read()
save_file.close()
try:
    save_data = json.loads(re.sub('^[^{]+(.*)[^}]+$', '\\1', save_raw))
except json.decoder.JSONDecodeError as exception:
    raise Exception('Input save file (getGameState) has incorrect content format') from exception

# Initialize output save data
highscores_data = {}
settings_data = {
    'settingsVersion': {
        'id': 4,
        'version': '4.3.0',
        'newId': 6
    },
    'isPremium': True,
    'shopChildlockOn': True,
    'cumulativeStars': 0
}

# Convert Golden Egg acquisition data
if 'acquisitions' in save_data:
    highscores_data['openGoldenEggLevels'] = {}
    for golden_egg in save_data['acquisitions']:
        highscores_data['openGoldenEggLevels'][GoldenEggName[golden_egg['name']]] = {
            'unlocked': True,
            'opened': False
        }
    for golden_egg_name in GoldenEggName.values():
        if golden_egg_name not in highscores_data['openGoldenEggLevels']:
            highscores_data['openGoldenEggLevels'][golden_egg_name] = {
                'unlocked': False,
                'opened': False
            }
assert len(highscores_data['openGoldenEggLevels']) == len(GoldenEggName) - 5

# Convert score data
if 'episodes' in save_data:
    for episode in save_data['episodes']:
        for level in episode['levelScores']:
            is_minigame = '#' in level['LevelName']
            if is_minigame:
                level_name = GoldenEggName[level['LevelName']]
            else:
                level_name = 'Level' + level['LevelName']
            highscores_data[level_name] = {}
            highscores_data[level_name]['completed'] = level['Points'] > 0
            highscores_data[level_name]['legitScore'] = 0 if is_minigame else level['Points']
            highscores_data[level_name]['score'] = 0 if is_minigame else level['Points']
            highscores_data[level_name]['lowScore'] = 0 if is_minigame else level['Points']
            highscores_data[level_name]['powerUpScore'] = 0
            highscores_data[level_name]['birds'] = 0 if is_minigame else 1
            settings_data['cumulativeStars'] += level['Stars']
            if level['EagleHighScore'] > 0:
                highscores_data[level_name]['eagleScoreMax'] = level['EagleHighScore']
                highscores_data[level_name]['eagleScoreMin'] = level['EagleHighScore']
                highscores_data[level_name]['eagleScore'] = 100 if level['EagleTotalDestruction'] else 0
            if level_name in highscores_data['openGoldenEggLevels'] and level['Points'] > 0:
                highscores_data['openGoldenEggLevels'][level_name]['opened'] = True

# Convert shown tutorial data
if 'shownTutorials' in save_data:
    settings_data['tutorials'] = {}
    for tutorial in save_data['shownTutorials']:
        settings_data['tutorials'][BirdReference[tutorial][0]] = {
            'sprite': BirdReference[tutorial][1]
        }
        if BirdReference[tutorial][2]:
            settings_data['tutorials'][BirdReference[tutorial][0]]['showHelp'] = False

# Convert last viewed episode page data
if 'episodePages' in save_data:
    settings_data['currentLevelSelectionPages'] = {}
    for episode in save_data['episodePages']:
        settings_data['currentLevelSelectionPages'][EpisodeID[episode['id']]] = episode['page'] + 1

# Convert Boomerang bird acquisition data
if 'boomerangAcquired' in save_data:
    settings_data['boomerangBirdAchieved'] = save_data['boomerangAcquired']
else:
    settings_data['boomerangBirdAchieved'] = False

# Update powerups data
if do_activate_powerups:
    settings_data['shopChildlockOn'] = False
    settings_data['mightyEagleUnlocked'] = True
    settings_data['mightyEagleEnabled'] = True
    settings_data['flagTable'] = {
        'redsMightyFeathersPurchased': True
    }
    settings_data['syncedFlagTable'] = {
        'shockwavePowerupUnlocked': True
    }
    settings_data['installationSpecificInventory'] = {}
    for powerup in PowerupInventory:
        settings_data['installationSpecificInventory'][powerup] = {
            'totalCount': PowerupInventory[powerup],
            'usedCount': 0
        }

# Format and encrypt converted data
highscores_raw = encrypt(convert(highscores_data))
settings_raw = encrypt(convert(settings_data))

# Output converted data to file
try:
    highscores_file = open('highscores.lua', 'wb')
    settings_file = open('settings.lua', 'wb')
except PermissionError as exception:
    raise Exception('Output save file (highscores.lua / settings.lua) is not writable') from exception
highscores_file.write(highscores_raw)
highscores_file.close()
settings_file.write(settings_raw)
settings_file.close()
print("Translation completed")
