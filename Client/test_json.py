import json

# jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
jsonData='{}'

text = json.loads(jsonData)
if not text:
    print('yes')
print(type(text))
