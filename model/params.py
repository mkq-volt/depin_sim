from .provider import Provider

def params(demand_type: str, macro_condition: str, max_mint: int, percent_burned: float):
    
    demand = demand_scenarios(demand_type)

    return {
    'provider_inflow_rate': 10,
    'price_sensitivity': 0.1,
    'max_mint': max_mint,
    'sp_demand_sensitivity': 0.9,
    'sp_macro_sensitivity': 0.2,
    'tp_flows_sensitivity': 1,
    'tp_macro_sensitivity': 0.1,
    'macro_condition': macro_condition,
    'percent_burned': percent_burned,
    'demand_macro_sensitivity': 0.02,
    'cost_floor': 0.1,
    'cost_ceiling': 1,
    **demand
}

def demand_scenarios(type: str):
    if type == 'consistent':
        return {
            'demand_type': 'consistent',
            'base_demand': 12_000,
            'demand_price_elasticity': 0.1,
            'demand_growth_rate': 0.025,
            'demand_decay_rate': 0,
            'demand_volatility': 0
        }
    elif type == 'growth':
        return {
            'demand_type': 'growth',
            'base_demand': 4_000,
            'demand_price_elasticity': 0.4,
            'demand_growth_rate': 0.001,
            'demand_decay_rate': 0,
            'demand_volatility': 0
        }
    elif type == 'high-to-decay':
        return {
            'demand_type': 'high_to_decay',
            'base_demand': 15_000,
            'demand_price_elasticity': 0.4,
            'demand_growth_rate': 0,
            'demand_decay_rate': 0.02,
            'demand_volatility': 0
        }
    elif type == 'volatile':
        return {
            'demand_type': 'volatile',
            'base_demand': 12_000,
            'demand_price_elasticity': 1.2,
            'demand_growth_rate': 0,
            'demand_decay_rate': 0,
            'demand_volatility': 1.2
        }
    

def initial_state(initial_supply: float, demand_type: str):
    demand = demand_scenarios(demand_type)
    providers = [Provider(capacity_bias=1.3) for i in range(10)]
    capacity = sum([p.capacity for p in providers])
    
    return {
        'providers': providers,
        'service_price': .5,
        'demand': demand['base_demand'],
        'token_price': 3,
        'reward_rate': .3,
        'circulating_supply': initial_supply,
        'macro': 1,
        'total_capacity': capacity,
        'net_flow': 0,
        'tokens_bought': 0,
        'tokens_sold': 0
    }