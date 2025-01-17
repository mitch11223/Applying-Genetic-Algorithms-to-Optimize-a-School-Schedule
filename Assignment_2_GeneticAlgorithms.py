from data_init_class import courses, rooms, timeslots		#lists
import time
import random
import json
import os

#these lists contain Course, Room, Timeslot objects, which have these attributes
#courses:   [[Math 101, Dr. Smith, 71,2], [Physics 401, TBD, 42, 3]...]
#rooms:     [[Large Lecture 1, 100], [Lab A, 30]...]
#timeslots: [[Monday, 9], [Tuesday, 11]...]



#Chromosome contains genes which are represented as a Course, Room and Timeslot index as a solution
#chromosome can be changed and mutated


class Chromosome:
    def __init__(self, genes):
        self.genes = genes
    
    #This method allows for the mutation of genes.
        #For each gene in the chromosome, there is a mutation_rate% chance of trying mutation
            #Either Room or Timeslot gene will be randomly swapped with another from the read in Room and Timeslot data
        
    def mutate(self, mutation_rate):
        for i, gene in enumerate(self.genes):
            #i: the index of the chromosome in individuals
            #gene: the chromsome
            if random.random() < mutation_rate:
                #Randomly change either room or timeslot
                if random.choice([True, False]):  #50% chance to mutate room or timeslot
                    self.genes[i] = (gene[0], random.randint(0, len(rooms) - 1), gene[2])  #a new random room is selected
                else:
                    self.genes[i] = (gene[0], gene[1], random.randint(0, len(timeslots) - 1))#a new random timeslot is selected
 
 
    #This method elects random point to swap all genes past
    def one_point_crossover(self, other, crossover_rate):
        if random.random() < crossover_rate:
            point = random.randint(0, len(self.genes))
            child1 = self.genes[:point] + other.genes[point:]
            child2 = other.genes[:point] + self.genes[point:]
            return Chromosome(child1), Chromosome(child2)
        return self, other
    
    #This method andomly decide to take the gene from parent 1/2
    def uniform_crossover(self, other, crossover_rate):
        if random.random() < crossover_rate:
            child1_genes, child2_genes = [], []		#keep track of new genes for children
            for gene1, gene2 in zip(self.genes, other.genes):
                if random.choice([True, False]):  #50% chance to take from parent1 or parent2
                    child1_genes.append(gene1)
                    child2_genes.append(gene2)
                else:
                    child1_genes.append(gene2)
                    child2_genes.append(gene1)
            return Chromosome(child1_genes), Chromosome(child2_genes)
        return self, other

    #helper method
    def crossover(self, other, crossover_rate, crossover_type='one_point'):
        if crossover_type == 'one_point':
            return self.one_point_crossover(other, crossover_rate)
        elif crossover_type == 'uniform':
            return self.uniform_crossover(other, crossover_rate)
        else:
            raise ValueError("Unsupported crossover type")



#Population is a collection of chromosomes, can evolve through time or by using the evolve method to process the next generation
class Population:
    def __init__(self, size, courses, rooms, timeslots, seed):
        self.individuals = []		#contains all generated chromosomes
        
        random.seed(seed)
        #Create a population of 'size' of randomized solutions to the problem
        for _ in range(size):
            genes = [(i, random.randint(0, len(rooms) - 1), random.randint(0, len(timeslots) - 1)) for i in range(len(courses))]
            #i: index of the gene inside chromosome list of genes
            #room/timeslot are randomly chosen, allowing the swapping of rooms/timeslots in the genetic algorithm
            self.individuals.append(Chromosome(genes))		#create a chromosome for each generated course,room,timeslot pattern


    #applies tournament selection and evoles a population to the next generation
    def evolve(self, crossover_rate, mutation_rate, crossover_type='one_point', elitism_rate=0.05):
        #Sort individuals by fitness in descending order
        sorted_pop = sorted(self.individuals, key=lambda x: FitnessCalculator().calculate_fitness(x, courses, rooms, timeslots), reverse=True)
        
        #Determine how many elite individuals to copy directly to the next generation
        elite_count = max(1, int(len(self.individuals) * elitism_rate))  #At least 1 elite individual
        
        new_pop = sorted_pop[:elite_count]  #Copy elite individuals directly
        
        #Tournament Selection for the rest of the population
        while len(new_pop) < len(self.individuals):
            competitors = random.sample(sorted_pop, 4) #use a seed generated
            #select best parents
            parents = sorted(competitors, key=lambda x: FitnessCalculator().calculate_fitness(x, courses, rooms, timeslots), reverse=True)[:2]
            child1, child2 = parents[0].crossover(parents[1], crossover_rate, crossover_type)
            child1.mutate(mutation_rate)
            child2.mutate(mutation_rate)
            new_pop.extend([child1, child2])
        
        #Truncate new_pop to keep it at the original size
        self.individuals = new_pop[:len(self.individuals)]
 

#calculates fitness
#measured by the number of conflicts in the chromosome
#conflict is when an index in the gene does not adhere to the end goal of allowing a class to take place without issue for each part
        
        

class FitnessCalculator:
    def calculate_fitness(self, chromosome, courses, rooms, timeslots):
        conflicts = 0
        schedule = {}
        
        for gene in chromosome.genes:
            course = courses[gene[0]]
            room = rooms[gene[1]]
            timeslot = timeslots[gene[2]]
            
            #Room capacity check
            if course.students > room.capacity:
                conflicts += 1
            
            #Room usage conflict check
            if (room.name, timeslot.day, timeslot.hour) in schedule:
                conflicts += 1
            else:
                schedule[(room.name, timeslot.day, timeslot.hour)] = course.name
            
            #Professor availability check
            for other_gene in chromosome.genes:
                if other_gene[0] != gene[0] and courses[other_gene[0]].professor == course.professor:
                    other_timeslot = timeslots[other_gene[2]]
                    if other_timeslot.day == timeslot.day and abs(other_timeslot.hour - timeslot.hour) < course.duration:
                        conflicts += 1

        return 1 / (1 + conflicts)



#main function
    #Initialized with paramters
class GeneticAlgorithm:
    def __init__(self, crossover_rate, mutation_rate, max_generations, crossover_type='one_point', elitism_rate=0.05):
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.crossover_type = crossover_type
        self.elitism_rate = elitism_rate
      
        
    #size refers to the population size 
    def run(self, size):
        seed = int(time.time())
        self.population = Population(size=size, courses=courses, rooms=rooms, timeslots=timeslots, seed=seed)
            
        fitness_calculator = FitnessCalculator()
        results = []
        
        for generation in range(self.max_generations):
            fitnesses = [fitness_calculator.calculate_fitness(ind, courses, rooms, timeslots) for ind in self.population.individuals]
            best_fitness = max(fitnesses)
            avg_fitness = sum(fitnesses) / len(fitnesses)
            
            #Log the information for this generation
            results.append({
                'generation': generation,
                'best_fitness': best_fitness,
                'avg_fitness': avg_fitness
            })
            
            print(f"Generation {generation}: Best Fitness = {best_fitness}, Average Fitness = {avg_fitness}")
            self.population.evolve(self.crossover_rate, self.mutation_rate, self.crossover_type, self.elitism_rate)
        
        #Find the best solution after all generations
        best_chromosome = max(self.population.individuals, key=lambda x: fitness_calculator.calculate_fitness(x, courses, rooms, timeslots))
        best_solution_fitness = fitness_calculator.calculate_fitness(best_chromosome, courses, rooms, timeslots)
        
        #Return and log all results
        return [seed,{
            'ga_parameters': {
                'crossover_rate': self.crossover_rate,
                'mutation_rate': self.mutation_rate,
                'max_generations': self.max_generations,
                'crossover_type': self.crossover_type,
                'elitism_rate': self.elitism_rate,
                'seed': seed
            },
            'generations': results,
            'best_solution': {
                'fitness': best_solution_fitness,
                'chromosome': best_chromosome.genes
            }
        }]







#Change these

max_generations=150
problem_set = 't1'		#actual  data source is to be manually changed in data_init_class file by user as well


#The DIY parameter run
#own strategy: mr: 0.25, cr: 0.75
#When running this and the official parameter sets, the results are saved to jsons containing all genreational and metadata



for crossover_type in ['uniform', 'one_point']:
    for crossover_rate in [0.75]:
        for mutation_rate in [0.25]:
            inst = GeneticAlgorithm(
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            max_generations=max_generations,
            crossover_type=crossover_type,
            elitism_rate=0.1
            )
            for i in range(1, 6):  #Five different seeds 
                experiment_meta = f'ga_results/problemset_({problem_set})/crossovertype({crossover_type})/crossoverrate({crossover_rate})_mutationrate({mutation_rate})'

                if not os.path.exists(experiment_meta):
                    os.makedirs(experiment_meta)
                
                
                results = inst.run(100)
                seed = results[0]
                results = results[1]
                with open(f'{experiment_meta}/seed({seed}).json', 'w') as f:
                    json.dump(results, f, indent=2)
                
        


print('\n'*10, 'Instructed Runs', '\n'*10)#debug






#offical parameter sets

for crossover_type in ['uniform', 'one_point']:
    for crossover_rate in [0.9, 1.0]:  #Crossover rates
        for mutation_rate in [0.0, 0.1]:  #Mutation rates
            inst = GeneticAlgorithm(
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            max_generations=max_generations,
            crossover_type=crossover_type,
            elitism_rate=0.1
            )
            for i in range(1, 6):  #Five different seeds 
                experiment_meta = f'ga_results/problemset_({problem_set})/crossovertype({crossover_type})/crossoverrate({crossover_rate})_mutationrate({mutation_rate})'

                if not os.path.exists(experiment_meta):
                    os.makedirs(experiment_meta)
                
                
                results = inst.run(100)		#parameter is the population size
                seed = results[0]
                results = results[1]
                with open(f'{experiment_meta}/seed({seed}).json', 'w') as f:
                    json.dump(results, f, indent=2)
                
                
              
