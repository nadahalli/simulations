import unittest
from selfishmine import selfishmine

def miner_generator(chosen_miners):
    def miner(_1, _2):
        if 'index' not in miner.__dict__:
            miner.index = -1
        miner.index += 1
        return chosen_miners[miner.index]
    return miner

class TestSelfishMine(unittest.TestCase):
    def test_one(self):
        num_miners = 2
        alpha = 0.5
        gamma = 0.5
        chosen_miners = [(0, True),
                         (1, False),
                         (0, True),
                         (1, False),
                         (0, True),
                         (1, False)]
        _, _, _, actual_blockchain = selfishmine(num_miners,
                                                 len(chosen_miners),
                                                 alpha,
                                                 gamma,
                                                 miner_generator(chosen_miners),
                                                 False)
        self.assertEquals([1, 1, 1], actual_blockchain)

    def test_two(self):
        alpha = 0.5
        gamma = 0.5
        chosen_miners = [(0, False),
                         (1, False),
                         (2, False),
                         (3, False),
                         (4, True),
                         (5, False),
                         (6, True),
                         (7, False),
                         (8, True)]
        num_miners = len(chosen_miners)
        _, _, _, actual_blockchain = selfishmine(num_miners,
                                                 len(chosen_miners),
                                                 alpha,
                                                 gamma,
                                                 miner_generator(chosen_miners),
                                                 False)
        self.assertEquals([0, 1, 2, 3, 7, 8], actual_blockchain)

    def test_three(self):
        alpha = 0.5
        gamma = 0.5
        chosen_miners = [(4, None),
                         (0, None),
                         (1, None),
                         (5, None),
                         (4, None),
                         (0, None),
                         (1, None),
                         (2, None),
                         (5, True)]
        num_miners = len(chosen_miners)
        _, _, _, actual_blockchain = selfishmine(num_miners,
                                                 len(chosen_miners),
                                                 alpha,
                                                 gamma,
                                                 miner_generator(chosen_miners),
                                                 False)
        self.assertEquals([4, 0, 1, 4, 0], actual_blockchain)

if __name__ == '__main__':
    unittest.main()
