CREATE TABLE IF NOT EXISTS currency_symbols ( symbol TEXT PRIMARY KEY UNIQUE NOT NULL );

CREATE TABLE IF NOT EXISTS crypto_currency_symbols ( symbol TEXT PRIMARY KEY UNIQUE NOT NULL );

INSERT OR IGNORE INTO currency_symbols (symbol) VALUES ( 'GBP' ),
                                                       ( 'USD' ),
                                                       ( 'EUR' ),
                                                       ( 'JPY' ),
                                                       ( 'CNY' ),
                                                       ( 'INR' ),
                                                       ( 'CAD' ),
                                                       ( 'AUD' ),
                                                       ( 'SEK' );

INSERT OR IGNORE INTO crypto_currency_symbols (symbol) VALUES ( 'BTC' ),
                                                              ( 'ETH' ),
                                                              ( 'LTC' );

DROP TABLE IF EXISTS time_series_daily_adjusted;
CREATE TABLE IF NOT EXISTS time_series_daily_adjusted ( hash INTEGER PRIMARY KEY UNIQUE NOT NULL,
                                                        symbol TEXT NOT NULL,
                                                        timestamp FLOAT NOT NULL,
                                                        year INTEGER NOT NULL,
                                                        month INTEGER NOT NULL,
                                                        day INTEGER NOT NULL,
                                                        open FLOAT NOT NULL,
                                                        high FLOAT NOT NULL,
                                                        low float NOT NULL,
                                                        close FLOAT NOT NULL,
                                                        adj_close FLOAT,
                                                        volume FLOAT,
                                                        dividend FLOAT,
                                                        currency TEXT,
                                                        split FLOAT );

DROP TABLE IF EXISTS currency_intraday;
CREATE TABLE IF NOT EXISTS currency_intraday ( from_symbol TEXT NOT NULL,
                                               to_symbol TEXT NOT NULL,
                                               timestamp FLOAT NOT NULL,
                                               open FLOAT NOT NULL,
                                               high FLOAT NOT NULL,
                                               low FLOAT NOT NULL,
                                               close FLOAT NOT NULL,
                                               PRIMARY KEY (from_symbol,
                                                            to_symbol,
                                                            timestamp));

DROP TABLE IF EXISTS currency_daily;
CREATE TABLE IF NOT EXISTS currency_daily ( from_symbol TEXT NOT NULL,
                                            to_symbol TEXT NOT NULL,
                                            timestamp FLOAT NOT NULL,
                                            open FLOAT NOT NULL,
                                            high FLOAT NOT NULL,
                                            low FLOAT NOT NULL,
                                            close FLOAT NOT NULL,
                                            PRIMARY KEY (from_symbol,
                                                         to_symbol,
                                                         timestamp));

-- DROP TABLE IF EXISTS dollar_index;
CREATE TABLE IF NOT EXISTS dollar_index ( timestamp FLOAT PRIMARY KEY NOT NULL,
                                          open FLOAT NOT NULL,
                                          high FLOAT NOT NULL,
                                          low FLOAT NOT NULL,
                                          close FLOAT NOT NULL,
                                          volume FLOAT NOT NULL);
