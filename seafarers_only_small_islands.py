# python3
# seafarers_small_main_island_center.py - Prints a 9 - 5 map using the seafarers expansion 
# and the board pieces from the base game extension.

from seafarers_catan_board import SeafarerIslands
from random import randint

def generate_all_small_islands():

    # The lower this number is the more balanced the board will be; however, 
    # the number of possible boards will also be lower
    BALANCE_PARAMETER = 5
    total_diff = 100
    while total_diff > BALANCE_PARAMETER:
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
            'Sea': 25,
            }
        main_island_numbers = {
            '3': 1, 
            '4': 1, 
            '5': 1, 
            '6': 1, 
            '9': 1, 
            '10': 1, 
            '11': 1, 
        }
        small_islands_numbers = {
            '2': 2, 
            '3': 3, 
            '4': 3, 
            '5': 3, 
            '6': 3, 
            '8': 4, 
            '9': 3, 
            '10': 3, 
            '11': 3,  
            '12': 2,  
        }
        three_four_player_resources = {
            'Brick': 1,
            'Wood': 2,
            'Ore': 1,
            'Grain': 1,
            'Sheep': 2,
            }

        board = SeafarerIslands(9, 5, extension_and_seafarers_resources, three_four_player_resources, 
        main_island_numbers, small_islands_numbers, 1, False, (3, 2), False, 4)

        game_balance = board.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        # print(total_diff)
        if total_diff < BALANCE_PARAMETER:
            print()
            board.print_resources()
            board.print_numbers()
            print()
            print(total_diff)
            print(board.total_points_per_resource)


if __name__ == "__main__":
    generate_all_small_islands()
