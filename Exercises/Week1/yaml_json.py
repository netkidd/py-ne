#!/usr/bin/env python

'''
YAML/JSON
6. Write a Python program that creates a list. One of the elements of the list
should be a dictionary with at least two keys. Write this list out to a file
using both YAML and JSON formats. The YAML file should be in the expanded form.

7. Write a Python program that reads both the YAML file and the JSON file
created in exercise6 and pretty prints the data structure that is returned.
'''
import yaml
import json
import pprint

a = [0, 1, 2, 3, 4, 5]

b = "some test"

c = {"key1": 1, "key2": "Jimbo", "key3": ["bim", "bum", "bam"]}

base_list = [a, b, c]

pprint.pprint(base_list)


with open("yaml_file.yml", "w") as f:
    f.write("---\n\n")
    f.write(yaml.dump(base_list, default_flow_style=False))

with open("json_file.json", "w") as f:
    json.dump(base_list, f)


print("\n\nFrom files:\n\n")

with open("yaml_file.yml") as f:
    from_yaml = yaml.load(f)

with open("json_file.json") as f:
    from_json = json.load(f)

pprint.pprint(from_yaml)
print('\n')
pprint.pprint(from_json)
