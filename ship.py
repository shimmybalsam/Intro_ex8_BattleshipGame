############################################################
# Imports
############################################################
import copy
import ship_helper


############################################################
# Helper class
############################################################

class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 2
    DOWN = 8
    LEFT = 4
    RIGHT = 6

    NOT_MOVING = 0

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

############################################################
# Class definition
############################################################


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = pos
        self.__length = length
        self.__direction = direction
        self.__board_size = board_size
        self.__damaged_cells = []
        self.starting_direction = direction

    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)).
        The tuple's content should be (in the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        coordinates = copy.deepcopy(self.coordinates())
        damaged_list = copy.deepcopy(self.damaged_cells())
        description = (coordinates, damaged_list, ship_helper.direction_repr_str(Direction,self.__direction), self.__board_size)
        return str(description)

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement would
        take the ship outside of the board, in which case the ship switches
        direction and sails one board unit in the new direction.
        :return: A direction object representing the current movement direction.
        """
        x, y = self.__pos
        if len(self.__damaged_cells) != 0:
            self.__direction = Direction.NOT_MOVING
        elif self.__direction == Direction.DOWN:
            if y + self.__length < self.__board_size:
                y += 1
            else:
                self.__direction = Direction.UP
                y -= 1
        elif self.__direction == Direction.UP:
            if y > 0:
                y -= 1
            else:
                self.__direction = Direction.DOWN
                y += 1
        elif self.__direction == Direction.RIGHT:
            if x + self.__length < self.__board_size:
                x += 1
            else:
                self.__direction = Direction.LEFT
                x -= 1
        elif self.__direction == Direction.LEFT:
            if x > 0:
                x -= 1
            else:
                self.__direction = Direction.RIGHT
                x += 1
        self.__pos = (x,y)
        return copy.copy(self.__direction)

    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        for coordinate in self.coordinates():
            if coordinate not in self.__damaged_cells:
                if coordinate == pos:
                    self.__damaged_cells.append(pos)
                    self.__direction = Direction.NOT_MOVING
                    return True
        return False

    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns, False
        otherwise.
        """
        if self.__length == len(self.__damaged_cells):
            return True
        else:
            return False

    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinate, False otherwise.
        """
        if pos in self.coordinates():
            return True
        return False

    def coordinates(self):
        """
        Return ship's current coordinates on board.
        :return: A list of (x, y) tuples representing the ship's current
        occupying coordinates.
        """
        all_coordinates = []
        x, y = self.__pos
        if self.__length == 1:
            all_coordinates.append(self.__pos)
        elif self.starting_direction in Direction.HORIZONTAL:
            for i in range(self.__length):
                all_coordinates.append((x+i, y))
        elif self.starting_direction in Direction.VERTICAL:
            for j in range(self.__length):
                all_coordinates.append((x, y+j))
        return all_coordinates

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        copied_damaged_cells = copy.deepcopy(self.__damaged_cells)
        return copied_damaged_cells

    def intact_cells(self):
        """
        A helpful function which returns all of the intact cells of a ship.
        :return: A list of tuples, that each tuple indicates an in tact
        coordinate set of a ship
        """
        intact_cells = []
        ship_coordinates = self.coordinates()
        for coordinate in ship_coordinates:
            if coordinate not in self.damaged_cells():
                intact_cells.append(coordinate)
        return intact_cells

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current sailing direction or
         NOT_MOVING if the ship is hit and not moving.
        """
        direction = copy.copy(self.__direction)
        return direction

    def cell_status(self, pos):
        """
        Return the status of the given coordinate (hit\not hit) in current ship.
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        if pos not in self.coordinates():
            return None
        elif pos in self.__damaged_cells:
            return True
        else:
            return False

