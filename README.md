A buildpack for hosting an Electrum wallet, 
adapted from this older tutorial: http://www.genesisbloc.com/deploying-electrum-to-heroku/

Currently just starts the Electrum daemon and restores a basic wallet, given a seed, name, and encryption password in the envvars set by Heroku. This way your wallet can have everything up and running from scratch, and for what it's worth, the wallet is stored encrypted (but of course the password is sitting in an envvar).

Next, I may create a service that handles certain commands from, say, a web backend.

Use at your own risk. TBH I don't really know what I'm doing.
