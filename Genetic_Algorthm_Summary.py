import json
import os
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


#Running this script will print out a formatted summary of the different algortihm runs
#will also save graphs
data_set = 't2' #t1 or t2

def load_results(base_dir):
    results = defaultdict(list)
    for crossover_type in ['uniform', 'one_point']:
        for crossover_rate in [0.75, 0.9, 1.0]:
            for mutation_rate in [0.0, 0.1, 0.25]:
                directory = f"{base_dir}/problemset_({data_set})/crossovertype({crossover_type})/crossoverrate({crossover_rate})_mutationrate({mutation_rate})"
                if os.path.exists(directory):
                    for file in os.listdir(directory):
                        if file.endswith('.json'):
                            with open(os.path.join(directory, file), 'r') as f:
                                data = json.load(f)
                                results[(crossover_type, crossover_rate, mutation_rate)].append(data)
    return results




def calculate_metrics(all_results):
    analysis = {}
    for params, runs in all_results.items():
        crossover_type, crossover_rate, mutation_rate = params
        fitness_values = []
        for run in runs:
            #Collect fitness values for all generations from each run
            fitness_values.extend([gen['best_fitness'] for gen in run['generations']])
            #include the final best solution fitness
            fitness_values.append(run['best_solution']['fitness'])
        
        #Create and save the summary data into a meta json
        if fitness_values:
            analysis[params] = {
                'mean_best_fitness': np.mean(fitness_values),
                'max_fitness': max(fitness_values),
                'min_fitness': min(fitness_values),
                'std_dev_fitness': np.std(fitness_values),
                'median_fitness': np.median(fitness_values),
                'fitness_per_generation': [gen['best_fitness'] for run in runs for gen in run['generations']]  #New key for plotting
            }
    return analysis

#Plots all 5 generational sets for a parameter set
def plot_fitness(analysis, params, output_dir):
    fitness_data = analysis[params]['fitness_per_generation']
    generations = list(range(len(fitness_data)))  #Assuming each run has the same number of generations or use a unique counter
    
    plt.figure(figsize=(10, 5))
    plt.plot(generations, fitness_data, 'r-')
    plt.title(f'Best Fitness Over Generations: {params}')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f"{params[0]}_{params[1]}_{params[2]}.png"))
    plt.close()


#this method summarizes the data into human friendly ways
def summarize_findings(analysis):
    #Sort by mean best fitness to find most and least successful configurations
    sorted_params = sorted(analysis.items(), key=lambda x: x[1]['mean_best_fitness'], reverse=True)
    
    print("Summary of Findings:")
    print("-" * 40)
    print("Most Successful Configurations:")
    for i, (params, metrics) in enumerate(sorted_params[:3]):
        print(f"{i+1}. {params}: Mean Best Fitness = {metrics['mean_best_fitness']:.4f}")

    print("\nLeast Successful Configurations:")
    for i, (params, metrics) in enumerate(sorted_params[-3:], start=1):
        print(f"{i}. {params}: Mean Best Fitness = {metrics['mean_best_fitness']:.4f}")

    print("\nOverall Metrics:")
    for params, metrics in sorted_params:
        print(f"{params}:")
        for key, value in metrics.items():
            if key != 'fitness_per_generation':  #Don't print the raw fitness values
                print(f"  {key}: {value:.4f}")
        print()

    #Plotting each configuration's fitness over generations
    output_dir = 'fitness_plots'
    os.makedirs(output_dir, exist_ok=True)
    for params in analysis:
        plot_fitness(analysis, params, output_dir)

def main():
    base_dir = 'ga_results'
    all_results = load_results(base_dir)
    analysis = calculate_metrics(all_results)
    summarize_findings(analysis)

if __name__ == "__main__":
    main()