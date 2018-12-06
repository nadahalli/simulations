import unittest
from selfishmine import selfishmine

def miner_generator(chosen_miners):
    def miner(_):
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
        chosen_miners = [(0, None),
                         (1, True),
                         (0, None),
                         (1, True),
                         (0, None),
                         (1, True)]
        _, _, _, actual_blockchain = selfishmine(num_miners,
                                                 len(chosen_miners),
                                                 alpha,
                                                 gamma,
                                                 miner_generator(chosen_miners),
                                                 False)
        self.assertEquals([1, 1, 1], actual_blockchain)

    def test_two(self):
        num_miners = 2
        alpha = 0.5
        gamma = 0.5
        chosen_miners = [(1, None),
                         (0, None),
                         (0, None),
                         (0, None),
                         (1, True)]
        _, _, _, actual_blockchain = selfishmine(num_miners,
                                                 len(chosen_miners),
                                                 alpha,
                                                 gamma,
                                                 miner_generator(chosen_miners),
                                                 True)
        self.assertEquals([1, 1, 1], actual_blockchain)

if __name__ == '__main__':
    unittest.main()
