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
    beta_arr = [1.1+0.1*i for i in range(30)]
    h_arr = [10,20,30,40,50,100,200,500,1000,5000]
    n_arr = [5,10,20,50,100,150,200,500,1000,5000]
    num_trials=100
    for beta in beta_arr:
        for h in h_arr:
            for n in n_arr:
                print("beta  h  n")
                print(str(round(beta,1))+" " + str(h) + " " + str(n)+"\n")
                total_optimum = 0
                total_profit = 0
                worst_loss = -h*n-1
                for i in range (num_trials):
                    auction = BoundedExpertLearning(beta, h) #
                    seq = utils.gen_uniform_random_bid(n, h) #
                    optimum_price_and_profit = utils.compute_optimum_price_and_profit(seq)
                    for bid_price in seq:
                        auction.step(bid_price)
                    optimum_profit = optimum_price_and_profit[1]
                    total_optimum+=optimum_profit
                    total_profit+=auction.profit
                    worst_loss=max(worst_loss, optimum_profit/beta-auction.profit)
                print("average optimum profit:")
                print(round(total_optimum/num_trials,3))

                print("average actual profit:")
                print(round(total_profit/num_trials,3))

                ## can compute later, might not need this
                print("average loss:")
                print(round((total_optimum/beta-total_profit)/num_trials,3))
                ## can compute later, might not need this
                print("average loss per bid:") 
                print(round((total_optimum/beta-total_profit)/num_trials/n,3))
                
                print("worst loss:")
                print(round(worst_loss,3))

                ## can compute later, might not need this
                print("average loss:")
                print(round(worst_loss/n,3))
                print()