import os
from board import Board, RED, BLUE


with open('results/known_results_processed5.csv', 'wt') as output:
  # process the first few files multiple times since there are fewer results.
  #result_file_numbers = list(range(5,10)) + list(range(5,42))
  result_file_numbers = [1]
  for i in result_file_numbers:
    filename = 'results/unprocessed/moves%d.txt.out.txt' % i
    with open(filename, 'rt') as f:
      for line in f.readlines():
        print (filename + ' ' + line)
        board = Board()
        moves, result_str = line.split(' ')
        result = int(result_str)
        for move in moves:
          board.add_piece(int(move) - 1)
        real_result = 0.5
        if board.turn == BLUE:
          if result < 0:
            real_result = 1
          elif result > 0:
            real_result = 0
        elif board.turn == RED:
          if result < 0:
            real_result = 0
          elif result > 0:
            real_result = 1
        output_str = str(real_result) + ',' + board.get_features_str() + '\n'
        print (output_str)
        output.write(output_str)