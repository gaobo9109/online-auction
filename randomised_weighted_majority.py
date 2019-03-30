import utils
import math
import random

class RandomWeightedMajority:
    def __init__(self, beta, max):
        self.alpha = int(math.sqrt(beta))
        self.max = max
        self.experts = [self.alpha ** i for i in range(int(math.log(max, self.alpha))+1)]
        self.scores = [0 for i in range(len(self.experts))]
        self.cumulative_weights = 0
        self.compute_weights()
        self.profit = 0

    def compute_weights(self):
        weights = []
        for score in self.scores:
            weights.append(self.alpha ** (score / self.max))
        sum_weights = sum(weights)
        norm_weight = [weight / sum_weights for weight in weights]
        for i in range(1, len(weights)):
            norm_weight[i] = norm_weight[i] + norm_weight[i-1]
        self.cumulative_weights = norm_weight

    def recommend(self):
        recommended_price = self.experts[self.random_select_expert()]
        return recommended_price

    def update_score(self,bid_price):
        for i in range(len(self.experts)):
            if bid_price > self.experts[i]:
                self.scores[i] += self.experts[i]

    def random_select_expert(self):
        rand = random.random()
        index = 0
        cumulative_sum = 0

        while cumulative_sum < rand:
            cumulative_sum = self.cumulative_weights[index]
            index += 1
        return index - 1

    def step(self, bid_price):
        price = self.recommend()
        profit = price if price < bid_price else 0
        self.profit += profit
        self.update_score(bid_price)
        self.compute_weights()    


if __name__ == "__main__":
    auction = RandomWeightedMajority(4, 128)
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