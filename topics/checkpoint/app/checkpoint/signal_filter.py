"""Time-aware 1€ filter (Casiez, Roussel & Vogel, CHI 2012).
Independent implementation of the published equations; no third-party runtime.
A faster signal raises the cutoff, reducing lag without amplifying resting jitter.
"""
import math


class OneEuro:
    def __init__(self, min_cutoff=1.2, beta=.35, derivative_cutoff=1.):
        self.min_cutoff=min_cutoff;self.beta=beta;self.derivative_cutoff=derivative_cutoff
        self.time=None;self.raw=None;self.value=None;self.derivative=0.

    @staticmethod
    def alpha(cutoff,dt):return 1/(1+1/(2*math.pi*cutoff*dt))

    def update(self,value,now):
        value=float(value)
        if self.time is None or now-self.time>1.:
            self.time=now;self.raw=value;self.value=value;self.derivative=0.;return value
        dt=now-self.time
        if dt<=0:return self.value
        speed=(value-self.raw)/dt
        a=self.alpha(self.derivative_cutoff,dt);self.derivative+=a*(speed-self.derivative)
        cutoff=self.min_cutoff+self.beta*abs(self.derivative)
        self.value+=self.alpha(cutoff,dt)*(value-self.value)
        self.time=now;self.raw=value
        return self.value
