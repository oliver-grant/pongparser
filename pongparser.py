import sys
import requests
from operator import add
import re

def parse_score(score):
	p1_wins = 0
	p2_wins = 0
	p1_points = 0
	p2_points = 0
	p1_games = 0
	p2_games = 0
	scores = re.split(r"[ ,]+", score)
	for i in range(len(scores)):
		scores[i] = scores[i].split(':')
		if int(scores[i][0]) > int(scores[i][1]):
			p1_games += 1
		else:
			p2_games += 1
		p1_points += int(scores[i][0])
		p2_points += int(scores[i][1])
	if p1_games > p2_games:
		p1_wins = 1
	else:
		p2_wins = 1
	return[p1_wins, p2_wins, p1_games, p2_games, p1_points, p2_points]

def reverse_score(score):
	return (score[1], score[0], score[3], score[2], score[5], score[4])

def get_pool_scores(offset):
	results = []
	for i in range(1+offset, 8 + offset):
		for j in  range(1,8):
			if i-offset == 1:
				results.append([0,0,0,0,0,0])
			elif scores[i][j] != '' and scores[i][j] != 'X':
				res = parse_score(scores[i][j])
				rev_res = reverse_score(res)
				results[i-offset-2] = map(add, results[i-offset-2], res)
				results[j-1] = map(add, results[j-1], rev_res)
	print(results)
	return(results)

import csv
with open('pong.csv', 'rb') as f:
	reader = csv.reader(f)
	scores = list(reader)
	# Pool A
	poola = get_pool_scores(0)
	poolb = get_pool_scores(11)
	poolc = get_pool_scores(22)
	poold = get_pool_scores(33)

	scores = []
	pool_scores = []
	for pool in [poola, poolb, poolc, poold]:
		pool_score = []
		for player in pool:
			score = 0.0
			if (player[0] + player[1] != 0):
				score += float(player[0]) / (float(player[0]) + float(player[1]))
				score += (float(player[2]) - float(player[3]))/ 1000
				score += (float(player[4]) - float(player[5])) / 1000000
			else:
				score = -1
			scores.append(score)
			pool_score.append(score)
		pool_scores.append(pool_score)

	sorted_scores = sorted(scores, reverse = True)
	score_rank = [sorted_scores.index(v) + 1 for v in scores]
	score_rank_pools = []
	for i in range(4):
		sorted_scores = sorted(pool_scores[i], reverse = True)
		score_rank_pool = [sorted_scores.index(v) + 1 for v in pool_scores[i]]
		score_rank_pools += score_rank_pool

	p_index = 0
	for pool in [poola, poolb, poolc, poold]:
		for row in pool:
			row.append(score_rank_pools[p_index])
			row.append(score_rank[p_index])
	  		for col in row:
	  			print str(col) + ',',
	 		print '\n',
	 		p_index += 1
		print('\n\n\n')
