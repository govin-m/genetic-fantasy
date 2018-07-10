import pandas as pd
import numpy as np

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
population = pd.DataFrame(index=np.arange(0, POP_SIZE), columns=('Player1',   \
                          'Player2','Player3','Player4','Player5','Player6',  \
                          'Player7', 'Player8', 'Player9', 'Points', 'Salary',\
                          'Fitness', 'Norm_fitness', 'Breed_chance',          \
                          'Compliant'))
population_stats = pd.DataFrame(index=np.arange(0, 1), columns=('Avg_points', \
                                'Avg_salary', 'Avg_fitness', 'Max_fitness'))

# Main function that executes the genetci algorithm
def main():
    setup()
    


def setup():
    
    population_stats.at[0, 'Max_fitness'] = LEAST_FIT
    
    #Fill up our population with random teams
    seed = SEED
    for i in np.arange(0, POP_SIZE):
        for j in range(TEAM_SIZE):
            sample = data.sample(random_state = seed)['GID'].values[0]
            population.iloc[i,j] = sample
            seed += 1
            
    #Calculate the fitness of our starting teams
    for i in np.arange(0, POP_SIZE):
        calculate_fitness(i)
        
    update_stats()
        
        
            
def calculate_fitness(index):
    chromosome = population.iloc[index]

    fitness = 0
    team_points = 0
    team_salary = 0
    pos_count = [0, 0, 0, 0, 0] # QB, RB, WR, TE, Def
    compliant = true
    
    for i in range(TEAM_SIZE):
        player_data = data.loc[data['GID'] == chromosome.iloc[i]]
        team_points += player_data.iloc[0]['DK points']
        team_salary += player_data.iloc[0]['DK salary']
        pos_count[pos_dict(player_data.iloc[0]['Pos'])] += 1
    
    fitness = (team_points * 1000)
    
    if team_salary > SALARY_CAP:
        fitness -= (team_salary - SALARY_CAP)
        compliant = false
        
    if pos_count[0] > NUM_QB:
        fitness -= (pos_count[0] - NUM_QB) * 2000
        compliant = false
        
    if pos_count[1] > NUM_RB:
        fitness -= (pos_count[1] - NUM_RB + 1) * 2000
        compliant = false
        
    if pos_count[2] > NUM_WR:
        fitness -= (pos_count[2] - NUM_WR + 1) * 2000
        compliant = false
        
    if pos_count[3] > NUM_TE:
        fitness -= (pos_count[3] - NUM_TE + 1) * 2000
        compliant = false
        
    if pos_count[4] > NUM_DEF:
        fitness -= (pos_count[4] - NUM_DEF) * 2000
        compliant = false
        
    if pos_count[1] + pos_count[2] + pos_count[3] > NUM_RB + NUM_WR + NUM_QB:
        fitness -= (pos_count[1] + pos_count[2] + pos_count[3] - NUM_RB +     \
                    NUM_WR + NUM_QB) * 2000
        compliant = false
    
    if fitness < LEAST_FIT:
        fitness = LEAST_FIT
        
    if fitness > population_stats.at[0, 'Max_fitness']:
            population_stats.at[0, 'Max_fitness'] = fitness
    
    population.at[index, 'Points'] = team_points
    population.at[index, 'Salary'] = team_salary
    population.at[index, 'Fitness'] = fitness
    population.at[index, 'Compliant'] = compliant

def update_stats():
    fitness = 0
    points = 0
    salary = 0
    for i in range(POP_SIZE):
        chromosome = population.iloc[i]
        points += chromosome.iloc[9]
        salary += chromosome.iloc[10]
        fitness += chromosome.iloc[11]
    
    population_stats.at[0, 'Avg_points'] = points / POP_SIZE
    population_stats.at[0, 'Avg_salary'] = salary / POP_SIZE
    population_stats.at[0, 'Avg_fitness'] = fitness / POP_SIZE

def update_breed_chance(index):
    population.at[index, 'Norm_fitness'] = fitness / population_stats.at      \
        [0, 'Max_fitness']
        

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