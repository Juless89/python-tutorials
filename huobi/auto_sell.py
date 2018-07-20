import time
import huobiservices as hs


class Auto_seller():
    def __init__(self):
        # global variables
        self.tickers = ['usdt', 'steem']
        self.last_price = None
        self.balances = {}

    def sell_steem(self):
        # get current balance
        balance = self.balances['steem']

        # If balance greater than 1.000 sell total balance on the market
        if balance > 1.000:
            data = hs.send_order(balance, '', 'steemusdt', 'sell-market',
                                 price=0)
            print('\n\nCreated sell-market order')

            # check if sell order went ok
            if data['status'] == 'ok':
                order_id = data['data']

                # wait for exchange to process the order
                time.sleep(1)

                # retrieve and print information about the order
                data = hs.order_info(order_id)
                if data['status'] == 'ok':
                    cash_amount = float(data['data']['field-cash-amount'])
                    fees = float(data['data']['field-fees'])
                    print(f'id: {order_id}\nAmount: {balance:.3f} STEEM' +
                          f'\nSell value: {cash_amount:.5f} USDT\nFees: ' +
                          f'{fees:.5f} USDT\n')
                    time.sleep(1)

    # retrieve last order and extract the sell/buy price
    def update_price(self):
        data = hs.get_trade('steemusdt')
        if data['status'] == 'ok':
            self.last_price = data['tick']['data'][0]['price']

    # retrieve all balances and filter. Filter for funds that are tradeable
    def update_balances(self):
        # get balances
        data = hs.get_balance()

        # verify status message
        if data['status'] == 'ok':
            currencies = data['data']['list']

            # go over all currencies
            for currency in currencies:
                type = currency['type']
                if currency['currency'] in self.tickers and type == 'trade':
                    balance = currency['balance']
                    self.balances[currency['currency']] = float(balance)

    # Update balances and the STEEM price every second. When the STEEM
    # balane is greater than 1.000, sell total balance on the market.
    def run(self):
        while True:
            try:
                self.update_balances()
                self.update_price()
                print(f'STEEM/USDT: {self.last_price} STEEM: ' +
                      f'{self.balances["steem"]:.3f} USDT: ' +
                      f'{self.balances["usdt"]:.2f}', end='\r')
                self.sell_steem()
                time.sleep(1)
            except Exception as e:
                time.sleep(1)


if __name__ == '__main__':
    auto_seller = Auto_seller()
    auto_seller.run()
