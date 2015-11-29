import sys, pygame, random

n = int(input("What size should your nonogram square be? (at most 25):  "))
while n <= 0 or n > 25:
	n = int(input("Invalid number. Your number must be between 1 and 25:  "))

# Creating configuration
def random_grid(n):
	grid = [[1 if random.random() < .65 else 0 for i in range(n)] for j in range(n)]
	return grid

def count_col(col, grid, n):
	col_counts_array = []
	consecutive_count = 0
	for row in range(n):
		if grid[row][col] == 1:
			consecutive_count += 1
		elif consecutive_count > 0:
			col_counts_array.append(consecutive_count)
			consecutive_count = 0
	if consecutive_count > 0:
		col_counts_array.append(consecutive_count)
	return col_counts_array

def count_row(row, grid, n):
	row_counts_array = []
	consecutive_count = 0
	for col in range(n):
		if grid[row][col] == 1:
			consecutive_count += 1
		elif consecutive_count > 0:
			row_counts_array.append(consecutive_count)
			consecutive_count = 0
	if consecutive_count > 0:
		row_counts_array.append(consecutive_count)
	return row_counts_array

grid = random_grid(n)

col_counts = []
row_counts = []
for num in range(n):
	col_counts.append(count_col(num, grid, n))
	row_counts.append(count_row(num, grid, n))
if len(row_counts) > 0:
	row_max_counts = max([len(row) for row in row_counts])
else:
	row_max_counts = 0

if len(col_counts) > 0:
	col_max_counts = max([len(col) for col in col_counts])
else:
	row_max_counts = 0

# Creating board
white = 255, 255, 255
black = 0, 0, 0
tile_dim = 23
size = width, height = 62 + (row_max_counts + n) * tile_dim, 62 + (col_max_counts + n) * tile_dim
pygame.init()

screen = pygame.display.set_mode(size)
screen.fill(white)

# borders of board
board_rect = pygame.Rect((30, 30), (2 + (row_max_counts + n) * tile_dim, 2 + (col_max_counts + n) * tile_dim))
pygame.draw.rect(screen, black, board_rect, 3)

# interior lines
for col in range(n + 1):
	line_width = 1
	if col == 0:
		line_width = 3
	pygame.draw.line(screen, black, (width - 30, 30 + tile_dim * (col + col_max_counts)), (30, 30 + tile_dim * (col + col_max_counts)), 
		 line_width)
	pygame.draw.line(screen, black, (30 + tile_dim * (col + row_max_counts), 30), 
		(30 + tile_dim * (col + row_max_counts), height - 30), line_width)

black_image = pygame.image.load("black.jpg").convert()
white_image = pygame.image.load("white.jpg").convert()
num_images = [0]
num_images_rects = [0]

for i in range(1, n + 1):
	pic_name = str(i) + ".jpg"
	num_images.append(pygame.image.load(pic_name).convert())

for j in range(n):
	for count in range(len(col_counts[j])):
		image = num_images[col_counts[j][- 1 - count]]
		image_rect = image.get_rect()
		image_rect.top = 33 + tile_dim * (col_max_counts - 1 - count)
		image_rect.left = 33 + tile_dim * (row_max_counts + j)
		screen.blit(image, image_rect)

	for count in range(len(row_counts[j])):
		image = num_images[row_counts[j][- 1 - count]]
		image_rect = image.get_rect()
		image_rect.top = 33 + tile_dim * (col_max_counts + j)
		image_rect.left = 33 + tile_dim * (row_max_counts - 1 - count)
		screen.blit(image, image_rect)

pygame.display.flip()
clock = pygame.time.Clock()
clock.tick()
start_time = clock.get_rawtime()

# GAME DYNAMICS
def check_finished(row_counts, col_counts, display_grid):
	print(display_grid)
	print(row_counts)
	print(col_counts)

	n = len(row_counts)
	for num in range(n):
		# check row "num"
		display_row_count = count_row(num, display_grid, n)
		display_col_count = count_col(num, display_grid, n)
		if len(row_counts[num]) != len(display_row_count) or len(col_counts[num]) != len(display_col_count):
			return False
		
		for i in range(len(row_counts[num])):
			if row_counts[num][i] != display_row_count[i]:
				return False
		for j in range(len(col_counts[num])):
			if col_counts[num][j] != display_col_count[j]:
				return False
	return True

def color_tile(screen, tile_x, tile_y, x_offset, y_offset, image):
	image_rect = image.get_rect()
	image_rect.left = x_offset + 1 + tile_dim * tile_x
	image_rect.top = y_offset + 1 + tile_dim * tile_y 
	screen.blit(image, image_rect)
	pygame.display.update(image_rect)

pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP, pygame.JOYAXISMOTION, 
	pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN, 
	pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT, pygame.ACTIVEEVENT])

display_grid = [[0 for i in range(n)] for j in range(n)]
color = None
x_offset = 33 + tile_dim * row_max_counts
y_offset = 33 + tile_dim * col_max_counts
while True:
	pygame.event.wait
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:	
			mouse_x, mouse_y = event.pos
			tile_x, tile_y = int((mouse_x - x_offset) / tile_dim), int((mouse_y - y_offset) / tile_dim)

			if tile_x >= 0 and tile_x < n and tile_y >= 0 and tile_y < n:
				color = 1 - display_grid[tile_y][tile_x]
				display_grid[tile_y][tile_x] = color
				pygame.event.set_allowed(pygame.MOUSEMOTION)
				if color == 0: color_tile(screen, tile_x, tile_y, x_offset, y_offset, white_image)
				else: color_tile(screen, tile_x, tile_y, x_offset, y_offset, black_image)
				
				

		# Click and drag
		elif event.type == pygame.MOUSEMOTION:
			mouse_x, mouse_y = event.pos
			tile_x, tile_y = int((mouse_x - x_offset) / tile_dim), int((mouse_y - y_offset) / tile_dim)

			if tile_x >= 0 and tile_x < n and tile_y >= 0 and tile_y < n:
				display_grid[tile_y][tile_x] = color
				if color == 0: color_tile(screen, tile_x, tile_y, x_offset, y_offset, white_image)
				else: color_tile(screen, tile_x, tile_y, x_offset, y_offset, black_image)


		elif event.type == pygame.MOUSEBUTTONUP:
			color = None
			pygame.event.set_blocked(pygame.MOUSEMOTION)

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if check_finished(row_counts, col_counts, display_grid):
					clock.tick()
					print("YOU WIN! YOUR TIME ON " + str(n) + "x" + str(n) + " WAS " 
						+ str((clock.get_rawtime() - start_time) / 1000) + " SECONDS!")
					sys.exit()
				else:
					print("NOT FINISHED YET!")