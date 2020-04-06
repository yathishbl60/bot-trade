from enum import Enum


class SymbolStatus(Enum):
    PRE_TRADING = 'PRE_TRADING'
    TRADING = 'TRADING'
    POST_TRADING = 'POST_TRADING'
    END_OF_DAY = 'END_OF_DAY'
    HALT = 'HALT'
    AUCTION_MATCH = 'AUCTION_MATCH'
    BREAK = 'BREAK'

