def update_providers(params, substep, state_history, prev_state, policy_input):
    """
    updates the providers based on the policy input
    """
    joined_providers = policy_input['joined_providers']
    providers = prev_state['providers']

    return ('providers', joined_providers)

def update_total_capacity(params, substep, state_history, prev_state, policy_input):
    """
    updates the total capacity based on the policy input
    """
    new_providers = policy_input['joined_providers']

    new_capacity = sum([p.capacity for p in new_providers])

    return ('total_capacity', new_capacity)

def update_leaving_provider_selling(params, substep, state_history, prev_state, policy_input):
    """
    updates the leaving provider selling based on the policy input
    """
    sold = policy_input['leaving_sold']

    return ('net_flow', -sold)