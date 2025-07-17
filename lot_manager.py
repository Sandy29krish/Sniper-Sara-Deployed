# lot_manager.py

import math

def calculate_lot_size(capital: float, option_price: float, lot_size: int = 25, max_allocation_percent: float = 0.25):
    """
    Calculate dynamic lot size based on available capital and option premium.

    Parameters:
    - capital: total available capital
    - option_price: price of one option (premium)
    - lot_size: number of options per lot (25 for NIFTY, 15 for BANKNIFTY)
    - max_allocation_percent: maximum % of capital to risk per trade (default: 25%)

    Returns:
    - number of lots (int)
    - total capital used (float)
    """
    max_capital_to_use = capital * max_allocation_percent
    cost_per_lot = option_price * lot_size

    if cost_per_lot == 0:
        return 0, 0.0

    lots = math.floor(max_capital_to_use / cost_per_lot)
    total_cost = lots * cost_per_lot
    return lots, total_cost


def filter_otm_option_chain(option_chain: list, spot_price: float, direction: str, max_price: float = 60):
    """
    Filter the next OTM strike option based on direction and price cap.

    Parameters:
    - option_chain: list of options with 'strike' and 'last_price'
    - spot_price: current index spot price
    - direction: 'CE' or 'PE'
    - max_price: max premium for option entry (e.g. 60)

    Returns:
    - selected option dict or None
    """
    sorted_chain = sorted(option_chain, key=lambda x: x['strike'])
    
    if direction == 'CE':
        otm_options = [opt for opt in sorted_chain if opt['strike'] > spot_price and opt['type'] == 'CE']
    else:
        otm_options = [opt for opt in reversed(sorted_chain) if opt['strike'] < spot_price and opt['type'] == 'PE']

    for opt in otm_options:
        if opt['last_price'] <= max_price:
            return opt

    return None  # No suitable OTM option found
