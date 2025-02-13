# Applied Genetic Algorithms

## Overview
This project applies genetic algorithms to solve the class scheduling problem, providing tools for data processing, algorithm execution, and result analysis.

## Project Components

### Data Source
- **Source**: `3p71_ga`

### Scripts and Files

#### Python Scripts
- **Assignment_2_GeneticAlgorithms.py**:
  - Implements the genetic algorithm for class scheduling.
  - Saves all resultant data in JSON format within the `ga_results` directory.

- **data_init_class.py**:
  - A helper class to initialize and manage data for Courses, Rooms, and Timeslots, making them accessible to the main class.

- **Genetic_Algorithm_Summary.py**:
  - Summarizes different parameter sets used in the genetic algorithm.
  - Generates and saves graphs for visualization.

#### Result Directories
- **ga_results**:
  - Contains folders for each parameter set, each storing JSON files with generational data and metadata.

- **fitness_plots**:
  - Houses graphs (represented here as 'grass') for each generational run, illustrating fitness progression for various parameter sets.

#### Documentation
- **COSC3P71A2_latex.pdf**:
  - A LaTeX report detailing the approach, methodology, and results of the class scheduling problem using genetic algorithms.

- **Pseudocode.txt**:
  - Provided with the assignment release; not authored by the project contributor.

