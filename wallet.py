import os
import time
import util
import json


class Wallet:

    def __init__(self, name, password, seed, testnet=False):
        dirname = "wallets"
        util.ensure_dir(dirname)
        self.name = name
        self.fname = dirname + "/" + name
        self.password = password
        self.seed = seed
        self.testnet = testnet

    def __str__(self):
        return "<Wallet name={}, testnet={}>".format(self.name, self.testnet)

    def __repr__(self):
        return str(self)

    def _args(self, cmd):
        if self.testnet:
            testnet_str = "--testnet"
        else:
            testnet_str = ""
        return "{} -w {} {}".format(cmd, self.fname, testnet_str)

    def _with_password(self, cmd):
        return "ELECTRUM_PASSWORD={}".format(self.password) + " " + cmd

    # should only be called once
    def create_and_start(self):
        util.debug("Starting and restoring wallet {}".format(self))
        util.rm_file_if_exists(self.fname)

        # start daemon # TODO messy; assumes it takes 5 seconds; for some reason shell_blocking won't work
        util.shell_expect("electrum daemon start")
        util.sleep(5)
        util.shell_expect(self._args("electrum daemon start"))
        util.sleep(5)

        util.shell_blocking(self._with_password(self._args("electrum restore -o \"{}\"".format(self.seed))))
        util.shell_blocking(self._args("electrum daemon load_wallet"))
        util.debug("Started and restored wallet {}".format(self))

    def create_address(self):
        output = util.shell_blocking(self._args("electrum createnewaddress"))
        return output.strip()

    def get_address_balance(self, address):
        output = util.shell_blocking(self._args("electrum getaddressbalance {}".format(address)))
        j = json.loads(output)
        return float(j["confirmed"])

    def get_balance(self):
        output = util.shell_blocking(self._args("electrum getbalance"))
        j = json.loads(output)
        return float(j["confirmed"])

    def pay(self, address, btc, fee=None):
        util.debug("Paying {} BTC to {}, fee={}".format(btc, address, fee))
        if fee == None:
            fee_str = ""
        else:
            assert fee > 0
            if fee >= btc:
                raise Exception("fee {} > btc {}".format(fee, btc))
            fee_str = "-f {}".format(fee)

        cmd = self._args("electrum payto {} {} {}".format(address, btc, fee_str)) \
                + " | " \
                + self._args("electrum broadcast") + " -"
        util.shell_blocking(self._with_password(cmd))
        util.debug("Done paying")


def load_default_wallet():
    try:
        name = os.environ["WALLET_NAME"]
        password = os.environ["WALLET_PASSWORD"]
        seed = os.environ["WALLET_SEED"]
    except KeyError:
        raise Exception("Must set WALLET_NAME, WALLET_PASSWORD, and WALLET_SEED envvars")
    testnet = util.env_bool_override(False, "WALLET_TESTNET")
    wallet = Wallet(name, password, seed, testnet=testnet)
    wallet.create_and_start()
    return wallet


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--createdefault", help="Creates a wallet and initializes its daemon and files based on the environmental variables.", action="store_true")
    args = parser.parse_args()
    if args.createdefault:
        wallet = load_default_wallet()
        
    

