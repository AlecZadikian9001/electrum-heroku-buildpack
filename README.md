A buildpack for running an Electrum wallet in CLI mode, 
adapted from this older tutorial: http://www.genesisbloc.com/deploying-electrum-to-heroku/

Setup:
- Add a `requirements.txt` file to your app root containing the following (used by the Python buildpack):
    - `git+https://github.com/AlecZadikian9001/electrum.git@alecz/dumb_password#egg=electrum`
    - `json-rpc`
- Add the official Python 3 buildpack first: `heroku buildpacks:add --index 1 heroku/python`
- Add this buildpack second: `heroku buildpacks:add --index 2 git://github.com/AlecZadikian9001/electrum-heroku-buildpack`
- Try it out: `heroku run bash`, and run `electrum --help` inside the shell.


Features:
- Wallet:
    - Initializes the entire wallet from a seed at startup (thanks to Electrum) and starts the daemons, no remote servers required.
    - Pays to an address.
    - Creates wallet addresses.
    - Checks wallet or address balance.
- JSON-RPC server:
    - Listens for commands for the above wallet actions; can support multiple wallets.


Flaws/TODO:
- Slow! There's overhead in starting up the Electrum script for every command. 
    - But I'm not experienced enough to do things manually using their Python library.
- "Battle testing" on my own Heroku server.


Use at your own risk. I barely know what I'm doing.
