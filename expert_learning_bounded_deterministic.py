import utils
import math
import random

class BoundedExpertLearning:
    def __init__(self, beta, max):
        self.alpha = float(math.sqrt(beta))
        self.max = max
        self.experts = [self.alpha ** i for i in range(int(math.log(max, self.alpha))+1)]
        self.scores = [0 for i in range(int(math.log(max, self.alpha))+1)]
        self.profit = 0

    def recommend(self):
        max_score = max(self.scores)
        max_index = 0
        for i, score in enumerate(self.scores):
            if score == max_score:
                max_index = i
        return self.experts[max_index]

    def update_score(self,bid_price):
        for i in range(len(self.experts)):
            if bid_price > self.experts[i]:
                self.scores[i] += self.experts[i]

    def step(self, bid_price):
        price = self.recommend()
        profit = price if price < bid_price else 0
        self.profit += profit
        self.update_score(bid_price)

if __name__ == "__main__":
    print("Input beta, num_bids, h, num_trials")
    params=input().split()
    beta = float(params[0])
    num_bids,h,num_trials = map(int, params[1:])
    #print(str(beta) + " " + str(num_bids) + " " + str(h) + " " + str(num_trials))
    #print()
    # beta, num_bids, h, num_trials = map(int, input().split())
    total_optimum = 0
    total_profit = 0
    for i in range (0,num_trials):
        auction = BoundedExpertLearning(beta, h) #
        seq = utils.gen_uniform_random_bid(num_bids, h) #
        optimum_price_and_profit = utils.compute_optimum_price_and_profit(seq)
        for bid_price in seq:
            auction.step(bid_price)
        optimum_profit = optimum_price_and_profit[1]
        total_optimum+=optimum_profit
        total_profit+=auction.profit
    
        #print("sequence of bidders:")
        #print(seq)
        #print()
        #print("Optimum price and profit:")
        #print(optimum_price_and_profit)
        #print()
        #print("List of experts:")
        #print(auction.experts)
        #print()
        #print("Expert scores:")
        #print(auction.scores)
        #print()
        #print("Profit:")
        #print(auction.profit)
    print("average optimum profit:")
    print(total_optimum/num_trials)
    print()
    print("average actual profit:")
    print(total_profit/num_trials)
    print()
    print("average loss:")
    print((total_optimum/beta-total_profit)/num_trials)
    