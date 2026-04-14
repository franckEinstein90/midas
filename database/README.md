# midas_db scaffold

This project uses `uv` to run a Python script that creates an SQLite database file named `midas.db` in this folder.

The initializer also creates portfolio tracking tables for:
- Institutions (banks/brokers)
- Accounts
- Exchanges
- Instruments (`STOCK`, `BOND`, `GIC`, `ETF`) with an optional exchange
- Facets plus instrument-to-facet associations
- Holdings snapshots by date

Seeded institutions and accounts:
- Wealthsimple: `FHSA`, `TFSA`, `Cash`
- Scotiabank: `LRSP`, `Cash`, `RRSP`, `TFSA`

Seeded facets:
- `materials`
- `gold`
- `silver`
- `defense`
- `china`
- `semidconductors`
- `big tech`

## Run

Initialize the database:

```bash
uv run scripts/create_database.py
```

Load the current Scotiabank Cash holdings snapshot:

```bash
uv run scripts/populate_scotiabank_cash_holdings.py
```

Start the Streamlit app (multi-page):

```bash
uv run streamlit run main.py
```

The app includes:
- **Dashboard**: Overview of holdings, accounts, and valuations across institutions.
- **Tags**: Tag individual instruments with facets, manage available facets, and create new ones.
- **Ingest**: Upload CSV or Excel files to add or update holdings data for an account.

The sidebar navigation will appear automatically and allow navigation between pages.
