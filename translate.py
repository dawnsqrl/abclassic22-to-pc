import re
import json
from encrypt import encrypt

# converted_save_data['LevelGE_14'] = {}
# converted_save_data['LevelGE_14']['completed'] = True
# converted_save_data['LevelGE_14']['legitScore'] = 0
# OR
# converted_save_data['LevelGE_14'] = []
# converted_save_data['LevelGE_14'].append({})
# converted_save_data['LevelGE_14'][0]['completed'] = True

# JSON dump formatting parameters
json_indent = 2
json_separators = (',', ' = ')

# Episode name mapping
EpisodeID = {
    1: 'pack1',
    2: 'pack2',
    3: 'pack3',
    4: 'pack4',
    5: 'pack5',
    6: 'pack6',
    7: 'pack7',
    8: 'packSURF',
    9: 'packG',
}

# Golden Eggs level name mapping
GoldenEgg = {
    'Minigame#CharsInOrder': 'SOUNDBOARD1',
    'Minigame#Radio': 'RADIO',
    'Minigame#AngryBirdsTune': 'KEYBOARD',
    'Minigame#Outlines': 'SEQUENCER',
    'Minigame#Accordion': 'ACCORDION',
}

# Read save data
save_file = open('getGameState', encoding='utf-8', errors='ignore')
save_raw = save_file.read()
save_file.close()
save_data = json.loads(re.sub('^[^{]+(.*)[^}]+$', '\\1', save_raw))

# Initialize output save data
converted_highscores = {}
converted_settings = {}

# Convert score data
if 'episodes' in save_data:
    for episode in save_data['episodes']:
        for level in episode['levelScores']:
            if '#' in level['LevelName']:
                continue
            level_name = 'Level' + level['LevelName']
            converted_highscores[level_name] = {}
            converted_highscores[level_name]['completed'] = True
            converted_highscores[level_name]['legitScore'] = level['Points']
            converted_highscores[level_name]['score'] = level['Points']
            converted_highscores[level_name]['lowScore'] = level['Points']
            converted_highscores[level_name]['powerUpScore'] = 0
            converted_highscores[level_name]['birds'] = 1
            if level['EagleHighScore'] > 0:
                converted_highscores[level_name]['eagleScoreMax'] = level['EagleHighScore']
                converted_highscores[level_name]['eagleScoreMin'] = level['EagleHighScore']
                if level['EagleTotalDestruction']:
                    converted_highscores[level_name]['eagleScore'] = 100
                else:
                    converted_highscores[level_name]['eagleScore'] = 0

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
encrypt('?')

# Output converted data to file
print(json.dumps(converted_highscores, indent=json_indent, separators=json_separators))
print(json.dumps(converted_settings, indent=json_indent, separators=json_separators))
