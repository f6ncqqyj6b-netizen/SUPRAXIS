
from supraxis.state import SupraxisState
from supraxis.consensus.lightclient import LightClient
from supraxis.consensus.headerchain import Header
from supraxis.consensus.types import QC
from supraxis.consensus.checkpoint import Checkpoint, validators_hash
from supraxis.crypto_keys import ed25519_keygen, ed25519_sign
from supraxis.consensus.vote_signing import vote_message

st = SupraxisState()
k1 = ed25519_keygen(seed=b"11"*16)
k2 = ed25519_keygen(seed=b"22"*16)
v1 = "0x"+k1.public.hex()
v2 = "0x"+k2.public.hex()
st.storage["validators.epoch.0"] = [{"vid": v1, "power": 10}, {"vid": v2, "power": 10}]
st.storage[f"validator.{v1}"] = {"vid": v1, "reward_address":"0x"+"aa"*32}
st.storage[f"validator.{v2}"] = {"vid": v2, "reward_address":"0x"+"bb"*32}
vh0 = validators_hash(st.storage["validators.epoch.0"])
st.storage["validators.epoch.1"] = [{"vid": v1, "power": 30}]
st.storage[f"validator.{v1}"] = {"vid": v1, "reward_address":"0x"+"aa"*32}
vh1 = validators_hash(st.storage["validators.epoch.1"])

lc = LightClient(chain_id=1, trusted=Checkpoint(chain_id=1, epoch=0, height=1, state_root="aa"*32, block_hash="01"*32, validators_hash=vh0))

msg2 = vote_message(chain_id=1, height=2, round=0, block_hash="02"*32)
qc2 = QC(height=2, round=0, block_hash="02"*32, power=20, sigs={v1: ed25519_sign(k1.private, msg2), v2: ed25519_sign(k2.private, msg2)})
h2 = Header(chain_id=1, epoch=0, height=2, round=0, block_hash="02"*32, parent_hash="01"*32, proposer="p", validators_hash=vh0, qc=qc2)

msg3 = vote_message(chain_id=1, height=3, round=0, block_hash="03"*32)
qc3 = QC(height=3, round=0, block_hash="03"*32, power=30, sigs={v1: ed25519_sign(k1.private, msg3)})
h3 = Header(chain_id=1, epoch=1, height=3, round=0, block_hash="03"*32, parent_hash="02"*32, proposer="p", validators_hash=vh1, qc=qc3)

print(lc.sync_headers(st, [h2, h3]))
