A buildpack for hosting an Electrum wallet, 
adapted from this older tutorial: http://www.genesisbloc.com/deploying-electrum-to-heroku/

Features:
- Initializes the entire wallet from a seed at startup (thanks to Electrum), no remote servers required.
- Pays to an address.
- Creates wallet addresses.
- Checks wallet or address balance.

TODO:
- JSON-RPC for communicating with a web server on the same dyno, etc.

Use at your own risk. I somewhat know what I'm doing but am not by any means an expert.
