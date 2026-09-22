from nexus.forecasting.linear import LinearForecaster

def test_forecast_trend():
    pred=LinearForecaster().fit([1,2,3]).predict(2)
    assert pred[0]>3 and pred[1]>pred[0]
