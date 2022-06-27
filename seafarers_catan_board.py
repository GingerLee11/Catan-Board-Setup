# python3
# seafarers_catan_board.py - Creates a Catan board using the seafarers expansion to make several different surrounding islands.

from collections import deque
from math import ceil, floor
from random import randint, shuffle
from string import ascii_uppercase

from catan_board import CatanIsland


class SeafarerIslands(CatanIsland):
    
    def __init__(self, max_width, min_width, 
            resource_dict, main_island_resources, numbers_dict,
            adj_resource_limit=2, main_island_center=False, main_island_dimensions=(5, 3)):
        
        # Constants
        self.letters = list(ascii_uppercase)
        self.number_to_letter = {
            0: 'A',
            1: 'A',
            2: 'B',
            3: 'C',
            4: 'D',
            5: 'E',
            6: 'F',
            7: 'G',
            8: 'H',
            9: 'I',
            10: 'J',
            11: 'K',
            13: 'L',
            14: 'M',
            15: 'N',
            16: 'O',
            17: 'P',
        }
        self.letter_to_number = {
            'A': 0,
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
            'I': 9,
            'J': 10,
            'K': 11,
            'L': 13,
            'M': 14,
            'N': 15,
            'O': 16,
            'P': 17,
        }
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
        # Check for small island that don't use all the numbers
        if len(numbers_dict) < 10:
            self.number_placement_order = deque(numbers_dict.keys())
        else:
            self.number_placement_order = [
                '2',
                '8', 
                '12', 
                '6', 
                '9',
                '5', 
                '4',
                '10',  
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
        
        # inputs
        self.max_width = max_width
        self.min_width = min_width
        self.resources = resource_dict
        self.numbers = numbers_dict

        # Reference variables
        self.diff = self.max_width - self.min_width
        self.vertical = (self.diff * 2) + 1
        self.horizontal = self.max_width + (self.max_width - 1)

        self.island = self._create_island()

        if resource_dict != {}:
            self._place_resources(resource_dict, main_island_resources, 
                adj_resource_limit,
                main_island_center, main_island_dimensions)
        if numbers_dict != {}:
            self._place_numbers_by_resource(numbers_dict)





    def _create_island(self):
        return super()._create_island()


    def _check_adjacents(self, tile, num_adj, resource, checked=None):
        return super()._check_adjacents(tile, num_adj, resource, checked)
    
    def _place_resources(self, resources_dict, main_island_resources, adj_resource_limit=1, 
        main_island_center=False, main_island_dimension=(5, 3), main_island_desert_center=True, 
        num_islands=4, dead_tiles=['Desert', 'Sea', None], sea_letters = set(['A', 'B'])):
        """
        Places the resources in a balanced manner on the board
        given a dictionary containing the amount of each resource.

        Rules for a balanced board (from a resource perspective):
        - No more than two resouces of the same kind next to one another.
        This includes strings of resources.

        main_island_dimensions takes in the maximum width and the minimum width of the main island
        to be generated on the board. main_island_center, if True, places the island in the center of the board.
        Otherwise, the island is generated in the top left corner (the start of the grid).
        """
        ADJ_RESOURCE_LIMIT = adj_resource_limit

        # Initially set the horizontal edges in the middle of the board to sea
        # (Due to how the physical board is setup)
        vert = floor(self.vertical / 2)
        letter = self.letters[vert]
        horz = '0'
        for x in range(2):
            if x == 1:
                horz = self.horizontal - 1
            pos = f"{letter}{horz}"
            if pos in self.position_dict:
                tile = self.position_dict[pos]
                if tile.resource == None:
                    tile.resource = 'Sea'
                    if tile.resource in resources_dict:
                        resources_dict[tile.resource] -= 1
                        if resources_dict[tile.resource] == 0:
                            resources_dict.pop(tile.resource)
                            resources.remove(tile.resource)
        
        # Generate the main island
        mini_catan = CatanIsland(main_island_dimension[0], main_island_dimension[1], main_island_resources, {}, main_island_desert_center, 2)
        main_island = deque([tile for tile in mini_catan.position_dict.values()])

        # Create resources list
        resources = [resource for resource in resources_dict.keys() if resource not in dead_tiles]
        # Create tile queue for big board
        tiles = [tile for tile in self.position_dict.values() if tile.resource == None]
        tiles_queue = deque(tiles)   

        # Place the island in its proper place.
        if main_island_center == True:
            # TODO: Write code to place the island in the center of the board.
            pass
        else:
            main_island_horz = main_island_dimension[1]
            big_board_horz = self.min_width
            i = 0
            k = 0
            while len(main_island) > 0:
                for x in range(main_island_horz):
                    main_island_tile = main_island.popleft()
                    tile = tiles_queue.popleft()
                    # Asign resource
                    tile.resource = main_island_tile.resource

                    # Add the tile to the tiles by resource dictionary
                    if tile.resource != None:
                        if tile.resource not in self.tiles_by_resource:
                            self.tiles_by_resource[tile.resource] = [tile]
                        else:
                            if tile not in self.tiles_by_resource[tile.resource]:
                                self.tiles_by_resource[tile.resource].append(tile)

                    resources_dict[tile.resource] -= 1
                    if resources_dict[tile.resource] == 0:
                        resources_dict.pop(tile.resource)
                if i == mini_catan.diff:
                    k += 1
                else:
                    k = 0
                for y in range((big_board_horz + k) - main_island_horz):
                    non_main_island_tile = tiles_queue.popleft()
                    tiles_queue.append(non_main_island_tile)
                
                # Update how many tiles need to be assigned
                if i < mini_catan.diff:
                    main_island_horz += 1
                else:
                    main_island_horz -= 1
                if i < self.diff:
                    big_board_horz += 1
                else:
                    big_board_horz -= 1
                i += 1

        # Place sea tiles all around the main island to make it an actual island
        for tile in tiles_queue:
            if tile.resource == None:
                for adj in tile.possible_adjacents:
                    if adj.resource not in dead_tiles:
                        tile.resource = 'Sea'
                        if tile.resource in resources_dict:
                            resources_dict[tile.resource] -= 1
                            if resources_dict[tile.resource] == 0:
                                resources_dict.pop(tile.resource)
                        break
        
        sea_tiles = [tile for tile in tiles_queue if tile.resource == 'Sea']
        # Randomize the sea tiles:
        if len(sea_tiles) > 1:
            for x in range(len(sea_tiles)):
                sea_int = randint(0, len(sea_tiles) - 1)
                sea_tiles = sea_tiles[sea_int:] + sea_tiles[:sea_int]
        sea_tiles = deque(sea_tiles)
        tiles_queue = deque(tile for tile in tiles_queue if tile.resource == None)

        # Create sea channels to split up islands
        # If there are three sea channels splitting up the board, 
        # There will be at least four islands.
        count = 0
        i = 0
        sea_numbers = set()
        while count < num_islands - 1:
            
            if len(sea_tiles) > 0:
                sea_tile = sea_tiles.popleft()
            else:
                break
            # Check the direction that the sea tile is facing:
            # If the sea tile is on the north side of the main island, 
            # The sea channel should go up, opposite for south.
            # East and west should go right and left respectively.
            next_tile = None
            tile_flag = None
            # Check for None conditions in all direction
            # Sea tiles on the edge of the map should not be added to anyways
            if (sea_tile.left != None and sea_tile.top_left != None and sea_tile.top_right != None 
                and sea_tile.right != None and sea_tile.bottom_right != None and sea_tile.bottom_left != None
                and (sea_tile.pos[0] not in sea_letters or sea_tile.pos[1:] not in sea_numbers)
                ):
                # Top and bottom of the main island
                if sea_tile.left.resource == 'Sea' and sea_tile.right.resource == 'Sea':
                    # South or bottom of main island
                    if sea_tile.top_left.resource in resources or sea_tile.top_right.resource in resources and (
                        sea_tile.bottom_left.resource == None
                        ):
                        next_tile = sea_tile.bottom_left
                        tile_flag = 'South'
                    # North or top of main island
                    if (sea_tile.bottom_left.resource in resources or sea_tile.bottom_right.resource in resources) and (
                        sea_tile.top_left.resource == None
                        ):
                        next_tile = sea_tile.top_left
                        tile_flag = 'North'
                    
                # Sides of the island
                if (sea_tile.top_left.resource == 'Sea' and sea_tile.bottom_right.resource == 'Sea') or (
                    sea_tile.top_right.resource == 'Sea' and sea_tile.bottom_left.resource == 'Sea'):
                    # East or right of the island
                    if sea_tile.left.resource in resources and sea_tile.right.resource == None:
                        next_tile = sea_tile.right
                        tile_flag = 'East'
                    # West or left of the island
                    if sea_tile.right.resource in resources and sea_tile.left.resource == None:
                        next_tile = sea_tile.left
                        tile_flag = 'West'
                    
                if tile_flag != None:
                # Aggregate count to 
                    count += 1

                    # Add letters and numbers to space out the Sea
                    sea_letter = sea_tile.pos[0]
                    sea_let_indx = self.letter_to_number[sea_letter]
                    sea_number = int(sea_tile.pos[1:])
                    sea_numbers.add(str(sea_number))
                    let_upper = self.number_to_letter[sea_let_indx + 1]
                    let_lower = self.number_to_letter[sea_let_indx - 1]
                    sea_letters.add(sea_letter)
                    sea_letters.add(let_upper)
                    sea_letters.add(let_lower)
                    num_upper = num_lower = sea_number
                    for x in range(4):
                        num_upper += 1
                        sea_numbers.add(str(num_upper))
                        num_lower -= 1
                        sea_numbers.add(str(num_lower))

                # TODO: Add six directions to mimic the hexagonal nature of the board.

                while next_tile != None:
                    if next_tile.resource == None:
                        next_tile.resource = 'Sea'

                    # Change the next tile resource based on the flags
                    if tile_flag == 'South':
                        if i % 2 == 0:
                            next_tile = next_tile.bottom_left
                        else:
                            next_tile = next_tile.bottom_right
                    elif tile_flag == 'North':
                        if i % 2 == 0:
                            next_tile = next_tile.top_left
                        else:
                            next_tile = next_tile.top_right
                    elif tile_flag == 'East':
                        next_tile = next_tile.right
                    elif tile_flag == 'West':
                        next_tile = next_tile.left

                    i += 1
                    # Decrease the resource amount by one
                    # And remove the resource as an option if it's been all used up.
                    resources_dict['Sea'] -= 1
                    if resources_dict['Sea'] == 0:
                        resources_dict.pop('Sea')

        # Instead of randomly assigning resources like in the base game,
        # Creates an island, surrounds it with sea, and repeats until all the land tiles are used up
        # Then fill in the rest of the board with sea tiles until all the tiles are used.
        # Set a max allowable size for an island determined by how many tiles are left available
        adj_count = 0
        i = 0
        while len(resources) > 0:

            # TODO: Right now instead of creating a bunch of islands there
            # is usually one big land mass and a couple small islands
            if i % 2 == 0:
                tile = tiles_queue.popleft()
            else:
                tile = tiles_queue.pop()
            while tile.resource == None:

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
                if num_adj < ADJ_RESOURCE_LIMIT:
                    tile.resource = resource

                    # Add the tile to the tiles by resource dictionary
                    if tile.resource != None:
                        if tile.resource not in self.tiles_by_resource:
                            self.tiles_by_resource[tile.resource] = [tile]
                        else:
                            if tile not in self.tiles_by_resource[tile.resource]:
                                self.tiles_by_resource[tile.resource].append(tile)

                    # Decrease the resource amount by one
                    # And remove the resource as an option if it's been all used up.
                    resources_dict[resource] -= 1
                    if resources_dict[resource] == 0:
                        resources_dict.pop(resource)
                        resources.pop(resource_indx)

                elif adj_count > 5:
                    for adj in tile.possible_adjacents:
                        # This prevents desert from being moved from the center
                        if adj.resource not in dead_tiles:
                            if adj.resource not in resources_dict:
                                resources_dict[adj.resource] = 1
                                resources.append(adj.resource)
                            else:
                                resources_dict[adj.resource] += 1
                            adj.resource = None
                            tiles_queue.append(adj)

                else:
                    adj_count += 1
            i += 1

        while len(tiles_queue) > 0:

            tile = tiles_queue.popleft()

            if tile.resource == None:
                if 'Sea' in resources_dict:
                    tile.resource = 'Sea'

                    # Decrease the resource amount by one
                    # And remove the resource as an option if it's been all used up.
                    resources_dict['Sea'] -= 1
                    if resources_dict['Sea'] == 0:
                        resources_dict.pop('Sea')

    def _check_adjacent_tiles(self, tile, number, resources):
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
                    
        # To prevent one island tiles from getting 1 point numbers            
        if points == 1:
            adj_tile_resources = [adj.resource for adj in tile.possible_adjacents]
            for resource in resources:
                if resource in adj_tile_resources:
                    return True
            return False

        # To prevent low numbers from being placed on small islands
        # Or on the edges of the main island.
        if points <= 2:
            sea_count = 0
            for adj in tile.possible_adjacents:
                if adj.resource == 'Sea':
                    sea_count += 1
            if sea_count >= 3:
                return False

        return True

    def _check_three_tile_sum(self, points, adj_1, adj_2):
        """
        Checks the adjacent tiles around the proposed tile
        and sums the points for all three tiles.
        If the sum is greater than a certain threshold; 12,
        or less than 4, return False
        Otherwise return True
        """
        if adj_1.number == None or adj_2.number == None:
            if points >= 2:
                return True
            elif adj_1.points > 2 or adj_2.points > 2:
                return True
            else:
                return False
        three_tile_sum = 0
        three_tile_sum += points
        # Check if the adj tile is None, 
        # Otherwise it will throw an error
        three_tile_sum += adj_1.points
        three_tile_sum += adj_2.points
        
        # Check if three tile sum is greater than 12 or
        # less than 4
        if three_tile_sum > 12 or three_tile_sum < 4:
            return False
        return True

    # TODO: Write a method for placing numbers on the island resources
    def _place_numbers_by_resource(self, numbers_dict, dead_tiles=['Desert', 'Sea', None]):
        """
        Place numbers by resource on all the tiles on the main island and all the smaller islands.
        """
        # Create a list and then a queue of resources to go through until all the resources
        # Have number tokens on them.
        all_tiles = [tile for tile in self.position_dict.values() if tile.resource not in dead_tiles]
        resources = [resource for resource in self.tiles_by_resource.keys() if resource not in dead_tiles]
        resources_queue = deque(resources)
        numbers_queue = deque(self.number_placement_order)
        
        count = 0

        while len(numbers_queue) != 0:

            count += 1  
            # Once the count reaches a certian threshold,
            # remove all the number and points from the tiles
            if count >= 1000:
                numbers_dict, numbers_queue = self._reset_tile_numbers(all_tiles, numbers_dict, numbers_queue)
                count = 0
                
            # Go through the resources and keep the number until that number is used up
            number = numbers_queue.popleft()
            points = self.num_to_points[number]
            resource = resources_queue.popleft()

            tiles = [tile for tile in reversed(self.tiles_by_resource[resource]) if tile.resource == resource]
            
            shuffle(tiles)
            for tile in tiles:
    
                if tile.number == None:
                    check_adjacents = self._check_adjacent_tiles(tile, number, resources)
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

        # Checks all the tiles to make sure all the tiles meet the three tile sum check
        # If even one tile fails the board is re-generated.
        for tile in all_tiles:

            prev = None
            for adj in tile.possible_adjacents:
                # Checks three tiles at a time
                # so this skips the first iteration
                # which would only check two tiles
                if prev != None:
                    three_tile_sum_check = self._check_three_tile_sum(tile.points, adj, prev)
                    if three_tile_sum_check == False:
                        break
                prev = adj
            # If one of the tile checks is False 
            # start over from scratch
            if three_tile_sum_check == False:
                numbers_dict, numbers_queue = self._reset_tile_numbers(all_tiles, numbers_dict, numbers_queue)
                self._place_numbers_by_resource(numbers_dict)

    
    def print_resources(self):
        """
        Prints where the resources are on the islands.
        """

        island = self.island

        horizontal_line_segment = '____'
        horizontal_line = horizontal_line_segment * self.horizontal
        print()

        for y in range(len(island)):
            for x in range(len(island[0])):
                tile = island[y][x]
                if tile.resource != None:
                    print(f'| {tile.resource[:2]} |', end='')
                else:
                    print(f'  ', end='')
            
            print(f'\n{horizontal_line}')

    def print_numbers(self):
        """
        Prints where the numbers are on the island.
        """

        island = self.island

        horizontal_line_segment = '____'
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


def example():

    # Test with a 9 max, 5 min board
    # No desert tiles on the small islands, 
    # desert tiles flipped over to provide more sea tiles
    extension_and_seafarers_resources = {
            'Brick': 7,
            'Wood': 7,
            'Ore': 7,
            'Grain': 7,
            'Sheep': 7,
            'Gold': 2,
            'Desert': 1,
            'Sea': 23,
        }
    extension_and_seafarers_numbers = {
        '2': 3, 
        '3': 4, 
        '4': 4, 
        '5': 4, 
        '6': 4, 
        '8': 4, 
        '9': 4, 
        '10': 4, 
        '11': 4, 
        '12': 2, 
    }
    three_four_player_resources = {
            'Brick': 3,
            'Wood': 4,
            'Ore': 3,
            'Grain': 4,
            'Sheep': 4,
            'Desert': 1,
        }


    board = SeafarerIslands(9, 5, extension_and_seafarers_resources, three_four_player_resources, 
    extension_and_seafarers_numbers, 1, False, (5, 3))
    board.print_resources()
    board.print_numbers()


if __name__ == "__main__":
    example()
