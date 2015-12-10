import sys, pygame, random

input_string = "What size should your nonogram square be? (at most 25):  "

def get_num_input():
	while True:
		try:
			val = int(raw_input(input_string))
		except ValueError:
			print("Please enter an integer.")
		else:
			break
	return val

# Receives user input on desired nonogram size.
n = get_num_input()
while n <= 0 or n > 25:
	print("Invalid number. Your number must be between 1 and 25")
	n = get_num_input()

# CREATING GRID CONFIGURATION

# Creates random configuration of black squares in grid
def random_grid(n):
	# Each tile has a probability of 65% to be black and 35% to be white.
	grid = [[1 if random.random() < .65 else 0 for i in range(n)] for j in range(n)]
	return grid

# Finds the counts of consecutive black squares in column 'col' in grid
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

# Finds the counts of consecutive black squares in row 'row' in grid
def count_row(row, grid, n):
	row_counts_array = []
	consecutive_count = 0
	one_row = grid[row]
	for col in range(n):
		if one_row[col] == 1:
			consecutive_count += 1
		elif consecutive_count > 0:
			row_counts_array.append(consecutive_count)
			consecutive_count = 0
	if consecutive_count > 0:
		row_counts_array.append(consecutive_count)
	return row_counts_array

# Gets random grid
grid = random_grid(n)

col_counts = []
row_counts = []
for num in range(n):
	# Accumulates the column counts and row counts in each column and row
	col_counts.append(count_col(num, grid, n))
	row_counts.append(count_row(num, grid, n))

# Finds the max number of counts in a row
if len(row_counts) > 0:
	row_max_counts = max([len(row) for row in row_counts])
else:
	row_max_counts = 0

# Finds the max number of counts in a column
if len(col_counts) > 0:
	col_max_counts = max([len(col) for col in col_counts])
else:
	col_max_counts = 0

# Creating board
white = 255, 255, 255
black = 0, 0, 0
# Tile width and height
tile_dim = 23
# Screen width and height
size = width, height = 62 + (row_max_counts + n) * tile_dim, 62 + (col_max_counts + n) * tile_dim
# Position of top-left corner of the grid
x_offset = 33 + tile_dim * row_max_counts
y_offset = 33 + tile_dim * col_max_counts

# Starts pygame
pygame.init()

# Initializes screen as blank white screen
screen = pygame.display.set_mode(size)
screen.fill(white)

# Draw borders of board
board_rect = pygame.Rect((30, 30), (2 + (row_max_counts + n) * tile_dim, 2 + (col_max_counts + n) * tile_dim))
pygame.draw.rect(screen, black, board_rect, 3)

# Draw interior lines
for num in range(n + 1):
	line_width = 1
	# Thicken the lines between the counts and the grid
	if num == 0:
		line_width = 3
	pygame.draw.line(screen, black, (width - 30, 30 + tile_dim * (num + col_max_counts)), 
		(30, 30 + tile_dim * (num + col_max_counts)), line_width)
	pygame.draw.line(screen, black, (30 + tile_dim * (num + row_max_counts), 30), 
		(30 + tile_dim * (num + row_max_counts), height - 30), line_width)

# Load the black square and white square images
black_image = pygame.image.load("black.jpg").convert()
white_image = pygame.image.load("white.jpg").convert()
# Initialize the array that will hold the images of the numbers for the counts
num_images = [0]
inverted_num_images = [0]
# Load necessary count number images
for i in range(1, n + 1):
	pic_name = str(i) + ".jpg"
	num_images.append(pygame.image.load(pic_name).convert())
	pic_inverted_name = str(i) + "_inverted.jpg"
	inverted_num_images.append(pygame.image.load(pic_inverted_name).convert())

# Blit the counts onto the screen
for j in range(n):
	for count in range(len(col_counts[j])):
		image = num_images[col_counts[j][- 1 - count]]
		image_rect = image.get_rect()
		# Sets position of image
		image_rect.top = y_offset - tile_dim * (1 + count)
		image_rect.left = x_offset + tile_dim * j
		screen.blit(image, image_rect)

	for count in range(len(row_counts[j])):
		image = num_images[row_counts[j][- 1 - count]]
		image_rect = image.get_rect()
		# Sets position of image
		image_rect.top = y_offset + tile_dim * j
		image_rect.left = x_offset - tile_dim * (1 + count)
		screen.blit(image, image_rect)
# Update the screen to show the initial starting board to user
pygame.display.flip()

# GAME DYNAMICS

# Start timer
start_time = pygame.time.get_ticks()
print("Time started! Press ENTER to have your grid checked and a time-update.\n")

# Returns true if the user's grid satisfies the row_counts and col_counts of the original grid.
def check_finished(row_counts, col_counts, display_grid):
	n = len(row_counts)
	for num in range(n):
		# check row "num"
		one_col = col_counts[num]
		one_row = row_counts[num]
		display_row_count = count_row(num, display_grid, n)
		display_col_count = count_col(num, display_grid, n)
		if len(one_row) != len(display_row_count) or len(one_col) != len(display_col_count):
			return False
		
		for i in range(len(one_row)):
			if one_row[i] != display_row_count[i]:
				return False
		for j in range(len(one_col)):
			if one_col[j] != display_col_count[j]:
				return False
	return True

# Colors the tile at the given position with the color of the given image.
def color_tile(screen, tile_x, tile_y, x_offset, y_offset, image):
	image_rect = image.get_rect()
	image_rect.left = x_offset + 1 + tile_dim * tile_x
	image_rect.top = y_offset + 1 + tile_dim * tile_y 
	screen.blit(image, image_rect)
	pygame.display.update(image_rect)

# Disables unnecessary events for performance purposes.
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.KEYUP, pygame.JOYAXISMOTION, 
	pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN, 
	pygame.VIDEORESIZE, pygame.VIDEOEXPOSE, pygame.USEREVENT, pygame.ACTIVEEVENT])

# Initializes the user's grid that is displayed on the screen with all white tiles.
display_grid = [[0 for i in range(n)] for j in range(n)]
# Initializes all column counts as non-inverted images
col_counts_inverted = [[0 for num in col_counts[col]] for col in range(n)]
# Initializes all row counts as non-inverted images
row_counts_inverted = [[0 for num in row_counts[row]] for row in range(n)]

# This color variable keeps track of what color the cursor will change tiles it passed over while
# click and drag ability is enabled.
color = None
while True:
	# Wait for key to be pressed, mouse button to be pressed, released, or moved while button is pressed down
	pygame.event.wait
	for event in pygame.event.get():
		# Quit the game by exiting window
		if event.type == pygame.QUIT: sys.exit()
		# Mouse is clicked: toggles the color of chosen tile; starts click and drag ability
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Obtains the mouse position	
			mouse_x, mouse_y = event.pos
			# Find the row and column of the tile in the grid that the mouse has clicked on
			tile_x, tile_y = int((mouse_x - x_offset) / tile_dim), int((mouse_y - y_offset) / tile_dim)

			if tile_x >= 0 and tile_x < n:
				if tile_y >= 0 and tile_y < n:
					# Sets color to the opposite color that already exists at the clicked tile; toggles tile's color
					color = 1 - display_grid[tile_y][tile_x]
					display_grid[tile_y][tile_x] = color
					if color == 0: color_tile(screen, tile_x, tile_y, x_offset, y_offset, white_image)
					else: color_tile(screen, tile_x, tile_y, x_offset, y_offset, black_image)
					# Enables the click and drag ability (Now when mouse passes over another tile, the tile becomes 'color')
					pygame.event.set_allowed(pygame.MOUSEMOTION)
				# Toggles inversion of individual counts in columns
				elif tile_y < 0 and - 1 - tile_y < len(col_counts_inverted[tile_x]):
					length = len(col_counts[tile_x])
					inverted = col_counts_inverted[tile_x][length + tile_y]

					if inverted == 0: color_tile(screen, tile_x, tile_y, x_offset - 1, y_offset - 1, 
							inverted_num_images[col_counts[tile_x][length + tile_y]])
					else: color_tile(screen, tile_x, tile_y, x_offset - 1, y_offset - 1, 
							num_images[col_counts[tile_x][length + tile_y]])

					col_counts_inverted[tile_x][length + tile_y] = 1 - inverted
			# Toggles inversion of individual counts in rows
			elif tile_y >= 0 and tile_y < n and tile_x < 0 and - 1 - tile_x < len(row_counts_inverted[tile_y]):
				length = len(row_counts[tile_y])
				inverted = row_counts_inverted[tile_y][length + tile_x]
				
				if inverted == 0: color_tile(screen, tile_x, tile_y, x_offset - 1, y_offset - 1, 
						inverted_num_images[row_counts[tile_y][length + tile_x]])
				else: color_tile(screen, tile_x, tile_y, x_offset - 1, y_offset - 1, 
						num_images[row_counts[tile_y][length + tile_x]])

				row_counts_inverted[tile_y][length + tile_x] = 1 - inverted

		# Click and drag
		elif event.type == pygame.MOUSEMOTION:
			# SAME AS ABOVE
			mouse_x, mouse_y = event.pos
			tile_x, tile_y = int((mouse_x - x_offset) / tile_dim), int((mouse_y - y_offset) / tile_dim)

			if tile_x >= 0 and tile_x < n and tile_y >= 0 and tile_y < n:
				display_grid[tile_y][tile_x] = color
				if color == 0: color_tile(screen, tile_x, tile_y, x_offset, y_offset, white_image)
				else: color_tile(screen, tile_x, tile_y, x_offset, y_offset, black_image)

		# End click and drag capability
		elif event.type == pygame.MOUSEBUTTONUP:
			color = None
			# Disables click and drag ability
			pygame.event.set_blocked(pygame.MOUSEMOTION)
		# Checks if the user has won and gives user a time update on console
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				# Checks if the user's grid satisfies the row_counts and col_counts.
				if check_finished(row_counts, col_counts, display_grid):
					print("YOU WIN! YOUR TIME ON " + str(n) + "x" + str(n) + " WAS " 
						+ str((pygame.time.get_ticks() - start_time) / 1000) + " SECONDS!")
					sys.exit()
				else:
					print("NOT FINISHED YET! TIME SPENT IS " + str((pygame.time.get_ticks() - start_time) / 1000)
						+ " SECONDS.")