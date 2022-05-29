# python3
# catan_board.py - Tile and Catan Board classes. Set up a balanced catan board given proper inputs.

from string import ascii_uppercase
from math import floor


class Tile:
    """
    Tile class from which the Catan Board is created.
    This is a hexagonal tile, with the positional relationships defined as:
    right, top_right, top_left, left, bottom_left, bottom_right
    """

    def __init__(self, x, y, position, number=None, point_value=None, resource=None):
        # Positional inputs:
        self.x = x
        self.y = y
        self.pos = position

        # Catan Inputs
        self.number = number
        self.pt_value = point_value
        self.resource = resource


        # positional relationships
        self.right = None
        self.top_right = None
        self.top_left = None
        self.left = None
        self.bottom_left = None
        self.bottom_right = None

        # Create a list of possible adjacent positions
        self.possible_adjacents = self._check_possible_adjacents()

    def _check_possible_adjacents(self):
        possible_options = []
        check_options = [
            self.right, 
            self.top_right, 
            self.top_left, 
            self.left, 
            self.bottom_left, 
            self.bottom_right, 
        ]
        for option in check_options:
            if option !=None:
                possible_options.append(option)

        return possible_options


class CatanIsland:
    """
    Creates the Island of Catan using the tile class.
    """
    
    def __init__(self, max_width, min_width, resource_dict, numbers_dict, num_to_pts_dict):
        # Constants
        self.letters = list(ascii_uppercase)
        
        # Reference variables
        self.position_dict = {}
        
        # inputs
        self.max_width = max_width
        self.min_width = min_width
        self.resources = resource_dict
        self.numbers = numbers_dict
        self.convert_num_to_pts = num_to_pts_dict

        # Create the island:
        self.island = self._create_island()


    def _create_grid(self, max_width, min_width):
        """
        Creates the grid based on the max and min width supplied
        """
        letters = self.letters
        grid = []
        diff = max_width - min_width
        vertical = diff * 2
        horizontal = max_width + (max_width - 1)
        for y in range(vertical + 1):
            row = []

            # TODO: Create empty tiles so that the tiles line up properly

            for x in range(0, horizontal, 1):
                pos = f'{letters[y]}{x}'
                tile = Tile(x, y, pos)
                row.append(tile)    
            grid.append(row)
                 

        return grid

    def _create_island(self):
        """
        Creates a balanced catan board setup and ready for playing.
        """
        grid = self._create_grid(self.max_width, self.min_width)
        max_width = self.max_width
        min_width = self.min_width

        diff = max_width - min_width
        vertical = diff * 2
        horizontal = max_width + (max_width - 1)
        offset = diff
        horizontal = self.max_width + (self.max_width - 1)

        for y in range(len(grid)):
            # Create the board offsets 
            # Since the island is a hexagon
            if y <= diff and y != 0:
                offset -= 1
            elif y > diff:
                offset += 1
            for x in range(offset, horizontal - offset, 2):

                tile = grid[y][x]

                # There are no top_left or top_right tiles
                if y == 0:
                    tile.bottom_left = grid[y + 1][x - 1]
                    tile.bottom_right = grid[y + 1][x + 1]
                    # On the far left side
                    if x <= diff:
                        tile.right = grid[y][x + 2]
                    # On the far right side
                    elif x >= horizontal - diff:
                        tile.left = grid[y][x - 2]
                    else:
                        tile.right = grid[y][x + 2]
                        tile.left = grid[y][x - 2]

                # If the tile is at the bottom of the board
                elif y == len(grid) -  1:
                    tile.top_left = grid[y - 1][x - 1]
                    tile.top_right = grid[y - 1][x + 1]
                    # On the far left side
                    if x <= diff:
                        tile.right = grid[y][x + 2]
                    # On the far right side
                    elif x >= horizontal - diff:
                        tile.left = grid[y][x - 2]
                    else:
                        tile.right = grid[y][x + 2]
                        tile.left = grid[y][x - 2]

                # If the tile is at the far left side, but not top or bottom
                elif x <= diff:
                    tile.right = grid[y][x + 2]
                    tile.top_right = grid[y - 1][x + 1]
                    tile.bottom_right = grid[y + 1][x + 1]
                    # Only include the top_left tile if 
                    # more than halfway down the board
                    if y > len(grid) / 2:
                        tile.top_left = grid[y - 1][x - 1]

                # Tile on the far right side, but not top or bottom
                elif x >= horizontal - diff:
                    tile.left = grid[y][x - 2]
                    tile.top_left = grid[y - 1][x - 1]
                    tile.bottom_left = grid[y + 1][x - 1]
                    # Only include the top_left tile if 
                    # less than halfway down the board
                    if y < floor(len(grid) / 2):
                        tile.bottom_right = grid[y + 1][x + 1]

                else:
                    tile.right = grid[y][x + 2]
                    tile.top_right = grid[y - 1][x + 1]
                    tile.bottom_right = grid[y + 1][x + 1]
                    tile.left = grid[y][x - 2]
                    tile.top_left = grid[y - 1][x - 1]
                    tile.bottom_left = grid[y + 1][x - 1]
                    

                tile.possible_adjacents = tile._check_possible_adjacents()
                self.position_dict[tile.pos] = tile

        return grid


def example():

    catan = CatanIsland(6, 3, {}, {}, {})
    


if __name__ == "__main__":
    example()
