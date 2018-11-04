from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import map
from builtins import hex
from builtins import range
from past.utils import old_div
import logging
import json
import numpy as np
#from pomdpy.util import console, config_parser
#from .grid_position import GridPosition
from .dsa_state import DSAState
from .dsa_action import DSAAction, ActionType
from .dsa_observation import DSAObservation
from pomdpy.discrete_pomdp import DiscreteActionPool, DiscreteObservationPool
from pomdpy.pomdp import Model, StepResult
from .dsa_position_history import DSAData, PositionAndDSAData

module = "DSAModel"


class RSCellType:
    """
    DSAs are enumerated 0, 1, 2, ...
    other cell types should be negative.
    """
    DSA = 0
    EMPTY = -1
    GOAL = -2
    OBSTACLE = -3


class DSAModel:
    def __init__(self, args):
        
        self.discount = 0.99 #
        self.use_tf = 0 #
        self.n_start_states = 8 #
        self.ucb_coefficient = 0.9
        self.action_selection_timeout = 0.5
        self.max_depth = 4
        self.max_particle_count = 4
        self.epsilon_minimum = 0.01
        self.timeout = 0.5
        self.test = 2
        self.preferred_actions = 4
        
        # super(DSAModel, self).__init__(args)
        # super of DSAModel is Model with lots of empty function
        # logging utility
        self.logger = logging.getLogger('POMDPy.DSAModel')
  #      self.DSA_config = json.load(open(config_parser.DSA_cfg, "r"))

        # -------- Model configurations -------- #

        # The reward for sampling a good DSA
#        self.good_DSA_reward = self.DSA_config['good_DSA_reward']
        # The penalty for sampling a bad DSA.
   #     self.bad_DSA_penalty = self.DSA_config['bad_DSA_penalty']
        # The reward for exiting the map
     #   self.exit_reward = self.DSA_config['exit_reward']
        # The penalty for an illegal move.
     #   self.illegal_move_penalty = self.DSA_config['illegal_move_penalty']
        # penalty for finishing without sampling a DSA
      #  self.half_efficiency_distance = self.DSA_config['half_efficiency_distance']

        # ------------- Flags --------------- #
        # Flag that checks whether the agent has yet to successfully sample a DSA
        self.sampled_DSA_yet = False
        # Flag that keeps track of whether the agent currently believes there are still good DSAs out there
        self.any_good_DSAs = False

        # ------------- Data Collection ---------- #
        self.unique_DSAs_sampled = []
        self.num_times_sampled = 0.0
        self.good_samples = 0.0
        self.num_reused_nodes = 0
        self.num_bad_DSAs_sampled = 0
        self.num_good_checks = 0
        self.num_bad_checks = 0

        # -------------- Map data ---------------- #
        # The number of rows in the map.
        self.n_rows = 0
        # The number of columns in the map
        self.n_cols = 0
        # The number of DSAs on the map.
        self.n_DSAs = 4  # ToDo
        self.num_states = 0
        self.min_val = 0
        self.max_val = 0

  #      self.start_position = GridPosition()

        # The coordinates of the DSAs.
        self.DSA_positions = []
        # The coordinates of the goal squares.
        self.goal_positions = []
        # The environment map in vector form.
        # List of lists of RSCellTypes
        self.env_map = []

        # The distance from each cell to the nearest goal square.
        self.goal_distances = []
        # The distance from each cell to each DSA.
        self.DSA_distances = []

        # Smart DSA data
        self.all_DSA_data = []

        # Actual DSA states
        self.actual_DSA_states = []

        # The environment map in text form.
   #     self.map_text, dimensions = config_parser.parse_map(self.DSA_config['map_file'])
    #    self.n_rows = int(dimensions[0])
   #     self.n_cols = int(dimensions[1])

#        self.initialize()
   
   
   
        self.solver = "POMCP"
        
        self.epsilon_start = 0.99
   
        # hand input - due to miss the args for paras
        
        self.n_epochs = 20
        
        self.n_dsa = 4    # num of chans
        
    def create_action_pool(self):
        return DiscreteActionPool(self)
    
    def create_observation_pool(self, solver):
        return DiscreteObservationPool(solver)
    
    
    
    def create_root_historical_data(self, solver):
        self.create_new_dsa_data()
        return PositionAndDSAData(self, solver)

    def create_new_dsa_data(self):
        self.all_dsa_data = []
        for i in range(0, self.n_dsa):
            self.all_dsa_data.append(DSAData())

#    # initialize the maps of the grid
#    def initialize(self):
#        p = GridPosition()
#        for p.i in range(0, self.n_rows):
#            tmp = []
#            for p.j in range(0, self.n_cols):
#                c = self.map_text[p.i][p.j]
#
#                # initialized to empty
#                cell_type = RSCellType.EMPTY
#
#                if c is 'o':
#                    self.DSA_positions.append(p.copy())
#                    cell_type = RSCellType.DSA + self.n_DSAs
#                    self.n_DSAs += 1
#                elif c is 'G':
#                    cell_type = RSCellType.GOAL
#                    self.goal_positions.append(p.copy())
#                elif c is 'S':
#                    self.start_position = p.copy()
#                    cell_type = RSCellType.EMPTY
#                elif c is 'X':
#                    cell_type = RSCellType.OBSTACLE
#                tmp.append(cell_type)
#
#            self.env_map.append(tmp)
#        # Total number of distinct states
#        self.num_states = pow(2, self.n_DSAs)
#        self.min_val = old_div(-self.illegal_move_penalty, (1 - self.discount))
#        self.max_val = self.good_DSA_reward * self.n_DSAs + self.exit_reward
#
#    ''' ===================================================================  '''
#    '''                             Utility functions                        '''
#    ''' ===================================================================  '''
#
#    # returns the RSCellType at the specified position
#    def get_cell_type(self, pos):
#        return self.env_map[pos.i][pos.j]
#
#    def get_sensor_correctness_probability(self, distance):
#        assert self.half_efficiency_distance is not 0, self.logger.warning("Tried to divide by 0! Naughty naughty!")
#        return (1 + np.power(2.0, old_div(-distance, self.half_efficiency_distance))) * 0.5
#
#    ''' ===================================================================  '''
#    '''                             Sampling                                 '''
#    ''' ===================================================================  '''
#
#    def sample_an_init_state(self):
#        self.sampled_DSA_yet = False
#        self.unique_DSAs_sampled = []
#        return DSAState(self.start_position, self.sample_DSAs())
#
#    def sample_state_uninformed(self):
#        while True:
#            pos = self.sample_position()
#            if self.get_cell_type(pos) is not RSCellType.OBSTACLE:
#                return DSAState(pos, self.sample_DSAs())
#
#    def sample_state_informed(self, belief):
#        return belief.sample_particle()
#
#    def sample_position(self):
#        i = np.random.random_integers(0, self.n_rows - 1)
#        j = np.random.random_integers(0, self.n_cols - 1)
#        return GridPosition(i, j)
#
#    def sample_DSAs(self):
#        return self.decode_DSAs(np.random.random_integers(0, (1 << self.n_DSAs) - 1))
#
#    def decode_DSAs(self, value):
#        DSA_states = []
#        for i in range(0, self.n_DSAs):
#            DSA_states.append(value & (1 << i))
#        return DSA_states
#
#    def encode_DSAs(self, DSA_states):
#        value = 0
#        for i in range(0, self.n_DSAs):
#            if DSA_states[i]:
#                value += (1 << i)
#        return value
#
#    ''' ===================================================================  '''
#    '''                 Implementation of abstract Model class               '''
#    ''' ===================================================================  '''
#
#
#
#    def is_terminal(self, DSA_state):
#        return self.get_cell_type(DSA_state.position) is RSCellType.GOAL
#
#    def is_valid(self, state):
#        if isinstance(state, DSAState):
#            return self.is_valid_state(state)
#        elif isinstance(state, GridPosition):
#            return self.is_valid_pos(state)
#        else:
#            return False
#
#    def is_valid_state(self, DSA_state):
#        pos = DSA_state.position
#        return 0 <= pos.i < self.n_rows and 0 <= pos.j < self.n_cols and \
#               self.get_cell_type(pos) is not RSCellType.OBSTACLE
#
#    def is_valid_pos(self, pos):
#        return 0 <= pos.i < self.n_rows and 0 <= pos.j < self.n_cols and \
#               self.get_cell_type(pos) is not RSCellType.OBSTACLE
#
#    def get_legal_actions(self, state):
#        legal_actions = []
#        all_actions = range(0, 5 + self.n_DSAs)
#        new_pos = state.position.copy()
#        i = new_pos.i
#        j = new_pos.j
#
#        for action in all_actions:
#            if action is ActionType.NORTH:
#                new_pos.i -= 1
#            elif action is ActionType.EAST:
#                new_pos.j += 1
#            elif action is ActionType.SOUTH:
#                new_pos.i += 1
#            elif action is ActionType.WEST:
#                new_pos.j -= 1
#
#            if not self.is_valid_pos(new_pos):
#                new_pos.i = i
#                new_pos.j = j
#                continue
#            else:
#                if action is ActionType.SAMPLE:
#                    DSA_no = self.get_cell_type(new_pos)
#                    if 0 > DSA_no or DSA_no >= self.n_DSAs:
#                        continue
#                new_pos.i = i
#                new_pos.j = j
#                legal_actions.append(action)
#        return legal_actions
#
#    def get_max_undiscounted_return(self):
#        total = 10
#        for _ in self.actual_DSA_states:
#            if _:
#                total += 10
#        return total
#
#    def reset_for_simulation(self):
#        self.good_samples = 0.0
#        self.num_reused_nodes = 0
#        self.num_bad_DSAs_sampled = 0
#        self.num_bad_checks = 0
#        self.num_good_checks = 0
#
    def reset_for_epoch(self):
        self.actual_DSA_states = self.sample_DSAs()
#        console(2, module, "Actual DSA states = " + str(self.actual_DSA_states))
#
#    def update(self, step_result):
#        if step_result.action.bin_number == ActionType.SAMPLE:
#            DSA_no = self.get_cell_type(step_result.next_state.position)
#            self.unique_DSAs_sampled.append(DSA_no)
#            self.num_times_sampled = 0.0
#            self.sampled_DSA_yet = True
#
#    def get_all_states(self):
#        """
#        :return: Forgo returning all states to save memory, return the number of states as 2nd arg
#        """
#        return None, self.num_states
#
#    def get_all_observations(self):
#        """
#        :return: Return a dictionary of all observations and the number of observations
#        """
#        return {
#            "Empty": 0,
#            "Bad": 1,
#            "Good": 2
#        }, 3
#
    def get_all_actions(self):
        """
        :return: Return a list of all actions along with the length
        """
        all_actions = []
        for code in range(0, 5 + self.n_DSAs):
            all_actions.append(DSAAction(code))
        return all_actions
#
#
#
#    def create_root_historical_data(self, solver):
#        self.create_new_DSA_data()
#        return PositionAndDSAData(self, self.start_position.copy(), self.all_DSA_data, solver)
#
#    def create_new_DSA_data(self):
#        self.all_DSA_data = []
#        for i in range(0, self.n_DSAs):
#            self.all_DSA_data.append(DSAData())
#
#    @staticmethod
#    def make_adjacent_position(pos, action_type):
#        if action_type is ActionType.NORTH:
#            pos.i -= 1
#        elif action_type is ActionType.EAST:
#            pos.j += 1
#        elif action_type is ActionType.SOUTH:
#            pos.i += 1
#        elif action_type is ActionType.WEST:
#            pos.j -= 1
#        return pos
#
#    def make_next_position(self, pos, action_type):
#        is_legal = True
#
#        if action_type >= ActionType.CHECK:
#            pass
#
#        elif action_type is ActionType.SAMPLE:
#            # if you took an illegal action and are in an invalid position
#            # sampling is not a legal action to take
#            if not self.is_valid_pos(pos):
#                is_legal = False
#            else:
#                DSA_no = self.get_cell_type(pos)
#                if 0 > DSA_no or DSA_no >= self.n_DSAs:
#                    is_legal = False
#        else:
#            old_position = pos.copy()
#            pos = self.make_adjacent_position(pos, action_type)
#            if not self.is_valid_pos(pos):
#                pos = old_position
#                is_legal = False
#        return pos, is_legal
#
#    def make_next_state(self, state, action):
#        action_type = action.bin_number
#        next_position, is_legal = self.make_next_position(state.position.copy(), action_type)
#
#        if not is_legal:
#            # returns a copy of the current state
#            return state.copy(), False
#
#        next_state_DSA_states = list(state.DSA_states)
#
#        # update the any_good_DSAs flag
#        self.any_good_DSAs = False
#        for DSA in next_state_DSA_states:
#            if DSA:
#                self.any_good_DSAs = True
#
#        if action_type is ActionType.SAMPLE:
#            self.num_times_sampled += 1.0
#
#            DSA_no = self.get_cell_type(next_position)
#            next_state_DSA_states[DSA_no] = False
#
#        return DSAState(next_position, next_state_DSA_states), True
#
#    def make_observation(self, action, next_state):
#        # generate new observation if not checking or sampling a DSA
#        if action.bin_number < ActionType.SAMPLE:
#            # Defaults to empty cell and Bad DSA
#            obs = DSAObservation()
#            # self.logger.info("Created DSA Observation - is_good: %s", str(obs.is_good))
#            return obs
#        elif action.bin_number == ActionType.SAMPLE:
#            # The cell is not empty since it contains a DSA, and the DSA is now "Bad"
#            obs = DSAObservation(False, False)
#            return obs
#
#        # Already sampled this DSA so it is NO GOOD
#        if action.DSA_no in self.unique_DSAs_sampled:
#            return DSAObservation(False, False)
#
#        observation = self.actual_DSA_states[action.DSA_no]
#
#        # if checking a DSA...
#        dist = next_state.position.euclidean_distance(self.DSA_positions[action.DSA_no])
#
#        # NOISY OBSERVATION
#        # bernoulli distribution is a binomial distribution with n = 1
#        # if half efficiency distance is 20, and distance to DSA is 20, correct has a 50/50
#        # chance of being True. If distance is 0, correct has a 100% chance of being True.
#        correct = np.random.binomial(1.0, self.get_sensor_correctness_probability(dist))
#
#        if not correct:
#            # Return the incorrect state if the sensors malfunctioned
#            observation = not observation
#
#        # If I now believe that a DSA, previously bad, is now good, change that here
#        if observation and not next_state.DSA_states[action.DSA_no]:
#            next_state.DSA_states[action.DSA_no] = True
#        # Likewise, if I now believe a DSA, previously good, is now bad, change that here
#        elif not observation and next_state.DSA_states[action.DSA_no]:
#            next_state.DSA_states[action.DSA_no] = False
#
#        # Normalize the observation
#        if observation > 1:
#            observation = True
#
#        return DSAObservation(observation, False)
#
#    def belief_update(self, old_belief, action, observation):
#        pass
#
#    def make_reward(self, state, action, next_state, is_legal):
#        if not is_legal:
#            return -self.illegal_move_penalty
#
#        if self.is_terminal(next_state):
#            return self.exit_reward
#
#        if action.bin_number is ActionType.SAMPLE:
#            pos = state.position.copy()
#            DSA_no = self.get_cell_type(pos)
#            if 0 <= DSA_no < self.n_DSAs:
#                # If the DSA ACTUALLY is good, AND I currently believe it to be good, I get rewarded
#                if self.actual_DSA_states[DSA_no] and state.DSA_states[DSA_no]:
#                    # IMPORTANT - After sampling, the DSA is marked as
#                    # bad to show that it is has been dealt with
#                    # "next states".DSA_states[DSA_no] is set to False in make_next_state
#                    state.DSA_states[DSA_no] = False
#                    self.good_samples += 1.0
#                    return self.good_DSA_reward
#                # otherwise, I either sampled a bad DSA I thought was good, sampled a good DSA I thought was bad,
#                # or sampled a bad DSA I thought was bad. All bad behavior!!!
#                else:
#                    # self.logger.info("Bad DSA penalty - %s", str(-self.bad_DSA_penalty))
#                    self.num_bad_DSAs_sampled += 1.0
#                    return -self.bad_DSA_penalty
#            else:
#                # self.logger.warning("Invalid sample action on non-existent DSA while making reward!")
#                return -self.illegal_move_penalty
#        return 0
#
#    def generate_reward(self, state, action):
#        next_state, is_legal = self.make_next_state(state, action)
#        return self.make_reward(state, action, next_state, is_legal)
#
#    def generate_step(self, state, action):
#        if action is None:
#            print("Tried to generate a step with a null action")
#            return None
#        elif type(action) is int:
#            action = DSAAction(action)
#            "##### action = DSAAction(action) execute"
#
#        result = StepResult()
#        result.next_state, is_legal = self.make_next_state(state, action)
#        result.action = action.copy()
#        result.observation = self.make_observation(action, result.next_state)
#        result.reward = self.make_reward(state, action, result.next_state, is_legal)
#        result.is_terminal = self.is_terminal(result.next_state)
#
#        return result, is_legal
#
#    def generate_particles_uninformed(self, previous_belief, action, obs, n_particles):
#        old_pos = previous_belief.get_states()[0].position
#
#        particles = []
#        while particles.__len__() < n_particles:
#            old_state = DSAState(old_pos, self.sample_DSAs())
#            result, is_legal = self.generate_step(old_state, action)
#            if obs == result.observation:
#                particles.append(result.next_state)
#        return particles
#
#    @staticmethod
#    def disp_cell(rs_cell_type):
#        if rs_cell_type >= RSCellType.DSA:
#            print(hex(rs_cell_type - RSCellType.DSA), end=' ')
#            return
#
#        if rs_cell_type is RSCellType.EMPTY:
#            print(' . ', end=' ')
#        elif rs_cell_type is RSCellType.GOAL:
#            print('G', end=' ')
#        elif rs_cell_type is RSCellType.OBSTACLE:
#            print('X', end=' ')
#        else:
#            print('ERROR-', end=' ')
#            print(rs_cell_type, end=' ')
#
#    def draw_env(self):
#        for row in self.env_map:
#            list(map(self.disp_cell, row))
#            print('\n')
