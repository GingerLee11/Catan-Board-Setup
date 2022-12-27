# python3
# seafarers_small_main_island_center.py - Prints a 9 - 5 map using the seafarers expansion 
# and the board pieces from the base game extension.

from seafarers_catan_board import SeafarerIslands
from random import randint

def generate_small_main_island_center_map():

    for x in range(200):
        # Test with a 9 max, 5 min board
        # No desert tiles on the small islands, 
        # desert tiles flipped over to provide more sea tiles
        # Ten tiles is too small of two 1 point tile, so there will only be one
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
        
        '''
        # Randomly add an extra quantity to one of the numbers in the main island dict
        low_or_high = randint(0, 1)
        if low_or_high == 0:
            add_num_quant = randint(3, 5)
        else:
            add_num_quant = randint(9, 11)
        main_island_numbers[str(add_num_quant)] += 1
        '''

        board = SeafarerIslands(9, 5, extension_and_seafarers_resources, three_four_player_resources, 
        main_island_numbers, small_islands_numbers, 1, True, (4, 3), False)
        #board.print_resources()
        #board.print_numbers()

        game_balance = board.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)


if __name__ == "__main__":
    generate_small_main_island_center_map()
