import logging

import msgpack
import numpy as np
import rpyc


class Supervisor(rpyc.Service):
    def exposed_get_states(self) -> bytes:
        return msgpack.packb(np.random.choice([0, 1], size=250).tolist())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    server = rpyc.utils.server.ThreadedServer(
        Supervisor,
        port=18861,
    )
    server.start()
