import util.blockchain as blockchain

class MemPool:
    # it's a centrallised pool of transactions

    def __init__(self):
        # txn ID : txn object
        self.txns = {}
        self.txnsCount = 0

        self.blockPackCount = 5

    def Add(self, txn):

        self.txns[self.txnsCount] = txn
        txn.id = self.txnsCount
        self.txnsCount+=1

        return txn.id

    def RemoveID(self, txnID):
        '''meant to be removed when txn is in-valid or when all have been checked'''

        if txnID in self.txns:
            del self.txns[txnID]

    def DisplayTxns(self):
        print('Unfinished Transactions:')
        print('ID \tfrom \tto \tamt \tSignatrue \tHash')
        for i in self.txns:            
            txn = self.txns[i]
            print("{0} {1} {2} {3} {4} {5}".format(txn.id, txn.fromPublicKey, txn.toPublicKey, txn.amount ,txn.signature, txn.hash))
                
    def PackTransactions(self, blockId, n = 5):

        # packs 5 transaction per block
        block = blockchain.Block(blockId)

        packedTxns = []

        for txnId in list(self.txns.keys())[:n]:
            txn = self.txns[txnId]
            block.AddTransaction(txn)

        return block

    def GetActiveTxnsCount(self):
        return len(self.txns)