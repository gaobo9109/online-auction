import utils
import math
import random
import pandas as pd

class BoundedHallucinatedGain:
    def __init__(self, beta, max):
        self.alpha = float(math.sqrt(beta))
        self.max = max
        self.experts = [self.alpha ** i for i in range(int(math.log(max, self.alpha))+1)]
        self.scores = [expert * utils.coin_flip(beta) for expert in self.experts]
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
    beta_arr = [1.1+0.1*i for i in range(30)]
    h_arr = [10,20,30,40,50,100,200,500,1000,5000,10000]
    n_arr = [5,10,20,50,100,150,200,500,1000]
    num_trials=50
    rows = []
    for beta in beta_arr:
        for h in h_arr:
            for n in n_arr:
                print("beta  h  n")
                print(str(round(beta,1))+" " + str(h) + " " + str(n))
                total_optimum = 0
                total_profit = 0
                worst_loss = -h*n-1
                for i in range (num_trials):
                    auction = BoundedHallucinatedGain(beta, h) #
                    seq = utils.gen_uniform_random_bid(n, h) #
                    optimum_price_and_profit = utils.compute_optimum_price_and_profit(seq)
                    for bid_price in seq:
                        auction.step(bid_price)
                    optimum_profit = optimum_price_and_profit[1]
                    total_optimum+=optimum_profit
                    total_profit+=auction.profit
                    worst_loss=max(worst_loss, optimum_profit/beta-auction.profit)
                
                average_optimum_profit = round(total_optimum / num_trials, 3)
                print("average optimum profit:")
                print(average_optimum_profit)

                average_actual_profit = round(total_profit/num_trials,3)
                print("average actual profit:")
                print(average_actual_profit)

                ## can compute later, might not need this
                average_loss = round((total_optimum/beta-total_profit)/num_trials,3)
                print("average loss:")
                print(average_loss)

                ## can compute later, might not need this
                average_loss_per_bid = round((total_optimum/beta-total_profit)/num_trials/n,3)
                print("average loss per bid:") 
                print(average_loss_per_bid)
                
                worst_loss = round(worst_loss, 3)
                print("worst loss:")
                print(worst_loss)

                ## can compute later, might not need this
                average_worst_loss = round(worst_loss/n, 3)
                print("average worst loss:")
                print(average_worst_loss)
                print()

                row = [beta, h, n, average_optimum_profit, average_actual_profit, average_loss,
                       average_loss_per_bid, worst_loss, average_worst_loss]
                rows.append(row)

    df = pd.DataFrame(rows, columns=["Beta Value", "Max Bid", "Num Bids", "Average Optimum Profit", 
                                     "Average Actual Profit", "Average Loss", "Average Loss Per Bid", 
                                     "Worst Loss", "Average Worst Loss"])
    df.to_csv("hallucinated_gain_bounded.csv")