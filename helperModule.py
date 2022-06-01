# define instruction
import userBase
import nodepool
import util.node
import util.blockchain
import mempool
import util.transaction

# pre-initialise the module
userBase.UserBase.INIT()

def CreateUserBase(n,v):
    '''Creates a user base of v voters, with c contestants
    note the contestants also vote.

    -This also create a superUser with the max possible voteBalance.

    : Returns the userBase objects'''

    # create a custom UserBase object
    uBase = userBase.UserBase()

    # first create the non-contestant users account
    for i in range(n):
        uBase.GenerateUser()

    # now create the user account of constestant
    for i in range(v):
        regisID = uBase.GenerateUser()
        uBase.contestants.append(regisID)

    # now create a superUser account    
    uBase.superUserID = uBase.GenerateUser()
    uBase.users[uBase.superUserID].votePower = uBase.userCounter - 1

    # return the created UserBase object
    return uBase

def CreateNodes(n,v, uBase):
    '''On the userBase, create v no. of validator nodes and n numbers of
    spectator nodes, whose aim is to take part in consensus over the
    block and transaction verified by the chosen validator node
    
    NOTE: each node will be initialised with an empty blockchain

    The validator are assigned a fixed reputation point at beggining
    say 100.

    '''

    # create a custom nodePool
    uBase.nodepool = nodepool.NodePool()

    for i in range(n):
        # create a custom node
        node = util.node.Node(uBase)
        nodeID = uBase.nodepool.Add(node)

        # attach an empty blockchain to this node    
        node.blockChain = util.blockchain.BlockChain(nodeID)
        
    # create the validator nodes
    for i in range(v-1):
        # create a custom node
        node = util.node.Node(uBase)
        nodeID = uBase.nodepool.Add(node)

        uBase.nodepool.validatorNodes.append(nodeID)

        # attach an empty blockchain to this node    
        node.blockChain = util.blockchain.BlockChain(nodeID)

        # just any constant value
        node.reputation = 100

    # create the fradulant validator nodes
    for i in range(1):
        # create a custom node
        node = util.node.Node(uBase)
        nodeID = uBase.nodepool.Add(node)

        uBase.nodepool.validatorNodes.append(nodeID)

        # attach an empty blockchain to this node    
        node.blockChain = util.blockchain.BlockChain(nodeID)

        # just any constant value
        node.reputation = 100
        uBase.nodepool.fraudulantNodeID = nodeID

def DisplayWinner(uBase):
    contestantsID = []
    votes = []
    for userID in uBase.contestants:        
        contestantsID.append(userID)
        votes.append(uBase.users[userID].votePower)

    maxVotes = max(votes)

    print('Election won by User with ID:')
    for i in range(len(votes)):
        if votes[i] == maxVotes:
            print('\t', contestantsID[i])
            
    print('------------------------')
        

def SolveMempool(uBase):
    print('--------------------------------------------------')
    print('Creating Blocks and finishing transactions:')

    Mempool = uBase.mempool
    Nodepool = uBase.nodepool

    # define the 50% of actual node count
    MinConcensusRequired = Nodepool.nodeCount/2

    # keep doing transaction until mempool emtpy
    while len(Mempool.txns) > 0:

        # create a temporary block to store transactions
        # let the ID be the current blockCounter value, since it's always unique         
        blockId = Nodepool.blockCounter

        # take a few transaction from the mempool and pack them into a block
        block = Mempool.PackTransactions(blockId, Mempool.blockPackCount)

        print('1. Packed a block, displaying:')
        block.Display()
        print()
        
        print('2. Sent Block copy to each node.')
        # broadcast the block to all nodes
        for nodeID in Nodepool.nodes:
            node = Nodepool.nodes[nodeID]
            node.CatchBlock(block)
        
        print('------------------------------')

        # validator check-------------------------------------
        # choose a validator
        print('3. Choosing a validator.')
        validatorID = Nodepool.ChooseValidator(Nodepool.validatorNodes)
        print("\t Choosen Validator ID:", validatorID, 'Reputation:', Nodepool.nodes[validatorID].reputation)

        # now ask the validator to verify the block

        # let's store the wrong transactions seperately
        wrongTxns = []

        # get the result from the validator
        validatorResult, wrongTxns, blockHash = Nodepool.nodes[validatorID].VerifyBlock(block)
        print("\t Validator Gives: ")
        print('\t\t IsBlock Correct:', validatorResult)
        print('\t\t Total Wrong Transactions:',len(wrongTxns))
        print('------------------------------')

        # let's create a consensus for wrong transaction by the block
        wrongTxnsDict = {i:1 for i in wrongTxns}

        # take concensus for this block
        blockConcensus = 0
        blockConcensus += validatorResult

        # now take a consenus over each block and let each block return a set of wrongTxns        
        for nodeID in Nodepool.nodes:
            # don't ask the validator node as it has already verified
            if nodeID == validatorID: continue

            # get the node
            node = Nodepool.nodes[nodeID]

            # current nodes result
            thisResult, thisWrongTxns, thisHash = node.VerifyBlock(block)

            # first check generated blockHash with validators block hash
            if thisHash == blockHash:
                # if same then increment the validator's result 
                blockConcensus += thisResult

            # check if the validators transactions are wrong actual and take consensus
            # also add new wrong transactions if any
            for w in thisWrongTxns:
                if w in wrongTxnsDict:
                    wrongTxnsDict[w] += 1
                else:
                    wrongTxnsDict[w] = 1

        print("4. Consensus Results:")
        print('\t Has Validator Verified Block Correctly?', 'YES' if validatorResult > MinConcensusRequired else 'NO')        
        print('------------------------------')
        print("\t Checking wrong Transaction...", end ='')
        actuallyWrongTxnsCount = 0
        for txnID in wrongTxnsDict:
            if wrongTxnsDict[txnID] > MinConcensusRequired:
                actuallyWrongTxnsCount += 1
                Mempool.RemoveID(txnID)
        print('\t\t Wrong Transactions counted are:', actuallyWrongTxnsCount)
        print()

        # NOTE: One more limitation to note is that here a simulated version of
        # node and block broadcasting is used, hence, this doesn't actually dispicted
        # the actual working of the blockchain, but a fair idea can be deduced.

        # Also, important to note that if a block wrongly verify a block
        # then other nodes automatically (based on consensus) sends the right
        # block to each other
        # because the each node has it's own unique copy of the orignal block sent to them,
        # also a new block with all wrong transaction removed is sent to each, below.

        # if there are wrong tranaction then create a new block
        print('------------------------------')
        print('Creating a new block for taking IN genuine transactions')

        if wrongTxnsDict:
                Nodepool.blockCounter += 1

                # the new Block
                newBlockId = Nodepool.blockCounter
                newBlock = util.blockchain.Block(newBlockId)

                for txn in block.data:
                    if txn in wrongTxnsDict: continue
                    newBlock.AddTransaction(txn)

                # since the previous block is always verified and correct in each node, hence
                # choose any node and get it's last block information
                lastBlockID = Nodepool.nodes[0].blockChain.lastBlockId
                newBlock.prevBlockHash = Nodepool.nodes[0].blockChain.blocks[lastBlockID].hash
                newBlock.hash = newBlock.GenerateHash()

                block = newBlock
                print('5.1 Destroyed the incorrect block, hence new block is:')
                block.Display()
        else:
            # link the broadcasted block to the blockchain
            # since the previous block is always verified and correct in each node, hence
            # choose any node and get it's last block information
            lastBlockID = Nodepool.nodes[0].blockChain.lastBlockId
            block.prevBlockHash = Nodepool.nodes[0].blockChain.blocks[lastBlockID].hash
            block.hash = block.GenerateHash()

        print('------------------------------')

        # if the validator is wrong
        if (validatorResult < MinConcensusRequired and validatorResult == 1) or (validatorResult > Nodepool.nodeCount/2 and validatorResult == 0):
            print('6. The Validator is cheater.')
            # put penalty to it, the penaly is just random some comparitively high value
            Nodepool.nodes[validatorID].reputation -= 10
        else:
            print('6. The Validator is trustworhty.')
            # give repuation point, which is very less compared to the penalty
            # this is ensured that the nodes don;t commit any fraud
            Nodepool.nodes[validatorID].reputation += 1


        print('------------------------------')
        print('7. Saving Block to each node')
        # now save the block to each node
        for nodeID in Nodepool.nodes:
            node = Nodepool.nodes[nodeID]
            node.CatchBlock(block)
            # add the caught block
            node.AddBlock()

        print()
        print('7. The saved block is along with verified tranactions:')
        block.Display()

        # remove the completed txns from packed txns
        print('------------------------------')
        print('8. Completing and Removing Verified Transaction from mempool.')

        for txn in block.data:      
            # before removing
            # complete the transaction
            uBase.CompleteTransaction(txn)
            Mempool.RemoveID(txn.id)

        print('------------------------------')
        print('UserInfo and Vote Balance')
        uBase.DisplayFormattedUserProfiles()
        print('------------------------------')

        # increment the nodepool's block counter of this simulation
        # it is incremented after every mempool packing cycle or when a new block is created
        # in between a cycle other than the temporary packing block
        Nodepool.blockCounter += 1

        if len(Mempool.txns) > 0:
            print('------------------------------')
        
            Mempool.DisplayTxns()
            print('------------------------------\n')

        #input()