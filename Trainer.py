import csv
import tensorflow as tf
import os
from numpy import genfromtxt
import numpy as np
import random
import math
import constants

import pickle
from tfx import v1 as tfx

ITERATIONS = 60
NODES = 43 # 42 locations on the board, and the last is the current turn
HIDDEN_NODES = 128

def get_next_model_file_name() -> str:
  i = 0
  while os.path.exists("models/win_estimate_%s.model" % i):
    i += 1
  return "models/win_estimate_%s.model" % i

def get_latest_model_file_name() -> str:
  i = 0
  while os.path.exists("models/win_estimate_%s.model" % i):
    i += 1
  return "models/win_estimate_%s.model" % (i-1)

def get_most_recent_model():
  return tf.keras.models.load_model(get_latest_model_file_name())

def get_total_data_files() -> int:
  i = 0
  for filename in os.listdir('results'):
    i += 1
  return i - 1


def data_with_only_known_results(file_data):
  known_lines = []
  for line in file_data:
    if line[0] == 0 or line[0] == 1:
      known_lines.append(line)
  return np.array(known_lines)

def load_data_newest():
  total_files = get_total_data_files()

  data = {
    'labels': None,
    'features': None
  }
  file_data = None
  i = 0
  for filename in os.listdir('results'):
    only_take_known_results = True
    if i > total_files - 20:
      only_take_known_results = False
    i += 1

    file_data = genfromtxt('results/' + filename, delimiter=',')
    if only_take_known_results:
      file_data = data_with_only_known_results(file_data)

    label_array = np.array(file_data[:, 0])
    label_array = np.reshape(label_array, (-1, 1))

    if data['labels'] is None:
      data['labels'] = label_array
      data['features'] = np.vstack([file_data[:, 1:]])
    else:
      data['labels'] = np.vstack([data['labels'], label_array])
      data['features'] =  np.vstack([data['features'], np.array(file_data[:,1:])])
  return data


def load_pickled_data():
  with open(constants.MOST_RECENT_PICKLE_FILE, 'rb') as f:
    obj = pickle.load(f)
    return obj


def load_data():
  data = {
    'labels': None,
    'features': None
  }
  file_data = None
  for filename in os.listdir('results'):
    file_data = genfromtxt('results/' + filename, delimiter=',')
    if data['labels'] is None:
      label_array = np.array(file_data[:,0])
      label_array = np.reshape(label_array, (-1, 1))
      data['labels'] = label_array
      data['features'] = np.vstack([file_data[:, 1:]])
    else:
      label_array = np.array(file_data[:,0])
      label_array = np.reshape(label_array, (-1, 1))
      data['labels'] = np.vstack([data['labels'], label_array])
      data['features'] =  np.vstack([data['features'], np.array(file_data[:,1:])])
  return data

def get_thick_model():
  hidden_nodes = 256
  model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(NODES, input_shape=(NODES,)),
    tf.keras.layers.Dense(hidden_nodes, activation='relu'),
    tf.keras.layers.Dense(hidden_nodes, activation='relu'),
    tf.keras.layers.Dense(1)
  ])
  return model

def get_long_model():
  model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(NODES, input_shape=(NODES,)),
    tf.keras.layers.Dense(92, activation='relu'),
    tf.keras.layers.Dense(42, activation='relu'),
    tf.keras.layers.Dense(42, activation='relu'),
    tf.keras.layers.Dense(7, activation='sigmoid'),
    tf.keras.layers.Dense(1)
  ])
  return model

def get_massive_model():
  model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(NODES, input_shape=(NODES,)),
    tf.keras.layers.Dense(528, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(7, activation='sigmoid'),
    tf.keras.layers.Dense(1)
  ])
  return model

def train_model(data):
  model = get_massive_model()

  loss_fn = tf.keras.losses.MeanSquaredError()

  model.compile(optimizer='adam',
                loss=loss_fn,
                metrics=['accuracy'])
  model.fit(data['train_features'], data['train_labels'],
            epochs=ITERATIONS,
            validation_data=(data['validation_features'], data['validation_labels']))
  return model

def show_sample_output(data, model):
  for i in range(40):
    rand_row = random.randint(0, data['test_features'].shape[0])
    print("looking at  move number " + str(rand_row))
    features = np.copy(data['test_features'][rand_row, :])
    prediction = model.predict(np.reshape(features, (1, NODES)))
    print("expected" + str(data['test_labels'][rand_row]) + " prediction " + str(prediction))

    board = np.copy(features[0:42])
    print(np.reshape(board, (7, 6)))

def get_num_moves(board) -> int:
  total = 0
  for val in board:
    if val == 0 or val ==1:
      total += 1
  return total

def show_wrong_output(data, model):
  print('=================== Wrong Labels ==============')
  total_wrong = 0
  very_wrong_total = 0
  wrong_at_num = {}
  for i in range(6*7 + 1):
    wrong_at_num[i] = 0
  for i in range(data['test_features'].shape[0]):
    features = np.copy(data['test_features'][i, :])
    prediction_arr = model.predict(np.reshape(features, (1, NODES)))
    prediction = prediction_arr[0][0]

    actual = data['test_labels'][i]
    if abs(actual - prediction) > 0.25:
      print("expected" + str(data['test_labels'][i]) + " prediction " + str(prediction))
      board = np.copy(features[0:42])
      print(np.reshape(board, (7, 6)))
      total_wrong += 1
      wrong_at_num[get_num_moves(board)] += 1

    if abs(actual - prediction) > 0.7:
      very_wrong_total +=1
  print( ' ==========> WRONG ' + str(total_wrong) + ' / ' + str(data['test_features'].shape[0]))
  print( ' ==========> VERY_WRONG ' + str(very_wrong_total) + ' / ' + str(data['test_features'].shape[0]))
  print(' wrong by number of moves ' + str(wrong_at_num))

def evaluate_model(model, data):
  predictions = model.predict(data['test_features'])
  total = 0
  total_wrong = 0
  very_wrong = 0
  for prediction, label in zip(predictions, data['test_labels']):
    total += 1
    p = prediction[0]
    if p > 1:
      p = 1
    if p < 0:
      p = 0
    if (p-label) > 0.4:
      total_wrong += 1
    if (p-label) > 0.7:
      very_wrong += 1

  print ('wrong ' + str(total_wrong) + '/' + str(total) + "    very wrong " + str(very_wrong) + "/" + str(total) )

def test_model(model, data):
  results = model.evaluate(data['test_features'], data['test_labels'])
  print(results)

def train_newest_model():
  data = load_pickled_data()
  model = train_model(data)

  #show_sample_output(data, model)

  #show_wrong_output(data,model)
  evaluate_model(model, data)
  test_model(model, data)

  out_file_name = get_next_model_file_name()
  model.save(out_file_name)


# TFX will call this function.
def run_fn(fn_args: tfx.components.FnArgs):
  train_newest_model()


if __name__ == '__main__':
  train_newest_model()