import json

def pretty_print_json(json_response):
    
    jsonifyed = json.dumps(json_response, indent = 4)

    print('\033[1m' + '\033[92m' + str(jsonifyed))