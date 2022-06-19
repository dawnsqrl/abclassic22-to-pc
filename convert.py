import json
import re


# Format dictionary into JSON, then into Lua table
def convert(data: dict):
    result = json.dumps(data, indent=4, separators=(',', ' = '))
    result = re.sub('{\n(.+)\n}', '\\1\n', result, flags=re.S)
    result = re.sub('(\n\s*})', ',\\1', result, flags=re.S)
    result = re.sub('^\s{4}', '', result, flags=re.M)
    result = re.sub('^},', '}', result, flags=re.M)
    result = re.sub('"(\w+)" = ', '\\1 = ', result)
    result = re.sub('^(\w.*),$', '\\1', result, flags=re.M)
    return result
