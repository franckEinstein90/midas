from app.main import app


def test_portfolio_routes_are_registered_under_api_prefix() -> None:
    paths = {route.path for route in app.routes}

    assert "/api/portfolio/summary" in paths
    assert "/api/portfolio/holdings" in paths
    assert "/api/portfolio/exposure" in paths
    assert "/portfolio/summary" not in paths
