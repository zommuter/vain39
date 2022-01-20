# %%
from bip_utils import (
    Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44Changes, Bip44Coins, Bip44, Bip84Coins, Bip84, Bip49Coins, Bip49
)
from bip_utils.bip.bip44_base import Bip44Base

import colorama, re
colorama.init(autoreset=True)

def new_mnemonic():
    return Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)

class Address_Generator(object):
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

#%%
pattern = r'(?<=^bc1.)(42)'
keep_running = True

done = False
while(not done or keep_running):
    # Generate random mnemonic
    mnemonic = new_mnemonic()

    address_generators = {}
#    for bip in (44, 84, 49, -44):
    for bip in (84,):
        coin_type = "ETHEREUM" if bip == -44 else "BITCOIN"
        address_generators[bip] = Address_Generator(bip=abs(bip), coin_type=coin_type, mnemonic=mnemonic, accounts=5, addresses=5)
        addresses = address_generators[bip].addresses
        for acc_key, accounts in enumerate(addresses):
            for key, address in enumerate(addresses[acc_key]):
                if re.search(pattern, address):
                    match = re.sub(pattern, colorama.Fore.RED + r'\1' + colorama.Fore.RESET, address)
                    done = True
                    print(f"{match}: {bip}/{acc_key}/{key} @ {mnemonic} ")
# %%
