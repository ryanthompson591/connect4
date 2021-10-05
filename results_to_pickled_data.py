import numpy as np
import pickle
import os
from numpy import genfromtxt
import math
import constants

def load_data(file_prefix=''):
  all_data = None
  for filename in os.listdir('results'):
    if not filename.startswith(file_prefix):
      continue
    file_data = genfromtxt('results/' + filename, delimiter=',')
    if all_data is None:
      all_data = np.vstack(file_data)
    else:
      all_data = np.vstack([all_data, file_data])

  np.random.shuffle(all_data)
  validation_index = math.floor(all_data.shape[0] * 0.8)
  test_index = math.floor(all_data.shape[0] * 0.9)

  train_data = all_data[0:validation_index,:]
  validation_data = all_data[validation_index:test_index,:]
  test_data = all_data[test_index:, :]

  train_features = train_data[:,1:]
  train_labels = train_data[:,0]
  train_labels = np.reshape(train_labels, (-1, 1))

  validation_features = validation_data[:,1:]
  validation_labels = validation_data[:,0]
  validation_labels = np.reshape(validation_labels, (-1, 1))

  test_features = test_data[:,1:]
  test_labels = test_data[:,0]
  test_labels = np.reshape(test_labels, (-1, 1))


  return {
    'train_features':train_features,
    'train_labels':train_labels,
    'validation_features':validation_features,
    'validation_labels':validation_labels,
    'test_features': test_features,
    'test_labels': test_labels
  }


if __name__ == '__main__':
  with open(constants.MOST_RECENT_PICKLE_FILE, 'wb') as file_handle:
    obj = load_data(file_prefix='known_results')
    pickle.dump(obj, file_handle, protocol=pickle.HIGHEST_PROTOCOL)
