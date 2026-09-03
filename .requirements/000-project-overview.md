# 000 — MIDAS Portfolio Tracking Overview

## Purpose

MIDAS is a personal capital-management and portfolio-analysis system that consolidates investments held across multiple institutions and account types into a coherent internal model while preserving where each position is actually held.

The system should make it easy to answer not only "what do I own now?" but also how the portfolio has changed over time, how exposure is distributed across sectors, geographies, asset classes, strategies, and user-defined themes, and how actual investment decisions compare with plausible alternatives.

This requirement extends the existing MIDAS concept rather than replacing it. The flexible tagging model described in the existing project README remains a central design principle.

## Initial institution coverage

The first useful version should support portfolio data from:

- Wealthsimple
- Scotia / ScotiaMcLeod

The architecture should allow additional institutions to be added later, including Interactive Brokers, without changing the core portfolio model.

Institution-specific ingestion logic must remain separate from the normalized internal representation.

## Accounts

MIDAS should represent multiple accounts independently while also supporting consolidated portfolio views.

Examples include:

- TFSA
- RRSP
- LRSP / LIRA-style locked-in retirement accounts
- FHSA
- non-registered / cash / margin accounts
- institution-specific account types

Each account should retain its institution, account type, base currency where known, and other useful metadata.

## Holdings and instruments

The system should distinguish between an instrument and a holding.

An instrument represents the security or asset itself. A holding represents ownership of that instrument in a particular account at a particular point in time.

MIDAS should normalize securities across institutions so that the same instrument is recognized consistently even when broker exports use different names or identifiers.

Useful identifiers may include ticker, exchange, ISIN, CUSIP, broker symbol, or other provider-specific identifiers where available.

## Flexible classification and tagging

MIDAS should retain its existing flexible tagging approach rather than relying exclusively on a rigid classification hierarchy.

An instrument may simultaneously carry tags representing concepts such as:

- sector:energy
- sector:healthcare
- sector:industrials
- geography:canada
- geography:united-states
- strategy:dividend
- strategy:growth
- theme:inflation-hedge
- asset-class:equity
- asset-class:fixed-income

The application may also support standard classifications, but user-defined tags should remain first-class and should be usable for aggregation and analysis.

## Data ingestion

A primary product requirement is to make portfolio updates easy to ingest.

The first version should favor pragmatic ingestion methods rather than requiring direct brokerage integrations.

Potential ingestion mechanisms include:

- CSV imports
- spreadsheet imports
- copy/paste from brokerage tables
- simple manual position entry and correction
- institution-specific import adapters

Direct APIs may be introduced later where available and worthwhile.

Every import should preserve enough provenance to determine where the data came from and when it was captured.

The import process should allow preview, validation, normalization, and correction before changes are incorporated into the historical portfolio record.

## Historical portfolio state

MIDAS should preserve portfolio history instead of merely overwriting today's positions.

The system should support dated portfolio snapshots that represent what was held at a particular point in time.

Historical data should make it possible to examine changes such as:

- portfolio value through time
- security quantities through time
- account balances through time
- institution allocation through time
- sector exposure through time
- geographic exposure through time
- asset-class exposure through time
- tag/theme exposure through time

Historical snapshots should be treated as immutable observations. Corrections should be explicit rather than silently rewriting prior history.

## Transactions

Where transaction data can be obtained, MIDAS should support transactions such as:

- buys
- sells
- dividends
- distributions
- deposits
- withdrawals
- transfers
- fees
- currency conversions
- splits and other corporate actions

Transaction history and portfolio snapshots are complementary. The system should not require complete transaction history before portfolio tracking is useful.

## Valuation

MIDAS should be able to calculate portfolio value at the instrument, account, institution, and consolidated portfolio levels.

The system should distinguish clearly among:

- quantity
- market price
- market value
- currency
- converted value in a selected reporting currency

Historical valuation should eventually support historical market prices and historical FX rates so that past portfolio states can be reconstructed meaningfully.

Market-data providers should be abstracted behind a service boundary so the system is not permanently coupled to one vendor.

## Exposure analysis

The application should support aggregation and visualization across dimensions including:

- institution
- account
- account type
- instrument
- sector
- geography
- asset class
- currency
- arbitrary tags and themes

The same portfolio should be viewable at multiple levels without duplicating underlying holdings data.

## Actual versus hypothetical scenarios

MIDAS should support counterfactual analysis: comparing what actually happened with what might have happened under a different investment decision.

Examples include:

- What would the portfolio be worth if I had not sold a position?
- What if I had sold only half of it?
- What if I had moved the proceeds into a particular ETF?
- What if I had rebalanced at an earlier date?
- How has the actual portfolio performed relative to simply holding an earlier portfolio unchanged?

These scenarios should be modeled as explicit hypothetical timelines or scenario overlays.

A critical rule is that scenarios must never mutate or overwrite the historical record of what actually happened.

A scenario should identify:

- the historical starting point
- one or more hypothetical changes
- assumptions used
- resulting simulated holdings through time
- comparison metrics against actual history

The scenario engine should eventually support A/B-style comparisons between two or more portfolio histories.

## Performance analysis

MIDAS should eventually support performance views such as:

- absolute gains and losses
- percentage return
- contribution by security
- contribution by sector or tag
- realized versus unrealized gains where sufficient data exists
- comparison of actual versus hypothetical scenarios

Care must be taken to distinguish market performance from cash flows into or out of the portfolio.

Sophisticated performance metrics can be added incrementally rather than being required for the first usable version.

## Data integrity principles

MIDAS should behave as a personal financial system of record.

Important principles include:

1. Imported source data should retain provenance.
2. Historical portfolio states should not be silently overwritten.
3. Broker-specific representations should be normalized behind a common model.
4. Hypothetical scenarios must remain distinct from actual history.
5. Derived analytics should be reproducible from underlying holdings, transactions, market data, and assumptions.
6. Manual corrections should be possible and auditable.

## Initial scope

The first implementation does not need to connect directly to brokerage APIs, execute trades, produce tax filings, or provide investment advice.

A useful first milestone is:

1. represent institutions and accounts;
2. import holdings from at least one Wealthsimple export and one Scotia export or manually structured equivalent;
3. normalize instruments;
4. preserve dated snapshots;
5. show consolidated holdings and allocations by account, institution, sector, geography, and tags;
6. compare two historical snapshots;
7. support one simple counterfactual scenario such as "what if I had continued holding this security?"

## Long-term direction

MIDAS may eventually evolve from portfolio tracking into a broader personal investment intelligence system with automated ingestion, market-data enrichment, portfolio diagnostics, scenario modeling, decision journaling, and AI-assisted analysis.

The historical record and normalized portfolio model should remain the foundation for those capabilities.