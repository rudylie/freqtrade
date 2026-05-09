# Testplan

## Bronstrategie omgezet

- originele GitHub-map gelezen:
  - `https://github.com/CryptoRobotFr/TrueStrategy/tree/main/Cross%20EMA%20%2B%20stoch%20RSI%231`
- bronlogica vertaald naar Freqtrade:
  - `EMA28 > EMA48`
  - `StochRSI` koop- en verkoopsignalen
  - long-only exit op bear-structuur

## Uitgevoerde controles

### Strategievalidatie

- `python -m py_compile user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/CrossEMAStochRSI1.py`
- `python -m py_compile user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/CrossEMAStochRSI1Hyperopt.py`
- `python -m freqtrade list-strategies --strategy-path user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1`

### Brede baseline

- `python -m freqtrade backtesting --config .../config/no_dot_sol_unlimited_3.json --strategy CrossEMAStochRSI1 --timerange 20251215-20260331`

### Single-pair screen

Getest op:

- `AAVE`
- `ATOM`
- `BTC`
- `DOT`
- `ETH`
- `NEAR`
- `NIGHT`
- `SOL`
- `TAO`
- `WMTX`
- `XMR`
- `XRP`

Artifacts staan onder:

- `results/experiments_pairs/single_pairs/`

### Pairselectie

Getest op meerdere subsets, waaronder:

- `TAO + WMTX`
- `TAO + ATOM`
- `TAO + WMTX + ATOM`

Artifacts staan onder:

- `results/top2_taowmtx_full/`
- `results/top2_taoatom_full/`
- `results/targeted/`

### Holdout-check

Getest op:

- `2026-02-16` t/m `2026-03-31`
- `2026-03-01` t/m `2026-03-31`

Voor:

- `TAO + WMTX`
- `TAO + ATOM`

### Hyperopt

- `python -m freqtrade hyperopt --config .../config/no_dot_sol_unlimited_3.json --strategy CrossEMAStochRSI1Hyperopt --timerange 20251215-20260215 --max-open-trades 2 -p TAO/USDT WMTX/USDT --spaces buy sell -e 60 -j 2 --hyperopt-loss ProfitDrawDownHyperOptLoss --early-stop 30 --random-state 42`

### Hyperopt-validatie

- `CrossEMAStochRSI1Hyperopt` getest op:
  - `20251215-20260331`
  - `20260216-20260331`
  - `20260301-20260331`

## Verwachte keuze

- standaardprofiel: `config/top2_taowmtx_unlimited_2.json`
- secundaire kandidaat: `config/top2_taoatom_unlimited_1.json`
- hyperopt-profiel: alleen bewaard als referentie, niet als voorkeursset
