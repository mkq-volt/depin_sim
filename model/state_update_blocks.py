from model.environment.policies import *
from model.environment.state_updates import *
from model.agents.policies import *
from model.agents.state_updates import *


state_update_blocks = [
    {
        'label': 'macro and provider flow',
        'policies': {
            'providers': generate_providers,
            'demand': generate_weekly_demand
        },
        'variables': {
            'macro': update_macro,
            'providers': update_providers,
            'total_capacity': update_total_capacity,
            'demand': update_demand,
            'net_flow': update_leaving_provider_selling
        }
    },
    {
        'label': 'protocol',
        'policies': {
            'protocol_service': protocol_service
        },
        'variables': {
            'circulating_supply': update_circulating_supply,
            'reward_rate': update_reward_rate,
            'service_price': update_service_price,
            'net_flow': update_net_flow,
            'tokens_bought': update_tokens_bought,
            'tokens_sold': update_tokens_sold
        }
    },
    {
        'label': 'price',
        'policies': {
            'get_token_price': get_token_price
        },
        'variables': {
            'token_price': update_token_price
        }
    }
]