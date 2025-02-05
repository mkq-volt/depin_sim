from radcad import Simulation, Model, Engine, Experiment
import pandas as pd
from .params import params, initial_state
import time
import logging

def execute(params, initial_state, state_update_blocks, T, R):


    model = Model(initial_state=initial_state, state_update_blocks=state_update_blocks, params=params)
    simulation = Simulation(model=model, timesteps=T, runs=R)
    experiment = Experiment([simulation])
    experiment.engine.exceptions = False
    experiment.engine.drop_substeps = True
    experiment.engine.deepcopy = True

    start_time = time.time()
    result = experiment.run()
    end_time = time.time()
    logging.info(f"simulation completed in {end_time - start_time:.2f} seconds")

    df = pd.DataFrame(result)
    
    df = post_process(df)
    

    return df


def post_process(df):
    # extract numeric information from provider column and drop it
    # extract number of providers, average capacity, average reward rate, average service price

    df['num_providers'] = df['providers'].apply(lambda x: len(x))
    df['avg_capacity'] = df['providers'].apply(lambda x: sum([p.capacity for p in x]) / len(x))
    

    df = df.drop(columns=['providers'])
    
    df = df.groupby(['timestep']).agg(['mean', 'std']).reset_index()
    
    
    return df