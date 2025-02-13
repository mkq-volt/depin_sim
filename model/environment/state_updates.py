import numpy as np


def update_service_price(params, substep, state_history, prev_state, policy_input):
    """
    calculates price from demand, cost of service floor, and a macro adjustment. 

    p_{t+1} = max(cost_floor, p_t *  [demand_sensitivity * (demand_t - capacity_t) / capacity_t] * macro_adjustment)

    where the macro adjustment is (macro_sensitivity * macro_t)
    """
    capacity = prev_state['total_capacity']
    base_demand = params.get('base_demand', 1)
    price_elasticity = params.get('demand_price_elasticity', 1)
    cost_floor = params.get('cost_floor', 0.1)
    cost_ceiling = params.get('cost_ceiling', 1)

    noise = np.random.uniform(0.97, 1.03)  # Optional: keep noise for some randomness
    market_clearing_price = (capacity / (base_demand * noise)) ** (-1 / price_elasticity)

    # Ensure the price doesn't go below the cost floor
    new_price = max(min(market_clearing_price, cost_ceiling), cost_floor)

    return ('service_price', new_price)

def update_demand(params, substep, state_history, prev_state, policy_input):
    """
    updates demand based on the service price and a macro adjustment
    """
    demand = policy_input['demand']
    macro = prev_state['macro']
    demand_macro_sensitivity = params.get('demand_macro_sensitivity', 1)

    return ('demand', demand * (1 + macro * demand_macro_sensitivity))

def update_token_price(params, substep, state_history, prev_state, policy_input):
    """ 
    updates the token price based on net flows and macro

    P_t = P_{t-1} * [1 + (net flow / circulating supply)] * macro
    """

    new_price = policy_input['price'] * prev_state['macro']
    return ('token_price', new_price)

def update_reward_rate(params, substep, state_history, prev_state, policy_input):
    """
    updates the reward per unit of capacity rewarded in this week. This is 
    a product of the u
    """

    reward_rate = policy_input['reward_rate']

    return ('reward_rate', reward_rate)

def update_circulating_supply(params, substep, state_history, prev_state, policy_input):
    """
    updates the circulating supply based on the policy input
    """
    curr_circulating_supply = prev_state['circulating_supply']
    minted_tokens = policy_input['minted_tokens']
    burned_tokens = policy_input['burned_tokens']


    return ('circulating_supply', curr_circulating_supply + minted_tokens - burned_tokens)

def update_net_flow(params, substep, state_history, prev_state, policy_input):
    """
    updates the net flow based on the policy input
    """
    curr_net_flow = prev_state['net_flow']
    tokens_bought = policy_input['tokens_bought']
    tokens_sold = policy_input['tokens_sold']

    return ('net_flow', curr_net_flow + tokens_bought - tokens_sold)

def update_macro(params, substep, state_history, prev_state, policy_input):
    """
    updates the macro based on the policy input
    """
    macro_condition = params.get('macro_condition', 1)

    if macro_condition == 'bullish':
        macro = np.random.uniform(0.995, 1.011)
    elif macro_condition == 'bearish':
        macro = np.random.uniform(0.995, 1.0049)
    else:
        macro = np.random.uniform(0.998, 1.002)

    return ('macro', macro)

def update_tokens_bought(params, substep, state_history, prev_state, policy_input):
    """
    updates the tokens bought based on the policy input
    """
    return ('tokens_bought', policy_input['tokens_bought'])

def update_tokens_sold(params, substep, state_history, prev_state, policy_input):
    """
    updates the tokens sold based on the policy input
    """
    return ('tokens_sold', policy_input['tokens_sold'])