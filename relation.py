"""
A class representing a relation between two finite groups.
"""
from randomizer import Randomizer


class Relation:
    def __init__(self, randomizer, set_a, set_b):
        """
        Initializes the sets.
        
        @params set_a, set_b: The sets (set objects) which include elements. 
        """
        self.set_a = set_a
        self.set_b = set_b
        self.randomizer = randomizer

    def get_binary_representation(self, shuffle):
        """
        Returns a binary string that represents whether each member of the first set is in
        the intersection of the first set and the secound set

        @params shuffle: whether to shuffle the ones and zeros in the binary representation.
                         If False, the order of ones and zeros is arbitrary.
        @type shuffle: bool
        @return: A binary string as described
        """
        binary_representation = ["1" if member in (self.set_a & self.set_b) else "0"
                                 for member in self.set_a]
        if shuffle:
            self.randomizer.get_prng().shuffle(binary_representation)
        return ''.join(binary_representation) + '#'
