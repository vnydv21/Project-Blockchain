import hashlib
import random
import util.user as user
import util.transaction as transaction

class UserBase:

    # repersents a char-set for generating pulblic or private keys from
    # X-> is just space
    BASE = "0123456789ABCDEFX"
    # for around 10K users, check how public-private encruyption is working
    PADDING = 5

    @staticmethod
    def INIT():
        '''Always call this method when the module is imported'''
        # init the static variables in transaction and user modules
        transaction.Transaction.PADDING = UserBase.PADDING
        transaction.Transaction.BASE = UserBase.BASE

        user.User.PADDING = UserBase.PADDING
        user.User.BASE = UserBase.BASE
    
    def __init__(self):

        # regisID : user
        self.users = {}

        # stores the number of users created so far
        # this never decrements
        self.userCounter = 0
        
        # only the first 4 character of public keys are constant rest are random and unique
        # will hash and store for fast access
        # publicKeyHash : userId
        self.userKeys = {}

        self.contestants = []
        self.superUserID = 0


        # the link to nodepool
        self.nodepool = None
        
        # the link to mempool
        self.mempool = None


    def ContestantCount(self):
        return len(self.contestants)

    def GenerateUser(self):    
        regisID = self.userCounter

        newUser = user.User(regisID)
        newUser._privateKey = UserBase.GetaPrivateKey()
        newUser.publicKey = self.GeneratePublicKey(newUser)

        self.users[regisID] = newUser
        self.userKeys[newUser.publicKey] = regisID

        self.userCounter += 1

        return regisID

    @staticmethod
    def GetaPrivateKey():
        newKey = list(UserBase.BASE)
        random.shuffle(newKey)
        return ''.join(newKey)
        
    def GeneratePublicKey(self, user):
        # do sth
        _privateKey = user._privateKey

        # use private key find letter that subsitue to regisID str zfilled wrt BASE
        # 4 chars + rest of the BASE chars in shuffle order such that there is no user for that ID doesn't exist in userBase
        
        regisID = str(user.id).zfill(UserBase.PADDING)

        # substitue required regisIDs with given subsitution and don't touch any other
        # regisID is not encryptred
        

        privateDict = dict(zip(UserBase.BASE,_privateKey))
        publicDict = dict(zip(UserBase.BASE, ''*len(UserBase.BASE)))

        notToIncAsKey = []
        notToIncAsValue = []

        for m in set(regisID):
            enc = privateDict[m]            
            publicDict[enc] = m

            notToIncAsKey.append(enc)
            notToIncAsValue.append(m)

        
        newValue = list(UserBase.BASE)
        for value in  notToIncAsValue:
            newValue.remove(value)

        random.shuffle(newValue)

        newKey = list(UserBase.BASE)
        for key in  notToIncAsKey:
            newKey.remove(key)

        publicDict.update(dict(zip(newKey,newValue)))

        publicKey = ''.join([publicDict[i] for i in UserBase.BASE])

        return publicKey


    def CompleteTransaction(self, txn):
        '''This finalise the transaction between user
        call only when the transaction are forged into blocks
        on each nodes' blockchain'''

        # take the public keys
        A, B, amt = txn.fromPublicKey, txn.toPublicKey, txn.amount

        # get user IDs
        userAid = self.userKeys.get(A)
        userBid = self.userKeys.get(B)

        # get the users object
        userA = self.users.get(userAid)
        userB = self.users.get(userBid)
        
        # do the balance
        userA.votePower -= amt
        userB.votePower += amt

    def GetPublicKey(self, userID):
        '''get the public key of user specified by ID'''
        user = self.users.get(userID)
        return user.publicKey


    def DisplayFormattedUserProfiles(self, n = 0):
        '''Layout the user profiles on console in clear and concise way
        n => the minimun no. of user to display on screen'''

        # if n is 0 or a negative number
        # or n is more than total user count
        if (n <= 0) or (n > self.userCounter):
            n = self.userCounter

        # print the formatted code
        print('---------------------------------------------------')
        print('Displaying User Profiles from UserBase:')
        print()
        print('Total User Counted:', self.userCounter)
        print()
        print('   RegisId    \tPublic Key    \t\tVotePower')
        print('---------------------------------------------------')
        # assumes all users exist and have regisIds as integers <= userCount
        for i in range(n):
            user = self.users[i]
            print('     ',str(user))
        print()

        print('Contestant Ids: ', self.contestants, sep='\n')
        print('---------------------------------------------------')
        print()
