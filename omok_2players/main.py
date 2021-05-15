from omok import *
pygame.init()
SURFACE = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
black_turn = True
running = True
is_down = False
is_valid = False
new_pos = (0,0)

while running:
	for e in pygame.event.get():
		if e.type == QUIT:
			running = False
		elif e.type == MOUSEBUTTONDOWN:
			is_down = True
		elif e.type == MOUSEBUTTONUP:
			if is_down:
				is_valid, i_new, j_new = checkValid(pygame.mouse.get_pos())
				if is_valid:
					is_down = False
					if board[i_new][j_new] == NO_DOL:
						board[i_new][j_new] = BLACK_DOL if black_turn else WHITE_DOL
						dols_order.append((i_new, j_new, board[i_new][j_new]))
						printBoard()
						if checkOmok(i_new,j_new, black_turn):
							running = False
							win = board[i_new][j_new]
						black_turn = not black_turn
	SURFACE.fill(YELLOW)
	draw_board(SURFACE)
	draw_dols_order(SURFACE, 0, len(dols_order))
	pygame.display.update()
	clock.tick(30)

if win:
	win_text = "검은 돌" if win == BLACK_DOL else "흰 돌"
	win_text += " 승리!"
	text_surface = myfont.render(win_text, False, (0, 0, 255))
	SURFACE.blit(text_surface, (w//2 - 200, h//2-font_size))
	pygame.display.update()
	for i in range(6):
		clock.tick(1)



pygame.quit()

