import math
import random

logging = False

num_miners = 100

def selfish_mine(num_miners, alpha, gamma):
    num_selfish_miners = int(alpha * num_miners)

    selfish_miners = set([i for i in range(0, num_selfish_miners)])
    honest_miners = set([i for i in range(num_selfish_miners, num_miners)])

    public_blockchain = []
    private_blockchain = []
    private_branch_length = 0
    for _ in range (10000):
        winning_miner = random.randint(0, num_miners - 1)
        if logging: print public_blockchain
        if logging: print private_blockchain
        if logging: print 'winning_miner =', winning_miner
        if logging: print 'private_branch_length =', private_branch_length
        delta = len(private_blockchain) - len(public_blockchain)
        if logging: print 'delta =', delta
        if winning_miner in selfish_miners:
            if logging: print 'selfish'
            private_blockchain.append(winning_miner)
            private_branch_length += 1 
            if delta == 0 and private_branch_length == 2:
                if logging: print 'if delta == 0 and private_branch_length == 2'
                public_blockchain = list(private_blockchain)
                private_branch_length = 0
        if winning_miner in honest_miners:
            if logging: print 'honest'
            public_blockchain.append(winning_miner)
            if delta == 0:
                if logging: print 'honest and delta == 0'
                private_blockchain = list(public_blockchain)
                private_branch_length = 0
            elif delta == 1:
                if logging: print 'honest and delta == 1'
                if random.random() > gamma:
                    if logging: print 'gamma plus'
                    public_blockchain = list(public_blockchain)
                else:
                    if logging: print 'gamma minus'
                    public_blockchain = list(private_blockchain)
            elif delta == 2:
                if logging: print 'honest and delta == 2'
                public_blockchain = list(private_blockchain)
                private_branch_length = 0
            else:
                if logging: print 'honest and delta > 2'
                public_blockchain.pop(len(public_blockchain) - 1)
                public_blockchain.append(private_blockchain[len(private_blockchain) - delta])
                public_blockchain.append(private_blockchain[len(private_blockchain) - delta + 1])
                private_branch_length = private_branch_length - 2
        if logging: print '-' * 10

    selfish_count = 0
    honest_count = 0
    total_count = 0
    for b in public_blockchain:
        if b in selfish_miners:
            selfish_count += 1
        if b in honest_miners:
            honest_count += 1
        total_count += 1
            
    return selfish_count * 1.0/total_count, honest_count * 1.0/total_count, total_count

num_trials = 100
gamma = 0.5
for alpha in [0.2, 0.24, 0.25, 0.26, 0.3, 0.33, 0.34, 0.4, 0.5, 0.6]:
    selfish_total = 0
    honest_total = 0
    total_total = 0
    for i in range(num_trials):
        selfish_count, honest_count, total_count = selfish_mine(num_miners, alpha, gamma)
        selfish_total += selfish_count
        honest_total += honest_count
        total_total += total_count
    print alpha, selfish_total * 1.0/num_trials, honest_total * 1.0/num_trials, total_total * 1.0/num_trials
        
                






