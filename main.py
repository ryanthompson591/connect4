import pygame
from pygame.locals import *
from board import Board, TIE, RED, BLUE
import sys
import os

from HumanPlayer import HumanPlayer
from RandomBot import RandomBot
from SimpleHeuristicBot import SimpleHeuristicBot
from HeuristicBot import HeuristicBot
from MinMaxBot import MinMaxBot
from NeuralNetBot import NeuralNetBot
from NeuralMinMaxBot import NeuralMinMaxBot
from Trainer import train_newest_model
from MinMaxBotHeuristic import MinMaxBotHeuristic

from Game import Game, WIDTH, HEIGHT, ENABLE_FILE_SAVE


MIN_MAX_BOT = 0
NEURAL_NET_BOT = 1
BASE_OUTPUT_NAME = 'results/known_results%s.csv'

def run_games(bot1, bot2, num_games):
  win_total = [0] * 3
  game_results_file_name = None
  if ENABLE_FILE_SAVE:
    i = 0
    while os.path.exists(BASE_OUTPUT_NAME % i):
      i += 1
    game_results_file_name = BASE_OUTPUT_NAME % i

  for _ in range(num_games):
    # draw, red win, blue win
    game = Game(bot1, bot2, display_surface, save_to_file_name=game_results_file_name)
    game.run()
    result = game.get_result()
    if result[0] == TIE:
      win_total[0] += 1
    else:
      win_total[result[0]] += 1
    print("Totals (Draw - Red - Blue): " + str(win_total) + " The winner was " + str(game.get_result()))
    bot1.reset()
    bot2.reset()
  return win_total


def single_training_pass():
  sum_results = [0,0]

  results = run_games(MinMaxBot(), NeuralMinMaxBot(), 8)
  sum_results[MIN_MAX_BOT] += results[RED]
  sum_results[NEURAL_NET_BOT] += results[BLUE]
  results = run_games(NeuralMinMaxBot(), MinMaxBot(), 8)
  sum_results[MIN_MAX_BOT] += results[BLUE]
  sum_results[NEURAL_NET_BOT] += results[RED]
  run_games(NeuralMinMaxBot(), NeuralMinMaxBot(), 1)
  train_newest_model()
  return sum_results


def multi_pass_training(repetitions):
  for i in range(repetitions):
    sum_results = single_training_pass()
    print(" ======================================== ")
    if sum_results[NEURAL_NET_BOT] > sum_results[MIN_MAX_BOT]:
      print("THE NEURAL NET POWER WINS " + str(sum_results))
    else:
      print("OH NO STILL TOO WEAK " + str(sum_results))
    print ("\n\n\n ======================================== ")

if __name__ == '__main__':
  pygame.init()
  display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Connect Four")

#  multi_pass_training(5)
  win_total = run_games(MinMaxBotHeuristic(), NeuralMinMaxBot(), 5)
  heuristic_wins = win_total[BLUE]
  ties = win_total[0]
  win_total = run_games(NeuralMinMaxBot(), MinMaxBotHeuristic(),  5)
  heuristic_wins += win_total[RED]
  ties += win_total[0]
  print ('The bot won %d, with %d ties.' % (heuristic_wins, ties))