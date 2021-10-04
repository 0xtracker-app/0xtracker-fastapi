from solana.publickey import PublicKey

class SolanaNetwork:

    def __init__(self, wallet=None):
        self.wallet = wallet
        self.public_key = PublicKey(wallet)