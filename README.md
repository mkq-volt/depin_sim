### Generalized DePIN Simulation   

This repo is a simulation based on a dynamical system modeling a a general DePIN Economy. We use radCAD as the simulation engine, with streamlit as a frontend based on 
our 'default' parameter set. Streamlit related code is in `app.py`. 

The flow of the simulation can be found in `state_update_blocks.py`, which shows the step-by-step evolution of state variables and the policies that feed into them. 

#### Agent Actions
We model Providers as agents with their own capacities and costs. Providers make decisions weekly to stay or leave the protocol based on the rewards. 
User demand is aggregated into one stochastic function, the output of which is converted into bought tokens for purchase of service. The protocol divides the tokens to reward
Providers proportional to their service. Providers then sell the amount of tokens needed to cover their costs. 


#### Protocol and Environment Actions
Once the agents have acted, the protocol updates the price per unit of service based on the balance of supply and demand. Token price is updated based on net token flows, and the current reward 
rate is updated for prospective Providers to use in their decision to join the network. 

During all of these processes, there are a variety of parameters and coefficients that have been 'tuned' to create realistic relationships between different forces. 
These can be edited to reflect fine-tuned scenarios or add more optionality for input parameters. These can be found in `params.py`. 