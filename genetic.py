import pandas as pd
import numpy as np
import random

# Definitions of changeable variables
DATA = 'data/2017-1.csv'

POP_SIZE = 100
TEAM_SIZE = 9
SALARY_CAP = 50000
NUM_QB = 1
NUM_RB = 2
NUM_WR = 3
NUM_TE = 1
NUM_FLEX = 1
NUM_DEF = 1
SEED = 0
LEAST_FIT = 0.1

#Initialize module variables
data = pd.read_csv(DATA)

# Population dataframe.  PLAYERS 1 - 9 MUST OCCUPY THE 1ST 9 COLUMNS!
population = pd.DataFrame(index=np.arange(0, POP_SIZE + 1), columns=('Player1', 'Player2','Player3','Player4','Player5','Player6',  \
                          'Player7', 'Player8', 'Player9', 'Gen_born', 'Points', 'Salary', 'Fitness', 'Compliant', 'Selection_chance'))

# Various stats describing population health
population_stats = pd.DataFrame(index=np.arange(0, 1), columns=('Avg_points', 'Avg_salary', 'Avg_fitness', 'Total_fitness', 'Max_fitness', 'Num_compliant', 'Avg_age'))

# Main function that executes the genetci algorithm
def main():
    setup()
    crossover()
    print("Success")

# Performs the crossover process, produces new child
def crossover():
    parents = select_parents()
    chromosome_a = population.iloc[parents[0]].values.tolist()
    chromosome_b = population.iloc[parents[1]].values.tolist()
    
    print(chromosome_a)
    print(chromosome_b)

# Selects parents to for offspring production
def select_parents():
    parents_selected = 0
    selected = []
    
    while (parents_selected < 2):
        for i in np.arange(0, POP_SIZE):
            if random_bool(population.at[i, 'Selection_chance'] * 100):
                parents_selected += 1
                selected.append(i)
                break
            
    return selected

# Initial setup of data.  Create random population, calculate all fitnesses, update stats
def setup():
    
    population_stats.at[0, 'Max_fitness'] = LEAST_FIT
    random.seed(SEED)
    
    #Fill up our population with random teams
    seed = SEED
    for i in np.arange(0, POP_SIZE):
        for j in range(TEAM_SIZE):
            sample = data.sample(random_state = seed)['GID'].values[0]
            population.iloc[i,j] = sample
            seed += 1
        population.at[i, 'Gen_born'] = 0
            
    #Calculate the fitness of our starting teams
    for i in np.arange(0, POP_SIZE):
        calculate_fitness(i)
        
    update_all_stats()
    
    for i in np.arange(0, POP_SIZE):
        update_selection_probability(i)
    
        
#Update the fitness and related information for a given individual referred to by index within the population          
def calculate_fitness(index):
    chromosome = population.iloc[index]

    fitness = 0
    team_points = 0
    team_salary = 0
    pos_count = [0, 0, 0, 0, 0] # QB, RB, WR, TE, Def
    compliant = True
    
    for i in range(TEAM_SIZE):
        player_data = data.loc[data['GID'] == chromosome.iloc[i]]
        team_points += player_data.iloc[0]['DK points']
        team_salary += player_data.iloc[0]['DK salary']
        pos_count[pos_dict(player_data.iloc[0]['Pos'])] += 1
    
    fitness = (team_points * 1000)
    
    if team_salary > SALARY_CAP:
        fitness -= (team_salary - SALARY_CAP)
        compliant = False
        
    if pos_count[0] > NUM_QB:
        fitness -= (pos_count[0] - NUM_QB) * 2000
        compliant = False
        
    if pos_count[1] > NUM_RB:
        fitness -= (pos_count[1] - NUM_RB + 1) * 2000
        compliant = False
        
    if pos_count[2] > NUM_WR:
        fitness -= (pos_count[2] - NUM_WR + 1) * 2000
        compliant = False
        
    if pos_count[3] > NUM_TE:
        fitness -= (pos_count[3] - NUM_TE + 1) * 2000
        compliant = False
        
    if pos_count[4] > NUM_DEF:
        fitness -= (pos_count[4] - NUM_DEF) * 2000
        compliant = False
        
    if pos_count[1] + pos_count[2] + pos_count[3] > NUM_RB + NUM_WR + NUM_QB:
        fitness -= (pos_count[1] + pos_count[2] + pos_count[3] - NUM_RB + NUM_WR + NUM_QB) * 2000
        compliant = False
        
    if compliant == True:
        fitness += 10000
    
    if fitness < LEAST_FIT:
        fitness = LEAST_FIT
        
    if fitness > population_stats.at[0, 'Max_fitness']:
            population_stats.at[0, 'Max_fitness'] = fitness
    
    population.at[index, 'Points'] = team_points
    population.at[index, 'Salary'] = team_salary
    population.at[index, 'Fitness'] = fitness
    population.at[index, 'Compliant'] = compliant

#Update the stats for all population.  Done at start of program
def update_all_stats():
    fitness = 0
    points = 0
    age = 0
    salary = 0
    compliant = 0
    
    for i in range(POP_SIZE):
        points += population.at[i, 'Points']
        salary += population.at[i, 'Salary']
        age += population.at[i, 'Gen_born']
        fitness += population.at[i, 'Fitness']
        if population.at[i, 'Compliant'] == True:
            compliant += 1

    population_stats.at[0, 'Avg_points'] = points / POP_SIZE
    population_stats.at[0, 'Avg_salary'] = salary / POP_SIZE
    population_stats.at[0, 'Avg_age'] = age / POP_SIZE
    population_stats.at[0, 'Avg_fitness'] = fitness / POP_SIZE
    population_stats.at[0, 'Total_fitness'] = fitness
    population_stats.at[0, 'Num_compliant'] = compliant

# Update the stats dataframe by removing information of least fit individual and adding information of new child
#def update_stats(add, remove):


# Update the selection chance for a given index    
def update_selection_probability(index):
    probability = population.at[index, 'Fitness'] / population_stats.at[0, 'Total_fitness']
    population.at[index, 'Selection_chance'] = probability
    
# Returns random bool based on percentage
def random_bool(percent):
    return random.randrange(100) < percent
        

def pos_dict(x):
    return {
         'QB': 0,
         'RB': 1,
         'WR': 2,
         'TE': 3,
         'Def': 4,
    }[x]
        

if __name__ == '__main__':
    main()