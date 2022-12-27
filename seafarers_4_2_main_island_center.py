# python3
# seafarers_small_main_island_center.py - Prints a 9 - 5 map using the seafarers expansion 
# and the board pieces from the base game extension.

from seafarers_catan_board import SeafarerIslands

def generate_4_by_2_main_island_center_map():

    # The lower this number is the more balanced the board will be; however, 
    # the number of possible boards will also be lower
    BALANCE_PARAMETER = 4
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
            '2': 1, 
            '3': 2, 
            '4': 2, 
            '5': 1, 
            '6': 1, 
            '8': 1, 
            '9': 2, 
            '10': 2, 
            '11': 1, 
            '12': 1, 
        }
        small_islands_numbers = {
            '2': 1, 
            '3': 2, 
            '4': 2, 
            '5': 3, 
            '6': 3, 
            '8': 3, 
            '9': 2, 
            '10': 2, 
            '11': 3,  
            '12': 1,  
        }
        ### A main island with 14 tiles must have 14 resources ###
        three_four_player_resources = {
            'Brick': 2,
            'Wood': 3,
            'Ore': 3,
            'Grain': 3,
            'Sheep': 3,
            }

        board = SeafarerIslands(9, 5, extension_and_seafarers_resources, three_four_player_resources, 
        main_island_numbers, small_islands_numbers, 1, True, (4, 2), False)

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
    generate_4_by_2_main_island_center_map()
