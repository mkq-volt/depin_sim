"""
providers are initialized with the following:
    - an amount of weekly capacity they generate
    - their cost per unit of capacity in usd
    - their token balance in terms of the token
    - a history of their weekly rewards
 
every week, they provide their service to the market at a protocol-set price and
sell their capacity to the protocol, which rewards them for maintaining their service in the 
protocol token.

every week, they evaluate their rewards and decide whether to stay in the protocol or leave.
when they leave, they sell their tokens on the market.
"""
import numpy as np

class Provider:
    def __init__(self, capacity_bias=1):
        self.capacity = np.random.lognormal(5, 0.7) * capacity_bias
        self.cost_per_unit = np.random.uniform(0.05, 0.2)
        self.token_balance = 0
        self.reward_history = []
        self.onboarded = False
        

    def __str__(self):
        return f"Provider(capacity={self.capacity}, cost_per_unit={self.cost_per_unit}, token_balance={self.token_balance})"

    def get_profit(self, price) -> float:
        """
        returns the profit of the provider in usd. 
        can be negative
        """
        cost = self.cost_per_unit * self.capacity
        latest_reward = self.reward_history[-1][1] if len(self.reward_history) > 0 else cost + 1
        return latest_reward - cost
        # return self.token_balance > 0
    def sell_for_costs(self, price):
        """
        sells tokens to cover their costs for the week 
        """
        cost_in_token = self.cost_per_unit * self.capacity
        tokens_sold = cost_in_token / price
        self.token_balance -= tokens_sold

        return tokens_sold

    def decide_to_stay(self, state):
        """
        providers decide to stay or leave
        """
        
        staying = self.get_profit(state['token_price']) > 0
        sold = 0

        if not staying: 
          sold = self.token_balance
          self.onboarded = False
          
        
        return {
            'decision': staying,
            'sold': sold
        }
    

    def decide_onboard(self, state):
        """
        candidates decide to join if the current token price times their 
        capacity exceeds their cost per unit of capacity
        """

        token_price = state['token_price']
        reward_per_unit = state['reward_rate']

        revenue = token_price * reward_per_unit * self.capacity
        cost = self.cost_per_unit * self.capacity
        return revenue > cost

    def get_reward(self, state, reward):
        """
        providers get rewards, cover their costs, and decide to stay or leave
        """
        self.reward_history.append((reward, reward * state['token_price']))
        self.token_balance += reward

        sold = self.sell_for_costs(state['token_price'])

        return sold