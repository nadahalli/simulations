import math
import random

def format_blockchain(chain):
    return [str(i) if i > 9 else '0'+str(i) for i in chain]

def random_mine_fn(num_miners, gamma):
    return random.randint(0, num_miners - 1), random.random() < gamma

def selfishmine(num_miners, num_blocks, alpha, gamma, random_mine_fn, logging):
    num_selfish_miners = int(alpha * num_miners)

    selfish_miners = set([i for i in range(0, num_selfish_miners)])
    honest_miners = set([i for i in range(num_selfish_miners, num_miners)])

    public_blockchain = []
    private_blockchain = []

    temp_pub_honest_blockchain = []
    temp_pub_selfish_blockchain = []

    private_branch_length = 0
    for _ in range (num_blocks):
        temp_pub_selfish_blockchain = list(public_blockchain)
        temp_pub_honest_blockchain = list(public_blockchain)
        winning_miner, gamma_decision = random_mine_fn(num_miners, gamma)
        delta = len(private_blockchain) - len(public_blockchain)
        if logging: print 'public_blockchain           =', format_blockchain(public_blockchain)
        if logging: print 'private_blockchain          =', format_blockchain(private_blockchain)
        if logging:
            print('winning_miner =',
                  winning_miner,
                  '[selfish]' if winning_miner in selfish_miners else '[honest]')
        if logging: print 'private_branch_length =', private_branch_length
        if logging: print 'delta =', delta
        if winning_miner in selfish_miners:
            private_blockchain.append(winning_miner)
            private_branch_length += 1
            # The following is true if the chains are the same length,
            # but are not the same. They differ in their last block.
            # So, if the selfish pool finds a new block, it will add it
            # to its chain and broadcast it immediately to orphan the
            # last block of the honest chain.
            if delta == 0 and private_branch_length == 2:
                if logging: print 'delta == 0 and private_branch_length == 2'
                temp_pub_selfish_blockchain = list(private_blockchain)
                private_branch_length = 0
        if winning_miner in honest_miners:
            temp_pub_honest_blockchain.append(winning_miner)
            # If the chains are the same length (irrespective of whether
            # they are the same blocks or not), if an honest miner finds
            # a block, the honest chain has a lead of 1 and so the selfish
            # pool just copies it over and resets.
            if delta == 0:
                if logging: print 'honest and delta == 0'
                temp_pub_selfish_blockchain.append(winning_miner)
                private_blockchain = list(temp_pub_selfish_blockchain)
                private_branch_length = 0
            # If the selfish pool is leading by 1, and a honest miner
            # finds a block, the selfish pool releases its private
            # 1-length-lead block to create a race between the two
            # blocks to see who gets picked up.
            elif delta == 1:
                if logging: print 'honest and delta == 1'
                temp_pub_selfish_blockchain = list(private_blockchain)
            elif delta == 2:
                if logging: print 'honest and delta == 2'
                temp_pub_selfish_blockchain = list(private_blockchain)
                private_branch_length = 0
            else:
                if logging: print 'honest and delta > 2'
                temp_pub_selfish_blockchain.append(
                    private_blockchain[len(private_blockchain) - delta])
                private_branch_length = private_branch_length - 1

            if logging:
                print('temp_pub_honest_blockchain  =',
                      format_blockchain(temp_pub_honest_blockchain))
            if logging:
                print('temp_pub_selfish_blockchain =',
                      format_blockchain(temp_pub_selfish_blockchain))
            if temp_pub_selfish_blockchain == temp_pub_honest_blockchain:
                public_blockchain = list(temp_pub_honest_blockchain)
            elif len(temp_pub_selfish_blockchain) > len(temp_pub_honest_blockchain):
                public_blockchain = list(temp_pub_selfish_blockchain)
            elif len(temp_pub_selfish_blockchain) < len(temp_pub_honest_blockchain):
                public_blockchain = list(temp_pub_honest_blockchain)
            else:
                assert(gamma_decision in [True, False])
                if gamma_decision:
                    if logging: print 'selfish chain wins'
                    public_blockchain = list(temp_pub_selfish_blockchain)
                else:
                    if logging: print 'honest chain wins'
                    public_blockchain = list(temp_pub_honest_blockchain)
                    if delta == 1:
                        private_blockchain = list(temp_pub_honest_blockchain)

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
            
    return (selfish_count * 1.0/total_count,
            honest_count * 1.0/total_count,
            total_count,
            public_blockchain)

if __name__ == '__main__':
    logging = False
    num_trials = 10
    num_miners = 100
    num_blocks = 10000

    gamma = 0.5
    for alpha in [0.25, 0.1, 0.2, 0.3, 0.4, 0.5]:
        selfish_total = 0
        honest_total = 0
        total_total = 0
        for i in range(num_trials):
            selfish_count, honest_count, total_count, blockchain = selfishmine(num_miners,
                                                                               num_blocks,
                                                                               alpha,
                                                                               gamma,
                                                                               random_mine_fn,
                                                                               logging)
            selfish_total += selfish_count
            honest_total += honest_count
            total_total += total_count
        print(alpha,
              selfish_total * 1.0/num_trials,
              honest_total * 1.0/num_trials,
              total_total * 1.0/num_trials)
        
                






