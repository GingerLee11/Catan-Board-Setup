# python3
# four_islands_custom_seafarers.py - Creates a custom four island setup using the seafarers expansion.
# There is one 5 point token (8 or 6) and one 1 point token (2)

from catan_board import CatanIsland


def four_islands_custom_seafarers():
    print("Settlers Island:")
    for x in range(10):
        # Settler Island (balances island with an even balance of resources)
        settler_island_resources = {
            'Brick': 2,
            'Wood': 2,
            'Grain': 2,
            'Sheep': 1,
        }
        settler_island_numbers = {
            '4': 1, 
            '5': 1,
            '8': 1, 
            '9': 1,
            '10': 1, 
            '11': 1,
            '12': 1, 
        }

        settlers_island = CatanIsland(3, 2, settler_island_resources, settler_island_numbers, False)
        
        # settlers_island.print_resources()
        # settlers_island.print_numbers()
        game_balance = settlers_island.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)
        if total_diff < 3:
            print()
            settlers_island.print_resources()
            settlers_island.print_numbers()
            print()

    # City Island (good island for getting resources to build cities)
    print("City Island:")
    for x in range(25):
        
        city_island_resources = {
            'Brick': 1,
            'Wood': 1,
            'Ore': 3,
            'Grain': 2,
        }
        city_island_numbers = {
            '2': 1, 
            '3': 1, 
            '4': 1, 
            '5': 1,
            '6': 1,
            '9': 1,
            '10': 1,
            
        }

        city_island = CatanIsland(3, 2, city_island_resources, city_island_numbers, False)
        
        # city_island.print_resources()
        # city_island.print_numbers()
        game_balance = city_island.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)
        # print(total_diff)
        if total_diff < 9:
            print()
            city_island.print_resources()
            city_island.print_numbers()
            print()

    # Ship Island: Good resources for building ships (and roads)
    print("Ship Island:")
    for x in range(15):
        
        ship_island_resources = {
            'Brick': 1,
            'Wood': 2,
            'Grain': 1,
            'Sheep': 3,
        }
        ship_island_numbers = {  
            '3': 1,
            '4': 1,
            '5': 1,
            '8': 1,
            '9': 1,
            '10': 1,
            '12': 1,

        }
        
        ship_island = CatanIsland(3, 2, ship_island_resources, ship_island_numbers, False)
        
        # ship_island.print_resources()
        # ship_island.print_numbers()
        game_balance = ship_island.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)
        if total_diff < 5:
            print()
            ship_island.print_resources()
            ship_island.print_numbers()
            print()

    # Knight Island: Good for building and activating knights
    print("Knight Island:")
    for x in range(10):
        knight_island_resources = {
            'Brick': 1,
            'Ore': 2,
            'Grain': 2,
            'Sheep': 2,
        } 
        knight_island_numbers = {
            '2': 1,
            '4': 1,
            '5': 1,
            '6': 1,
            '9': 1,
            '10': 1,
            '11': 1,
        }
        knight_island = CatanIsland(3, 2, knight_island_resources, knight_island_numbers, False)
        # knight_island.print_resources()
        # knight_island.print_numbers()
        game_balance = knight_island.calculate_points_per_resource()
        average_points = sum(game_balance.values()) / len(game_balance.values())
        total_diff = 0
        for points in game_balance.values():
            total_diff += abs(average_points - points)

        print(total_diff)
        if total_diff < 3:
            print()
            knight_island.print_resources()
            knight_island.print_numbers()
            print()


if __name__ == "__main__":
    four_islands_custom_seafarers()
