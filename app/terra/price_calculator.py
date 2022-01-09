from .oracles import get_price_from_terraswap
from . import token_routes

class TokenOverride:

    def __init__(self, session=None):
        self.tokens = {
            'terra1zsaswh926ey8qa5x4vj93kzzlfnef0pstuca0y' : [get_price_from_terraswap, {'query' : token_routes.bPsiDP24m(), 'amount' : '1000000', 'decimal' : 6, 'router' : 'terra19qx5xe6q9ll4w0890ux7lv2p4mf3csd4qvt3ex', 'client' : self.client}],
}