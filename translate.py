import re
import json
from mapping import *
from convert import *
from encrypt import *

# Do you want to give up the grind?
do_activate_powerups = True

# Read save data
save_file = open('getGameState', encoding='utf-8', errors='ignore')
save_raw = save_file.read()
save_file.close()
save_data = json.loads(re.sub('^[^{]+(.*)[^}]+$', '\\1', save_raw))

# Initialize output save data
highscores_data = {}
settings_data = {
    'settingsVersion': {
        'id': 4,
        'version': '4.3.0',
        'newId': 6
    },
    'cumulativeStars': 0,
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
    settings_data['mightyEagleUnlocked'] = True
    settings_data['mightyEagleEnabled'] = True
    settings_data['flagTable'] = {
        'redsMightyFeathersPurchased': True
    }

# Format and encrypt converted data
highscores_raw = encrypt(convert(highscores_data))
settings_raw = encrypt(convert(settings_data))

# Output converted data to file
highscores_file = open('highscores.lua', 'wb')
highscores_file.write(highscores_raw)
highscores_file.close()
settings_file = open('settings.lua', 'wb')
settings_file.write(settings_raw)
settings_file.close()

print(convert(settings_data))
