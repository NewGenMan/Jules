class Broker:
    """Base class for broker integrations."""
    def get_account_balance(self):
        raise NotImplementedError

    def place_order(self, symbol, qty, side, order_type='MARKET'):
        raise NotImplementedError

    def get_positions(self):
        raise NotImplementedError

class MockBroker(Broker):
    """
    A mock broker for paper trading and testing.
    Records trades in memory without executing on a real exchange.
    """
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance
        self.positions = {} # {symbol: qty}
        self.trades = []

    def get_account_balance(self):
        return self.balance

    def place_order(self, symbol, qty, side, order_type='MARKET'):
        print(f"MOCK ORDER: {side} {qty} {symbol} ({order_type})")

        # Update positions
        current_qty = self.positions.get(symbol, 0)
        if side.upper() == 'BUY':
            self.positions[symbol] = current_qty + qty
        elif side.upper() == 'SELL':
            self.positions[symbol] = current_qty - qty

        self.trades.append({
            'symbol': symbol,
            'qty': qty,
            'side': side,
            'type': order_type
        })
        return {"status": "success", "order_id": len(self.trades)}

    def get_positions(self):
        return self.positions
