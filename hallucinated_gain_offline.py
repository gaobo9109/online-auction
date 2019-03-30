import utils
import math
import random

class OfflineHallucinatedGain:
    def __init__(self, beta, max):
        self.alpha = int(math.sqrt(beta))
        self.max = max
        self.experts = [self.alpha ** i for i in range(int(math.log(max, self.alpha))+1)]
        self.scores = [expert * utils.coin_flip() for expert in self.experts]
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
    auction = OfflineHallucinatedGain(4, 128)
    seq = utils.gen_bid(10, 128)
    optimum_price_and_profit = utils.compute_optimum_price_and_profit(seq)
    for bid_price in seq:
        auction.step(bid_price)
    print("sequence of bidders:")
    print(seq)
    print()
    print("Optimum price and profit:")
    print(optimum_price_and_profit)
    print()
    print("List of experts:")
    print(auction.experts)
    print()
    print("Expert scores:")
    print(auction.scores)
    print()
    print("Profit:")
    print(auction.profit)
    