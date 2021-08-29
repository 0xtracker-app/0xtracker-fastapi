import asyncio
from evm import return_farms_list, get_evm_positions, get_one_inch_quote


asyncio.run(get_one_inch_quote([
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0xf7069e41C57EcC5F122093811d8c75bdB5f7c14e', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    {'token' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'network' : 'bsc'},
    ]))