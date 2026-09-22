def naive_forecast(values,horizon=5):
    last=float(values[-1]); return [last]*horizon
