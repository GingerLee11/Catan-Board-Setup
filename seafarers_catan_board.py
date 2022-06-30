# python3
# seafarers_catan_board.py - Creates a Catan board using the seafarers expansion to make several different surrounding islands.

from collections import deque
from math import ceil, floor
from random import randint, shuffle
from string import ascii_uppercase

from catan_board import CatanIsland


class SeafarerIslands(CatanIsland):
    
    def __init__(self, max_width, min_width, 
            resource_dict, main_island_resources, main_island_numbers_dict, small_islands_numbers_dict, 
            adj_resource_limit=2, main_island_center=False, main_island_dimensions=(5, 3), main_island_desert_center=True):
        
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
        if len(small_islands_numbers_dict) < 10:
            self.small_islands_number_placement_order = deque(small_islands_numbers_dict.keys())
        else:
            self.small_islands_number_placement_order = [
                '8', 
                '12', 
                '2',
                '9',
                '5', 
                '4',
                '6', 
                '10',  
                '11', 
                '3',          
            ]
        if len(main_island_numbers_dict) < 10:
            self.main_island_number_placement_order = deque(main_island_numbers_dict.keys())
        else:
            self.main_island_number_placement_order = [
                '8', 
                '12', 
                '2',
                '9',
                '5', 
                '4',
                '6', 
                '10',  
                '11', 
                '3',          
            ]
        
        # Tile Information:
        self.position_dict = {}
        self.main_island_position_dict = {}
        self.main_island_tiles_by_resource = {}
        self.small_islands_position_dict = {}
        self.small_islands_tiles_by_resource = {}
        self.total_points_per_resource = {}
        self.resource_numbers = {}
        self.resource_points = {}
        self.resources_dict = resource_dict
        self.main_island_numbers_dict = main_island_numbers_dict
        
        # inputs
        self.max_width = max_width
        self.min_width = min_width
        self.resources = resource_dict
        self.main_island_numbers = main_island_numbers_dict
        self.small_island_numbers_dict = small_islands_numbers_dict

        # Reference variables
        self.diff = self.max_width - self.min_width
        self.vertical = (self.diff * 2) + 1
        self.horizontal = self.max_width + (self.max_width - 1)
        self.dead_tiles = ['Desert', 'Sea', None]

        self.island = self._create_island()

        if resource_dict != {}:
            self._place_resources(resource_dict, main_island_resources, 
                adj_resource_limit,
                main_island_center, main_island_dimensions, main_island_desert_center)
        if main_island_numbers_dict != {} and small_islands_numbers_dict != {}:
            self._place_numbers_by_resource_main_island(main_island_numbers_dict)
            self._place_numbers_by_resource_smaller_islands(small_islands_numbers_dict)

    def _create_island(self):
        return super()._create_island()


    def _check_adjacents(self, tile, num_adj, resource, checked=None):
        return super()._check_adjacents(tile, num_adj, resource, checked)

    def _reset_tile_resources(self, tiles, resource_dict):
        """
        Resets the tiles back to before resources were placed
        """
        for tile in tiles:
            if tile.resource != None:
                if tile.resource not in resource_dict:
                    resource_dict[tile.resource] = 1
                else:
                    resource_dict[tile.resource] += 1
            tile.resource = None
        return resource_dict

    def _place_resources(self, resources_dict, main_island_resources, adj_resource_limit=1, 
        main_island_center=False, main_island_dimension=(5, 3), main_island_desert_center=True, 
        num_islands=4, dead_tiles=['Desert', 'Sea', None]):
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
        mini_catan = CatanIsland(main_island_dimension[0], main_island_dimension[1], main_island_resources, {}, main_island_desert_center, 1)
        main_island = deque([tile for tile in mini_catan.position_dict.values()])

        # Create resources list
        resources = [resource for resource in resources_dict.keys() if resource not in dead_tiles]
        # Create tile queue for big board
        tiles = [tile for tile in self.position_dict.values() if tile.resource == None]
        tiles_queue = deque(tiles)   

        # Place the island in its proper place.
        if main_island_center == True:
            # TODO: Write code to place the island in the center of the board.
            main_island_horz = main_island_dimension[0]
            main_island_vert = mini_catan.vertical
            big_board_horz = self.horizontal
            big_board_vert = self.vertical

            # Find the position of where the first tile of the main island will go on the board
            vert_pos = floor(big_board_vert / 2) - floor(main_island_vert / 2)
            letter = self.letters[vert_pos]
            horz_pos = floor(big_board_horz / 2) - floor(main_island_horz / 2)
            
            pos = f"{letter}{horz_pos}"
            while pos not in self.position_dict:
                horz_pos -= 1
                pos = f"{letter}{horz_pos}"    
            main_island_horz = main_island_dimension[1]
            i = 0
            while len(main_island) > 0:
                tile = self.position_dict[pos]
                for x in range(main_island_horz):
                    main_island_tile = main_island.popleft()
                    # Assign resource
                    tile.resource = main_island_tile.resource
                    # Add tile to the main island position dictionary
                    self.main_island_position_dict[tile.pos] = tile
                    # Decrease the total resources
                    resources_dict[tile.resource] -= 1
                    if resources_dict[tile.resource] == 0:
                        resources_dict.pop(tile.resource)

                    # Add the tile to the tiles by resource dictionary
                    if tile.resource != None:
                        if tile.resource not in self.main_island_tiles_by_resource:
                            self.main_island_tiles_by_resource[tile.resource] = [tile]
                        else:
                            if tile not in self.main_island_tiles_by_resource[tile.resource]:
                                self.main_island_tiles_by_resource[tile.resource].append(tile)

                    # Increment the tile position by two 
                    # Since each horizontal tile is offset by two
                    horz_pos += 2
                    pos = f"{letter}{horz_pos}"
                    tile = self.position_dict[pos]

                # Bring the horizontal position back to the start of the island
                # For the next row
                horz_pos -= (main_island_horz * 2)
                if i < mini_catan.diff:
                    horz_pos -= 1
                    main_island_horz += 1
                else:
                    horz_pos += 1
                    main_island_horz -= 1
                # Change the letter down to the next row
                letter_pos = self.letter_to_number[letter]
                letter = self.number_to_letter[letter_pos + 1]

                # Define new tile
                pos = f"{letter}{horz_pos}"
                i += 1

        else:
            main_island_horz = main_island_dimension[1]
            big_board_horz = self.min_width
            i = 0
            k = 0
            while len(main_island) > 0:
                for x in range(main_island_horz):
                    main_island_tile = main_island.popleft()
                    tile = tiles_queue.popleft()
                    # Assign resource
                    tile.resource = main_island_tile.resource
                    # Add tile to the main island position dictionary
                    self.main_island_position_dict[tile.pos] = tile

                    # Add the tile to the tiles by resource dictionary
                    if tile.resource != None:
                        if tile.resource not in self.main_island_tiles_by_resource:
                            self.main_island_tiles_by_resource[tile.resource] = [tile]
                        else:
                            if tile not in self.main_island_tiles_by_resource[tile.resource]:
                                self.main_island_tiles_by_resource[tile.resource].append(tile)

                    if tile.resource in resources_dict:
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
        
        # Calculate the max island size
        tiles = [tile for tile in tiles if tile.resource == None]
        remaining_land_tiles = len(tiles) - resources_dict['Sea']
        max_island_size = ceil(remaining_land_tiles / num_islands)

        # Randomize the tiles
        shuffle(tiles)
        tiles_queue = deque(tiles)

        # Create a number of island
        island_count = 0
        while remaining_land_tiles > 0:

            # Randomize the tiles before creating each new island
            tiles = [tile for tile in tiles if tile.resource == None]
            if 'Sea' in resources_dict:
                remaining_land_tiles = len(tiles) - resources_dict['Sea']
            else:
                remaining_land_tiles = len(tiles)
            if remaining_land_tiles < max_island_size:
                max_island_size = remaining_land_tiles

            # Randomize the tiles
            shuffle(tiles)
            tiles_queue = deque(tiles)

            # There is no need to check for adjacent islands
            # because the existing islands are surrounded by sea
            # Any islands that are not surrounded by sea,
            # would signal that there are no more sea tiles,
            # and should be added to anyways
            tile = tiles_queue.popleft()
            # Create island:
            island_finished = False
            island = []
            while len(island) < max_island_size and island_finished == False:

                # Add the tile to the island
                island.append(tile)
                adj_count = 0
                count = 0
                while tile.resource == None and len(resources) > 0:

                    # Prevents from getting stuck in an infinite loop when there is only one
                    # tile left and there is an adjacent tile with the same resource.
                    if count > 250:
                        main_island_tiles = []
                        for tile_list in self.main_island_tiles_by_resource.values():
                            for tile in tile_list:
                                main_island_tiles.append(tile)
                        # Set the resource dictionary to an empty dictionary to avoid adding double resources
                        # Clear all the resources currently allocated and attempt to reallocate the resources
                        # First define the main island resource dict to pass into the base game Catan class
                        main_island_resources = self._reset_tile_resources(main_island_tiles, {})
                        # Setting the resources dict equal to the main island resources dict will ensure that all
                        # resources are accounted for
                        resources_dict = self._reset_tile_resources(self.position_dict.values(), resources_dict)
                        # Add the main_island_resources to the overall resources dict
                        for resource, quantity in main_island_resources.items():
                            if resource in resources_dict:
                                resources_dict[resource] += quantity
                        # Rerun the method
                        self._place_resources(
                            resources_dict, main_island_resources, ADJ_RESOURCE_LIMIT, 
                            main_island_center, main_island_dimension, main_island_desert_center, 
                            num_islands, dead_tiles
                        )
                    # TODO: See if I need to add another check here
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
                        if resource in resources_dict:
                            tile.resource = resource
                        
                            resources_dict[resource] -= 1
                            if resources_dict[resource] == 0:
                                resources_dict.pop(resource)
                                resources.pop(resource_indx)

                    elif adj_count > 5:
                        for tile in island:
                            # This prevents sea tiles from being moved around
                            if tile.resource not in dead_tiles:
                                if tile.resource not in resources_dict:
                                    resources_dict[tile.resource] = 1
                                    resources.append(tile.resource)
                                else:
                                    resources_dict[tile.resource] += 1
                                tile.resource = None
                                tiles_queue.append(tile)
                        # Reset the island back to an empty list
                        island = []
                        # Check to see if there are any remaining land tiles
                        # Before popping a tile from the queue
                        if remaining_land_tiles > 0:
                            tiles = [tile for tile in tiles if tile.resource == None]
                            tiles_queue = deque(tiles)
                            if len(tiles_queue) > 0:
                                tile = tiles_queue.popleft()
                        else:
                            island_finished = True
                        adj_count = 0

                    else:
                        adj_count += 1
                    
                    # Randomize the tiles before creating each new island
                    tiles = [tile for tile in tiles if tile.resource == None]
                    if 'Sea' in resources_dict:
                        remaining_land_tiles = len(tiles) - resources_dict['Sea']
                    else:
                        remaining_land_tiles = len(tiles) 
                
                    count += 1

                possible_adjs = []
                # Pick an adjacent tile that doesn't yet have a resource
                for adj in tile.possible_adjacents:
                    if adj.resource == None:
                        possible_adjs.append(adj)

                # Pick a random adjacent tile to continue the island
                possible_adjs = [adj for adj in possible_adjs if adj.resource==None and adj not in island]
                if len(possible_adjs) > 0:
                    random_indx = randint(0, len(possible_adjs) - 1)
                    tile = possible_adjs[random_indx]
                else:
                    island_finished = True

            # Place sea tile all around the island 
            # to make it an island
            for tile in island:
                for adj in tile.possible_adjacents:
                    if adj.resource == None:
                        adj.resource = 'Sea'
                        if adj.resource in resources_dict:
                            resources_dict[adj.resource] -= 1
                            if resources_dict[adj.resource] == 0:
                                resources_dict.pop(adj.resource)

            island_count += 1
            # Randomize the tiles before creating each new island
            tiles = [tile for tile in tiles if tile.resource == None]
            if 'Sea' in resources_dict:
                remaining_land_tiles = len(tiles) - resources_dict['Sea']
            else:
                remaining_land_tiles = len(tiles)


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

        for tile in self.position_dict.values():
            if tile.pos not in self.main_island_position_dict:
                if tile.resource not in dead_tiles:
                    self.small_islands_position_dict[tile.pos] = tile
                    # Add the tile to the tiles by resource dictionary
                    if tile.resource not in self.small_islands_tiles_by_resource:
                        self.small_islands_tiles_by_resource[tile.resource] = [tile]
                    else:
                        if tile not in self.small_islands_tiles_by_resource[tile.resource]:
                            self.small_islands_tiles_by_resource[tile.resource].append(tile)

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
        if points < 2:
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
            elif adj_1.number == None and adj_2.number == None:
                return True
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

    
    def _place_numbers_by_resource_main_island(self, numbers_dict, dead_tiles=['Desert', 'Sea', None]):
        """
        Places numbers by resource on all the tiles on the main island.
        """
        # Create a list and then a queue of resources to go through until all the resources
        # Have number tokens on them.
        main_island_tiles = [tile for tile in self.main_island_position_dict.values() if tile.resource not in dead_tiles]
        resources = [resource for resource in self.main_island_tiles_by_resource.keys() if resource not in dead_tiles]
        shuffle(resources)
        resources_queue = deque(resources)
        numbers = [n for n in numbers_dict.keys()]
        for x in range(10):
            n_shuff = randint(0, len(numbers) - 1)
            numbers = numbers[n_shuff:] + numbers[:n_shuff]
        numbers_queue = deque(numbers)
        # numbers_queue = deque(self.main_island_number_placement_order)
        
        count = 0
        meta_count = 0
        while len(numbers_queue) != 0 and meta_count < 250:

            count += 1  
            # Once the count reaches a certian threshold,
            # remove all the number and points from the tiles
            if count >= 250:
                numbers_dict, numbers_queue = self._reset_tile_numbers(main_island_tiles, numbers_dict, numbers_queue)
                # Shuffle the resources_queue and numbers_queue so as not to run into the same placing order problem
                numbers = [n for n in numbers_dict.keys()]
                for x in range(10):
                    r_shuff = randint(0, len(resources) - 1)
                    n_shuff = randint(0, len(numbers) - 1)
                    resources = resources[r_shuff:] + resources[:r_shuff]
                    numbers = numbers[n_shuff:] + numbers[:n_shuff]
                resources_queue = deque(resources)
                numbers_queue = deque(numbers)
                count = 0
                meta_count += 1
                
            # Go through the resources and keep the number until that number is used up
            number = numbers_queue.popleft()
            points = self.num_to_points[number]
            resource = resources_queue.popleft()

            tiles = [tile for tile in reversed(self.main_island_tiles_by_resource[resource]) if tile.resource == resource]
            
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
        for tile in main_island_tiles:

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
                numbers_dict, numbers_queue = self._reset_tile_numbers(main_island_tiles, numbers_dict, numbers_queue)
                self._place_numbers_by_resource_main_island(numbers_dict)


    def _place_numbers_by_resource_smaller_islands(self, numbers_dict, dead_tiles=['Desert', 'Sea', None]):
        """
        Places numbers on the outlying smaller islands.
        """
        # Create a list and then a queue of resources to go through until all the resources
        # Have number tokens on them.
        small_islands_tiles = [tile for tile in self.small_islands_position_dict.values() if tile.resource not in dead_tiles]
        resources = [resource for resource in self.small_islands_tiles_by_resource.keys() if resource not in dead_tiles]
        resources_queue = deque(resources)
        numbers_queue = deque(self.small_islands_number_placement_order)
        
        count = 0
        all_have_numbers = False
        while len(numbers_queue) != 0 and all_have_numbers == False:

            count += 1  
            # Once the count reaches a certian threshold,
            # remove all the number and points from the tiles
            if count >= 500:
                # Check to see if all the tiles have numbers
                # This is because the number of island tiles can 
                # vary depending on the small islands generation
                no_numbers = []
                for tile in self.small_islands_position_dict.values():
                    if tile.number == None:
                        no_numbers.append(tile)
                if len(no_numbers) == 0:
                    all_have_numbers = True
                else:
                    numbers_dict, numbers_queue = self._reset_tile_numbers(small_islands_tiles, numbers_dict, numbers_queue)
                    count = 0
                
            # Go through the resources and keep the number until that number is used up
            number = numbers_queue.popleft()
            points = self.num_to_points[number]
            resource = resources_queue.popleft()

            tiles = [tile for tile in reversed(self.small_islands_tiles_by_resource[resource]) if tile.resource == resource]
            
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
        for tile in small_islands_tiles:

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
                numbers_dict, numbers_queue = self._reset_tile_numbers(small_islands_tiles, numbers_dict, numbers_queue)
                self._place_numbers_by_resource_smaller_islands(numbers_dict)


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
                    print(f'    ', end='')
            
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
            'Sea': 24,
        }
    main_island_numbers = {
        '2': 1, 
        '3': 1, 
        '4': 1, 
        '5': 1, 
        '6': 1, 
        '8': 1, 
        '9': 1, 
        '10': 1, 
        '11': 1, 
        '12': 1, 
    }
    small_islands_numbers = {
        '2': 1, 
        '3': 3, 
        '4': 3, 
        '5': 3, 
        '6': 3, 
        '8': 3, 
        '9': 3, 
        '10': 3, 
        '11': 3,  
        '12': 1,  
    }
    three_four_player_resources = {
        'Brick': 2,
        'Wood': 2,
        'Ore': 2,
        'Grain': 2,
        'Sheep': 2,
        }


    board = SeafarerIslands(9, 5, extension_and_seafarers_resources, three_four_player_resources, 
    main_island_numbers, small_islands_numbers, 1, True, (4, 3), False)
    board.print_resources()
    board.print_numbers()


if __name__ == "__main__":
    example()
