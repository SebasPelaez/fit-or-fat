import numpy as np
import os

def matriz_features(data_path):
    features_dict = dict()

    for base, dis, files in os.walk(os.path.join('dataset',data_path)):
        for file in files:

            file_dir_split = base.split(os.sep)
            meta_class = file_dir_split[-2]
            if meta_class not in features_dict:
                features_dict[meta_class] = list()

            image_path = os.path.join(base, file)
            feature = np.loadtxt(image_path, delimiter=' ',dtype='str')
            features_dict[meta_class].extend(feature)

    class_list = list()

    for i,(key,value) in enumerate(features_dict.items()):
        value_as_matrix = np.array(value)
        feature_matrix = np.insert(value_as_matrix, value_as_matrix.shape[1], values=i, axis=1)
        class_list.append(feature_matrix)

    matriz_final = np.concatenate(class_list, axis=0)
    return(matriz_final)