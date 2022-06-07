# python3
# four_islands_custom_seafarers.py - Creates a custom four island setup using the seafarers expansion.

from catan_board import CatanIsland


def four_islands_custom_seafarers():

    # resources
    settler_island_resources = {
        'Brick': 2,
        'Wood': 2,
        'Grain': 2,
        'Sheep': 1,
    }
    city_island_resources = {
        'Brick': 1,
        'Wood': 1,
        'Ore': 3,
        'Grain': 2,
    }
    ship_island_resources = {
        'Brick': 1,
        'Wood': 2,
        'Grain': 1,
        'Sheep': 3,
    }
    knight_island_resources = {
        'Brick': 1,
        'Ore': 2,
        'Grain': 2,
        'Sheep': 2,
    }

    # Numbers:
    settler_island_numbers = {
        '8': 1, 
        '5': 1,
        '10': 1, 
        '3': 1, 
        '12': 1, 
        '11': 1,
        '6': 1,
    }
    city_island_numbers = {
        '4': 1, 
        '9': 1, 
        '2': 1, 
        '11': 1, 
        '5': 1, 
        '8': 1, 
        '10': 1, 
    }
    ship_island_numbers = {
        '12': 1,
        '9': 1,
        '6': 1,
        '4': 1,
        '3': 1,
        '11': 1,
        '8': 1,
    }
    knight_island_numbers = {
        '2': 1,
        '3': 1,
        '4': 1,
        '5': 1,
        '6': 1,
        '9': 1,
        '10': 1,
    }


    settlers_island = CatanIsland(3, 2, settler_island_resources, settler_island_numbers, False)
    print("Settlers Island:")
    settlers_island.print_resources()
    settlers_island.print_numbers()
    print()
    game_balance = settlers_island.calculate_points_per_resource()
    average_points = sum(game_balance.values()) / len(game_balance.values())
    total_diff = 0
    for points in game_balance.values():
        total_diff += abs(average_points - points)

    print(total_diff)

    city_island = CatanIsland(3, 2, city_island_resources, city_island_numbers, False)
    print("City Island:")
    city_island.print_resources()
    city_island.print_numbers()
    print()
    game_balance = city_island.calculate_points_per_resource()
    average_points = sum(game_balance.values()) / len(game_balance.values())
    total_diff = 0
    for points in game_balance.values():
        total_diff += abs(average_points - points)

    print(total_diff)

    ship_island = CatanIsland(3, 2, ship_island_resources, ship_island_numbers, False)
    print("Ship Island:")
    ship_island.print_resources()
    ship_island.print_numbers()
    print()
    game_balance = ship_island.calculate_points_per_resource()
    average_points = sum(game_balance.values()) / len(game_balance.values())
    total_diff = 0
    for points in game_balance.values():
        total_diff += abs(average_points - points)

    print(total_diff)

    knight_island = CatanIsland(3, 2, knight_island_resources, knight_island_numbers, False)
    print("Knight Island:")
    knight_island.print_resources()
    knight_island.print_numbers()
    print()
    game_balance = knight_island.calculate_points_per_resource()
    average_points = sum(game_balance.values()) / len(game_balance.values())
    total_diff = 0
    for points in game_balance.values():
        total_diff += abs(average_points - points)

    print(total_diff)


if __name__ == "__main__":
    four_islands_custom_seafarers()
