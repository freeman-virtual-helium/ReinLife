# Changelog

All notable changes to this project will be documented in this file. This changelog
follows the following style:
- Added
- Changed
- Fixed
- Removed


## [1.0.1] - 2020-05-01
 
### Removed
- Removed commented code in test.py and train.py
- Removed images that were currently not used 

## [1.0] - 2020-05-01

Major overhaul to the structure of the code, repository, and readme since
this is the first version I feel is ready to be used by others. 

### Added
- Option to save experiments, results, and brains
- Option to run both offline and in google colab
- More options for controlling environment (reward system, reproduction, etc.)
- Tester and Trainer functions
- License


### Changed
- Updated requirements and removed tensorflow
- Updated readme with all current information, visualizations, results, documentation
etc. 
 
### Fixed
- Major optimization of code, especially in the environment

### Removed
- Removed DRQN

## [0.3] - 2020-04-13

### Added
- Added PERD3QN and D3QN
- Added True evolution where each family has a single brain, but any amount
of families can be created. Any new entity will have its brain "scrambled" to mimic
mutation when evolving
- Updated results such that it also works for any amount of families

### Changed
- Created N families such that every family has a single brain that is trained independently
- Updated training structure to make training easier 
- All reward, states, etc. are now preserved in the Agent class
- Updated model structure such that all models have similar structure

### Fixed
- Updated folder structure

### Removed
- Removed older models that were not used or had significant bugs

## [0.2.4] - 2020-04-07

### Added
- Added DRQN
- Added additional live visualizations
- Visualizations for Google Colab
- Option to choose for pastel colors in Render
- Option to choose an extended fov for testing purposes
- Option for PPO to select input_dim and output_dim

### Changed
- General structure and lay-out of main code
- Implemented a maximum age, after which the entity dies
- Attacks, if fatal, now also result in increased health
- If no agent, then health_fov is -1 instead of zero to better identify empty spaces
- Show a decrease in health by the black border slowly going towards the color of its body
- Updated fitness function: 
    -  reward = sum([other_agent.age / 200 for other_agent in self.agents
                     if agent.gen == other_agent.gen])
    -  reward = (sum([1 for other_agent in self.agents
                      if agent.gen == other_agent.gen]) - 1) / self.max_agents

- Instant kill instead of decreasing health

### Fixed
- Of the best agents, the worst agent is replaced by a better agent only
if it is not already one of the best agents (which was previously the case)

## [0.2.3] - 2020-03-23

### Fixed
- Rendering only worked for squares, now fixed
- Food generated is now proportional to size of grid
- The best agent was tracked in the environment by age instead of fitness
- Fixed an infitine while loop in movement (I think...)

### Added
- Can save and load A2C, DQN, and PERDQN 'brains'
- Choose between the top 5 brains
- Red border for an entity if it attacks

### Changed
- Updated the basic structure of the grid which results in a minor speed-up

## [0.2.2] - 2020-03-13

### Fixed
- The fov for entities and their health was incorrect and now fixed.  

## [0.2.1] - 2020-03-13

### Added
- Added changelog 

### Changed
- Major overhaul of the readme

### Fixed
- Improved reward function
    - From:
        - 5 + (5 * sum([1 for other_agent in self.agents if agent.gen == other_agent.gen]))

    - To
        - sum([other_agent.health / max_age for other_agent in self.agents if agent.gen == other_agent.gen])

## [0.2.0] - 2020-03-13

### Added
- Implemented A2C, DQN, PER-DQN, and PPO (although it does has some stability issues)
- Added genes, additional observation space, asexual reproduction

### Changed
- Major restructure of packages

## [0.1.0] - 2020-03-02

### Added
* Created a Sprite Generator which is currently not used
* Implemented infiniteworld with fov through borders
* Agents can attack or move (8 actions, attack in direction or move in direction)
* PPO (+LSTM) and DQN work

### Changed
* Did a rework of the environment which led to a speed-up of 7x


