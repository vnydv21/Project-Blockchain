import helperModule
import nodepool
import mempool
import util.blockchain
import util.transaction


# the program random cause a validator block to cause return true take all transaction even if wrong as OK
# this raised the validator block reputation to die

#------------------
# 1. first create userAccounts
TotalNon_Contestants = 10
TotalContestants = 2

EC = helperModule.CreateUserBase(TotalNon_Contestants, TotalContestants)
EC.DisplayFormattedUserProfiles(0)

#------------------
# 2. now create nodes

# the non-validators nodes should be more than validator nodes
# the more the better to prevent 51% consensus attack
# which is major problem in Blockchains esp. cryptocurrencies

TotalNon_ValidtorNodes = TotalContestants * 5
TotalValidatorNodes = TotalContestants

helperModule.CreateNodes(TotalNon_ValidtorNodes, TotalValidatorNodes, EC)

EC.nodepool.DisplayNodes()
#------------------
# 3. now create a genesis block (starter block)
# and add this to all blockchains
# this block acts as the starting block of blockchain and
# contains no trasactions

genesisBlock = util.blockchain.Block(0)
genesisBlock.prevBlockHash = 0
genesisBlock.hash = genesisBlock.GenerateHash()

#increment the block counter of the nodepool to next index
EC.nodepool.blockCounter += 1

# display the genesis block
print('Displaying a Block:')
genesisBlock.Display()
print('---------------------------------------------------')

# now save this block to each nodes' blockchain
for nodeID in EC.nodepool.nodes:
    EC.nodepool.nodes[nodeID].blockChain.AddBlock(genesisBlock)

#------------------
# 4. now create a custom mempool to UserBase for storing transactions
# basically a MemPool sotres all the un-finished transaction, and as such is a technical name
EC.mempool = mempool.MemPool()

#------------------
# 5. now create initial transaction
# in the initial transaction the superUser distributes votePower to equally to each user

for regisID in EC.users:
    if regisID == EC.superUserID: continue

    # get the user
    user = EC.users.get(regisID)

    fromPublicKey = EC.users.get(EC.superUserID).GetPublicKey()
    toPublicKey = user.GetPublicKey()
    amount = 1

    # create a txns
    txn = util.transaction.Transaction(fromPublicKey, toPublicKey, amount)
    txn.SignTransaction(user)
    txn.hash = txn.GenerateHash()

    # save this txn to mempool
    EC.mempool.Add(txn)

EC.mempool.DisplayTxns()
print()
# ----------------

# 6. Now solve these initial transaction
helperModule.SolveMempool(EC)

# get the total no. verified block => just the number of blocks in any blockchain
print('Total Verified Block Count in Blockchain: ', len(EC.nodepool.nodes[0].blockChain.blocks))

# 7. now start voting


#-------------------------
import random

# now vote randomly to random party
for regisID in EC.users:
    if regisID == EC.superUserID: continue
    user = EC.users.get(regisID)

    # getRandom contestest
    constestentId = random.choice(EC.contestants)
    constestentPublicKey = EC.GetPublicKey(constestentId)
    
    txn = util.transaction.Transaction(EC.GetPublicKey(regisID), constestentPublicKey, 1)
    txn.SignTransaction(user)
    txn.hash = txn.GenerateHash()
    
    # save to mempool
    EC.mempool.Add(txn)
    
# now add some fraudulant txns
# now vote randomly to random party
for regisID in random.sample(EC.users.keys(), 3):
    if regisID == EC.superUserID: continue
    user = EC.users.get(regisID)

    # getRandom contestest
    constestentId = random.choice(EC.contestants)
    constestentPublicKey = EC.GetPublicKey(constestentId)
    
    txn = util.transaction.Transaction(EC.GetPublicKey(regisID), constestentPublicKey, 1)
    txn.SignTransaction(user)
    txn.hash = txn.GenerateHash()
    
    # save to mempool
    EC.mempool.Add(txn)


print('------------------------------')
print('Transaction during the voting phase:')
EC.mempool.DisplayTxns()
print('------------------------------')

# now solve the transactions again
helperModule.SolveMempool(EC)

# 9. get the winner
print('--------------------')
helperModule.DisplayWinner(EC)
