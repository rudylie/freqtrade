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

## Actieve bot-config

De live bot-instantie staat niet in deze strategy-map, maar onder:

- `user_data/bots/live/CrossEMAStochRSI1/`

Daarbij horen:

- `config/CrossEMAStochRSI1.live.json`: publieke live-config zonder secrets.
- `config/CrossEMAStochRSI1.live.private.json`: lokale private config met API/Telegram secrets.
- `data/tradesv3.CrossEMAStochRSI1.live.sqlite`: live trade database.
- `docker-compose.yml`: containerdefinitie voor de live bot.

De huidige live-config gebruikt `VolumePairList` met de top 10 assets op KuCoin. Bestandsnamen bevatten bewust geen cryptomuntnamen meer.

## Historische onderzoeksconfigs

De oude `top2_*` configs waren onderzoeksartefacten uit de vorige mapstructuur. Ze zijn niet meer de actieve live-config. De historische conclusie blijft wel relevant:

- hoofdadvies uit backtest: `TAO/USDT` + `WMTX/USDT`, `max_open_trades = 2`
- tweede kandidaat uit backtest: `TAO/USDT` + `ATOM/USDT`, `max_open_trades = 1`
- hyperopt-variant: bewaard als referentie, niet aanbevolen als standaardprofiel

## Gebruik

Live bot starten via de botmap:

```bash
cd user_data/bots/live/CrossEMAStochRSI1
./run_live.sh
```

Strategie laden vanuit de nieuwe approved-map:

```bash
python -m freqtrade list-strategies \
  --strategy-path user_data/strategies/approved/CrossEMAStochRSI1
```

## Belangrijke noot

Het maanddoel is historisch ruim gehaald op de lokale KuCoin-data in deze workspace. De basisvariant `TAO + WMTX` blijft ook op de late holdout en op maart 2026 afzonderlijk ruim boven `50 USDT/maand`. De hyperopt-set haalt dat juist niet out-of-sample en blijft daarom alleen als referentie bewaard. Zie `RESULTS.md` voor de details.
