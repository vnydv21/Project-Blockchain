

class NodePool:

    def __init__(self):
        self.nodes = {}
        self.nodeCount = 0

        # this is counter for all block created ever
        self.blockCounter = 0

        # stores the id of validator nodes
        # these the the acutal stakeholder in voting
        # whode reputation will be at stake.
        self.validatorNodes = []

        self.fraudulantNodeID = 0
        self.fraudulantNodeID = 0

    def DisplayNodes(self):
        print('Nodes:')
        print('ID \treputations')
        for i in self.nodes:
            node = self.nodes[i]
            print("{0} \t{1} ".format(i, node.reputation))

        print()
        print('Validator Node ID:', self.validatorNodes)
        print('Fraudulant Node ID:', self.fraudulantNodeID)
        print('---------------------------------------------------')

    def Add(self, node):
        self.nodes[self.nodeCount] = node
        node.id = self.nodeCount
        self.nodeCount += 1

        return node.id

    def ChooseValidator(self, availableStakeHolder):
        # for good solving +1 Reputation
        # for wrong solving -10 Reputation

        # simple approach
        # not using random but choosing the one max reputation
        # choose the one with max Reputation
        maxNodeID = max(availableStakeHolder, key = lambda nodeID: self.nodes[nodeID].reputation)

        return maxNodeID