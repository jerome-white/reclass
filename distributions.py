import math

import pandas as pd

class Distribution:
    def __init__(self, t_min, t_max):
        if t_max <= t_min:
            raise ValueError('Invalid range: {} {}'.format(t_min, t_max))

        self.t_min = t_min
        self.t_max = t_max

    def __call__(self, n=100):
        col = 'F'

        return (pd
                .Series(self.pdf(n + 1), name=col)
                .cumsum()
                .to_frame()
                .assign(Pk=lambda x: x[col].diff().shift(-1))
                .dropna())

    def pdf(self, n):
        raise NotImplementedError()

class Z(Distribution):
    def __init__(self, t_c, sigma, t_min, t_max):
        super().__init__(t_min, t_max)

        self.t_c = t_c
        self.s2 = sigma * math.sqrt(2)

    def pdf(self, n):
        chi = 1 / (2 * (self.t_max - self.t_min))
        erf = lambda x, y: math.erf(math.log((x - y) / self.t_c) / self.s2)

        for z in range(n):
            if z <= self.t_min:
                ans = 0
            else:
                left = erf(z, self.t_min)
                if z <= self.t_max:
                    ans = 1 + left
                else:
                    assert z > self.t_max
                    ans = left - erf(z, self.t_max)
                ans *= chi

            yield ans

class Triangle(Distribution):
    def pdf(self, n):
        span = self.t_max - self.t_min
        pa = 2 / span

        for t in range(n):
            inside = self.t_min <= t <= self.t_max
            yield pa * (1 - (t - self.t_min) / span) if inside else 0
