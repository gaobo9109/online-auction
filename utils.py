import random

def gen_bid(num, max):
    result = []
    for i in range(num):
        result.append(random.randint(1, max))
    return result

def compute_optimum_price_and_profit(prices):
    sorted_prices = sorted(prices)
    profits = [price * (len(prices)-i) for i, price in enumerate(sorted_prices)]
    optimum_price_and_profit = max(zip(sorted_prices, profits), key=lambda x: x[1])
    return optimum_price_and_profit

def coin_flip():
    head_count = 0
    tail_count = 0
    while tail_count == 0:
        rand = random.randint(0, 1)
        if rand == 1:
            head_count += 1
        else:
            tail_count += 1
    return head_count