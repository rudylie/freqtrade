# Bot Instances

Bot folders represent runnable instances: strategy code plus config, private config, database, logs, and runtime files.

- `live/`: real-money bot instances.
- `dry-run/`: paper-trading bot instances.
- `archived/`: inactive bot databases or old bot instance snapshots.

Naming convention:

- Config: `<StrategyName>.<environment>.json`
- Private config: `<StrategyName>.<environment>.private.json`
- Database: `tradesv3.<StrategyName>.<environment>.sqlite`
- Log: `<StrategyName>.<environment>.log`
