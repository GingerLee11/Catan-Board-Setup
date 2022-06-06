# python3
# catan_board.py - Tile and Catan Board classes. Set up a balanced catan board given proper inputs.

from string import ascii_uppercase
from math import floor
from random import randint, shuffle
from collections import deque

import unittest


class Tile:
    """
    Tile class from which the Catan Board is created.
    This is a hexagonal tile, with the positional relationships defined as:
    right, top_right, top_left, left, bottom_left, bottom_right
    """

    def __init__(self, x, y, position, number=None, point_value=0, resource=None):
        # Positional inputs:
        self.x = x
        self.y = y
        self.pos = position

        # Catan Inputs
        self.number = number
        self.points = point_value
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
    
    def __init__(self, max_width, min_width, resource_dict, numbers_dict):
        # Constants
        self.letters = list(ascii_uppercase)
        self.num_to_points = {
            '2': 1, 
            '3': 2, 
            '4': 3, 
            '5': 4, 
            '6': 5, 
            '8': 5, 
            '9': 4, 
            '10': 3, 
            '11': 2, 
            '12': 1, 
        }
        self.number_placement_order = [
            '8', 
            '6', 
            '9',
            '12',
            '2', 
            '5', 
            '10', 
            '4', 
            '11', 
            '3', 
            
              
        ]
        
        # Tile Information:
        self.position_dict = {}
        self.tiles_by_resource = {}
        self.total_points_per_resource = {}
        self.resource_numbers = {}
        self.resource_points = {}
        self.resources_dict = resource_dict
        self.numbers_dict = numbers_dict

        # TODO: Create resource point dict
        # In order to find the resource with the current lowest point total
        
        # inputs
        self.max_width = max_width
        self.min_width = min_width
        self.resources = resource_dict
        self.numbers = numbers_dict


        # Reference variables
        self.diff = self.max_width - self.min_width
        self.vertical = (self.diff * 2) + 1
        self.horizontal = self.max_width + (self.max_width - 1)

        # Create the island:
        self.island = self._create_island()
        # For testing:
        if resource_dict != {}:
            self._place_resources(resource_dict)
        if numbers_dict != {}:
            self._place_numbers_by_resource(numbers_dict)


    def _create_grid(self, max_width, min_width):
        """
        Creates the grid based on the max and min width supplied
        """
        letters = self.letters
        grid = []
        diff = max_width - min_width
        vertical = self.vertical
        horizontal = max_width + (max_width - 1)
        for y in range(vertical):
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
        vertical = self.vertical
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
                    elif x >= (horizontal - 1) - diff:
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
                    elif x >= (horizontal - 1) - diff:
                        tile.left = grid[y][x - 2]
                    else:
                        tile.right = grid[y][x + 2]
                        tile.left = grid[y][x - 2]

                # If the tile is in the middle row of the island
                elif y == floor(len(grid) / 2):
                    if x == 0:
                        tile.right = grid[y][x + 2]
                        tile.top_right = grid[y - 1][x + 1]
                        tile.bottom_right = grid[y + 1][x + 1]
                    elif x == (horizontal - 1):
                        tile.left = grid[y][x - 2]
                        tile.top_left = grid[y - 1][x - 1]
                        tile.bottom_left = grid[y + 1][x - 1]
                    else:
                        tile.right = grid[y][x + 2]
                        tile.top_right = grid[y - 1][x + 1]
                        tile.bottom_right = grid[y + 1][x + 1]
                        tile.left = grid[y][x - 2]
                        tile.top_left = grid[y - 1][x - 1]
                        tile.bottom_left = grid[y + 1][x - 1]


                # If the tile is at the far left side, but not top or bottom or middle
                elif x < diff:
                    tile.right = grid[y][x + 2]
                    tile.top_right = grid[y - 1][x + 1]
                    tile.bottom_right = grid[y + 1][x + 1]
                    # Only include the top_left tile if 
                    # more than halfway down the board
                    if y > floor(len(grid) / 2):
                        tile.top_left = grid[y - 1][x - 1]
                    elif y < floor(len(grid) / 2):
                        tile.bottom_left = grid[y + 1][x - 1]

                # Tile on the far right side, but not top or bottom or middle
                elif x > (horizontal - 1) - diff:
                    tile.left = grid[y][x - 2]
                    tile.top_left = grid[y - 1][x - 1]
                    tile.bottom_left = grid[y + 1][x - 1]
                    # Only include the top_left tile if 
                    # less than halfway down the board
                    if y < floor(len(grid) / 2):
                        tile.bottom_right = grid[y + 1][x + 1]
                    elif y > floor(len(grid) / 2):
                        tile.top_right = grid[y - 1][x + 1]
                    

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

    def _check_adjacents(self, tile, num_adj, resource, checked=None):
        """
        Checks for adjacent tiles of the same resource type as the 
        given resource type
        """
        for adj in tile.possible_adjacents:
            if adj.resource == resource:
                if adj not in checked:
                    num_adj += 1
                    checked.append(adj)
                    self._check_adjacents(adj, num_adj, resource, checked)

        return num_adj
    
    def _place_resources(self, resources_dict, desert_center=True):
        """
        Places the resources in a balanced manner on the board
        given a dictionary containing the amount of each resource.

        Rules for a balanced board (from a resource perspective):
        - No more than two resouces of the same kind next to one another.
        This includes strings of resources.
        """
        # TODO: Add a queue or something here to prevent infinite loops

        resources = [resource for resource in resources_dict.keys()]

        # Place desert in the center of the island unless otherwise specified
        if desert_center == True:
            vert = floor(self.vertical / 2)
            letter = self.letters[vert]
            horz = floor(self.horizontal / 2)
            pos = f"{letter}{horz}"
            tile = self.position_dict[pos]
            tile.resource = 'Desert'
            if tile.resource in resources_dict:
                resources_dict[tile.resource] -= 1
                if resources_dict[tile.resource] == 0:
                    resources_dict.pop(tile.resource)
                    resources.remove(tile.resource)


        tiles = [tile for tile in self.position_dict.values() if tile.resource != 'Desert']
        tiles_queue = deque(tiles)   

        while len(tiles_queue) > 0:

            tile = tiles_queue.popleft()
            count = 0
            adj_count = 0
            while tile.resource == None:

                if count > 3:
                    tiles_queue.append(tile)
                    break
                count += 1
                
                # Randomly select a resource from the list
                resource_indx = randint(0, len(resources) - 1)
                resource = resources[resource_indx]

                # Find our how many of that resource is already adjacent
                num_adj = 0
                checked = []
                for adj in tile.possible_adjacents:
                    if adj.resource == resource:
                        if adj not in checked:
                            num_adj += 1
                            checked.append(adj)
                            # Check that adj tiles to see if it also has 
                            # An adjacent resource of the same type
                            num_adj = self._check_adjacents(adj, num_adj, resource, checked)
                        
                # If the check is met then decrease the number of that resource by one
                if num_adj < 2:
                    tile.resource = resource
                    
                    # TODO: Find out why other resources are being added to the 
                    # different resources
                    # i.e. grain in sheep and vice versa. 
                    # WHYYYYYYYYYYY????????? WTH!

                    # Add the tile to the tiles by resource dictionary
                    if tile.resource != None and resource != 'Desert' and tile.resource != 'Desert':
                        if resource not in self.tiles_by_resource:
                            self.tiles_by_resource[resource] = [tile]
                        else:
                            if tile not in self.tiles_by_resource[resource] and tile.resource == resource:
                                self.tiles_by_resource[resource].append(tile)

                    resources_dict[resource] -= 1
                    if resources_dict[resource] == 0:
                        resources_dict.pop(resource)
                        resources.pop(resource_indx)

                elif adj_count > 2:
                    for adj in tile.possible_adjacents:
                        if adj.resource not in resources_dict:
                            resources_dict[adj.resource] = 1
                            resources.append(adj.resource)
                        else:
                            resources_dict[adj.resource] += 1
                        adj.resource = None
                        tiles_queue.append(adj)

                else:
                    adj_count += 1

    def _check_adjacent_tiles(self, tile, number):
        """
        Checks adjacent tiles for the proposed tile 
        to check if any of the surrounding numbers are the same. 
        Or if 5 or 1 point tiles are adjacent to one another
        """
        points = self.num_to_points[number]

        for adj in tile.possible_adjacents:
            # If any of the adjacent numbers have the same number, 
            # return False
            if adj.number == number:
                return False

            if points == 5 or points == 1:
                if adj.points == points:
                    return False
        
        return True


    def _place_numbers_by_resource(self, numbers_dict):
        """
        Places the numbers in order from 5 point tokens to
        1 point tokens.
        Randomize which order the resources are chosen in to make 
        so that the board isn't the same everytime.
        """
        # Create a list and then a queue of resources to go through until all the resources
        # Have number tokens on them.
        all_tiles = [tile for tile in self.position_dict.values() if tile.resource != 'Desert']
        resources = [resource for resource in self.tiles_by_resource.keys()]
        resources_queue = deque(resources)
        numbers_queue = deque(self.number_placement_order)
        
        count = 0

        while len(numbers_queue) != 0:

            count += 1
            
            # Once the count reaches a certian threshold,
            # remove all the number and points from the tiles
            if count >= 100:
            
                for tile in all_tiles:
                    if tile.number != None:
                        if tile.number not in numbers_queue:
                            numbers_queue.append(tile.number)
                        if tile.number not in numbers_dict:
                            numbers_dict[tile.number] = 1
                        else:
                            numbers_dict[tile.number] += 1

                    tile.number = None
                    tile.points = 0
                count = 0
                

            # Go through the resources and keep the number until that number is used up
            number = numbers_queue.popleft()
            points = self.num_to_points[number]
            resource = resources_queue.popleft()

            tiles = [tile for tile in reversed(self.tiles_by_resource[resource]) if tile.resource == resource]
            
            shuffle(tiles)
            for tile in tiles:
    
                # TODO: Add checks for balancing
                # Iterate through the tiles until a tile that meets the criteria is met
                if tile.number == None:
                    check_adjacents = self._check_adjacent_tiles(tile, number)
                    if check_adjacents == True:
                        tile.number = number
                        tile.points = points

                        numbers_dict[number] -= 1
                        if numbers_dict[number] == 0:
                            numbers_dict.pop(number)
                        else:
                            numbers_queue.appendleft(number)   
                        break

            if number in numbers_dict and number not in numbers_queue:
                numbers_queue.appendleft(number) 
            resources_queue.append(resource) 


    def print_resources(self):
        """
        Prints where the resources are on the island.
        """

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


    def print_numbers(self):
        """
        Prints where the numbers are on the island.
        """

        island = self.island

        horizontal_line_segment = '___'
        horizontal_line = horizontal_line_segment * self.horizontal
        print()
        for resource, point_list in self.resource_points.items():
            print(f"{resource}: {sum(point_list)}", end=' ')
        print()

        for y in range(len(island)):
            for x in range(len(island[0])):
                tile = island[y][x]
                if tile.number != None:
                    print(f'| {tile.number} |', end='')
                else:
                    print(f'  ', end='')
            
            print(f'\n{horizontal_line}')


    def print_resources_by_tile(self):

        for resource, tiles in self.tiles_by_resource.items():
            tile_resources = [tile.resource for tile in tiles]
            tile_positions = [tile.pos for tile in tiles]

            print(f"{resource}: {tile_resources} @ {tile_positions}")
    
    def tiles(self):
        """
        Prints the position of all the tiles
        """
        tiles = [tile for tile in self.position_dict.values()]
        return tiles

    def calculate_points_per_resource(self):
        """
        Calculates how many points are allocated to each resource.
        (For determining how balanced the board is.)
        """
        tiles = [tile for tile in self.position_dict.values() if tile.resource != 'Desert']
        tppr = self.total_points_per_resource
        for tile in tiles:

            # Add up the total points to see how balanced the board is
            if tile.resource in tppr:
                tppr[tile.resource] += tile.points
            else:
                tppr[tile.resource] = tile.points

        return tppr

        



def generate_island():
    for x in range(100):
        three_four_player_resources = {
            'Brick': 3,
            'Wood': 4,
            'Ore': 3,
            'Grain': 4,
            'Sheep': 4,
            'Desert': 1,
        }
        three_four_player_numbers = {
            '2': 1, 
            '3': 2, 
            '4': 2, 
            '5': 2, 
            '6': 2, 
            '8': 2, 
            '9': 2, 
            '10': 2, 
            '11': 2, 
            '12': 1, 
        }
        
        catan = CatanIsland(5, 3, three_four_player_resources, three_four_player_numbers)
        # Only print the resources and the numbers if the game is balanced
        game_balance = catan.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)
        if total_diff < 3:

            catan.print_resources()
            catan.print_numbers()
        # catan.print_resources_by_tile()
    



class Test(unittest.TestCase):

    # Test the grid to make sure that all the relationships between tiles are correctly defined.
    # Relationships for 5, 3 (three to four player island)

    tests = [
        (5, 3),
        (3, 2),
    ]
    
    left_expected = [None, 'A2', 'A4', None, 'B1', 'B3', 'B5', None, 'C0', 'C2', 'C4', 'C6', None, 'D1', 'D3', 'D5', None, 'E2', 'E4']
    right_expected = ['A4', 'A6', None, 'B3', 'B5', 'B7', None, 'C2', 'C4', 'C6', 'C8', None, 'D3', 'D5', 'D7', None, 'E4', 'E6', None]
    top_left_expected = [None, None, None, None, 'A2', 'A4', 'A6', None, 'B1', 'B3', 'B5', 'B7', 'C0', 'C2', 'C4', 'C6', 'D1', 'D3', 'D5']
    top_right_expected = [None, None, None, 'A2', 'A4', 'A6', None, 'B1', 'B3', 'B5', 'B7', None, 'C2', 'C4', 'C6', 'C8', 'D3', 'D5', 'D7']
    bottom_left_expected = ['B1', 'B3', 'B5', 'C0', 'C2', 'C4', 'C6', None, 'D1', 'D3', 'D5', 'D7', None, 'E2', 'E4', 'E6', None, None, None]
    bottom_right_expected = ['B3', 'B5', 'B7', 'C2', 'C4', 'C6', 'C8', 'D1', 'D3', 'D5', 'D7', None, 'E2', 'E4', 'E6', None, None, None, None]

    three_four_player_test = [left_expected, right_expected, top_left_expected, top_right_expected, bottom_left_expected, bottom_right_expected]

    l_exp = [None, 'A1', None, 'B0', 'B2', None, 'C1']
    r_exp = ['A3', None, 'B2', 'B4', None, 'C3', None]
    t_l_exp = [None, None, None, 'A1', 'A3', 'B0', 'B2']
    t_r_exp = [None, None, 'A1', 'A3', None, 'B2', 'B4']
    b_l_exp = ['B0', 'B2', None, 'C1', 'C3', None, None]
    b_r_exp = ['B2', 'B4', 'C1', 'C3', None, None, None]

    small_test_island = [l_exp, r_exp, t_l_exp, t_r_exp, b_l_exp, b_r_exp]

    l_exp = [None, 'A3', 'A5', None, 'B2', 'B4', 'B6', None, 'C1', 'C3', 'C5', 'C7', None, 'D0', 'D2', 'D4', 'D6', 'D8', None, 'E1', 'E3', 'E5', 'E7', None, 'F2', 'F4', 'F6', None, 'G3', 'G5' ]
    r_exp = ['A5', 'A7', None, 'B4', 'B6', 'B8', None, 'C3', 'C5', 'C7', 'C9', None, 'D2', 'D4', 'D6', 'D8', 'D10', None, 'E3', 'E5', 'E7', 'E9', None, 'F4', 'F6', 'F8', None, 'G5', 'G7', None]
    t_l_exp = [None, None, None, None, 'A3', 'A5', 'A7', None, 'B2', 'B4', 'B6', 'B8', None, 'C1', 'C3', 'C5', 'C7', 'C9', 'D0', 'D2', 'D4', 'D6', 'D8', 'E1', 'E3', 'E5', 'E7', 'F2', 'F4', 'F6']
    t_r_exp = [None, None, None, 'A3', 'A5', 'A7', None, 'B2', 'B4', 'B6', 'B8', None, 'C1', 'C3', 'C5', 'C7', 'C9', None, 'D2', 'D4', 'D6', 'D8', 'D10', 'E3', 'E5', 'E7', 'E9', 'F4', 'F6', 'F8']
    b_l_exp = ['B2', 'B4', 'B6', 'C1', 'C3', 'C5', 'C7', 'D0', 'D2', 'D4', 'D6', 'D8', None, 'E1', 'E3', 'E5', 'E7', 'E9', None, 'F2', 'F4', 'F6', 'F8', None, 'G3', 'G5', 'G7', None, None, None]
    b_r_exp = ['B4', 'B6', 'B8', 'C3', 'C5', 'C7', 'C9', 'D2', 'D4', 'D6', 'D8', 'D10', 'E1', 'E3', 'E5', 'E7', 'E9', None, 'F2', 'F4', 'F6', 'F8', None, 'G3', 'G5', 'G7', None, None, None, None]

    five_six_player_test = [l_exp, r_exp, t_l_exp, t_r_exp, b_l_exp, b_r_exp]

    tests = [
        (5, 3, three_four_player_test), 
        (3, 2, small_test_island),
        (6, 3, five_six_player_test),
    ]

    def generate_catan_board(self, max_width, min_width):
        catan_island = CatanIsland(max_width, min_width, {}, {})
        actual_tiles = catan_island.tiles()
        return actual_tiles


    def test_catan_island_grid(self):
        for max_w, min_w, expected in self.tests:
            actual_tiles = self.generate_catan_board(max_w, min_w)

            # test relationships
            for actual, left, right, top_left, top_right, bottom_left, bottom_right in zip(actual_tiles, expected[0], expected[1], 
            expected[2], expected[3], expected[4], expected[5]):
                
                # print(actual.pos)

                if actual.left != None:
                    assert actual.left.pos == left
                else:
                    assert actual.left == left

                if actual.right != None:
                    assert actual.right.pos == right
                else:
                    assert actual.right == right

                if actual.top_left != None:
                    assert actual.top_left.pos == top_left
                else:
                    assert actual.top_left == top_left

                if actual.top_right != None:
                    assert actual.top_right.pos == top_right
                else:
                    assert actual.top_right == top_right

                if actual.bottom_left != None:
                    assert actual.bottom_left.pos == bottom_left
                else:
                    assert actual.bottom_left == bottom_left

                if actual.bottom_right != None:
                    assert actual.bottom_right.pos == bottom_right
                else:
                    assert actual.bottom_right == bottom_right


if __name__ == "__main__":
    generate_island()
