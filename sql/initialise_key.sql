CREATE TABLE IF NOT EXISTS api_key_store ( key TEXT PRIMARY KEY UNIQUE NOT NULL,
                                           last_accessed FLOAT,
                                           used INTEGER );
