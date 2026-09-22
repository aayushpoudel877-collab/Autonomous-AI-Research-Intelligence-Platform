import numpy as np
class LinearForecaster:
    def fit(self, values):
        y=np.asarray(values,dtype=float); self.slope=np.polyfit(np.arange(len(y)),y,1)[0] if len(y)>1 else 0.0; self.last=float(y[-1]); return self
    def predict(self, horizon=5): return [self.last+self.slope*(i+1) for i in range(horizon)]
