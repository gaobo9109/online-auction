import utils
import math
import random
from collections import deque

class UnboundedDeterministic:
    def __init__(self, beta):
        self.alpha = int(math.sqrt(beta))
        self.experts = deque()
        self.scores = deque()
        self.profit = 0
        self.step_count = 0

    def recommend(self):
        if not self.experts:
            return 1

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

    def add_experts(self, bid_price):
        k = int(math.log(bid_price, self.alpha))
        expert = self.alpha ** k
        if expert in self.experts:
            return

        if not self.experts:
            self.experts.append(expert)
            self.scores.append(0)
        elif expert < self.experts[0]:
            lowest_expert = expert if k == 0 else self.alpha ** (k-1)
            current_expert = self.experts[0]
            while current_expert > lowest_expert:
                current_expert = int(current_expert / self.alpha)
                self.experts.appendleft(current_expert)
                self.scores.appendleft(self.step_count * current_expert)
        elif expert > self.experts[-1]:
            highest_expert = expert
            current_expert = self.experts[-1]
            while current_expert < highest_expert:
                current_expert = current_expert * self.alpha
                self.experts.append(current_expert)
                self.scores.append(0)


    def step(self, bid_price):
        price = self.recommend()
        profit = price if price < bid_price else 0
        self.profit += profit
        self.update_score(bid_price)
        self.add_experts(bid_price)
        self.step_count += 1

if __name__ == "__main__":
    auction = UnboundedDeterministic(4)
    seq = utils.gen_uniform_random_bid(10, 200)
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

    