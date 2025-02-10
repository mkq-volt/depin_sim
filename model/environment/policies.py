import numpy as np

def generate_weekly_demand(params, substep, state_history, prev_state) -> float:
    """
    generates demand based on the scenario params

    D_t = scale * service_price^price_elasticity + noise

    macro effect is added in the state update fn
    """
    service_price = prev_state['service_price']
    type = params.get('demand_type', 1)
    price_elasticity = params.get('demand_price_elasticity', 1)
    noise = np.random.uniform(0.97, 1.03)
    base_demand = params.get('base_demand', 1)

    price_adjustment = 1 / (service_price ** price_elasticity) if service_price > 0 else 1
    price_adjustment = np.exp(-0.5 * price_elasticity * np.log(service_price))

    if type == 'consistent':
        demand = base_demand * price_adjustment * noise
    elif type == 'growth':
        growth_rate = params.get('demand_growth_rate', .001)
        prev_demand = prev_state['demand']
        demand = prev_demand * (1 + growth_rate * price_adjustment) * noise
    elif type == 'high_to_decay':
        decay_rate = params.get('demand_decay_rate', 1)
        t = len(state_history)
        demand = base_demand * np.exp(-decay_rate * t) * price_adjustment * noise
    elif type == 'volatile':
        volatility = params.get('demand_volatility', 1)
        demand = base_demand * (1 + np.random.uniform(-volatility, volatility)) * price_adjustment * noise
    else:
        raise ValueError(f"Invalid demand type: {type}")
    return {'demand': demand}

def get_token_price(params, substep, state_history, prev_state) -> float:
    """ 
    gets the updated token price based on net flows 

    P_t = P_{t-1} * [1 + price_sensitivity * net flow / circulating supply]
    """

    price = prev_state['token_price']
    net_flow = prev_state['net_flow']
    circulating_supply = prev_state['circulating_supply']
    flows_sensitivity = params.get('tp_flows_sensitivity', 1)

    flows_factor = np.exp(flows_sensitivity * net_flow / circulating_supply)

    new_price = price * flows_factor

    return {'price': new_price}


def protocol_service(params, substep, state_history, prev_state):
    """
    demand is converted to tokens bought for service and distributed as rewards to 
    the providers proportional to their capacity
    """
    
    demand = prev_state['demand']
    service_price = prev_state['service_price']
    supply = prev_state['circulating_supply']
    providers = prev_state['providers']
    capacity = prev_state['total_capacity']
    price = prev_state['token_price']
    max_mint = params.get('max_mint', 1)
    percent_burned = params.get('percent_burned', 0)


    tokens_bought = demand * service_price / price
    tokens_burned = tokens_bought * percent_burned
    minted_tokens = min(tokens_bought, max_mint)

    reward_rate = minted_tokens / capacity if capacity > 0 else 0
    tokens_sold = 0
    
    for provider in providers:
       tokens_sold += provider.get_reward(prev_state, reward_rate * provider.capacity)
    
    return {
            'tokens_bought': tokens_bought,
            'tokens_sold': tokens_sold,
            'reward_rate': reward_rate,
            'minted_tokens': minted_tokens,
            'burned_tokens': tokens_burned
        }


