# python3
# catan_board.py - Tile and Catan Board classes. Set up a balanced catan board given proper inputs.

from calendar import c
from pickle import PickleBuffer
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
        self._place_resources(resource_dict)
        self._place_numbers_2(numbers_dict)


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
                    elif x >= (horizontal - 1) - diff:
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


        tiles = [tile for tile in self.position_dict.values()]
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


    def _check_three_tile_sum(self, points, adj_tile_1, adj_tile_2):
        """
        Sum the point values of the three tiles to see if
        the sum exceeds 12 or is less than 3.
        """
        sum_check = False
        three_tile_sum = 0
        three_tile_sum += points

        if adj_tile_1.number == None and adj_tile_2 == None:
            if points > 1:
                sum_check = True
                return sum_check


        three_tile_sum += adj_tile_1.points
        three_tile_sum += adj_tile_2.points

        if three_tile_sum >= 3 and three_tile_sum <= 12:
            sum_check = True
        

        return sum_check

    def _reset_tile_numbers_and_points(self, tile):
        """
        Resets a tile back to just having a resource.
        """
        self.resource_numbers[tile.resource].remove(tile.number)
        self.resource_points[tile.resource].remove(tile.points)
        self.total_points_per_resource[tile.resource] -= tile.points

        tile.number = None
        tile.points = 0

        return tile

    def _place_numbers_2(self, numbers_dict):
        """
        Simple method of placing numbers:
        Randomly places a number in each tile
        """

        numbers = [number for number in numbers_dict.keys()]
        convert_to_points = self.num_to_points

        for tile in self.position_dict.values():

            # Selects a number from the remaining available numbers
            number_indx = randint(0, len(numbers) - 1)
            number = numbers[number_indx]

            # Gives how many points the number is equivalent to
            points = convert_to_points[number]

            if tile.resource != 'Desert':
                tile.number = number
                tile.points = points

                # If all checks are passed update all the resource, number and points information
                # Update the numbers_dict
                numbers_dict[number] -= 1
                if numbers_dict[number] == 0:
                    numbers_dict.pop(number)
                    numbers.pop(number_indx)
                
        self._check_adjacent_numbers()
        self._check_resource_number_balance()

    def _check_adjacent_numbers(self):
        """
        Makes sure that there are not any adjacent tiles with the same numbers. 
        """

        # Create a queue for the tiles
        tiles = [tile for tile in self.position_dict.values() if tile.resource != 'Desert']
        tiles_queue = deque(tiles)
        count = 0
        while len(tiles_queue) > 0:

            # TODO: Implement a failsafe to prevent
            # infinite loops
            if count > 100:
                self._place_resources(self.resources_dict)

            tile = tiles_queue.popleft()
            count += 1
            
            # Check to see if any adjacent numbers are the same
            for adj in tile.possible_adjacents:
                # If the numbers are the same, 
                # switch the number of the adjacent tile (b)
                # with an adjacent tile (c) of that tile b
                # that does not equal the number of the tile
                if tile.number == adj.number:
                    if tile not in tiles_queue:
                        tiles_queue.append(tile)
                    if adj not in tiles_queue:
                        tiles_queue.append(adj)
                    for adj_adj in adj.possible_adjacents:
                        if adj_adj.number != None:
                            if adj_adj.number != tile.number:
                                # Swap the numbers and the points
                                adj_number = adj.number
                                adj_points = adj.points
                                adj.number = adj_adj.number
                                adj.points = adj_adj.points
                                adj_adj.number = adj_number
                                adj_adj.points = adj_points
                                if adj_adj not in tiles_queue:
                                        tiles_queue.append(adj_adj)
                                break

                # Check to see if there are adjacent 1 or 5 point number tokens
                # And if there are move the tokens
                if tile.points == 5 or tile.points == 1:
                    if tile.points == adj.points:
                        if tile not in tiles_queue:
                            tiles_queue.append(tile)
                        if adj not in tiles_queue:
                            tiles_queue.append(adj)
                        for adj_adj in adj.possible_adjacents:
                            if adj_adj.number != None:
                                if adj_adj.points != tile.points:
                                # Swap the numbers and the points
                                    adj_number = adj.number
                                    adj_points = adj.points
                                    adj.number = adj_adj.number
                                    adj.points = adj_adj.points
                                    adj_adj.number = adj_number
                                    adj_adj.points = adj_points
                                    if adj_adj not in tiles_queue:
                                        tiles_queue.append(adj_adj)
                                    break

        return True

    def _check_resource_number_balance(self):
        """
        Checks to make sure that the numbers are balanced for each of the resources
        """
        for tile in self.position_dict.values():

            if tile.resource in self.tiles_by_resource:
                self.tiles_by_resource[tile.resource].append(tile)
            else: 
                self.tiles_by_resource[tile.resource] = tile
            
            if tile.resource in self.total_points_per_resource:
                self.total_points_per_resource[tile.resource] += tile.points
            else:
                self.total_points_per_resource[tile.resource] = tile.points

        return self.tiles_by_resource



    '''
    def _place_numbers(self, numbers_dict):
        """
        Places the resources in such a way to make the layout as balanced as possible.
        numbers is a dictionary containing the numbers used in the game and quantity of those numbers.
        num_to_pt_dict converts the numbers to the appropriate point value:
        8, 6: 5 pts
        9, 5: 4 pts
        10, 4: 3 pts
        11, 3: 2 pts
        12, 2: 1 pt

        Places numbers on the resource tile based on the following rules:
        No adjacent red tiles (5pt tiles)
        No adj 2's or 12's (1pt tiles)
        3 tile sum: 3 <= three_tile_sum <= 12
        no adj tiles with same numbers
        Balances the number distribution by resource
        """
        convert_to_points = self.num_to_points

        # Create a queue for the tiles
        tiles = [tile for tile in self.position_dict.values()]
        tiles_queue = deque(tiles)

        # Create a list of the numbers
        numbers = [number for number in numbers_dict.keys()]
        # Go through all the tiles until they all have numbers 
        # Except for the desert tiles
        while len(tiles_queue) > 0:
            tile = tiles_queue.popleft()
            if tile.resource != 'Desert':
                count = 0
                while tile.number == None:
                    # If count exceed the half the original length of the 
                    if count > 3:
                        tiles_queue.append(tile)
                        break
                        

                    # Selects a number from the remaining available numbers
                    number_indx = randint(0, len(numbers) - 1)
                    number = numbers[number_indx]

                    # Gives how many points the number is equivalent to
                    points = convert_to_points[number]

                    # No same numbers for the same resource
                    # (This may not work for bigger islands)
                    if tile.resource in self.resource_numbers:
                        if number in self.resource_numbers[tile.resource]: 
                            continue
                        
                    # Check to make sure no resource is assigned more than a single 1 point token
                    # Also ensure that the resource with a 1 pt token already has a 5 point token
                    if points == 1:
                        if tile.resource in self.resource_points:
                            if points in self.resource_points[tile.resource]:
                                continue
                            # elif 5 not in self.resource_points[tile.resource]:
                            #    continue

                    # Check that no resource has a second 5 point token before all other 
                    # resources already have a 5 point token
                    if points == 5:
                        tppr_dict = self.total_points_per_resource
                        if tile.resource in self.resource_points: # This might not be the check I want
                            if points in self.resource_points[tile.resource]:
                                has_points = 0
                                total_resources = len(self.resource_points) - 1
                                for p_resource in self.resource_points.keys():
                                    if points in self.resource_points[p_resource]:
                                        has_points += 1
                                if total_resources < 2 or has_points < total_resources:
                                    # Reset the tile from the resource with the most points
                                    max_resource = max(tppr_dict, key=tppr_dict.get)
                                    if points in self.resource_points[max_resource]:
                                        for max_tile in self.tiles_by_resource[max_resource]:
                                            if points == max_tile.points:
                                                if max_tile.number not in numbers_dict:
                                                    numbers_dict[max_tile.number] = 1
                                                    numbers.append(max_tile.number)
                                                else: 
                                                    numbers_dict[max_tile.number] += 1
                                                    max_tile = self._reset_tile_numbers_and_points(max_tile)
                                                    tiles_queue.append(max_tile)
                                                    break
                                    

                            # min_points = tppr_dict[min(tppr_dict, key=tppr_dict.get)]
                            # if tppr_dict[tile.resource] != min_points:
                            #     continue
                            # if len(tppr_dict) < 2:
                            #     continue

                    # Perform checks:
                    # Check for same adjacent numbers
                    same_num_adj = False
                    adj_1_or_5_point_tile = False
                    for adj in tile.possible_adjacents:
                        if adj.number == number:
                            same_num_adj = True
                            # Add the number back to the numbers dict
                            # and clear the tile
                            if adj.number not in numbers_dict:
                                numbers_dict[adj.number] = 1
                                numbers.append(adj.number)
                            else: 
                                numbers_dict[adj.number] += 1
                                adj_tile = self._reset_tile_numbers_and_points(adj)
                                tiles_queue.append(adj_tile)
                            break

                    for adj in tile.possible_adjacents:
                        if points == 1 or points == 5:
                            if adj.points == points:
                                adj_1_or_5_point_tile = True
                                # Add the number back to the numbers dict
                                # and clear the tile
                                if adj.number not in numbers_dict:
                                    numbers_dict[adj.number] = 1
                                    numbers.append(adj.number)
                                else: 
                                    numbers_dict[adj.number] += 1
                                    adj_tile = self._reset_tile_numbers_and_points(adj)
                                    tiles_queue.append(adj_tile)
                                break
                    
                    # If either of the conditions were true, 
                    # pick another remaining number and try again
                    if same_num_adj or adj_1_or_5_point_tile:
                        continue

                    # Three tile sum check: 
                    # Ensure that no settlement spot has an adjacency of more than 12 or less than 3
                    adj_tiles = tile.possible_adjacents
                    # Check to see if this tile is on the edge of the island
                    # If it is then the points value should not be 1
                    if len(adj_tiles) <= 3:
                        if points == 1:
                            continue

                    prev = None
                    for adj in adj_tiles:
                        if prev != None:
                            sum_check = self._check_three_tile_sum(points, prev, adj)
                            if sum_check == False:
                                # Remove adj tile
                                if adj.resource != 'Desert' and adj.number != None:
                                    if adj.number not in numbers_dict:
                                        numbers_dict[adj.number] = 1
                                        numbers.append(adj.number)
                                    else: 
                                        numbers_dict[adj.number] += 1
                                        adj_tile = self._reset_tile_numbers_and_points(adj)
                                        tiles_queue.append(adj_tile)
                                # Remove prev tile
                                if prev.resource != 'Desert' and prev.number != None:
                                    if prev.number not in numbers_dict:
                                        numbers_dict[prev.number] = 1
                                        numbers.append(prev.number)
                                    else: 
                                        numbers_dict[prev.number] += 1
                                        prev_tile = self._reset_tile_numbers_and_points(prev)
                                        tiles_queue.append(prev_tile)

                                break
                        prev = adj

                    # If either of the condition is False, 
                    # pick another remaining number and try again
                    if sum_check == False:
                        continue
                
                    # If all checks are passed update all the resource, number and points information
                    # Update the numbers_dict
                    numbers_dict[number] -= 1
                    if numbers_dict[number] == 0:
                        numbers_dict.pop(number)
                        numbers.pop(number_indx)

                    # Update the numbers for each resource
                    if tile.resource in self.resource_numbers:
                        self.resource_numbers[tile.resource].append(number)
                    else:
                        self.resource_numbers[tile.resource] = [number]

                    # Add the points token to the resource_points dict for tracking
                    if tile.resource in self.resource_points:
                        self.resource_points[tile.resource].append(points)
                    else:
                        self.resource_points[tile.resource] = [points]

                    # Update the total points for that resource
                    if tile.resource in self.total_points_per_resource:
                        self.total_points_per_resource[tile.resource] += points
                    else:
                        self.total_points_per_resource[tile.resource] = points

                    # Add the points and the number to the tile
                    tile.number = number
                    tile.points = points

                    # Add the resource to the tile_by_resource dictionary
                    if tile.resource not in self.tiles_by_resource:
                        self.tiles_by_resource[tile.resource] = [tile]
                    else:
                        self.tiles_by_resource[tile.resource].append(tile)
'''
                    


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

        for y in range(len(island)):
            for x in range(len(island[0])):
                tile = island[y][x]
                if tile.number != None:
                    print(f'| {tile.number} |', end='')
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
    catan.print_resources()
    catan.print_numbers()



if __name__ == "__main__":
    example()
