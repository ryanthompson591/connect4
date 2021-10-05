
import tensorflow as tf
import pickle
import os
import numpy as np
import constants

def evaluate_all(data):
  i = 30
  while os.path.exists("models/win_estimate_%s.model" % i):
    model_name = "models/win_estimate_%s.model" % i
    print ('\n\n===============================' + model_name + '=================')
    model = tf.keras.models.load_model(model_name)
    evaluate_model(model, data)
    i += 1

def evaluate_most_recent(data):
  i = 30
  while os.path.exists("models/win_estimate_%s.model" % i):
    i +=1
  i -= 1
  model_name = "models/win_estimate_%s.model" % i
  print('\n\n===============================' + model_name + '=================')
  model = tf.keras.models.load_model(model_name)
  evaluate_model_deep(model, data)


def load_pickled_data():
  with open(constants.MOST_RECENT_PICKLE_FILE, 'rb') as f:
    obj = pickle.load(f)
    return obj

def evaluate_model_deep(model, data):
  predictions = model.predict(data['test_features'])
  MAX_PLAYS = 44
  totals = np.zeros(MAX_PLAYS)
  total_wrong = np.zeros(MAX_PLAYS)
  very_wrong = np.zeros(MAX_PLAYS)

  features = data['test_features']
  plays_arr = np.sum(np.where(features != 0.5, 1,0), axis = 1)

  for prediction, label, plays in zip(predictions, data['test_labels'], plays_arr):
    totals[plays] += 1
    p = prediction[0]
    if p > 1:
      p = 1
    if p < 0:
      p = 0
    if (p-label) > 0.4:
      total_wrong[plays] += 1
    if (p-label) > 0.7:
      very_wrong[plays] += 1

  for i in range(2, MAX_PLAYS):
    print('%d\t%.2f\t%d\t%d\t%d' % (i-1, float(very_wrong[i]) / float(totals[i] + 1), total_wrong[i], very_wrong[i], totals[i]))

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



data = load_pickled_data()
evaluate_most_recent(data)