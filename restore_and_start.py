import pexpect
import os
import time

print("start script")

seed = os.environ["WALLET_SEED"]
password = os.environ["WALLET_PASSWORD"]
name = os.environ["WALLET_NAME"]

print("starting daemon...")
pexpect.spawn("electrum daemon start", timeout=30)
time.sleep(1)
print("daemon started")

print("restoring wallet...")
restore_cmd = pexpect.spawn("electrum restore -w \"{}\" -o \"{}\"".format(name, seed))
restore_cmd.expect(["Password"])
restore_cmd.sendline(password)
restore_cmd.sendline(password)
print("wallet restored")

print("loading wallet...")
time.sleep(1)
pexpect.spawn("electrum daemon load_wallet -w \"{}\"".format(name))
print("wallet loaded")

print("done")
