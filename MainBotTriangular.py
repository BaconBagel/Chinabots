__author__ = 'reddit.com/u/DotGaming'


import huobi
import huobi2
import sys
print sys.argv
import urllib2
import time
import json
import okcoin
list = []
import btcchina
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
counter = 0
# data logging

list_btc_profit = []
list_ltc_profit = []
list_ltc_tradeback = []
list_btc_tradeback = []
list_triangular_1 = []
list_triangular_2 = []
listcounter = 0



access_key_okcoin= 'Insert OKcoin Public Key!'
secret_key_okcoin = 'Insert OKcoin Secret Key!'
access_key_huobi= 'Insert Huobi Public Key!'
secret_key_huobi = 'Insert Huobi Secret Key!'

okconf = okcoin.TradeAPI(access_key_okcoin, secret_key_okcoin)
asd = huobi.HuoBi(access_key_huobi, secret_key_huobi)
asd2 = huobi2.HuoBi(access_key_huobi, secret_key_huobi)


from decimal import *

# Get balances and create prefixes
account_counter = 0

while 1 == 1:






    if account_counter == 0 or account_counter % 40 == 0:
        bbb = okconf.get_info()
        okcoin_cny_balance = float(bbb['info']['funds']['free']['cny'])
        okcoin_ltc_balance = float(bbb['info']['funds']['free']['ltc'])
        okcoin_btc_balance = float(bbb['info']['funds']['free']['btc'])

        resp2 = asd2.get_account_info2()
        huobi_ltc_balance = float(resp2["available_ltc_display"])
        huobi_cny_balance = float(resp2["available_cny_display"])
        huobi_btc_balance = float(resp2["available_btc_display"])

    response = urllib2.urlopen('http://market.huobi.com/staticmarket/depth_ltc_json.js')
    data = json.load(response)

    huobidepth = data

    a1 = huobidepth
    a1 = a1['bids'][0][0]
    huobi_highest_buy_price = float(a1)
    b2 = huobidepth
    b2 = b2['bids'][0][1]
    huobi_highest_buy_volume = float(b2)
    c3 = huobidepth
    c3 = c3["asks"][-1][1]
    huobi_lowest_sell_volume = float(c3)
    d4 = huobidepth
    d4 = d4["asks"][-1][0]
    huobi_lowest_sell_price = float(d4)



    huobidepth = huobi.get_depth("BTC", 10)

    a1 = huobidepth
    a1 = a1['top_buy'][0]['price']
    huobi_highest_buy_price_btc = float(a1)
    b2 = huobidepth
    b2 = b2['top_buy'][0]['amount']
    huobi_highest_buy_volume_btc = float(b2)
    c3 = huobidepth
    c3 = c3['top_sell'][0]['amount']
    huobi_lowest_sell_volume_btc = float(c3)
    d4 = huobidepth
    d4 = d4['top_sell'][0]['price']
    huobi_lowest_sell_price_btc = float(d4)

    M = okcoin.MarketData()
    okcoin_sell_list = dict.items(M.get_depth('ltc_cny').asks)


    lowest_sell = min(okcoin_sell_list)
    okcoin_lowest_sell_price = lowest_sell[0]
    okcoin_lowest_sell_volume = lowest_sell[1]
    okcoin_buy_list = dict.items(M.get_depth('ltc_cny').bids)

    highest_buy = max(okcoin_buy_list)
    okcoin_highest_buy_price = highest_buy[0]
    okcoin_highest_buy_volume = highest_buy[1]


    okcoin_sell_list = dict.items(M.get_depth('btc_cny').asks)

    lowest_sell = min(okcoin_sell_list)
    okcoin_lowest_sell_price_btc = lowest_sell[0]
    okcoin_lowest_sell_volume_btc = lowest_sell[1]
    okcoin_buy_list = dict.items(M.get_depth('btc_cny').bids)

    highest_buy = max(okcoin_buy_list)
    okcoin_highest_buy_price_btc = highest_buy[0]
    okcoin_highest_buy_volume_btc = highest_buy[1]


    #cheapest way to buy ltc?


    #difference = ((okcoin_highest_buy_price_btc - btcchina_lowest_sell_price_btc) / btcchina_lowest_sell_price_btc)*100
    #tradeback = ((btcchina_highest_buy_price_btc - okcoin_lowest_sell_price_btc)/okcoin_lowest_sell_price_btc) *100
    #ltc_difference = ((btcchina_highest_buy_price - okcoin_lowest_sell_price) / okcoin_lowest_sell_price)*100
    #difference2 = ((okcoin_highest_buy_price - btcchina_lowest_sell_price) / btcchina_lowest_sell_price)*100
    difference3 = ((huobi_highest_buy_price_btc- okcoin_lowest_sell_price_btc) /okcoin_lowest_sell_price_btc) *100
    difference4 = ((okcoin_highest_buy_price_btc - huobi_lowest_sell_price_btc)/ huobi_lowest_sell_price_btc) *100
    counter += 1





    f = okcoin_highest_buy_price_btc / okcoin_lowest_sell_price

    g = huobi_lowest_sell_price_btc / huobi_highest_buy_price

    triangular = ((f-g)/g)*100
    list5.append(triangular)
    print "triangular is " + str(max(list5))

    a = huobi_highest_buy_price_btc / huobi_lowest_sell_price

    l = okcoin_lowest_sell_price_btc / okcoin_highest_buy_price

    triangular2 = ((a-l)/l)*100
    list6.append(triangular2)
    print "Triangular2 is " + str(max(list6))

    ratio = huobi_highest_buy_price_btc/ huobi_highest_buy_price

    min_volume_triangular = min(okcoin_highest_buy_volume_btc*ratio, okcoin_lowest_sell_volume, huobi_lowest_sell_volume_btc*ratio,huobi_highest_buy_volume,okcoin_btc_balance*ratio, huobi_ltc_balance )
    min_volume_triangular2 = min(okcoin_highest_buy_volume, okcoin_lowest_sell_volume_btc*ratio, huobi_lowest_sell_volume,huobi_highest_buy_volume_btc*ratio, okcoin_ltc_balance, huobi_btc_balance*ratio )

    if 0 < triangular and 2 < min_volume_triangular:
        account_counter == 0
        print "trade"
        trade_okcoin = okconf.trade('btc_cny', 'sell', okcoin_highest_buy_price_btc, min_volume_triangular/ratio)

        trade_huobi = asd2.sell(2,huobi_highest_buy_price, min_volume_triangular, currency="ltc")
        print trade_huobi


        #Handle partials

        trade_okcoin_id = trade_okcoin['order_id']
        okcoin_order_status = okconf.get_order(trade_okcoin_id, "btc_cny")
        okcoin_order_status = okcoin_order_status['orders']
        print okcoin_order_status
        partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        while 1 < partial_amount:
            okconf.cancel_order(trade_okcoin_id, "btc_cny")
            time.sleep(1)
            okcoin_buy_list = dict.items(M.get_depth('btc_cny').bids)
            highest_buy = max(okcoin_buy_list)
            okcoin_highest_buy_price_btc = highest_buy[0]
            okcoin_highest_buy_volume_btc = highest_buy[1]
            time.sleep(1)
            trade_okcoin = okconf.trade('btc_cny', 'sell', okcoin_highest_buy_price_btc, min_volume_triangular/ratio)
            time.sleep(2)
            trade_okcoin_id = trade_okcoin['order_id']
            okcoin_order_status = okconf.get_order(trade_okcoin_id, "btc_cny")
            okcoin_order_status = okcoin_order_status['orders']

            partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]


        trade_huobi_id = trade_huobi['id']
        trade_huobi_status = asd2.get_order(2, trade_huobi_id, currency="ltc")
        partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])

        while 2 < partial_amount2:
            asd2.cancel_order(2,trade_huobi_id, 'ltc')
            time.sleep(2)

            response = urllib2.urlopen('http://market.huobi.com/staticmarket/depth_ltc_json.js')
            data = json.load(response)
            huobidepth = data
            a1 = huobidepth
            a1 = a1['bids'][1][0]
            huobi_highest_buy_price = float(a1)
            trade_huobi = asd2.sell(2,huobi_highest_buy_price, min_volume_triangular, currency="ltc")
            print trade_huobi
            trade_huobi_id = trade_huobi['id']
            time.sleep(2)
            trade_huobi_status = asd2.get_order(2, trade_huobi_id, currency="ltc")
            trade_huobi_state = trade_huobi_status['status']
            partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])
            print("we have a partial in huobi, handling")

        time.sleep(1)

        trade_okcoin = okconf.trade('ltc_cny', 'buy', okcoin_lowest_sell_price, min_volume_triangular)

        trade_huobi = asd2.buy(1,huobi_lowest_sell_price_btc, min_volume_triangular/ratio, currency="btc")
        print trade_huobi

        trade_okcoin_id = trade_okcoin['order_id']
        okcoin_order_status = okconf.get_order(trade_okcoin_id, "ltc_cny")
        okcoin_order_status = okcoin_order_status['orders']
        print okcoin_order_status

        partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        while 0.2 < partial_amount:
            okconf.cancel_order(trade_okcoin_id, "ltc_cny")
            time.sleep(1)
            okcoin_sell_list = dict.items(M.get_depth('ltc_cny').asks)
            lowest_sell = min(okcoin_sell_list)
            okcoin_lowest_sell_price = lowest_sell[0]
            okcoin_lowest_sell_volume = lowest_sell[1]
            time.sleep(1)
            trade_okcoin = okconf.trade('ltc_cny', 'buy', okcoin_lowest_sell_price, min_volume_triangular)
            time.sleep(4)
            trade_okcoin_id = trade_okcoin['order_id']
            okcoin_order_status = okconf.get_order(trade_okcoin_id, "ltc_cny")
            okcoin_order_status = okcoin_order_status['orders']

            partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        trade_huobi_id = trade_huobi['id']
        trade_huobi_status = asd2.get_order(1, trade_huobi_id, currency="btc")
        partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])

        while 0.2 < partial_amount2:
            asd2.cancel_order(1,trade_huobi_id, 'btc')
            time.sleep(1)
            huobidepth = huobi.get_depth("BTC", 10)
            d4 = huobidepth
            d4 = d4['top_sell'][1]['price']
            huobi_lowest_sell_price_btc = float(d4)
            print trade_huobi
            time.sleep(1)
            trade_huobi = asd2.buy(1,huobi_lowest_sell_price_btc, min_volume_triangular/ratio, currency="btc")
            trade_huobi_id = trade_huobi['id']
            time.sleep(5)
            trade_huobi_status = asd2.get_order(1, trade_huobi_id, currency="btc")
            trade_huobi_state = trade_huobi_status['status']
            partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])
            print("we have a partial in huobi, handling")


    if 0 < triangular2 and 2 < min_volume_triangular2:
        account_counter == 0
        print "trade"
        trade_okcoin = okconf.trade('ltc_cny', 'sell', okcoin_highest_buy_price, min_volume_triangular2)

        trade_huobi = asd2.sell(1,huobi_highest_buy_price_btc, min_volume_triangular2/ratio, currency="btc")
        print trade_huobi

        #Handle partials

        trade_okcoin_id = trade_okcoin['order_id']
        okcoin_order_status = okconf.get_order(trade_okcoin_id, "ltc_cny")
        okcoin_order_status = okcoin_order_status['orders']
        print okcoin_order_status
        partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        while 1 < partial_amount:
            okconf.cancel_order(trade_okcoin_id, "ltc_cny")
            time.sleep(1)
            okcoin_buy_list = dict.items(M.get_depth('ltc_cny').bids)
            highest_buy = max(okcoin_buy_list)
            okcoin_highest_buy_price = highest_buy[0]
            time.sleep(1)
            trade_okcoin = okconf.trade('ltc_cny', 'sell', okcoin_highest_buy_price, min_volume_triangular2)
            time.sleep(4)
            trade_okcoin_id = trade_okcoin['order_id']
            okcoin_order_status = okconf.get_order(trade_okcoin_id, "ltc_cny")
            okcoin_order_status = okcoin_order_status['orders']

            partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]


        trade_huobi_id = trade_huobi['id']
        trade_huobi_status = asd2.get_order(1, trade_huobi_id, currency="btc")
        partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])

        while 2 < partial_amount2:
            asd2.cancel_order(1, trade_huobi_id, currency="btc")
            time.sleep(2)
            huobidepth = huobi.get_depth("BTC", 10)
            a1 = huobidepth
            a1 = a1['top_buy'][1]['price']
            huobi_highest_buy_price_btc = float(a1)
            time.sleep(1)
            trade_huobi = asd2.sell(1,huobi_highest_buy_price_btc, min_volume_triangular2/ratio, currency="btc")
            print trade_huobi
            trade_huobi_id = trade_huobi['id']
            time.sleep(5)
            trade_huobi_status = asd2.get_order(1, trade_huobi_id, currency="btc")
            trade_huobi_state = trade_huobi_status['status']
            partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])
            print("we have a partial in huobi, handling")

        time.sleep(1)

        trade_okcoin = okconf.trade('btc_cny', 'buy', okcoin_lowest_sell_price_btc, min_volume_triangular2/ratio)

        trade_huobi = asd2.buy(2,huobi_lowest_sell_price, min_volume_triangular2, currency="ltc")
        print trade_huobi

        trade_okcoin_id = trade_okcoin['order_id']
        okcoin_order_status = okconf.get_order(trade_okcoin_id, "btc_cny")
        okcoin_order_status = okcoin_order_status['orders']

        partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        while 0.2 < partial_amount:
            okconf.cancel_order(trade_okcoin_id, "btc_cny")
            time.sleep(1)
            okcoin_sell_list = dict.items(M.get_depth('btc_cny').asks)

            lowest_sell = min(okcoin_sell_list)
            okcoin_lowest_sell_price_btc = lowest_sell[0]
            okcoin_lowest_sell_volume_btc = lowest_sell[1]
            time.sleep(1)
            trade_okcoin = okconf.trade('btc_cny', 'buy', okcoin_lowest_sell_price_btc, min_volume_triangular2/ratio)
            time.sleep(4)
            trade_okcoin_id = trade_okcoin['order_id']
            okcoin_order_status = okconf.get_order(trade_okcoin_id, "btc_cny")
            okcoin_order_status = okcoin_order_status['orders']

            partial_amount = okcoin_order_status[0]['amount'] - okcoin_order_status[0]["deal_amount"]

        trade_huobi_id = trade_huobi['id']
        trade_huobi_status = asd2.get_order(2, trade_huobi_id, currency="ltc")
        partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])

        while 0 < partial_amount2:
            asd2.cancel_order(2,trade_huobi_id, 'ltc')
            time.sleep(2)
            response = urllib2.urlopen('http://market.huobi.com/staticmarket/depth_ltc_json.js')
            data = json.load(response)
            huobidepth = data
            d4 = huobidepth
            d4 = d4["asks"][-2][0]
            huobi_lowest_sell_price = float(d4)
            time.sleep(1)
            trade_huobi = asd2.buy(2,huobi_lowest_sell_price, min_volume_triangular2, currency="ltc")
            trade_huobi_id = trade_huobi['id']
            time.sleep(5)
            trade_huobi_status = asd2.get_order(2, trade_huobi_id, currency="ltc")
            trade_huobi_state = trade_huobi_status['status']
            partial_amount2 = float(trade_huobi_status["order_amount"]) - float(trade_huobi_status["processed_amount"])
            print("we have a partial in huobi, handling")

        print min_volume_triangular
        print min_volume_triangular2


