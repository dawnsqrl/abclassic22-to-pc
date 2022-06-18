import re
import json
from mapping import *
from encrypt import *

# JSON dump formatting parameters
json_indent = 2
json_separators = (',', ' = ')

# Read save data
save_file = open('getGameState', encoding='utf-8', errors='ignore')
save_raw = save_file.read()
save_file.close()
save_data = json.loads(re.sub('^[^{]+(.*)[^}]+$', '\\1', save_raw))

# Initialize output save data
converted_highscores = {}
converted_settings = {
    'settingsVersion': {
        'id': 4,
        'version': '4.3.0',
        'newId': 6
    },
    'cumulativeStars': 0
}

# Convert Golden Egg acquisition data
if 'acquisitions' in save_data:
    converted_highscores['openGoldenEggLevels'] = {}
    for golden_egg in save_data['acquisitions']:
        converted_highscores['openGoldenEggLevels'][GoldenEggName[golden_egg['name']]] = {
            'unlocked': True,
            'opened': False
        }
    for golden_egg_name in GoldenEggName.values():
        if golden_egg_name not in converted_highscores['openGoldenEggLevels']:
            converted_highscores['openGoldenEggLevels'][golden_egg_name] = {
                'unlocked': False,
                'opened': False
            }
assert len(converted_highscores['openGoldenEggLevels']) == len(GoldenEggName) - 5

# Convert score data
if 'episodes' in save_data:
    for episode in save_data['episodes']:
        for level in episode['levelScores']:
            is_minigame = '#' in level['LevelName']
            if is_minigame:
                level_name = GoldenEggName[level['LevelName']]
            else:
                level_name = 'Level' + level['LevelName']
            converted_highscores[level_name] = {}
            converted_highscores[level_name]['completed'] = level['Points'] > 0
            converted_highscores[level_name]['legitScore'] = 0 if is_minigame else level['Points']
            converted_highscores[level_name]['score'] = 0 if is_minigame else level['Points']
            converted_highscores[level_name]['lowScore'] = 0 if is_minigame else level['Points']
            converted_highscores[level_name]['powerUpScore'] = 0
            converted_highscores[level_name]['birds'] = 0 if is_minigame else 1
            converted_settings['cumulativeStars'] += level['Stars']
            if level['EagleHighScore'] > 0:
                converted_highscores[level_name]['eagleScoreMax'] = level['EagleHighScore']
                converted_highscores[level_name]['eagleScoreMin'] = level['EagleHighScore']
                converted_highscores[level_name]['eagleScore'] = 100 if level['EagleTotalDestruction'] else 0
            if level_name in converted_highscores['openGoldenEggLevels'] and level['Points'] > 0:
                converted_highscores['openGoldenEggLevels'][level_name]['opened'] = True

# Convert shown tutorial data
if 'shownTutorials' in save_data:
    converted_settings['tutorials'] = {}
    for tutorial in save_data['shownTutorials']:
        if tutorial == 'TutorialRed':
            converted_settings['tutorials']['BIRD_RED'] = {
                'sprite': 'TUTORIAL_1'
            }
        elif tutorial == 'TutorialBlues':
            converted_settings['tutorials']['BIRD_BLUE'] = {
                'sprite': 'TUTORIAL_2',
                'showHelp': False
            }
        elif tutorial == 'TutorialChuck':
            converted_settings['tutorials']['BIRD_YELLOW'] = {
                'sprite': 'TUTORIAL_3',
                'showHelp': False
            }
        elif tutorial == 'TutorialBomb':
            converted_settings['tutorials']['BIRD_GREY'] = {
                'sprite': 'TUTORIAL_4',
                'showHelp': False
            }
        elif tutorial == 'TutorialMatilda':
            converted_settings['tutorials']['BIRD_GREEN'] = {
                'sprite': 'TUTORIAL_5',
                'showHelp': False
            }
        elif tutorial == 'TutorialHal':
            converted_settings['tutorials']['BIRD_BOOMERANG'] = {
                'sprite': 'TUTORIAL_6',
                'showHelp': False
            }
        elif tutorial == 'TutorialTerence':
            converted_settings['tutorials']['BIRD_BIG_BROTHER'] = {
                'sprite': 'TUTORIAL_7'
            }
        elif tutorial == 'TutorialMightyEagle':
            converted_settings['tutorials']['BAIT_SARDINE'] = {
                'sprite': 'TUTORIAL_8'
            }
        elif tutorial == 'TutorialBubbles':
            converted_settings['tutorials']['BIRD_PUFFER_1'] = {
                'sprite': 'TUTORIAL_9',
                'showHelp': False
            }
        elif tutorial == 'TutorialStella':
            converted_settings['tutorials']['BIRD_PINK'] = {
                'sprite': 'TUTORIAL_10',
                'showHelp': False
            }

# Convert last viewed episode page data
if 'episodePages' in save_data:
    converted_settings['currentLevelSelectionPages'] = {}
    for episode in save_data['episodePages']:
        converted_settings['currentLevelSelectionPages'][EpisodeID[episode['id']]] = episode['page'] + 1

# Convert Boomerang bird acquisition data
if 'boomerangAcquired' in save_data:
    converted_settings['boomerangBirdAchieved'] = save_data['boomerangAcquired']
else:
    converted_settings['boomerangBirdAchieved'] = False

# Format and encrypt converted data
# encrypt('?')

# Output converted data to file
print(json.dumps(converted_highscores, indent=json_indent, separators=json_separators))
print(json.dumps(converted_settings, indent=json_indent, separators=json_separators))
