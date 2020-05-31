import cv2
import mahotas as mt
import numpy as np
import os
import wget
import zipfile
import utils

def verify_folder(folder):
  if not os.path.exists(folder):
    os.makedirs(folder)

def extract_features(image):
  textures = mt.features.haralick(image)
  ht_mean = textures.mean(axis=0)
  ht_std = textures.std(axis=0)
  ht = np.concatenate((ht_mean,ht_std))
  return ht

def download_data(params):

  url_tar_file = params['url_dataset']

  if not os.path.exists(params['data_dir']):
    os.makedirs(params['data_dir'])

  wget.download(url_tar_file, params['data_dir'])

def extract_data(params):

  tar_file = os.path.join(params['data_dir'],params['compressed_data_name'])
  zip_ref = zipfile.ZipFile(tar_file, 'r')
  zip_ref.extractall(params['data_dir'])
  zip_ref.close()

def save_features(params,feature_dict):

  features_data_dir = os.path.join(params['data_dir'],params['features_dir'])
  verify_folder(features_data_dir)

  for key,value in feature_dict.items():
    meta_class_dir = os.path.join(features_data_dir,key)
    verify_folder(meta_class_dir)
    for inner_key, inner_value in value.items():
      sub_class_dir = os.path.join(meta_class_dir,inner_key)
      features_path = os.path.join(sub_class_dir,params['features_file_name'])
      verify_folder(sub_class_dir)
      features = np.asarray(inner_value)
      with open(features_path, 'wb') as f:
        np.savetxt(f, features)

def generate_textural_features(params):

  data_path = os.path.join(params['data_dir'],params['data_dir_images'])
  feature_dict = dict()

  i = 0
  for root, dirs, files in os.walk(data_path, topdown=False):

    for name in files:
      file_dir_split = root.split(os.sep)
      meta_class = file_dir_split[-2]
      sub_class = file_dir_split[-1]
      image_path = os.path.join(root, name)
      
      if meta_class not in feature_dict:
        feature_dict[meta_class] = dict()
      if sub_class not in feature_dict[meta_class]:
        feature_dict[meta_class][sub_class] = list()
      
      # read the training image
      image = cv2.imread(image_path)

      # convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # extract haralick texture from the image
      print(i,':',name)
      textures = extract_features(gray)
      
      feature_dict[meta_class][sub_class].append(textures)
      i += 1

  save_features(params,feature_dict)

if __name__ == '__main__':

  params = utils.yaml_to_dict('config.yml')
  download_data(params)
  extract_data(params)
  generate_textural_features(params)