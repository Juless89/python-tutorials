<center>![banner.png](https://cdn-images-1.medium.com/max/1600/1*W3Lh17Km2be2NPIZAu5jbg.png)</center>

This tutorial is part of a series where different aspects of programming with Python are explained, using Python and public libraries to make useful tools.

---

#### Repository
https://github.com/huobiapi/REST-Python3-demo

#### What will I learn

- Setting up your Huobi API keys
- Retrieving account balances
- Retrieving current market price
- Creating market-sell orders
- Automated selling

#### Requirements

- Python3.6
- [Huobi account](https://www.huobi.com/en-us/)

#### Difficulty

- intermediate

---

### Tutorial

#### Preface

[Huobi](https://www.huobi.com/en-us/) is a Chinese exchange that offers trading in `STEEM/USDT`. While their website offers decent translation to English, the API documentation is lacking a bit. `STEEM/USDT` is a useful pair that offers great stability. For example setting up a bot that automatically sells any incoming `STEEM` for `USDT`. The value of the `USDT` will not change.

#### Setup
Download the files from [Github](https://github.com/Juless89/python-tutorials/tree/master/huobi). There are 3 files. The code is contained in `auto_sell.py` the other 2 files are files from Huobi that contain their API code. `huobiservices.py` contains all the functions that allow for interaction with the exchange functionality. `utils.py` contains the required code to perform the API requests. In this file the API `ACCESS_KEY` and `SECRET_KEY` are set.

Run scripts as following:
`> python auto_sell.py`

#### Setting up your Huobi API keys
In order to perform API requests with the Huobi exchange you need to set up an `API key` within your account. Go to `API Management` from the drop down menu which is found in the top right corner.

<center>![Screenshot 2018-07-20 13.00.58.png](https://cdn.steemitimages.com/DQmYjApLMuKnMy7wfrYPM4mpgb2XKd6kUaxh6b4p1maNqRC/Screenshot%202018-07-20%2013.00.58.png)</center>

Here you can create an `API key`. It is recommended to bind an IP address for added security. Keep in mind that an `API key` allows for full access to your exchange account. Including withdrawals.

<center>![Screenshot 2018-07-20 13.01.13.png](https://cdn.steemitimages.com/DQmTXbz9o4jtVuHgowbVeJDdiBNmDgGi6Gg4V72rsuPD7pY/Screenshot%202018-07-20%2013.01.13.png)</center>

#### Retrieving account balances
The `get_balance()` function can be used to retrieve a full list of all the account's balances. Every response contains a `status` message and the `data` relevant to to the request.  Inside data there is a list that contains all the currencies and their balances. Each currency has two entries, the difference is their type: `trade` or `frozen`.


```
{
	'status': 'ok',
	'data': {
		'id': 9999999,
		'type': 'spot',
		'state': 'working',
		'list': [{
			'currency': 'hb10',
			'type': 'trade',
			'balance': '0'
    }, {
			'currency': 'hb10',
			'type': 'frozen',
			'balance': '0'
		}
```
In order to retrieve the trade able balances for `STEEM` and `USDT` a list is set with their tickers. The `get_balance()` request is performed and checked to be `ok`. The currency list is then extracted from the returned data and checked against the tickers. For each ticker that matches and is of the type `trade`, their balance is taken and added to the `balances` dict.

```
self.tickers = ['usdt', 'steem']
self.balances = {}


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
```

#### Retrieving current market price
Huobi does not offer a direct API for the current market price for a given trade pair. Instead the last trade can be requested which contains the last trading price. This is done with the `get_trade(symbol)` function. Inside the response the `price` can be found.

```
{
	'status': 'ok',
	'ch': 'market.steemusdt.trade.detail',
	'ts': 1532039331826,
	'tick': {
		'id': 12997659863,
		'ts': 1532039302973,
		'data': [{
			'amount': 0.0358,
			'ts': 1532039302973,
			'id': 129976598638136614141,
			'price': 1.5018,
			'direction': 'sell'
		}]
	}
}
```

The price is retrieved by first checking if the request went `ok`. If so the `price` can be extracted.

```
# retrieve last order and extract the sell/buy price
def update_price(self):
    data = hs.get_trade('steemusdt')
    if data['status'] == 'ok':
        self.last_price = data['tick']['data'][0]['price']
```



#### Creating market-sell orders
There are different kind of orders: `buy-market`, `sell-market`, `buy_limit` and `sell-limit`. Market orders execute on the current market price while limit order allow for a buy/sell price to be set. When wanting to sell everything a `sell-market` order is the simplest. Doing so with a `sell-limit` would require additional research into the depth of the market to decide what price to sell at. This example will be using the `sell-market` type. The `send_order()` functions takes 5 arguments: the `amount` to buy/sell, `source` which is only required for margin orders, `symbol` which trade pair, `_type` of order and the `price` which is set to 0 by default for market orders. An order that is accepted return the the status `ok` and the `order_id`.


```
{
	'status': 'ok',
	'data': '8133838204'
}
```

The `order_id` can than be used to retrieve the full status about the order with the `order_info()` function.

```
{
	'status': 'ok',
	'data': {
		'id': 8133838204,
		'symbol': 'steemusdt',
		'account-id': 4244527,
		'amount': '1.000000000000000000',
		'price': '0.0',
		'created-at': 1532036264999,
		'type': 'sell-market',
		'field-amount': '1.000000000000000000',
		'field-cash-amount': '1.501600000000000000',
		'field-fees': '0.003003200000000000',
		'finished-at': 1532036265361,
		'source': 'spot-api',
		'state': 'filled',
		'canceled-at': 0
	}
}
```

In this example the order is send and verified to be `ok`. If so the `order_i` is taken and the additional information about the order is requested. There is a 1 second delay to account for the exchange processing the order. The status of the returned data is checked and then the preferred information is taken, converted and printed to the terminal.

```
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
                          f'{fees:.5f} US
```

#### Automated selling

All of this can be combined to create an automated selling script. Every second the script updates the balances and the current price of `STEEM/USDT`. These are printed to the terminal with the additional argument `end='\r'` so the same line is updated instead of a new line being created. Then the balance of `STEEM` is checked, if greater than 1.000 the whole balance is sold in a `sell-market` order.


```
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
```


#### Running the code

Running the script allows for easy automated selling of `STEEM` for `USDT`. Whenever new `STEEM` gets deposited into the account it will be automatically sold after it reached a certain threshold.

<center>![Screenshot 2018-07-20 13.51.26.png](https://cdn.steemitimages.com/DQmYe2X1D9YqZ1PKn1ipbz9wYd9mVp8AJgnrxUqmfGxJYH7/Screenshot%202018-07-20%2013.51.26.png)</center>


```
python auto_sell.py
STEEM/USDT: 1.4598 STEEM: 1.150 USDT: 74.17

Created sell-market order
id: 8177315461
Amount: 1.150 STEEM
Sell value: 1.67762 USDT
Fees: 0.00336 USDT

STEEM/USDT: 1.4588 STEEM: 0.000 USDT: 75.84
```

---

The code for this tutorial can be found on [Github](https://github.com/Juless89/python-tutorials/tree/master/huobi)!

This tutorial was written by @juliank.
