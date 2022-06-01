import copy

class Node:
    # nodes the collected and stored in "main" under Manager class

    def __init__(self, uBase):
        self.id = 0

        # get a link to uBase under which the node works
        self.uBase = uBase

        #type: blockchain
        self.blockChain = None

        # type: block
        # temporary stores the block broadcasted
        self.savedBlock = None

        self.reputation = 0
        
    
    def CatchBlock(self, block):
        # note there won't be two block with the same id
        # as block generation are controlled by main function
        self.savedBlock = copy.deepcopy(block)
        
    def AddBlock(self):
        # adds the saved block to chain
        # only when the "main" consensus reach 51%, it prompts and do so
        self.blockChain.AddBlock(self.savedBlock)

        # reset the variable to none
        self.savedBlock = None

    def VerifyBlock(self, ablock):
        
        block = copy.deepcopy(ablock)
        # a temporray list to store userBalances and updates based on transctions
        # if success in all then all transactions are carried out else return False
        # the unsuccesfull transaction ID is returned and deleted from list
        UserBalanceList = {}

        # logic to verify blocks transactions        
        # using the node's linked uBase

        # iter through each transaction and check if valid
        # first check if user linked to the public key has votingpower
        wrongTxns = []

        
        # now verify transactions
        # if block correct -> return block hash and prev-Hash

        for txn in block.data:
            A, B, amt = txn.fromPublicKey, txn.toPublicKey, txn.amount
            
            userA = userB = None

            if A in self.uBase.userKeys and B in self.uBase.userKeys:
                userAid = self.uBase.userKeys.get(A)
                userBid = self.uBase.userKeys.get(B)

                userA = self.uBase.users.get(userAid)
                userB = self.uBase.users.get(userBid)

                if not userAid in UserBalanceList:
                    UserBalanceList[userAid] = userA.votePower
                
                '''
                if userA.votePower - amt < 0:
                    wrongTxns.append(txn.id)
                '''
                # temporarily store the transaction

                # assume the fraudulant block carries out all the transactions without checking
                if self.id == self.uBase.nodepool.fraudulantNodeID:
                    UserBalanceList[userAid] -= amt
                else:
                    if UserBalanceList[userAid] - amt < 0:
                        wrongTxns.append(txn.id)
                    else:
                        UserBalanceList[userAid] -= amt
                    

            else:
                wrongTxns.append(txn.id)
                
        if wrongTxns:
            return 0, wrongTxns, 0
        else:
            if self.blockChain.lastBlockId == -1:
                block.prevBlockHash = 0
            else:
                block.prevBlockHash = self.blockChain.blocks[self.blockChain.lastBlockId].hash

            block.hash = block.GenerateHash()

            return 1, [], block.hash
