############################################################
# Imports
############################################################
import game_helper as gh

############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    GAME_STATUS_ONGOING = 1
    GAME_STATUS_OVER = 0
    NEW_BOMB = 3

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.__ships = ships
        self.bombs = {}
        self.__game_status = self.GAME_STATUS_ONGOING
        self.intact_cells = []
        for ship in ships:
            self.intact_cells.extend(ship.coordinates())

    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        hits = []
        ships_terminated = 0
        still_alive_ships = []
        new_intact_cells = []
        damaged_cells = []
        new_bombs = {}
        target = gh.get_target(self.__board_size)
        self.bombs[target] = self.NEW_BOMB

        for ship in self.__ships:
            ship.move()
            for bomb in self.bombs:
                if ship.hit(bomb):
                    hits.append(bomb)
                damaged_cells.extend(ship.damaged_cells())
            new_intact_cells.extend(ship.intact_cells())
            self.intact_cells = new_intact_cells

        for ship in self.__ships:
            if ship.terminated():
                ships_terminated += 1
            else:
                still_alive_ships.append(ship)
        self.__ships = still_alive_ships

        for bomb in self.bombs:
            if bomb != target:
                self.bombs[bomb] -= 1
            if self.bombs[bomb] != 0 and bomb not in hits:
                new_bombs[bomb] = self.bombs[bomb]
        self.bombs = new_bombs
        print(gh.board_to_string(self.__board_size,hits,self.bombs,damaged_cells,self.intact_cells))

        if len(self.__ships) == 0:
            self.__game_status = self.GAME_STATUS_OVER
        gh.report_turn(len(hits),ships_terminated)
        return self.__game_status

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        description = (self.__board_size,self.bombs,self.__ships)
        return str(description)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report_legend()
        print(gh.board_to_string(self.__board_size,[],self.bombs,[],self.intact_cells))
        while self.__game_status != self.GAME_STATUS_OVER:
            self.__play_one_round()
        gh.report_gameover()



############################################################
# An example usage of the game
############################################################

if __name__=="__main__":
    # game = Game(5, gh.initialize_ship_list(4, 2))
    game = Game(5, gh.getShips())
    game.play()
