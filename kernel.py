import msgpack
import rpyc
from artiq.experiment import *


class TTLStates(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("core_dma")

        self.trg = self.get_device("ttl4")
        self.outputs = [self.get_device(f"ttl{5+n}") for n in range(2)]

        self.remote = rpyc.connect("localhost", 18861)

    def get_states(self) -> TList(TInt32):
        return msgpack.unpackb(self.remote.root.get_states())

    @kernel
    def loop(self):
        states = self.get_states()
        self.playback(states)

    @kernel
    def run(self):
        self.core.reset()

        while True:
            self.loop()

    @kernel
    def playback(self, states: TList(TInt32)):
        with self.core_dma.record("inner"):
            self.inner(states)

        handle = self.core_dma.get_handle("inner")
        self.core.break_realtime()

        for _ in range(10):
            at_mu(now_mu() & ~7)
            self.core_dma.playback_handle(handle)
            delay(100 * us)

    @kernel
    def inner(self, states: TList(TInt32)):
        self.trg.pulse_mu(500)

        for n in range(len(states)):
            self.outputs[n % 2].set_o(bool(states[n]))
            delay(10 * us)

        for dout in self.outputs:
            dout.off()
