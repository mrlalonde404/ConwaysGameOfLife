import pygame
from Colors import *

class Cell:
	def __init__(self, row, col, cell_size, WIN):
		# what row and column the node is at
		self.row = row
		self.col = col

		# get the size of the cell so that the 
		self.cell_size = cell_size
		
		# window to draw the node onto
		self.WIN = WIN

		# if this cell is alive
		self.alive = False

		# the row,col combinations for the 8 possible neighbors around the cell
		self.neighbors_pos = self.find_neighbors_positions(self.WIN.get_size()[0] // self.cell_size, self.WIN.get_size()[1]// self.cell_size)

	# this function populates the row,col combinations for neighbors_pos, it gets all of the positions for every neighbor 
	# in the 8 cells around the current node and wraps around the top, left, right, and bottom borders
	def find_neighbors_positions(self, cells_wide, cells_high):
		# All possible offsets, (0,0) is the current node that we are getting neighbors for:
		# (-1,-1)  (-1,0)  (-1,1)
		# (0,-1)   (0,0)   (0,1)
		# (1,-1)   (1,0)   (1,1)

		# after all the proper offsets have been gathered we will return the list of neighbors positions
		neighbors_pos = []

		for j in range(-1, 2):
			for i in range(-1, 2):
				if j != 0 or i != 0:
					col = (self.col + i + cells_wide) % cells_wide
					row = (self.row + j + cells_high) % cells_high
					neighbors_pos.append((row, col))
		return neighbors_pos

	def draw_cell(self):
		# get the color for the cell depending on if the cell is alive or not
		if self.alive:
			color = WHITE
		else:
			color = BLACK

		# get the left x coordinate, the column and cell size product, and the top, the row and cell size product 
		left = self.col * self.cell_size
		top =  self.row * self.cell_size

		# draw a rectangle to fill the cell with the color depending on if it is alive or not
		pygame.draw.rect(self.WIN, color, (left, top, self.cell_size, self.cell_size))

	def get_row(self):
		return self.row

	def get_col(self):
		return self.col

	def get_alive(self):
		return self.alive

	def get_neighbors_pos(self):
		return self.neighbors_pos

	def set_row(self, row):
		self.row = row

	def set_col(self, col):
		self.col = col

	def set_alive(self, alive):
		self.alive = alive

	def set_neighbors_pos(self, neighbors_pos):
		self.neighbors_pos = neighbors_pos

	def __repr__(self):
		return f"pos: ({self.row},{self.col}), alive: {self.alive}"