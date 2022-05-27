# python3
# catan_board.py - Tile and Catan Board classes. Set up a balanced catan board given proper inputs.


class Tile:

    def __init__(self, position, number, point_value, resource):
        # Inputs
        self.pos = position
        self.number = number
        self.pt_value = point_value
        self.resource = resource


        # positional relationships
        self.right = None
        self.top_right = None
        self.top_left = None
        self.left = None
        self.bottom_left = None
        self.bottom_right = None

        # Create a list of possible adjacent positions
        self.possible_options = self._check_possible_adjacents()

    def _check_possible_adjacents(self):
        possible_options = []
        check_options = [
            self.right, 
            self.top_right, 
            self.top, 
            self.top_left, 
            self.left, 
            self.bottom_left, 
            self.bottom, 
            self.bottom_right, 
        ]
        for option in check_options:
            if option !=None:
                possible_options.append(option)

        return possible_options