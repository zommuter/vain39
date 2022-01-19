# %%
import binascii
import bip_utils

from bip_utils import (
    Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44Changes, Bip44Coins, Bip44, Bip84Coins, Bip84, Bip49Coins, Bip49
)

#%% Generate random mnemonic
def new_mnemonic():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

mnemonic = new_mnemonic()
print(f"Mnemonic string: {mnemonic}")

class Bipper(object):
    def __init__(self, bip=44, seed_bytes:bytes = None, mnemonic=None, coin_type = "BITCOIN"):
        self.Bip = {44: Bip44, 49: Bip49, 84: Bip84}[bip]
        self.coin_type = {44: Bip44Coins, 49: Bip49Coins, 84: Bip84Coins}[bip][coin_type]
        assert (seed_bytes is None) or (mnemonic is None), "Cannot provide both seed_bytes and mnemonic"
        if seed_bytes is None:
            # Generate seed from mnemonic
            self.mnemonic = mnemonic or new_mnemonic()
            self.seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate()
        else:  # seed_bytes provided, hence mnemonic is None
            self.mnemonic = None
            self.seed_bytes = seed_bytes

        # Construct from seed
        self.mst_ctx = self.Bip.FromSeed(self.seed_bytes, self.coin_type)

        # Print master key
        #print(f"Master key (bytes): {self.mst_ctx.PrivateKey().Raw().ToHex()}")
        #print(f"Master key (extended): {self.mst_ctx.PrivateKey().ToExtended()}")
        #print(f"Master key (WIF): {self.mst_ctx.PrivateKey().ToWif()}")

    def generate_account_keys(self, account:int = 0):
        self.acc_ctx = self.mst_ctx.Purpose().Coin().Account(account)
        self.chg_ctx = self.acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    def get_address(self, account:int = None, address_index:int = 0):
        if account is not None: self.generate_account_keys(account=account)
        return self.chg_ctx.AddressIndex(address_index)

bippers = {}
for bip in (44, 84, 49, -44):
    coin_type = "ETHEREUM" if bip == -44 else "BITCOIN"
    print(f"BIP{bip}")
    bippers[bip] = Bipper(bip=abs(bip), coin_type=coin_type)
    bippers[bip].generate_account_keys()

# Generate the first 3 addresses: m/44'/0'/0'/0/i
    for i in range(3):
        addr_ctx = bippers[bip].get_address(i)
        #print(f"{i}. Address public key (extended): {addr_ctx.PublicKey().ToExtended()}")
        #print(f"{i}. Address private key (extended): {addr_ctx.PrivateKey().ToExtended()}")
        print(f"{i}. Address: {addr_ctx.PublicKey().ToAddress()}")

# %%
