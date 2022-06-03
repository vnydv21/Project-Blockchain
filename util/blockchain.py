import copy
import hashlib
import json


class Block:

    def __init__(self, blockId):
        # is basically a counter that increments when a new block is created        
        # id must be provided from the chain creator
        self.id = blockId
        self.hash : hex = 0

        # are transactions ids
        self.data = []
                
        self.prevBlockHash : hex = 0

        # not a part of the overall data but included to link blocks
        self.prevBlockId : int = -1
        self.nextBlockId : int = 0
    
    def GenerateHash(self):
        # first convert the info into json format
        # go with converting transaction data into json format
        blockData = []

        for txn in self.data:
            blockData.append(txn.hash)

        blockData = {
            'id': self.id,
            'prevHash': self.prevBlockHash,
            'data': blockData
        }

        #encode it
        jsonified = json.dumps(blockData)
        encoded = jsonified.encode('utf-8')

        return hashlib.sha256(encoded).hexdigest()

    def AddTransaction(self, txn):
        '''add the copy of the transaction to this block
        this doesn't verfiy but assumes it's verified.'''
        self.data.append(copy.deepcopy(txn))

    def Display(self):
        '''prints the data of this block on console'''

        blockData = []

        for txn in self.data:
            blockData.append(txn.hash)

        blockData = {
            'id': self.id,
            'prevHash': self.prevBlockHash,
            'data': blockData,
            'hash': self.hash
        }

        print(json.dumps(blockData,indent=3))


class BlockChain:

    def __init__(self, nodeId):

        self.nodeId = nodeId
        self.id : int = 0
        
        self.lastBlockId : int = -1

        # stored as id - block (object) pair
        self.blocks : dict = {}

    def AddBlock(self, block):        
        thisBlockId = block.id

        # get the last block in chain
        if self.lastBlockId != -1:
            lastBlock = self.blocks[self.lastBlockId]
            # make its' next block id to thisblockid
            lastBlock.nextBlockId = thisBlockId
        else:
            pass

        #deepcopy the block and add to chain
        thisBlock = copy.deepcopy(block)
        
        if self.lastBlockId != -1:            
            thisBlock.prevBlockId = lastBlock.id
            thisBlock.prevBlockHash = lastBlock.hash
        else:
            thisBlock.prevBlockId = -1
            thisBlock.prevBlockHash = 0

        self.blocks[thisBlockId] = thisBlock
        self.lastBlockId = thisBlockId
        # return success block added successfully
        return True

    def Display(self):
        print('Blockchain of Node', self.nodeId)

        for blockID in self.blocks:
            print(self.blocks[blockID].JSONify())
        

