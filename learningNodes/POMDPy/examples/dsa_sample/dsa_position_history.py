from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
from builtins import object
import numpy as np
from pomdpy.pomdp import HistoricalData
from .DSA_action import ActionType
import itertools


# Utility function
class DSAData(object):
    """
    Stores data about each DSA
    """

    def __init__(self):
        pass
        # The number of times this DSA has been checked.
#        self.check_count = 0
        # The "goodness number"; +1 for each good observation of this DSA, and -1 for each bad
        # observation of this DSA.
#        self.goodness_number = 0
        # The calculated probability that this DSA is good.
#        self.chance_good = 0.5

#    def to_string(self):
#        """
#        Pretty printing
#        """
#        data_as_string = " Check count: " + str(self.check_count) + " Goodness number: " + \
#                         str(self.goodness_number) + " Probability that DSA is good: " + str(self.chance_good)
#        return data_as_string


class PositionAndDSAData(HistoricalData):
    """
    A class to store the robot position associated with a given belief node, as well as
    explicitly calculated probabilities of goodness for each DSA.
    """

    def __init__(self, model, dsa_grid_position, all_DSA_data, solver):
        self.model = model
        self.solver = solver
        self.grid_position = dsa_grid_position

        # List of DSAData indexed by the DSA number
        self.all_DSA_data = all_DSA_data

        # Holds reference to the function for generating legal actions
        if self.model.preferred_actions:
            self.legal_actions = self.generate_smart_actions
        else:
            self.legal_actions = self.generate_legal_actions

#    @staticmethod
#    def copy_DSA_data(other_data):
#        new_DSA_data = []
#        [new_DSA_data.append(DSAData()) for _ in other_data]
#        for i, j in zip(other_data, new_DSA_data):
#            j.check_count = i.check_count
#            j.chance_good = i.chance_good
#            j.goodness_number = i.goodness_number
#        return new_DSA_data
#
#    def copy(self):
#        """
#        Default behavior is to return a shallow copy
#        """
#        return self.shallow_copy()
#
#    def deep_copy(self):
#        """
#        Passes along a reference to the DSA data to the new copy of DSAPositionHistory
#        """
#        return PositionAndDSAData(self.model, self.grid_position.copy(), self.all_DSA_data, self.solver)
#
#    def shallow_copy(self):
#        """
#        Creates a copy of this object's DSA data to pass along to the new copy
#        """
#        new_DSA_data = self.copy_DSA_data(self.all_DSA_data)
#        return PositionAndDSAData(self.model, self.grid_position.copy(), new_DSA_data, self.solver)
#
#    def update(self, other_belief):
#        self.all_DSA_data = other_belief.data.all_DSA_data
#
#    def any_good_DSAs(self):
#        any_good_DSAs = False
#        for DSA_data in self.all_DSA_data:
#            if DSA_data.goodness_number > 0:
#                any_good_DSAs = True
#        return any_good_DSAs
#
#    def create_child(self, DSA_action, DSA_observation):
#        next_data = self.deep_copy()
#        next_position, is_legal = self.model.make_next_position(self.grid_position.copy(), DSA_action.bin_number)
#        next_data.grid_position = next_position
#
#        if DSA_action.bin_number is ActionType.SAMPLE:
#            DSA_no = self.model.get_cell_type(self.grid_position)
#            next_data.all_DSA_data[DSA_no].chance_good = 0.0
#            next_data.all_DSA_data[DSA_no].check_count = 10
#            next_data.all_DSA_data[DSA_no].goodness_number = -10
#
#        elif DSA_action.bin_number >= ActionType.CHECK:
#            DSA_no = DSA_action.DSA_no
#            DSA_pos = self.model.DSA_positions[DSA_no]
#
#            dist = self.grid_position.euclidean_distance(DSA_pos)
#            probability_correct = self.model.get_sensor_correctness_probability(dist)
#            probability_incorrect = 1 - probability_correct
#
#            DSA_data = next_data.all_DSA_data[DSA_no]
#            DSA_data.check_count += 1
#
#            likelihood_good = DSA_data.chance_good
#            likelihood_bad = 1 - likelihood_good
#
#            if DSA_observation.is_good:
#                DSA_data.goodness_number += 1
#                likelihood_good *= probability_correct
#                likelihood_bad *= probability_incorrect
#            else:
#                DSA_data.goodness_number -= 1
#                likelihood_good *= probability_incorrect
#                likelihood_bad *= probability_correct
#
#            if np.abs(likelihood_good) < 0.01 and np.abs(likelihood_bad) < 0.01:
#                # No idea whether good or bad. reset data
#                # print "Had to reset DSAData"
#                DSA_data = DSAData()
#            else:
#                DSA_data.chance_good = old_div(likelihood_good, (likelihood_good + likelihood_bad))
#
#        return next_data
#
#    def generate_legal_actions(self):
#        legal_actions = []
#        all_actions = range(0, 5 + self.model.n_DSAs)
#        new_pos = self.grid_position.copy()
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
#            if not self.model.is_valid_pos(new_pos):
#                new_pos.i = i
#                new_pos.j = j
#                continue
#            else:
#                if action is ActionType.SAMPLE:
#                    DSA_no = self.model.get_cell_type(new_pos)
#                    if 0 > DSA_no or DSA_no >= self.model.n_DSAs:
#                        continue
#                new_pos.i = i
#                new_pos.j = j
#                legal_actions.append(action)
#        return legal_actions
#
#    def generate_smart_actions(self):
#
#        smart_actions = []
#
#        n_DSAs = self.model.n_DSAs
#
#        # check if we are currently on top of a DSA
#        DSA_no = self.model.get_cell_type(self.grid_position)
#
#        # if we are on top of a DSA, and it has been checked, sample it
#        if 0 <= DSA_no < n_DSAs:
#            DSA_data = self.all_DSA_data[DSA_no]
#            if DSA_data.chance_good == 1.0 or DSA_data.goodness_number > 0:
#                smart_actions.append(ActionType.SAMPLE)
#                return smart_actions
#
#        worth_while_DSA_found = False
#        north_worth_while = False
#        south_worth_while = False
#        east_worth_while = False
#        west_worth_while = False
#
#        # Check to see which DSAs are worthwhile
#
#        # Only pursue one worthwhile DSA at a time to prevent the agent from getting confused and
#        # doing nothing
#        for i in range(0, n_DSAs):
#            # Once an interesting DSA is found, break out of the for loop
#
#            if worth_while_DSA_found:
#                break
#            DSA_data = self.all_DSA_data[i]
#            if DSA_data.chance_good != 0.0 and DSA_data.goodness_number >= 0:
#                worth_while_DSA_found = True
#                pos = self.model.DSA_positions[i]
#                if pos.i > self.grid_position.i:
#                    south_worth_while = True
#                elif pos.i < self.grid_position.i:
#                    north_worth_while = True
#                if pos.j > self.grid_position.j:
#                    east_worth_while = True
#                elif pos.j < self.grid_position.j:
#                    west_worth_while = True
#
#        # If no worth while DSAs were found, just head east
#        if not worth_while_DSA_found:
#            smart_actions.append(ActionType.EAST)
#            return smart_actions
#
#        if north_worth_while:
#            smart_actions.append(ActionType.NORTH)
#        if south_worth_while:
#            smart_actions.append(ActionType.SOUTH)
#        if east_worth_while:
#            smart_actions.append(ActionType.EAST)
#        if west_worth_while:
#            smart_actions.append(ActionType.WEST)
#
#        # see which DSAs we might want to check
#        for i in range(0, n_DSAs):
#            DSA_data = self.all_DSA_data[i]
#            if DSA_data.chance_good != 0.0 and DSA_data.chance_good != 1.0 and np.abs(DSA_data.goodness_number) < 2:
#                smart_actions.append(ActionType.CHECK + i)
#
#        return smart_actions
#






