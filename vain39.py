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

#%% Generate seed from mnemonic
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
# Construct from seed
bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
# Print master key
print(f"Master key (bytes): {bip44_mst_ctx.PrivateKey().Raw().ToHex()}")
print(f"Master key (extended): {bip44_mst_ctx.PrivateKey().ToExtended()}")
print(f"Master key (WIF): {bip44_mst_ctx.PrivateKey().ToWif()}")

# Construct from seed
bip84_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
# Print master key
print(f"Master key (bytes): {bip84_mst_ctx.PrivateKey().Raw().ToHex()}")
print(f"Master key (extended): {bip84_mst_ctx.PrivateKey().ToExtended()}")
print(f"Master key (WIF): {bip84_mst_ctx.PrivateKey().ToWif()}")

# Construct from seed
bip49_mst_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.LITECOIN)
# Print master key
print(f"Master key (bytes): {bip49_mst_ctx.PrivateKey().Raw().ToHex()}")
print(f"Master key (extended): {bip49_mst_ctx.PrivateKey().ToExtended()}")
print(f"Master key (WIF): {bip49_mst_ctx.PrivateKey().ToWif()}")

#%% Generate BIP44 account keys: m/44'/0'/0'
bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
# Generate BIP44 chain keys: m/44'/0'/0'/0
bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

# Generate BIP84 account keys: m/49'/0'/0'
bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0)
# Generate BIP49 chain keys: m/49'/0'/0'/0
bip84_chg_ctx = bip84_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

# Generate BIP49 account keys: m/49'/0'/0'
bip49_acc_ctx = bip49_mst_ctx.Purpose().Coin().Account(0)
# Generate BIP49 chain keys: m/49'/0'/0'/0
bip49_chg_ctx = bip49_acc_ctx.Change(Bip44Changes.CHAIN_EXT)


#%% Generate the first 10 addresses: m/44'/0'/0'/0/i
for i in range(10):
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(i)
    print(f"{i}. Address public key (extended): {bip44_addr_ctx.PublicKey().ToExtended()}")
    print(f"{i}. Address private key (extended): {bip44_addr_ctx.PrivateKey().ToExtended()}")
    print(f"{i}. Address: {bip44_addr_ctx.PublicKey().ToAddress()}")

    bip84_addr_ctx = bip84_chg_ctx.AddressIndex(i)
    print(f"{i}. Address public key (extended): {bip84_addr_ctx.PublicKey().ToExtended()}")
    print(f"{i}. Address private key (extended): {bip84_addr_ctx.PrivateKey().ToExtended()}")
    print(f"{i}. Address: {bip84_addr_ctx.PublicKey().ToAddress()}")

    bip49_addr_ctx = bip49_chg_ctx.AddressIndex(i)
    print(f"{i}. Address public key (extended): {bip49_addr_ctx.PublicKey().ToExtended()}")
    print(f"{i}. Address private key (extended): {bip49_addr_ctx.PrivateKey().ToExtended()}")
    print(f"{i}. Address: {bip49_addr_ctx.PublicKey().ToAddress()}")

# %%
