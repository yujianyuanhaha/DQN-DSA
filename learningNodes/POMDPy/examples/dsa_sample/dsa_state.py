from __future__ import print_function
# from builtins import range
from pomdpy.discrete_pomdp import DiscreteState


class DSAState(DiscreteState):
    """
    The state contains the position of the robot, as well as a boolean value for each DSA
    representing whether it is good (true => good, false => bad).

    This class also implements DiscretizedState in order to allow the state to be easily
    converted to a List
    """

    def __init__(self, dsa_grid_position, DSA_states):
        if DSA_states is not None:
            assert DSA_states.__len__() is not 0
        self.position = dsa_grid_position
        self.DSA_states = DSA_states  # list

#    def distance_to(self, other_DSA_state):
#        """
#        Distance is measured between beliefs by the sum of the num of different DSAs
#        """
#        assert isinstance(other_DSA_state, DSAState)
#        distance = 0
#        # distance = self.position.manhattan_distance(other_DSA_state.position)
#        for i, j in zip(self.DSA_states, other_DSA_state.DSA_states):
#            if i != j:
#                distance += 1
#        return distance
#
#    def __eq__(self, other_DSA_state):
#        return self.position == other_DSA_state.position and self.DSA_states is other_DSA_state.DSA_states
#
#    def copy(self):
#        return DSAState(self.position, self.DSA_states)
#
#    def __hash__(self):
#        """
#        Returns a decimal value representing the binary state string
#        :return:
#        """
#        return int(self.to_string(), 2)
#
#    def to_string(self):
#        state_string = self.position.to_string()
#        state_string += " - "
#
#        for i in self.DSA_states:
#            if i:
#                state_string += "1 "
#            else:
#                state_string += "0 "
#        return state_string
#
#    def print_state(self):
#        """
#        Pretty printing
#        :return:
#        """
#        self.position.print_position()
#
#        print('Good: {', end=' ')
#        good_DSAs = []
#        bad_DSAs = []
#        for i in range(0, self.DSA_states.__len__()):
#            if self.DSA_states[i]:
#                good_DSAs.append(i)
#            else:
#                bad_DSAs.append(i)
#        for j in good_DSAs:
#            print(j, end=' ')
#        print('}; Bad: {', end=' ')
#        for k in bad_DSAs:
#            print(k, end=' ')
#        print('}')
#
#    def as_list(self):
#        """
#        Returns a list containing the (i,j) grid position boolean values
#        representing the boolean DSA states (good, bad)
#        :return:
#        """
#        state_list = [self.position.i, self.position.j]
#        for i in range(0, self.DSA_states.__len__()):
#            if self.DSA_states[i]:
#                state_list.append(True)
#            else:
#                state_list.append(False)
#        return state_list
#
#    def separate_DSAs(self):
#        """
#        Used for the PyGame sim
#        :return:
#        """
#        good_DSAs = []
#        bad_DSAs = []
#        for i in range(0, self.DSA_states.__len__()):
#            if self.DSA_states[i]:
#                good_DSAs.append(i)
#            else:
#                bad_DSAs.append(i)
#        return good_DSAs, bad_DSAs