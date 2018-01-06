# JSON-RPC server imports
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import wallet as btc_wallet


class WalletServer:

    def __init__(self):
        self.wallets = {} # name: wallet

    def add_wallet(self, wallet):
        assert type(wallet) == btc_wallet.Wallet
        name = wallet.name
        assert name not in self.wallets
        self.wallets[name] = wallet

    def get_wallet(self, name):
        return self.wallets[name]

    def create_address(self, w):
        return self.get_wallet(w).create_address()

    def get_address_balance(self, w, addr):
        return self.get_wallet(w).get_address_balance(addr)

    def get_balance(self, w):
        return self.get_wallet(w).get_balance()

    def pay(self, w, addr, btc, fee):
        return self.get_wallet(w).pay(addr, btc, fee=fee)


wallet_server = WalletServer()

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["create_address"] = lambda w: wallet_server.create_address(w)
    dispatcher["get_address_balance"] = lambda w, addr: wallet_server.get_address_balance(w, addr)
    dispatcher["get_balance"] = lambda w: wallet_server.get_balance(w)
    dispatcher["pay"] = lambda w, addr, btc, fee: wallet_server.pay(w, addr, btc, fee)

    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    # load the default wallet
    default_wallet = btc_wallet.load_default_wallet()
    wallet_server.add_wallet(default_wallet)

    # parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port number for server")
    args = parser.parse_args()
    if not args.port:
        port = 9001
    else:
        port = args.port
    run_simple('localhost', port, application)
