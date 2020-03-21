import websocket
import json


def on_open(ws):
    print("openned connection")

    subscribe_message = {
        "type": "subscribe",
        "product_ids": [
            "BTC-USD"
        ],
        "channels": [
            "level2",
            "heartbeat",
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    }

    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    print("recieved message")
    print(json.loads(message))


def on_error(ws, error):
    print(error)


socket = "wss://ws-feed.pro.coinbase.com"

print("Start scoket")
ws = websocket.WebSocketApp(socket, on_open=on_open,
                            on_message=on_message, on_error=on_error)
ws.run_forever()
