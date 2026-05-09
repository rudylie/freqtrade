# CrossEMAStochRSI1

Deze map bevat een Freqtrade-vertaling van de originele strategie uit:

- `https://github.com/CryptoRobotFr/TrueStrategy/tree/main/Cross%20EMA%20%2B%20stoch%20RSI%231`

De kern van de bronstrategie is behouden:

- bullish trend wanneer `EMA28 > EMA48`,
- long entries zolang `StochRSI` onder de koopdrempel blijft,
- bear-exit wanneer de trend draait en `StochRSI` boven de verkoopdrempel komt.

## Bestanden

- `CrossEMAStochRSI1.py`: basisimplementatie van de bronlogica, plus optionele `ADX`, `ATR` en trendfilters om gericht te kunnen testen.
- `CrossEMAStochRSI1Hyperopt.py`: aparte alias voor een gehyperopte variant.
- `CrossEMAStochRSI1Hyperopt.json`: opgeslagen hyperopt-parameters. Deze variant is bewaard voor referentie, maar niet het hoofdadvies.

## Aanbevolen configs

- `config/top2_taowmtx_unlimited_2.json`
  - hoofdadvies
  - pairs: `TAO/USDT`, `WMTX/USDT`
  - `stake_amount = unlimited`
  - `max_open_trades = 2`
- `config/top2_taoatom_unlimited_1.json`
  - tweede kandidaat
  - pairs: `TAO/USDT`, `ATOM/USDT`
  - `stake_amount = unlimited`
  - `max_open_trades = 1`
- `config/top2_taowmtx_hyperopt_unlimited_2.json`
  - gehyperopte testvariant
  - niet aanbevolen als standaardprofiel

## Gebruik

Backtest hoofdprofiel:

```bash
python -m freqtrade backtesting \
  --config user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/config/top2_taowmtx_unlimited_2.json \
  --strategy CrossEMAStochRSI1 \
  --strategy-path user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1 \
  --timerange 20251215-20260331 \
  --backtest-directory user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/results/manual_top2
```

Backtest tweede kandidaat:

```bash
python -m freqtrade backtesting \
  --config user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/config/top2_taoatom_unlimited_1.json \
  --strategy CrossEMAStochRSI1 \
  --strategy-path user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1 \
  --timerange 20251215-20260331 \
  --backtest-directory user_data/archived-strategies/TrueStrategy/CrossEMAStochRSI1/results/manual_top2_alt
```

## Belangrijke noot

Het maanddoel is historisch ruim gehaald op de lokale KuCoin-data in deze workspace. De basisvariant `TAO + WMTX` blijft ook op de late holdout en op maart 2026 afzonderlijk ruim boven `50 USDT/maand`. De hyperopt-set haalt dat juist niet out-of-sample en blijft daarom alleen als referentie bewaard. Zie `RESULTS.md` voor de details.
