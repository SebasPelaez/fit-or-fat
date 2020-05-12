import yaml
import os
import json

def yaml_to_dict(yml_path):
  with open(yml_path, 'r') as stream:
    try:
      params = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
      print(exc)

  return params

def make_label_map(directory):
  id_label_map = {key:value for key,value in enumerate(os.listdir(directory))}
  label_id_map = {value:key for key,value in enumerate(os.listdir(directory))}
  return id_label_map,label_id_map