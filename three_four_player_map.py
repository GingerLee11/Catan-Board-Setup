# Python3
# three_four_player_map.py - generates a three to four player island using the original rules.

from catan_board import CatanIsland


def generate_three_four_player_island():

    # The lower this number is the more balanced the board will be; however, 
    # the number of possible boards will also be lower
    BALANCE_PARAMETER = 3

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
        
        catan = CatanIsland(5, 3, three_four_player_resources, three_four_player_numbers, True, 1)
        # Only print the resources and the numbers if the game is balanced
        game_balance = catan.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        # print(total_diff)
        if total_diff < BALANCE_PARAMETER:
            print()
            catan.print_resources()
            catan.print_numbers()
            print()


if __name__ == "__main__":
    generate_three_four_player_island()
