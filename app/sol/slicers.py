from solana.rpc.types import TokenAccountOpts, MemcmpOpts

def memcmp_owner(owner, offset):
    return [MemcmpOpts(offset=offset, bytes=str(owner)),]