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
    ax2.set_xlabel('Weeks')
    ax2.set_ylabel('Supply')
    
    # Demand Plot
    sns.lineplot(data=results['demand']['mean'], ax=ax3, label='Mean Demand')
    ax3.fill_between(range(len(results['demand']['mean'])),
                     results['demand']['mean'] - results['demand']['std'],
                     results['demand']['mean'] + results['demand']['std'],
                     alpha=0.2)
    ax3.set_title('Service Demand Over Time', fontsize=12, pad=10)
    ax3.set_xlabel('Weeks')
    ax3.set_ylabel('Units of Capacity Demanded')

    # Number of Providers Plot
    sns.lineplot(data=results['num_providers']['mean'], ax=ax4, label='Mean Number of Providers')
    ax4.fill_between(range(len(results['num_providers']['mean'])),
                     results['num_providers']['mean'] - results['num_providers']['std'],
                     results['num_providers']['mean'] + results['num_providers']['std'],
                     alpha=0.2)
    ax4.set_title('Number of Providers Over Time', fontsize=12, pad=10)
    ax4.set_xlabel('Weeks')
    ax4.set_ylabel('Number of Providers')

    # Capacity Plot
    sns.lineplot(data=results['total_capacity']['mean'], ax=ax5, label='Mean Capacity')
    ax5.fill_between(range(len(results['total_capacity']['mean'])),
                     results['total_capacity']['mean'] - results['total_capacity']['std'],
                     results['total_capacity']['mean'] + results['total_capacity']['std'],
                     alpha=0.2)
    ax5.set_title('Total Units of Capacity Over Time', fontsize=12, pad=10)
    ax5.set_xlabel('Weeks')
    ax5.set_ylabel('Units of Capacity')

    # Service Price Plot
    sns.lineplot(data=results['service_price']['mean'], ax=ax6, label='Mean Service Price')
    ax6.fill_between(range(len(results['service_price']['mean'])),
                     results['service_price']['mean'] - results['service_price']['std'],
                     results['service_price']['mean'] + results['service_price']['std'],
                     alpha=0.2)
    ax6.set_title('Service Price Over Time', fontsize=12, pad=10)
    ax6.set_xlabel('Weeks')
    ax6.set_ylabel('Price per Unit of Capacity')
    
    # Adjust layout and style
    plt.tight_layout()
    sns.despine()
    
    return fig

# Initialize session state for storing simulation history
if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

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
2. **Users** generate demand for the service and purchase tokens to pay for it
3. The **Protocol** manages token emissions/burns and service pricing to maintain network stability
4. **Market Forces** (macro conditions) influence token price and participant behavior
            
This is a model of a dynamical system, and this tool can help protocol designers find the 'optimal' parameters for 
their designs. In different scenarios, one can 'solve' for the maximum weekly mint and percent burned to create a stable deflation, for example.  

The simulation runs multiple scenarios to show how they affect network growth and stability over time. Each simulation is run for 52 weeks
20 times. The plots are the aggregated results, showing the variance as the shaded area.



""")

# Input parameters
with st.sidebar:
    st.header('Simulation Parameters')
    demand_type = st.radio(
        '***Demand Type***',
        [
            'volatile',
            'consistent',
            'high-to-decay', 
            'growth'
        ],
        format_func=lambda x: {
            'volatile': 'volatile: highly variable demand',
            'consistent': 'consistent: stable, predictable demand',
            'high-to-decay': 'high-to-decay: initially high demand that decays', 
            'growth': 'growth: steadily increasing demand'
        }[x]
    )
    macro_condition = st.radio(
        '***Macro Condition***',
        [
            'bearish',
            'bullish'
        ],
        format_func=lambda x: {
            'bearish': 'bearish: declining market conditions',
            'bullish': 'bullish: growing market conditions'
        }[x]
    )
    
    max_mint = st.number_input(
        '***Maximum Mint Weekly***',
        min_value=0,
        value=3500,
        step=1000
    )

    percent_burned = st.slider(
        '***Percent of Tokens Burned***',
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1
    )
    
    initial_supply = st.number_input(
        '***Initial Supply***',
        min_value=100,
        value=1_000_000,
        step=10_000
    )
    
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button('***Run Simulation***')
    with col2:
        clear_button = st.button('Clear History')

# Clear simulation history if clear button is pressed
if clear_button:
    st.session_state.simulation_history = []
    st.query_params.clear()

# Run simulation when button is clicked
if run_button:
    # Create a dictionary to store the current run's parameters
    current_params = {
        'demand_type': demand_type,
        'macro_condition': macro_condition,
        'max_mint': max_mint,
        'percent_burned': percent_burned,
        'initial_supply': initial_supply
    }


    params_config = params(demand_type, macro_condition, max_mint, percent_burned)
    initial_state_config = initial_state(initial_supply, demand_type)
    
    with st.spinner('Running simulations...'):
        results = execute(params_config, initial_state_config, state_update_blocks, 52, 20)
        fig = plot_results(results)
        
        # Add new simulation to history
        st.session_state.simulation_history.append({
            'parameters': current_params,
            'figure': fig
        })
        
        # Keep only the last 5 runs
        if len(st.session_state.simulation_history) > 5:
            st.session_state.simulation_history.pop(0)

# Display simulation history
if st.session_state.simulation_history:
    st.markdown("---")
    st.write(f"***Showing {len(st.session_state.simulation_history)} most recent simulation runs***")
    for i, run in enumerate(reversed(st.session_state.simulation_history)):
        run_number = len(st.session_state.simulation_history) - i
        st.subheader(f"Run #{run_number} Parameters:")
        
        # Display parameters in a more readable format
        col1, col2 = st.columns(2)
        with col1:
            st.write("Demand Type: `" + str(run['parameters']['demand_type']) + "`")
            st.write("Macro Condition: `" + str(run['parameters']['macro_condition']) + "`")
            st.write("Maximum Mint Weekly:", run['parameters']['max_mint'])
        with col2:
            st.write("Percent Burned:", run['parameters']['percent_burned'])
            st.write("Initial Supply:", run['parameters']['initial_supply'])
        
        # Display the plot
        st.pyplot(run['figure'])
        
        # Add a divider between runs
        if i < len(st.session_state.simulation_history) - 1:
            st.markdown("---")




# Add a spacer to push the disclaimer to the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("*Like any model, the metrics tracked here are not predictive, but instead represent the relationships between the parameters in a generalized DePIN economy.*")
