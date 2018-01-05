import pexpect
import os
import time
import util
import json


class Wallet:

    def __init__(self, name, password, seed, testnet=False):
        dirname = "wallets"
        util.ensure_dir(dirname)
        self.name = dirname + "/" + name
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
        return "{} -w {} {}".format(cmd, self.name, testnet_str)

    def _with_password(self, cmd):
        return "ELECTRUM_PASSWORD={}".format(self.password) + " " + cmd

    # should only be called once
    def create_and_start(self):
        delay_time = 3

        util.debug("Starting and restoring wallet {}".format(self))
        util.rm_file_if_exists(self.name)
        util.shell_expect("electrum daemon start")
        util.shell_blocking(self._with_password(self._args("electrum restore -o \"{}\"".format(self.seed))))
        util.shell_blocking(self._args("electrum daemon load_wallet"))
        util.debug("Started and restored wallet {}".format(self))

    def get_balance(self):
        output = util.shell_blocking(self._args("electrum getbalance"))
        j = json.loads(output)
        return j

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
    name = os.environ["WALLET_NAME"]
    password = os.environ["WALLET_PASSWORD"]
    seed = os.environ["WALLET_SEED"]
    testnet = util.env_bool_override(False, "WALLET_TESTNET")
    wallet = Wallet(name, password, seed, testnet=testnet)
    wallet.create_and_start()
    return wallet


if __name__ == "__main__":
    wallet = load_default_wallet()

