import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model.params import params, initial_state
from model.state_update_blocks import state_update_blocks
from model.run import execute  # We'll need to adapt the notebook code into a module
import seaborn as sns



def plot_results(results):
    """Create plots with error bands"""

    
    # Set the style for all plots
    sns.set_style("whitegrid")
    sns.set_palette("crest")
    
    # make the plots a 2x2 grid
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(12, 10))
    
    # Price Plot
    sns.lineplot(data=results['token_price']['mean'], ax=ax1, label='Mean Price')
    ax1.fill_between(range(len(results['token_price']['mean'])),
                     results['token_price']['mean'] - results['token_price']['std'],
                     results['token_price']['mean'] + results['token_price']['std'],
                     alpha=0.2)
    ax1.set_title('Token Price Over Time', fontsize=12, pad=10)
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Price')
    
    # Supply Plot  
    sns.lineplot(data=results['circulating_supply']['mean'], ax=ax2, label='Mean Supply')
    ax2.fill_between(range(len(results['circulating_supply']['mean'])),
                     results['circulating_supply']['mean'] - results['circulating_supply']['std'],
                     results['circulating_supply']['mean'] + results['circulating_supply']['std'],
                     alpha=0.2)
    ax2.set_title('Token Supply Over Time', fontsize=12, pad=10)
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Supply')
    
    # Demand Plot
    sns.lineplot(data=results['demand']['mean'], ax=ax3, label='Mean Demand')
    ax3.fill_between(range(len(results['demand']['mean'])),
                     results['demand']['mean'] - results['demand']['std'],
                     results['demand']['mean'] + results['demand']['std'],
                     alpha=0.2)
    ax3.set_title('Service Demand Over Time', fontsize=12, pad=10)
    ax3.set_xlabel('Time Steps')
    ax3.set_ylabel('Demand')

    # Number of Providers Plot
    sns.lineplot(data=results['num_providers']['mean'], ax=ax4, label='Mean Number of Providers')
    ax4.fill_between(range(len(results['num_providers']['mean'])),
                     results['num_providers']['mean'] - results['num_providers']['std'],
                     results['num_providers']['mean'] + results['num_providers']['std'],
                     alpha=0.2)
    ax4.set_title('Number of Providers Over Time', fontsize=12, pad=10)
    ax4.set_xlabel('Time Steps')
    ax4.set_ylabel('Number of Providers')

    # Capacity Plot
    sns.lineplot(data=results['total_capacity']['mean'], ax=ax5, label='Mean Capacity')
    ax5.fill_between(range(len(results['total_capacity']['mean'])),
                     results['total_capacity']['mean'] - results['total_capacity']['std'],
                     results['total_capacity']['mean'] + results['total_capacity']['std'],
                     alpha=0.2)
    ax5.set_title('Total Capacity Over Time', fontsize=12, pad=10)
    ax5.set_xlabel('Time Steps')
    ax5.set_ylabel('Capacity')

    # Service Price Plot
    sns.lineplot(data=results['service_price']['mean'], ax=ax6, label='Mean Service Price')
    ax6.fill_between(range(len(results['service_price']['mean'])),
                     results['service_price']['mean'] - results['service_price']['std'],
                     results['service_price']['mean'] + results['service_price']['std'],
                     alpha=0.2)
    ax6.set_title('Service Price Over Time', fontsize=12, pad=10)
    ax6.set_xlabel('Time Steps')
    ax6.set_ylabel('Price')
    
    # Adjust layout and style
    plt.tight_layout()
    sns.despine()
    
    return fig

# Streamlit UI

# Set Streamlit theme
st.set_page_config(
    page_title="DePIN Simulation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.title('Generalized DePIN Simulation')
st.markdown("""
This simulation models a decentralized physical infrastructure network (DePIN) where:

1. **Providers** join the network based on expected rewards and contribute capacity
2. **Users** generate demand for the service, which affects service pricing
3. The **Protocol** manages token emissions to reward providers and maintain network stability
4. **Market Forces** (macro conditions) influence token price and participant behavior

The simulation runs multiple scenarios to show how different parameters and scenarios affect network growth and stability over time.

In essence, this is a model of a dynamical system, and this tool can help protocol designers find the 'optimal' parameters for 
their designs. In different scenarios, one can 'solve' for the Maximum weekly mint and percent burned to create a stable deflation, for example. 
Additionally, setting the percent burned to 0 can emulate a non Burn-and-Mint fee design. 
            
Like any model, the metrics tracked here are not predictive, but instead represent the relationships between the parameters
in a generalized DePIN economy. 

""")

# Input parameters
with st.sidebar:
    st.header('Simulation Parameters')
    
    st.markdown("""
    **Demand Type**: Choose how demand for the service evolves over time:
    - Volatile: Highly variable demand
    - Consistent: Stable, predictable demand
    - High-to-decay: Initially high demand that decays
    - Growth: Steadily increasing demand
    """)
    demand_type = st.radio(
        'Demand Type',
        ['volatile', 'consistent', 'high-to-decay', 'growth']
    )
    
    st.markdown("""
    **Macro Condition**: Set the overall market environment:
    - Bearish: Declining market conditions
    - Bullish: Growing market conditions
    """)
    macro_condition = st.radio(
        'Macro Condition',
        ['bearish', 'bullish']
    )
    
    st.markdown("""
    **Maximum Weekly Mint**: Maximum number of new tokens that can be created each week
    """)
    max_mint = st.number_input(
        'Maximum Mint Weekly',
        min_value=0,
        value=30_000,
        step=1000
    )
    
    st.markdown("""
    **Percent Burned**: Portion of tokens destroyed from circulation with each transaction
    """)
    percent_burned = st.slider(
        'Percent Burned',
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1
    )
    
    st.markdown("""
    **Initial Supply**: Starting amount of tokens in circulation
    """)
    initial_supply = st.number_input(
        'Initial Supply',
        min_value=100,
        value=10_000_000,
        step=100
    )
    
    run_button = st.button('Run Simulation')

# Run simulation when button is clicked
if run_button:
    params = params(demand_type, macro_condition, max_mint, percent_burned)
    initial_state = initial_state(initial_supply, demand_type)
    
    with st.spinner('Running simulations...'):
        results = execute(params, initial_state, state_update_blocks, 52, 20)
        fig = plot_results(results)
        st.pyplot(fig)