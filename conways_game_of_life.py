from PIL import Image, ImageDraw
import numpy as np
import pygame
from Cell import *
from Colors import *
import random

pygame.init()

# screen size
WIDTH, HEIGHT = 1000, 1000

# size of the cell
CELL_SIZE = 50

# how many frames per second the game should run at
FPS = 5

# global variables
global WIN
global clock
global cells
global CELLS_WIDE
global CELLS_HIGH
		

# mpos is the input mouse position
def get_row_col_from_mouse(mpos):
	mx, my = mpos
	# use integer division to get the row and col that the cell is in using the cell size
	return ((my // CELL_SIZE), (mx // CELL_SIZE)) 


# draws the grid lines that separate every cell
def draw_grid_lines():
	    # draw the horizontal lines first from the left of the screen to the right(the width)
	    for i in range(CELLS_HIGH):
	        pygame.draw.line(WIN, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

	    # draw the vertical lines from the top of the screen to the bottom(the height)
	    for j in range(CELLS_WIDE):
	        pygame.draw.line(WIN, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))


def draw():
	# fill the screen with a white background to reset it
	WIN.fill(BLACK)

	# draw every cell
	for cell in cells:
		cell.draw_cell()

	# draw the grid lines
	draw_grid_lines()		

	# update the screen to show changes
	pygame.display.update()


def get_cell(row, col):
	for cell in cells:
		if cell.get_row() == row and cell.get_col() == col:
			return cell
	return None


# gets the number of alive neighbors for this cell 
def get_num_alive_neighbors(node):
	count = 0
	for npos in node.get_neighbors_pos():
		neighbor = get_cell(npos[0], npos[1])
		if neighbor.get_alive():
			count += 1
	return count


def check_alive(node):
	# Conway's rules:
	# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # 2. Any live cell with two or three live neighbours lives on to the next generation.
    # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
	neighbors_alive = get_num_alive_neighbors(node)
		
	# if this cell is alive
	if node.get_alive():
		# rule 1
		if neighbors_alive < 2:
			return False

		# rule 3
		elif neighbors_alive > 3:
			return False

		# rule 2 is everything else while alive, the num alive neighbors being 2 or 3, it stays the same
		else:
			return True
	else:
		# if this cell is dead
		# rule 4
		if neighbors_alive == 3:
			return True
		else:
			return False


def total_alive_cells(cells):
	count = 0
	for c in cells:
		if c.get_alive():
			count += 1
	return count 


def main():
	global WIDTH
	global HEIGHT
	global clock
	global WIN
	global CELLS_WIDE
	global CELLS_HIGH
	global cells
	global FPS

	# if a random world should be made or not
	random_world = False

	# make a clock object to control FPS
	clock = pygame.time.Clock()

	# bool to keep track of when the game loop should stop running
	run = True

	# if the user is still making the world, True only if the random world is set to False
	if random_world:
		making_world = False
	else:
		making_world = True

	# get the number of cells wide and high
	CELLS_WIDE = WIDTH // CELL_SIZE
	CELLS_HIGH = HEIGHT // CELL_SIZE
	num_cells = CELLS_WIDE * CELLS_HIGH

	print(50*"-")
	print(f"Cells wide: {CELLS_WIDE} by Cells high: {CELLS_HIGH}")
	print(f"Total number of cells: {num_cells}")

	# make the pygame display
	WIN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Conway's Game of Life")

	# all the cells in the world
	cells = []

	# make all the cells in the world
	for row in range(CELLS_HIGH):
		for col in range(CELLS_WIDE):
			cell = Cell(row, col, CELL_SIZE, WIN)
			# if it is supposed to be a randomly generated world then use a random bit to flip some cells to be alive
			if random_world:
				bit = random.getrandbits(1)
				if bit == 1:
					cell.set_alive(True)

			# add the new cell to the world
			cells.append(cell)

	# how many generation/ changes the cells have gone through
	generations = 0

	# game loop
	while run:
		# caps the framerate at value of FPS to control how many times this while loop happens per second
		clock.tick(FPS)

		#fps_control()

		# loop through all game events
		for event in pygame.event.get():
			# stop the game loop
			if event.type == pygame.QUIT:
				run = False

			if pygame.key.get_pressed()[pygame.K_LEFT]:
				FPS = FPS / 2
				if FPS < 0.5:
					FPS = 0.5
				print(f"set new FPS to: {FPS}, real fps: {clock.get_fps()}")
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				FPS = FPS * 2
				if FPS > 60:
					FPS = 60
				print(f"set new FPS to: {FPS}, real fps: {clock.get_fps()}")

			if making_world:
				# look at mouse events
				if pygame.mouse.get_pressed()[0]: 
					# left mouse button pressed, get its position
					mpos = pygame.mouse.get_pos()

					# get the row, col of where the mouse is
					row, col = get_row_col_from_mouse(mpos)

					# set this cell to white, make it alive
					cell = get_cell(row, col)

					# if a valid cell was found
					if cell is not None:
						cell.set_alive(True)
					else:
						print(f"No cell here: {mpos}")

				elif pygame.mouse.get_pressed()[2]: 
					 # right mouse button pressed, get its positions
					mpos = pygame.mouse.get_pos()

					# get the row, col of where the mouse is
					row, col = get_row_col_from_mouse(mpos)

					# set this cell back to black, kill this cell
					cell = get_cell(row, col)

					# if a valid cell was found
					if cell is not None:
						cell.set_alive(False)
					else:
						print(f"No cell here: {mpos}")

				# the enter key was pressed, stop making the world
				if pygame.key.get_pressed()[pygame.K_RETURN]:
					making_world = False

		if not making_world:
			alive = total_alive_cells(cells)
			dead = num_cells - alive
			print(50*"-")
			print(f"Generation: {generations}, Cells alive: {alive}, Cells dead: {dead}")

			# new cells for the next world
			next_cells = [[False] for _ in range(len(cells))]

			# if the user is no longer making the world, check if every cell is alive according to Conway's rules
			for i in range(len(cells)):
				# the alive/dead state of the next cell
				next_cell_state = check_alive(cells[i])
					
				# copy the cell state over
				next_cells[i] = next_cell_state

			# the new cells are the next_cells thar got their state from the current world state
			for i in range(len(cells)):
				cells[i].set_alive(next_cells[i])

			# increment the generations now that all the cells have checked/changed their states
			generations += 1

		# draw the window to the screen
		draw()

	# quit the display for pygame
	pygame.quit()


if __name__ == "__main__":
	main()
