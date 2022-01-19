# %%
from bip_utils import (
    Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44Changes, Bip44Coins, Bip44, Bip84Coins, Bip84, Bip49Coins, Bip49
)
from bip_utils.bip.bip44_base import Bip44Base

def new_mnemonic():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

class Bipper(object):
    def __init__(self, bip=44, seed_bytes:bytes = None, mnemonic=None, coin_type = "BITCOIN"):
        self.Bip: Bip44Base = {44: Bip44, 49: Bip49, 84: Bip84}[bip]
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

        self.accounts = {}

    def get_account_key(self, account:int = 0):
        if not account in self.accounts:
            acc_ctx = self.mst_ctx.Purpose().Coin().Account(account)
            self.accounts[account] = {
                'acc_ctx': acc_ctx,
                'chg_ctx': acc_ctx.Change(Bip44Changes.CHAIN_EXT),
                'address_index': 0
            }
        return self.accounts[account]

    def get_address(self, address_index:int = None, account:int = 0):
        account_key = self.get_account_key(account=account)
        chg_ctx: Bip44Base = account_key['chg_ctx']
        if address_index is None:
            address_index = account_key['address_index']
            account_key['address_index'] += 1
        return (chg_ctx.AddressIndex(address_index), address_index)

#%% Generate random mnemonic
mnemonic = new_mnemonic()
print(f"Mnemonic string: {mnemonic}")

#%%
bippers = {}
for bip in (44, 84, 49, -44):
    coin_type = "ETHEREUM" if bip == -44 else "BITCOIN"
    print(f"BIP{bip}")
    bippers[bip] = Bipper(bip=abs(bip), coin_type=coin_type, mnemonic=mnemonic)

#%% Generate 3 addresses: m/44'/0'/0'/0/i
for bip in (44, 84, 49, -44):
    print(f"BIP{bip}")
    for i in range(3):
        (addr_ctx, address_index) = bippers[bip].get_address()
        print(f"{address_index}. Address: {addr_ctx.PublicKey().ToAddress()}")

# %%
