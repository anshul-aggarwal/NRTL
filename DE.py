#Differntial Evolution Algorithm - Anshul Aggarwal
#Python 3.4+

import random
import time
from copy import deepcopy
import fitnessFunction as ff # Fitness Function and Parameters


startTime = time.time()

algoName    = "NT" # Algo Name
CR 	    = 0.9  	# Crossover Rate
F 	    = 0.5       # Inertiea

iterations  = 200       # Number of iterations
popSize     = 500       # Population Size(i.e Number of Chromosomes)
pop         = []        # Store Population with Fitness
maxFunEval  = 10000000    # Maximum allowable function evaluations
funEval	    = 0		# Count function evaluations
bestFitness = 99999999  # Store Best Fitness Value
bestChromosome = []     # Store Best Chromosome

resultFileName="result"+algoName+".csv"

class Individual:
    def __init__(self, C, F):
        self.chromosome=C
        self.fitness=F

def Init():
    global funEval
    for i in range (0, popSize):
        chromosome = []
        chromosome.append(random.uniform(ff.LB,0))
        chromosome.append(random.uniform(0,ff.UB))
        fitness = ff.FitnessFunction(chromosome)
        funEval = funEval + 1
        newIndividual = Individual(chromosome,fitness)
        pop.append(newIndividual)
        
def MemoriseGlobalBest():
    global bestFitness,bestChromosome
    for p in pop:
        if p.fitness < bestFitness:
            bestFitness=p.fitness
            bestChromosome = deepcopy(p.chromosome)


def DEOperation():
    global funEval
    for i in range(0,popSize):

        # Choose three random indices
        i1,i2,i3=random.sample(range(0,popSize), 3)

	# Iterate for every Dimension
        newChild=[]
        for j in range(ff.D):
            if (random.random() <= CR):
                k = pop[i1].chromosome[j] + \
                    F * (pop[i2].chromosome[j] - pop[i3].chromosome[j])

                if j == 0:
                    # If new dimention cross LB
                    if k < ff.LB or k > 0:
                        k = random.uniform(ff.LB,0)

                elif j == 1:
                    # If new dimention cross LB
                    if k < 0 or k > ff.UB:
                        k = random.uniform(0,ff.UB)
    
                
                newChild.append(k)
                
            else:
                newChild.append(pop[i].chromosome[j])

	# Child Fitness
        newChildFitness=ff.FitnessFunction(newChild)
        funEval = funEval + 1
		
        # Select between parent and child
        if newChildFitness < pop[i].fitness:
            pop[i].fitness=newChildFitness
            pop[i].chromosome=newChild
                

Init()
globalBest=pop[0].chromosome
globalBestFitness=pop[0].fitness
MemoriseGlobalBest()
fp=open(resultFileName,"w");
fp.write("Iteration,Fitness,Chromosomes\n")

for i in range(0,iterations):
    DEOperation()
    MemoriseGlobalBest()
	
    if funEval >=maxFunEval:
        break

    if i%10==0:
        print( "I:",i,"\t Fitness:", bestFitness, str(bestChromosome))
        fp.write(str(i) + "," + str(bestFitness) + "," + str(bestChromosome) + "\n")

print( "I:",i+1,"\t Fitness:", bestFitness, str(bestChromosome))
fp.write(str(i+1) + "," + str(bestFitness) + "," + str(bestChromosome))    
fp.close()


print ("\nBestFitness:", bestFitness)
print ("Best chromosome:", bestChromosome)
