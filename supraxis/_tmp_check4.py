
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
hs = [
    Header(chain_id=1, epoch=0, height=2, round=0, block_hash="02"*32, parent_hash="01"*32, proposer="p", validators_hash=vh, qc=None),
    Header(chain_id=1, epoch=0, height=3, round=0, block_hash="03"*32, parent_hash="02"*32, proposer="p", validators_hash=vh, qc=None),
    Header(chain_id=1, epoch=0, height=4, round=0, block_hash="04"*32, parent_hash="03"*32, proposer="p", validators_hash=vh, qc=None),
]
prev_hash = str(lc.trusted.block_hash)
prev_h = int(lc.trusted.height)
for h in hs:
    print("check", h.height, "parent==prev?", str(h.parent_hash)==prev_hash, "prev_hash", prev_hash[:4], "parent", str(h.parent_hash)[:4])
    if str(h.parent_hash) != prev_hash:
        print("FAIL at", h.height)
        break
    prev_hash = str(h.block_hash)
    prev_h = int(h.height)
print("manual ok")
print("method", lc.sync_headers(st, hs))
