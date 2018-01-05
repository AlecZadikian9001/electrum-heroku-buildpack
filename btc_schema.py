import util


class BtcSchema:

    def __init__(db):
        self.db = db

    def create(self):
        self.db.execute("""
        CREATE SCHEMA IF NOT EXISTS btc;
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS btc.wallet (
            id bigserial PRIMARY KEY,
            name text UNIQUE
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS btc.wallet_address (
            id bigserial UNIQUE NOT NULL,
            wallet bigint REFERENCES btc.wallet(id) ON DELETE CASCADE,
            address text,
            PRIMARY KEY (wallet_id, address)
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS btc.wallet_deposit (
            id bigserial UNIQUE NOT NULL,
            rx_address bigint REFERENCES btc.wallet_address(id) ON DELETE CASCADE,
            tx_hash text,
            satoshi bigint
        )
        """)

    def destroy(self):
        self.db.execute("""
        DROP SCHEMA btc CASCADE;
        """)


    
