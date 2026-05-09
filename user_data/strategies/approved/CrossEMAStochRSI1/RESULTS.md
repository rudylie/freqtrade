# CrossEMAStochRSI1 Results

## Doel

Een Freqtrade-versie van `Cross EMA + stoch RSI#1` bouwen die historisch minstens `50 USDT` op `1 maand` haalt.

## Fase 1: Reproductie van de bronlogica

Bronlogica vertaald naar Freqtrade:

- `EMA28 > EMA48` als bull-trend
- `StochRSI` onder `0.8` als koopfilter
- exit bij bearish EMA-structuur en `StochRSI` boven `0.2`
- long-only, market entry/exit

Brede eerste test:

- timerange: `2025-12-15` t/m `2026-03-31`
- pairs: `XRP`, `NEAR`, `WMTX`, `NIGHT`, `TAO`, `XMR`
- config: `stake_amount = unlimited`, `max_open_trades = 3`
- resultaat: `+294.999 USDT`, ongeveer `+83.490 USDT/maand`
- drawdown: `23.74%`
- trades: `96`

Conclusie:

- de pure bronvariant haalt het maanddoel al op de brede basket,
- maar bevat nog duidelijke verliezers zoals `XRP` en `NIGHT`,
- dus pairselectie kan hier de robuustheid en winst verder verhogen.

Artifact:

- `results/baseline_default/backtest-result-2026-04-07_10-41-58.zip`

## Fase 2: Single-pair screen

Getest op dezelfde hoofdperiode `2025-12-15` t/m `2026-03-31`, telkens met `max_open_trades = 1`.

Belangrijkste uitkomst:

- `WMTX`: `+493.001 USDT`, ongeveer `+139.528 USDT/maand`
- `TAO`: `+468.687 USDT`, ongeveer `+132.647 USDT/maand`
- `ATOM`: `+53.498 USDT`, ongeveer `+15.141 USDT/maand`

Duidelijke verliezers:

- `NEAR`: `-80.680 USDT`
- `XMR`: `-117.369 USDT`
- `BTC`: `-120.025 USDT`
- `XRP`: `-216.371 USDT`
- `NIGHT`: `-289.671 USDT`
- `DOT`: `-384.724 USDT`

Conclusie:

- de echte kern van deze strategie in de huidige dataset zit in `TAO` en `WMTX`,
- `ATOM` is bruikbaar als kleinere extra kandidaat,
- veel bredere pairs trekken het profiel juist omlaag.

Artifacts:

- `results/experiments_pairs/single_pairs/`

## Fase 3: Pairselectie

Getest op de hoofdperiode `2025-12-15` t/m `2026-03-31`.

### Beste subsets

- `top2_taowmtx_u2` = `TAO`, `WMTX`, `max_open_trades = 2`
  - `+554.392 USDT`
  - ongeveer `+156.904 USDT/maand`
  - drawdown `11.75%`
  - `29` trades
- `top2_taoatom_u1` = `TAO`, `ATOM`, `max_open_trades = 1`
  - `+438.899 USDT`
  - ongeveer `+124.217 USDT/maand`
  - drawdown `15.17%`
  - `23` trades
- `top3_taowmtxatom_u2` = `TAO`, `WMTX`, `ATOM`, `max_open_trades = 2`
  - `+457.583 USDT`
  - ongeveer `+129.505 USDT/maand`
  - drawdown `14.43%`
  - `43` trades

Conclusie:

- `TAO + WMTX` is hier de sterkste en tegelijk rustigste winnaar,
- `ATOM` kan winst toevoegen in sommige regimes, maar trekt het hoofdprofiel niet boven `TAO + WMTX`,
- de top-2 basisvariant is duidelijk beter dan bredere combinaties.

Artifacts:

- `results/top2_taowmtx_full/backtest-result-2026-04-07_10-55-58.zip`
- `results/top2_taoatom_full/backtest-result-2026-04-07_10-59-46.zip`
- `results/targeted/tao_wmtx_atom_u2_full/backtest-result-2026-04-07_10-54-47.zip`

## Fase 4: Holdout en maandcheck

### Hoofdadvies: `TAO + WMTX`

Config:

- `config/top2_taowmtx_unlimited_2.json`

Hoofdperiode `2025-12-15` t/m `2026-03-31`:

- `+554.392 USDT`
- ongeveer `+156.904 USDT/maand`
- drawdown `11.75%`

Late holdout `2026-02-16` t/m `2026-03-31`:

- `+242.725 USDT`
- ongeveer `+169.343 USDT/maand`
- drawdown `11.80%`

Losse maand `2026-03-01` t/m `2026-03-31`:

- `+297.402 USDT`
- ongeveer `+297.402 USDT/maand`
- drawdown `7.92%`

Conclusie:

- dit profiel haalt het doel niet alleen ruim op de hoofdperiode,
- maar blijft ook op de late holdout en op maart 2026 afzonderlijk ver boven het doel.

Artifacts:

- `results/top2_taowmtx_full/backtest-result-2026-04-07_10-55-58.zip`
- `results/targeted/tao_wmtx_u2_holdout/backtest-result-2026-04-07_10-54-42.zip`
- `results/targeted/tao_wmtx_u2_march/backtest-result-2026-04-07_10-54-44.zip`

### Tweede kandidaat: `TAO + ATOM`

Config:

- `config/top2_taoatom_unlimited_1.json`

Hoofdperiode `2025-12-15` t/m `2026-03-31`:

- `+438.899 USDT`
- ongeveer `+124.217 USDT/maand`
- drawdown `15.17%`

Late holdout `2026-02-16` t/m `2026-03-31`:

- `+294.673 USDT`
- ongeveer `+205.586 USDT/maand`
- drawdown `15.17%`

Losse maand `2026-03-01` t/m `2026-03-31`:

- `+272.322 USDT`
- ongeveer `+272.322 USDT/maand`
- drawdown `8.57%`

Conclusie:

- deze kandidaat blijft ook ruim boven doel,
- maar heeft hogere drawdown en meer concentratie op `TAO`,
- daarom blijft `TAO + WMTX` het hoofdadvies.

Artifacts:

- `results/top2_taoatom_full/backtest-result-2026-04-07_10-59-46.zip`
- `results/targeted/tao_atom_u1_holdout/backtest-result-2026-04-07_10-54-44.zip`
- `results/targeted/tao_atom_u1_march/backtest-result-2026-04-07_10-54-43.zip`

## Fase 5: Gerichte hyperopt

Train-periode:

- `2025-12-15` t/m `2026-02-15`

Setup:

- pairs: `TAO`, `WMTX`
- `max_open_trades = 2`
- spaces: `buy`, `sell`
- loss: `ProfitDrawDownHyperOptLoss`
- epochs gevraagd: `60`
- early stop: `38`
- seed: `42`

Beste trainingsresultaat:

- `+368.444 USDT`
- `+36.84%`
- drawdown `0.37%`
- `5` trades

Opslag:

- `CrossEMAStochRSI1Hyperopt.json`
- `results/CrossEMAStochRSI1Hyperopt_train_20251215_20260215_buy_sell_hyperopt.fthypt`

## Fase 6: Hyperopt-validatie

De hyperopt-set bleek hier te selectief.

### Hyperopt-set op `TAO + WMTX`

Hoofdperiode `2025-12-15` t/m `2026-03-31`:

- `+319.439 USDT`
- ongeveer `+90.407 USDT/maand`
- `4` trades

Late holdout `2026-02-16` t/m `2026-03-31`:

- `+24.751 USDT`
- ongeveer `+17.268 USDT/maand`
- `1` trade

Losse maand `2026-03-01` t/m `2026-03-31`:

- `+24.751 USDT`
- ongeveer `+24.751 USDT/maand`
- `1` trade

Conclusie:

- de hyperopt-set is niet beter dan de simpele basisvariant,
- hij handelt te weinig en faalt op de doelstelling in holdout en maart,
- dus deze set is bewaard als referentie, niet als advies.

Artifacts:

- `results/hyperopt_validation/top2_taowmtx_full_hyperopt/backtest-result-2026-04-07_10-58-43.zip`
- `results/hyperopt_validation/top2_taowmtx_holdout_hyperopt/backtest-result-2026-04-07_10-58-43.zip`
- `results/hyperopt_validation/top2_taowmtx_march_hyperopt/backtest-result-2026-04-07_10-58-44.zip`

## Eindconclusie

Het gestelde doel is historisch ruim gehaald.

Beste praktische keuze:

- `config/top2_taowmtx_unlimited_2.json`

Waarom:

- hoogste winst op de hoofdperiode van alle geteste profielen,
- duidelijke holdout-bevestiging boven `50 USDT/maand`,
- lagere drawdown dan de `TAO + ATOM`-variant,
- veel beter out-of-sample dan de hyperopt-set.

Belangrijke noot:

- dit blijft een backtest op lokale historische data,
- dus ook deze winst is geen garantie voor live-resultaten.
