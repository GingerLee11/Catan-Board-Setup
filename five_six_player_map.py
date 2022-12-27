# python3
# five_six_player_map.py - generates a five to six player island map.

from catan_board import CatanIsland


def generate_five_six_player_island():
    """
    Creates several potential five to six player 
    Catan maps.
    """
    # The lower this number is the more balanced the board will be; however, 
    # the number of possible boards will also be lower
    BALANCE_PARAMETER = 3

    for x in range(100):
        five_six_player_resources = {
            'Brick': 5,
            'Wood': 6,
            'Ore': 5,
            'Grain': 6,
            'Sheep': 6,
            'Desert': 2,
        }
        five_six_player_numbers = {
            '2': 2, 
            '3': 3, 
            '4': 3, 
            '5': 3, 
            '6': 3, 
            '8': 3, 
            '9': 3, 
            '10': 3, 
            '11': 3, 
            '12': 2, 
        }
        
        catan = CatanIsland(6, 3, five_six_player_resources, five_six_player_numbers, True, 2)
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
    generate_five_six_player_island()
