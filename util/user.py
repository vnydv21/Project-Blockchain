
class User:

    PADDING = 0
    BASE = ""

    def __init__(self, regisID):
        self.id = regisID
        self._privateKey = 0
        self.publicKey = 0
        self.votePower = 0

    def __str__(self):
        '''to display user info'''
        return "{0} \t{1} \t{2}".format(self.id, self.publicKey, self.votePower)

    def GetPublicKey(self):
        return self.publicKey

    def VerifySignature(self, sign):
        publicKey = self.publicKey

        # take first padding characters of signature
        toCheck = sign[:User.PADDING]
        
        decoded = ""

        for character in toCheck:
            index =  User.BASE.index(character)
            decoded += publicKey[index]

        try:            
            decoded = int(decoded)
            if decoded == self.id:
                return True
        except:
            return False

    def GenerateSignuture(self, msg):
        privateKey = self._privateKey
        regisID = str(self.id).zfill(User.PADDING)

        # logic to use private key and msg to generate a signature
        # basically using substituion cipher privatekey => random hex digits => subsitution of "0123456789ABCDEF "
        # public key => a subsituin such that when applied to signature -> the first 4 numbers are XXXX -> user regisID

        # just a simplified version and very easy to hack.
        sign = regisID + msg
        encryptedSign = ""
        
        for character in sign:
            index =  User.BASE.index(character)
            encryptedSign += privateKey[index]
            
            
        return encryptedSign
