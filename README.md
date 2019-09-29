# Blotto Game
This folder contains the necessary steps required to run the logic as well as simulation

## Running without frontend 
### The simulation will run for 100 rounds 
   
1. To run the code without UI simulation
   Default command
   python main.py --troops 8 --battlefields 3 --orderofagent1 3 --orderofagent2 1  --simulation 0

These are compulsory command line arguments.

- Troops = Number of troops

- Battlefield = Number of battlefields

- orderofagent1 = Theory of mind order of the agent1  (Order of agent1 should be higher than agent2 for this experiment)

- orderofagent2 = Theory of mind order of agent2

- simulation =  0 if you don't want to see UI simulation.
                1 if you want to see UI simulation
                
 ## Running with frontend    
 ### The simulation will run for 1 round 
 #### Requirements linux 64 bit system
 #### Steps
 1. Go to Blotto-game-frontend folder.
 2. Copy the contents from executables folder. 
 3. Unzip the contents and keep it in Blotto Game directory 
 4. run in the terminal command 'sh run.sh' 


