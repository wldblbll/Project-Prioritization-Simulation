
# Project Prioritization Simulation

## Description
This Streamlit application is designed to simulate and visualize the prioritization of projects based on their Net Present Value (NPV) and budget constraints. It allows users to adjust project parameters, run Monte Carlo simulations, and visualize the results to identify viable project scenarios.

## Features
- **Project Generation**: Generate initial projects with configurable NPV and variance.
- **Interactive Data Editor**: Adjust the mean NPV and NPV variance for each project.
- **Visualization**: Display project distributions and stacked bar charts for budget visualization.
- **Monte Carlo Simulation**: Run simulations to evaluate project scenarios under budget constraints.
- **Scenario Selection**: View detailed distributions of selected scenarios.

## Installation
To run this application, you need to have Python and Streamlit installed. You can install the required packages using pip:

```bash
pip install streamlit numpy pandas matplotlib
```

Usage
Run the Application: Start the Streamlit application by running the following command in your terminal:

Copy
streamlit run your_script_name.py
Adjust Project Parameters: Use the interactive data editor to adjust the mean NPV and NPV variance for each project.

View Project Distributions: Visualize the distributions of individual projects before running the simulation.

View Stacked Bar Chart: Visualize the cumulative budgets by year for the projects.

Run Simulation: Click the "Lancer la simulation" button in the sidebar to run the Monte Carlo simulation.

View Results: After the simulation, view the general graphs and select a scenario to see its distribution.

Code Structure
Data Generation: Generate initial projects with configurable parameters.
Simulation: Run Monte Carlo simulations to evaluate project scenarios.
Visualization: Display project distributions, general graphs, and scenario-specific distributions.
Session State: Maintain simulation results across interactions.
Configuration
The application uses a configuration file to set parameters such as the number of projects, maximum budget per year, maximum iterations, and profitability threshold.

