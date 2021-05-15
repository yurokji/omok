import pygame
from pygame import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP

OMOK_NUM = 5
NO_DOL = 0
BLACK_DOL = 1
WHITE_DOL = 2
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,200,0)
pad = 40
cell_size = 50
dol_size = 40
board_width, board_height = 19, 19
w = cell_size * (board_width - 1) + pad * 2
h = cell_size * (board_height - 1) + pad * 2
board = []
dols_order = []
win = False

img_bg = pygame.image.load("./image/wooden.jpg")
img_bg = pygame.transform.scale(img_bg, (w,h))

img_go_black = pygame.image.load("./image/go_black.png")
img_go_black = pygame.transform.scale(img_go_black, (dol_size,dol_size))
img_go_white = pygame.image.load("./image/go_white.png")
img_go_white = pygame.transform.scale(img_go_white, (dol_size,dol_size))

pygame.font.init()
font_size = 80
myfont = pygame.font.SysFont("nanumgothicbold", font_size)


for i in range(board_height):
	row = []
	for j in range(board_width):
		row.append(NO_DOL)
	board.append(row)

def printBoard():
	for row in board:
		print(row)
	print()

def draw_board(screen):
	screen.blit(img_bg, (0,0))
	for i in range(board_height):
		py = pad + i * cell_size
		px = pad + i * cell_size
		pygame.draw.line(screen, BLACK, (pad, py), (w-pad, py), 2)
		pygame.draw.line(screen, BLACK, (px, pad), (px, h-pad), 2)

def draw_dols_order(screen, bgn=0, end=len(dols_order)):
	for i in range(bgn, end):
		py = pad + dols_order[i][0] * cell_size - dol_size //2
		px = pad + dols_order[i][1] * cell_size - dol_size //2
		if dols_order[i][2] == BLACK_DOL:
			screen.blit(img_go_black, (px,py))
		else:
			screen.blit(img_go_white, (px,py))


def checkValid(mouse_pos):
	mx = mouse_pos[0] - pad
	my = mouse_pos[1] - pad
	
	i_m = my / cell_size
	j_m = mx / cell_size

	i_ref = round(i_m)
	j_ref = round(j_m)
	if abs(i_m-i_ref) < 0.18 and abs(j_m-j_ref) < 0.18:
		return True, int(i_ref), int(j_ref)
	else:
		return False, -1, -1

def checkHorizontalOmok(new_i, new_j, bturn):
	count = 0
	for j in range(new_j, -1, -1):
		if j < 0:
			break
		if board[new_i][j] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for j in range(new_j+1, new_j + 1 + OMOK_NUM - count):
		if j > board_width - 1:
			break
		if board[new_i][j] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkVerticalOmok(new_i, new_j, bturn):
	count = 0
	for i in range(new_i, -1, -1):
		if i < 0:
			break
		if board[i][new_j] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for i in range(new_i + 1, new_i + 1 + OMOK_NUM - count):
		if i > board_height - 1:
			break
		if board[i][new_j] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkFirstDiagOmok(new_i, new_j, bturn):
	count = 0
	for d in range(0, OMOK_NUM):
		if new_i - d < 0 or new_j + d > board_width - 1:
			break
		if board[new_i - d][new_j + d] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for d in range(1, OMOK_NUM):
		if new_i + d > board_height - 1 or new_j - d < 0:
			break
		if board[new_i + d][new_j - d] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkSecondDiagOmok(new_i, new_j, bturn):
	count = 0
	for d in range(0, OMOK_NUM):
		if new_i - d < 0 or new_j - d < 0:
			break
		if board[new_i - d][new_j - d] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for d in range(1, OMOK_NUM):
		if new_i + d > board_height - 1 or new_j + d > board_height - 1 :
			break
		if board[new_i + d][new_j + d] == (BLACK_DOL if bturn else WHITE_DOL):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkOmok(new_i, new_j, bturn):
	if checkHorizontalOmok(new_i, new_j, bturn):
		return True
	elif checkVerticalOmok(new_i, new_j, bturn):
		return True
	if checkFirstDiagOmok(new_i, new_j, bturn):
		return True
	elif checkSecondDiagOmok(new_i, new_j, bturn):
		return True
	else:
		return False
