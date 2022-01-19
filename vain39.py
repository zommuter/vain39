# %%
from bip_utils import (
    Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44Changes, Bip44Coins, Bip44, Bip84Coins, Bip84, Bip49Coins, Bip49
)
from bip_utils.bip.bip44_base import Bip44Base

def new_mnemonic():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

class Bipper(object):
    def __init__(self, bip=44,
                 seed_bytes:bytes = None, mnemonic=None,
                 coin_type = "BITCOIN",
                 accounts = 1, addresses = 20):
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

        self.acc_ctxs = [self.mst_ctx.Purpose().Coin().Account(i) for i in range(accounts)]
        self.chg_ctxs = [acc_ctx.Change(Bip44Changes.CHAIN_EXT) for acc_ctx in self.acc_ctxs]
        self.address_indices = [0] * accounts
        self.keys = [[self.get_address(address_index=address_index, account=account)[0] for address_index in range(addresses)] for account in range(accounts)]
        self.addresses = [[self.keys[account][address_index].PublicKey().ToAddress() for address_index in range(addresses)] for account in range(accounts)]

    def get_address(self, address_index:int = None, account:int = 0):
        chg_ctx: Bip44Base = self.chg_ctxs[account]
        if address_index is None:
            address_index = self.address_indices[account]
            self.address_indices[account] += 1
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
    print(bippers[bip].addresses)

#%% Generate 3 addresses: m/44'/0'/0'/0/i
for bip in (44, 84, 49, -44):
    print(f"BIP{bip}")
    for i in range(3):
        (addr_ctx, address_index) = bippers[bip].get_address()
        print(f"{address_index}. Address: {addr_ctx.PublicKey().ToAddress()}")

# %%
