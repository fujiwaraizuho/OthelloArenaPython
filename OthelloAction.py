import random
import copy
import numpy
import OthelloLogic

"""
石の位置による重み付け値
"""
# https://www.info.kindai.ac.jp/~takasi-i/thesis/2014_10-1-037-0140_S_Okigaki_resume.pdf
BOARD_GAIN_SCORE_OKIGAKI_MODEL = [
	[45, -11, 4, -1, -1, 4, -11, 45],
	[-11, -16, -1, -3, -3, -1, -16, -11],
	[4, -1, 2, -1, -1, 2, -1, 4],
	[-1, 3, -1, 0, 0, -1, -3, -1],
	[-1, 3, -1, 0, 0, -1, -3, -1],
	[4, -1, 2, -1, -1, 2, -1, 4],
	[-11, -16, -1, -3, -3, -1, -16, -11],
	[45, -11, 4, -1, -1, 4, -11, 45]
]

# https://uguisu.skr.jp/othello/5-1.html
BOARD_GAIN_SCORE_UGUISU_MODEL = [
	[30, -12, 0, -1, -1, 0, -12, 30],
	[-12, -15, -3, -3, -3, -3, -15, -12],
	[0, -3, 0, -1, -1, 0, -3, 0],
	[-1, -3, -1, -1, -1, -1, -3, -1],
	[-1, -3, -1, -1, -1, -1, -3, -1],
	[0, -3, 0, -1, -1, 0, -3, 0],
	[-12, -15, -3, -3, -3, -3, -15, -12],
	[30, -12, 0, -1, -1, 0, -12, 30]
]

"""
board:現在の盤面の状態
moves:現在の合法手の一覧
"""
def getAction(board, moves):
	return getSimpleMaxGainAction(board, moves, BOARD_GAIN_SCORE_UGUISU_MODEL)

"""
ひっくり返せる枚数が一番多い合法手を打つやつ
"""
def getSimpleMaxAction(board, moves):
	selected_move = moves[0]
	selected_move_score = -64

	# すべての合法手のスコアを算出し最大値を求める
	for move in moves:
		# 合法手を打った後の盤面をシミュレーション
		simulation_board = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
		# 合法手を打った後の盤面全体の総和
		move_score = getMoveScore(simulation_board)

		# 前の合法手よりもスコアが大きければ置換
		if (move_score >= selected_move_score):
			selected_move = move
			selected_move_score = move_score

	return selected_move

"""
ひっくり返せる枚数が一番多い + マスに重み付けをして最適な合法手を打つやつ
"""
def getSimpleMaxGainAction(board, moves, gain_model):
	selected_move = moves[0]
	selected_move_score = -64

	# すべての合法手のスコアを算出し最大値を求める
	for move in moves:
		# 合法手を打った後の盤面をシミュレーション
		simulation_board = OthelloLogic.execute(copy.deepcopy(board), move, 1, 8)
		# 合法手を打った後の盤面全体の総和と合法手ごとの重み付けを足したスコア
		move_score = getMoveScore(simulation_board) + gain_model[move[1]][move[0]]

		# 前の合法手よりもスコアが大きければ置換
		if (move_score >= selected_move_score):
			selected_move = move
			selected_move_score = move_score

	return selected_move

"""
合法手からランダムに打つやつ
"""
def getRandomAction(_, moves):
	index = random.randrange(len(moves))
	return moves[index]

def getMoveScore(board):
	return numpy.sum(board)