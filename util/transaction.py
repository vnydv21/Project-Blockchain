import json
import hashlib

class Transaction:

    BASE = None
    PADDING = None

    def __init__(self, fromPublicKey, toPublicKey, amount):
        self.id = 0

        self.fromPublicKey = fromPublicKey
        self.toPublicKey = toPublicKey

        self.amount = amount

        # once created call the SignTransaction to sign this txn

        # the transaction has a hash consisting of all data
        # generated after signature is generated
        self.hash = 0


    def SignTransaction(self, user):
        # it's the last step, first from, to and amt must be set
        msg = self.GetMessage()
        
        self.signature = user.GenerateSignuture(msg)
        return self.signature
    
    def GetMessage(self):
        # returns the message for this transaction A B 1, X represents the space character
        return "{0}X{1}X{2}".format(self.fromPublicKey, self.toPublicKey, self.amount)

    def GenerateHash(self):
        # used to get the hash of this txn, the "main" will initially set a hash which can be later tested
        jsonData = self.JSONify()

        #convert to utf-8
        encoded = jsonData.encode('utf-8')

        #apply hashing
        return hashlib.sha256(encoded).hexdigest()

    def JSONify(self):
        data = {
            "id":self.id,
            "from": self.fromPublicKey,
            "to": self.toPublicKey,
            "amt": self.amount,
            "signature": self.signature
        }

        return json.dumps(data)
        

    def __str__(self):
        return self.JSONify()