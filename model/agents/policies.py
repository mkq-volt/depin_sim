import numpy as np
from model.provider import Provider
def generate_providers(params, substep, state_history, prev_state):
    """
    generates providers based on the scenario params. we model this as a 
    poisson process.

    """
    
    inflow_rate = params.get('provider_inflow_rate', 1)
    providers = prev_state['providers']

    # draw the size of the candidate pool
    num_candidates = np.random.poisson(inflow_rate)
    candidates = [Provider() for _ in range(num_candidates)]

    joined = []

    for candidate in candidates:
        if candidate.decide_onboard(prev_state):
            joined.append(candidate)
    
    leaving = []
    sold = 0

    for provider in providers:
        decision = provider.decide_to_stay(prev_state)
        if not decision['decision']:
            leaving.append(provider)
            sold += decision['sold']

    
    new_providers = [p for p in providers if p not in leaving] + joined
    
    return {'joined_providers': new_providers, 'leaving_sold': sold}
