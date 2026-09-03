# Portfolio API routes

The portfolio endpoints are defined in the dedicated router at `app/api/portfolio.py` and are mounted under the `/api/portfolio` prefix.

## Endpoints

### GET /api/portfolio/summary
Returns a consolidated portfolio summary using the configured reporting currency.

Response shape:
- `portfolio_total`
- `holding_count`
- `account_count`
- `currency`
- `as_of_date`

### GET /api/portfolio/holdings
Returns all holdings in the portfolio.

Response shape:
- list of holdings with account, instrument, quantity, market price, market value, and as-of date metadata

### GET /api/portfolio/exposure
Returns portfolio sector exposure.

Response shape:
- sector totals and percentages for the portfolio

### GET /api/portfolio/exposure/sector
Returns the same sector-based exposure breakdown as the dedicated sector exposure endpoint.

### GET /api/portfolio/exposure/currency
Returns portfolio exposure aggregated by instrument currency.

Response shape:
- currency totals and percentages relative to portfolio value

### GET /api/portfolio/value-history
Returns historical portfolio value snapshots over time.

Response shape:
- list of dated portfolio value summaries

## Notes

- These routes depend on the application's database session via `get_db`.
- The reporting currency is pulled from the application settings.
- The router is included in the main FastAPI app via `app.include_router(portfolio_router)`.
