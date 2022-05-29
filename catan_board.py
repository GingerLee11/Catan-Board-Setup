# python3
# catan_board.py - Tile and Catan Board classes. Set up a balanced catan board given proper inputs.

from string import ascii_uppercase
from math import floor
from random import randint
from collections import deque


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
        
        # Position dictionary
        self.position_dict = {}
        
        # inputs
        self.max_width = max_width
        self.min_width = min_width
        self.resources = resource_dict
        self.numbers = numbers_dict
        self.convert_num_to_pts = num_to_pts_dict

        # Reference variables
        self.diff = self.max_width - self.min_width
        self.vertical = self.diff * 2
        self.horizontal = self.max_width + (self.max_width - 1)

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
        
        # Place resources on the board:
        self._place_resources(self.resources)

        return grid

    
    def _place_resources(self, resources_dict):
        """
        Places the resources in a balanced manner on the board
        given a dictionary containing the amount of each resource.

        Rules for a balanced board (from a resource perspective):
        - No more than two resouces of the same kind next to one another.
        """
        resources = [resource for resource in resources_dict.keys()]
        for tile in self.position_dict.values():

            while tile.resource == None:

                resource_indx = randint(0, len(resources) - 1)
                resource = resources[resource_indx]
                if resources_dict[resource] == 0:
                    resources_dict.pop(resource)
                    resources.pop(resource_indx)
                    continue
                else:
                    resources_dict[resource] -= 1

                # Find our how many of that resource is already adjacent
                num_adj = 0
                for adj in tile.possible_adjacents:
                    if adj.resource == resource:
                        num_adj += 1
                
                if num_adj < 2:
                    tile.resource = resource
                else:
                    if resource in resources_dict:
                        resources_dict[resource] += 1
                    else:
                        resources_dict[resource] = 1
                        resources.append(resource)


    def print_resources(self):

        island = self.island

        horizontal_line_segment = '___'
        horizontal_line = horizontal_line_segment * self.horizontal
        print()

        for y in range(len(island)):
            for x in range(len(island[0])):
                tile = island[y][x]
                if tile.resource != None:
                    print(f'| {tile.resource[0]} |', end='')
                else:
                    print(f'  ', end='')
            
            print(f'\n{horizontal_line}')



def example():

    three_four_player_resources = {
        'Brick': 3,
        'Wood': 4,
        'Ore': 3,
        'Grain': 4,
        'Sheep': 4,
        'Desert': 1,
    }

    catan = CatanIsland(5, 3, three_four_player_resources, {}, {})
    catan.print_resources()
    


if __name__ == "__main__":
    example()
