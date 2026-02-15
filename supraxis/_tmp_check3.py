
from supraxis.state import SupraxisState
from supraxis.consensus.checkpoint import Checkpoint, validators_hash
from supraxis.consensus.headerchain import Header
from supraxis.consensus.lightclient import LightClient

st = SupraxisState()
st.storage["validators.epoch.0"] = [{"vid":"0x"+"01"*32,"power":10},{"vid":"0x"+"02"*32,"power":10}]
st.storage["validator." + "0x"+"01"*32] = {"vid":"0x"+"01"*32,"reward_address":"0x"+"aa"*32}
st.storage["validator." + "0x"+"02"*32] = {"vid":"0x"+"02"*32,"reward_address":"0x"+"bb"*32}
vh = validators_hash(st.storage["validators.epoch.0"])
lc = LightClient(chain_id=1, trusted=Checkpoint(chain_id=1, epoch=0, height=1, state_root="aa"*32, block_hash="01"*32, validators_hash=vh))
h2 = Header(chain_id=1, epoch=0, height=2, round=0, block_hash="02"*32, parent_hash="01"*32, proposer="p", validators_hash=vh, qc=None)
print(repr(lc.trusted.block_hash), type(lc.trusted.block_hash))
print(repr(h2.parent_hash), type(h2.parent_hash))
print("eq?", str(h2.parent_hash)==str(lc.trusted.block_hash))
print("cmp", str(h2.parent_hash), str(lc.trusted.block_hash))
