"""
A class representing a relation between two finite groups.
"""

class Relation:
    def __init__(self, set_a, set_b):
        """
        Initializes the sets.
        
        @params set_a, set_b: The sets (set objects) which include elements. 
        """
        self.set_a = set_a
        self.set_b = set_b

    def get_bianry_representation(self):
        """
        Returns a binary string that represents whether each member of the first set is in
        the intersection of the first set and the secound set

        @params set_a, set_b: TODO
        @return: A binary string as described
        """
        bianry_representation = ""
        intersection = self.set_a & self.set_b
        for member in self.set_a:
            if member in intersection:
                bianry_representation += "1"
            else:
                bianry_representation += "0"
        return bianry_representation
