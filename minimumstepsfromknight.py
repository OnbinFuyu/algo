import unittest

from queue import Queue
from collections import defaultdict


class KnightBoardGame:
    """
    n is the column and row size of the board
    Init creates the board
    """
    def __init__(self, n, starting_pos, target_pos):
        self.n = n
        self.visited_board = [[False for j in range(n)] for i in range(n)]
        self.target_pos = target_pos
        self.visited_board[starting_pos[0]][starting_pos[1]] = True
        self.graph = defaultdict(list)
        self.queue = Queue()
        self.queue.put(starting_pos)
        self.queue.put(None)
        self.cur_pos = starting_pos
        self.current_move = 0

    def print_board(self):
        print("\n".join([" ".join([str(self.visited_board[i][j]) for j in range(self.n)]) for i in range(self.n)]))

    def gen_next_set_of_moves(self):
        up = self.cur_pos[0] + 2
        down = self.cur_pos[0] - 2
        left = self.cur_pos[1] + 1
        right = self.cur_pos[1] - 1
        moves_generated = []

        for i in [up, down]:
            for j in [left, right]:
                if 0 <= i < self.n and 0 <= j < self.n:
                    if self.visited_board[i][j]:
                        pass
                    else:
                        self.visited_board[i][j] = True
                        moves_generated.append((i,j))

        up = self.cur_pos[0] + 1
        down = self.cur_pos[0] - 1
        left = self.cur_pos[1] + 2
        right = self.cur_pos[1] - 2

        for j in [left, right]:
            for i in [up, down]:
                if 0 <= i < self.n and 0 <= j < self.n:
                    if self.visited_board[i][j]:
                        pass
                    else:
                        self.visited_board[i][j] = True
                        moves_generated.append((i,j))

        return moves_generated

    def get_shortest_path(self):
        if self.cur_pos == self.target_pos:
            return self.current_move
        # We have moved past the base case where knight and target are in the same location. We are now forced to make a move
        num_moves_until_next_depth = 0

        while not self.queue.empty():
            self.cur_pos = self.queue.get()
            if self.cur_pos == None:
                self.current_move += 1
                self.queue.put(None)
                continue

            moves = self.gen_next_set_of_moves()
            # No more moves possible, return failure
            if len(moves) == 0:
                return None
            # Store the moves in case we want to display how we need to do a BFS later
            self.graph[self.cur_pos] = moves
            # Add the moves to the queue that we want to BFS on.
            map(self.queue.put, moves)
            for i in moves:
                self.queue.put(i)

            # We have found our target in the next set of moves
            if self.target_pos in moves:
                return self.current_move + 1

        # No moves possible to get to target
        return None


class TestShortestPath(unittest.TestCase):
    def test_return_none_if_no_paths(self):
        board_size = 2
        starting_pos = (0,0)
        target_pos = (1,1)
        kb = KnightBoardGame(board_size, starting_pos, target_pos)
        self.assertIsNone(kb.get_shortest_path())

    def test_shortest_path_of_zero_moves(self):
        board_size = 3
        starting_pos = (0,0)
        target_pos = (0,0)
        kb = KnightBoardGame(board_size, starting_pos, target_pos)
        self.assertEqual(kb.get_shortest_path(), 0)

    def test_shortest_path_of_one_move(self):
        board_size = 3
        starting_pos = (0,0)
        target_pos = (2,1)
        kb = KnightBoardGame(board_size, starting_pos, target_pos)
        self.assertEqual(kb.get_shortest_path(), 1)

    def test_shortest_path_of_two_moves(self):
        board_size = 3
        starting_pos = (0,0)
        target_pos = (0,2)
        kb = KnightBoardGame(board_size, starting_pos, target_pos)
        self.assertEqual(kb.get_shortest_path(), 2)

    def test_shortest_path_of_three_moves(self):
        board_size = 3
        starting_pos = (0,0)
        target_pos = (1,0)
        kb = KnightBoardGame(board_size, starting_pos, target_pos)
        self.assertEqual(kb.get_shortest_path(), 3)


if __name__ == "__main__":
    unittest.main()