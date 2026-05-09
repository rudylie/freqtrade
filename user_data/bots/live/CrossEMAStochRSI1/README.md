# CrossEMAStochRSI1 Live Bot

Live bot instance for `CrossEMAStochRSI1` on KuCoin spot.

## Files

- `config/CrossEMAStochRSI1.live.json`: non-secret live config.
- `config/CrossEMAStochRSI1.live.private.json`: local-only secrets and private runtime settings.
- `data/tradesv3.CrossEMAStochRSI1.live.sqlite`: live trade database.
- `logs/CrossEMAStochRSI1.live.log`: live log file.
- `docker-compose.yml`: container definition for this bot instance.

## Current Pair Mode

This bot currently uses `VolumePairList` with the top 10 assets by quote volume. Earlier research identified `TAO/WMTX` as the strongest historical static pair set, but coin names are intentionally kept out of live file names.

## Commands

Start:

```bash
./run_live.sh
```

Stop:

```bash
docker compose down
```

Logs:

```bash
docker compose logs -f
```
