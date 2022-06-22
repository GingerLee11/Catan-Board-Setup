# python3
# seafarers_catan_board.py - Creates a Catan board using the seafarers expansion to make several different surrounding islands.

from collections import deque
from math import ceil, floor
from random import randint
from string import ascii_uppercase

from catan_board import CatanIsland


class SeafarerIslands(CatanIsland):
    
    def __init__(self, max_width, min_width, 
            resource_dict, main_island_resources, numbers_dict,
            adj_resource_limit=2, main_island_center=False, main_island_dimensions=(5, 3)):
        
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
        # Check for small island that don't use all the numbers
        if len(numbers_dict) < 10:
            self.number_placement_order = deque(numbers_dict.keys())
        else:
            self.number_placement_order = [
                '8', 
                '6', 
                '9',
                '12',
                '2', 
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
        SEA_ADJACENCY_UPPER_LIMIT = 6
        SEA_ADJACENCY_LOWER_LIMIT = 1

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

        tiles_queue = deque(tile for tile in tiles_queue if tile.resource == None)

        # TODO: Instead of randomly assigning resources like in the base game,
        # Creates an island, surrounds it with sea, and repeats until all the land tiles are used up
        # Then fill in the rest of the board with sea tiles until all the tiles are used.
        # Set a max allowable size for an island determined by how many tiles are left available
        max_island_size = floor((len(tiles_queue) - resources_dict['Sea']) / num_islands)

        while len(tiles_queue) > 0:
           
            # Check to make sure there are actually enough tiles to create
            # an island of the randomly generated size
            if len(tiles_queue) < max_island_size:
                max_island_size = len(tiles_queue)
            if max_island_size > 1:
                island_size = randint(2, max_island_size)
            else:
                island_size = 1
            island_queue = deque([tiles_queue.pop()])
            checked = []
            # Add nearby tiles to create a island that is 
            # Smaller than the limit
            sea_count = 0
            j = 0
            while len(island_queue) < island_size:
                if sea_count > 4:
                    break
                if j > 10:
                    break
                for adj in tile.possible_adjacents:
                    if adj.resource == 'Sea':
                        sea_count += 1
                    if adj not in checked:
                        checked.append(adj)
                        if adj.resource == None:
                            island_queue.append(adj)
                            
                island_queue.appendleft(tile)
                tile = island_queue.pop()

                j += 1

            # Add resources to the tiles
            # while making sure to meet adjacency rules
            while len(island_queue) > 0:
                tile = island_queue.popleft()
                count = 0
                adj_count = 0
                while tile.resource == None:

                    if count > 3:
                        island_queue.append(tile)
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
                    if num_adj < ADJ_RESOURCE_LIMIT:
                        tile.resource = resource

                        # Add the tile to the tiles by resource dictionary
                        if tile.resource != None and resource not in dead_tiles and tile.resource not in dead_tiles:
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
                            # This prevents sea and desert tiles from being moved
                            if adj.resource not in dead_tiles:
                                if adj.resource not in resources_dict:
                                    resources_dict[adj.resource] = 1
                                    resources.append(adj.resource)
                                else:
                                    resources_dict[adj.resource] += 1
                                adj.resource = None
                                island_queue.append(adj)

                    else:
                        adj_count += 1

            # Place sea tiles all around the island to make it an actual island
            for tile in tiles_queue:
                if 'Sea' not in resources_dict:
                    break
                if tile.resource == None:
                    for adj in tile.possible_adjacents:
                        if adj.resource not in dead_tiles:
                            tile.resource = 'Sea'
                            if tile.resource in resources_dict:
                                resources_dict[tile.resource] -= 1
                                if resources_dict[tile.resource] == 0:
                                    resources_dict.pop(tile.resource)
                            break
            
            # This updates the tiles queue to contain only the tiles without resources
            tiles_queue = deque(tile for tile in tiles_queue if tile.resource == None)

            # TODO: Add a check to see if there are only sea tiles remaining
            if len(resources) == 0:
                for tile in tiles_queue:
                    if tile.resource == None:
                        tile.resource = 'Sea'
                        if tile.resource in resources_dict:
                            resources_dict[tile.resource] -= 1
                            if resources_dict[tile.resource] == 0:
                                resources_dict.pop(tile.resource)


    # TODO: Write a method for placing numbers on the island resources
    def _place_numbers_by_resource(self, numbers_dict, dead_tiles=['Desert', 'Sea', None]):
        print('Numbers!')
    
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
    # No Desert for this map, 
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
