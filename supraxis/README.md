# SUPRAXIS — Phase 21 (Option B) Economic Hardening

Clean Phase 21 built on Phase 19.

## Evidence economy
- Fees: `evidence.fee`, `evidence.fee_mode` (adaptive)
- Fee sink: `evidence.fee_sink_mode` (treasury/burn/split)
- Burn shares: `evidence.fee_burn_bps` (accept), `evidence.fee_burn_reject_bps` (reject)
- Refund on accept: `evidence.refund_bps`
- Bounty decay + cap: `evidence.bounty_bps`, `evidence.bounty_min_bps`, `evidence.max_bounty`
- Attempt cooldown: `evidence.cooldown_attempts`
- Rejects are non-fatal: emits `EVIDENCE_REJECTED`

## Treasury distribution
Governance sets:
- `treasury.dist_interval` (ticks)
- `treasury.dist_insurance_bps`
- `treasury.dist_committee_bps`

Anyone can call:
- `TREASURY_DISTRIBUTE` with optional `tick` (u32) to distribute treasury into:
  - `insurance_pool`
  - `committee_pool`

## Run tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py" -q
```

## Phase 22 additions
- Committee rewards: GOV_SET_COMMITTEE_DISTRIBUTION + COMMITTEE_DISTRIBUTE (permissionless; distributes committee_pool to committee members as stake)
- Insurance payouts: INSURANCE_PAYOUT (governance-gated) pays from insurance_pool to a 32-byte address

## Phase 23 additions
- Insurance claims lifecycle: INSURANCE_CLAIM (permissionless), INSURANCE_CLAIM_PAY / INSURANCE_CLAIM_REJECT (governance gated)
- Insurance policy: GOV_SET_INSURANCE_POLICY {max_payout, cooldown, claim_fee}
- Auto-funding: GOV_SET_TREASURY_TO_INSURANCE + AUTO_TREASURY_TO_INSURANCE (permissionless tick-based)

## Phase 24 additions
- Claims batching: CLAIMS_BATCH_PAY (governance gated) pays pending claims by mode=oldest/smallest/largest with limits.
- Dispute hooks: DISPUTE_SUBMIT (permissionless) + DISPUTE_RESOLVE (governance gated).
- Audit: AUDIT_INVARIANTS emits basic non-negativity snapshots.

## Phase 25 additions
- Claim freezing: CLAIM_FREEZE / CLAIM_UNFREEZE (governance gated) to pause payouts.
- Evidence linkage: LINK_EVIDENCE_TO_CLAIM (permissionless) maps evidence_hash -> claim_id.
- Claims batch policy: GOV_SET_CLAIMS_BATCH_POLICY sets default mode and skip flags (frozen/disputed).
- Stronger audit: AUDIT_INVARIANTS now reports claim counts and pending_sum.

## Phase 26 additions
- Hard failure invariants: runtime aborts on negative balances/pools/stakes or burned-category mismatch.
- Burn ledger categories: burned_fee/burned_slash/burned_penalty tracked; evidence fee burns now use categorized burning.
- Optional supply conservation (hard failure) when enabled: GOV_SET_SUPPLY sets supply.total and supply.enforce; if enforce=1, total_accounted must equal supply.total.
- Deterministic STATE_COMMITMENT event appended per executed envelope with a canonical snapshot + hash for cross-chain verification.


## Phase 27 additions
- Sovereign L1 consensus spec (HotStuff-style BFT) in docs/consensus/phase27_hotstuff_bft.md
- Reference consensus scaffolding: proposer selection, votes/QC formation, 3-chain commit rule, and deterministic simulator.

## Phase 28 additions
- P2P + mempool spec: docs/networking/phase28_p2p_mempool.md
- Deterministic mempool ordering + block assembly: src/supraxis/net/mempool.py
- In-memory deterministic gossip simulator: src/supraxis/net/gossip.py

## Phase 29 additions
- Domain separation: EnvelopeV2.signing_message() now prefixes b"SUPRAXIS|ENV2|" to prevent cross-context replay.
- CryptoVerifier fixed + enabled: Ed25519 (scheme 11) and secp256k1 ECDSA (scheme 12) verification via `cryptography`.
- New key utilities: src/supraxis/crypto_keys.py for Ed25519 keygen/sign helpers.

## Phase 30 additions
- Fee market (fixed supply): deterministic per-envelope fee = static_gas * gas_price, debited from sender; burn_bps optionally burns a portion; remainder funds treasury.
- Automatic rewards: after block, a portion of collected fees is paid to the proposer reward address (if registered) and a portion to committee_pool.
- Validator registry + staking lifecycle: VAL_REGISTER, STAKE_BOND, STAKE_UNBOND_REQUEST, STAKE_WITHDRAW.
- Consensus slashing hooks: CONSENSUS_SLASH_DOUBLE_VOTE and CONSENSUS_SLASH_EQUIVOCATION using signed-evidence verification.

## Phase 31 additions
- Epoch/tick system with deterministic advancement: EPOCH_ADVANCE increments tick; on epoch boundary emits EPOCH_ROLLOVER and snapshots validator set.
- Epoch policy governance: GOV_SET_EPOCH_POLICY sets epoch.len_ticks and epoch.max_validators.
- Pending unbond slashing: state.slash_with_pending() extends slashing to unbond records still locked (unlock > tick).

## Phase 32 additions
- Consensus validator-set wiring: consensus membership is derived from epoch snapshots (validators.epoch.*).
- New helpers: src/supraxis/consensus/validator_set.py and src/supraxis/consensus/node.py.
- New spec: docs/consensus/phase32_epoch_validator_set_consensus.md

## Phase 33 additions
- End-to-end block production pipeline (mempool → execute → block hash → votes/QC) in src/supraxis/consensus/pipeline.py
- Checkpoint primitives for fast sync: src/supraxis/consensus/checkpoint.py
- Spec: docs/consensus/phase33_block_production_pipeline.md

## Phase 34 additions
- Signed checkpoints with quorum verification: src/supraxis/consensus/signed_checkpoint.py
- Minimal light client verifier: src/supraxis/consensus/lightclient.py
- Spec: docs/consensus/phase34_signed_checkpoints_light_client.md

## Phase 35 additions
- Gossip cache for signed checkpoints + headers: src/supraxis/consensus/gossip.py
- Header-only chain structure: src/supraxis/consensus/headerchain.py
- Light client header sync: LightClient.sync_headers(...)
- Spec: docs/consensus/phase35_gossip_and_header_sync.md

## Phase 36 additions
- QC verification during header sync: src/supraxis/consensus/qc_verify.py
- Header sync now epoch-aware and QC-verified: LightClient.sync_headers(state, headers)
- Header structure includes epoch + validators_hash
- Spec: docs/consensus/phase36_qc_verified_header_sync.md

## Phase 37 additions
- Cryptographic QC verification (vote signatures): src/supraxis/consensus/vote_signing.py and qc_verify.py
- Light client enforces validator key registration (validator.<vid> must exist)
- Spec: docs/consensus/phase37_crypto_qc_and_validator_keys.md

## Phase 38 additions
- QC signatures now multi-scheme: QC.sigs maps voter -> {scheme,sig}
- QC crypto verification supports Ed25519 + secp256k1
- Signed header primitive: src/supraxis/consensus/signed_header.py
- Spec: docs/consensus/phase38_multischeme_qc_and_signed_headers.md

## Phase 39 additions
- GossipStore now caches SignedHeaders and can return signed-header paths
- LightClient prefers signed-header sync: LightClient.sync_signed_headers(...)
- Unsigned header sync now requires QC (rejects bare headers)
- Spec: docs/consensus/phase39_signed_header_gossip_and_lightclient.md

## Phase 40 additions
- Persistence helpers for gossip cache: src/supraxis/consensus/persist.py
- GossipStore.to_dict()/from_dict() for JSON save/load
- End-to-end fast sync orchestrator: src/supraxis/consensus/fastsync.py
- CLI demo: src/supraxis/cli_fastsync_demo.py
- Spec: docs/consensus/phase40_end_to_end_fastsync.md

## Phase 41 additions
- Full node bootstrap flow: src/supraxis/node/bootstrap.py
- In-memory block store/provider: src/supraxis/node/blockstore.py
- Deterministic replay helper: src/supraxis/node/state_exec.py
- Spec: docs/node/phase41_fullnode_bootstrap.md

## Phase 42 additions
- P2P message framing: src/supraxis/p2p/message.py
- Sync protocol constants/types: src/supraxis/p2p/protocol.py
- Disk persistence DB (JSON): src/supraxis/node/db.py
- Simulated networking ingestion + sync client: src/supraxis/node/sync.py
- Spec: docs/node/phase42_network_ingestion_and_db.md

## Phase 43 additions
- Async TCP transport with validation: src/supraxis/p2p/transport.py
- Peer scoring/decay/ban + limits: src/supraxis/p2p/peer_manager.py
- Anti-spam validation + rate limiting: src/supraxis/p2p/security.py
- Spec: docs/node/phase43_real_transport_peer_scoring_antispam.md

## Phase 44 additions
- Peer discovery protocol: peers/peers_ok
- Persistent peer DB: src/supraxis/node/peerdb.py
- Discovery service: src/supraxis/p2p/discovery.py
- Peer sync with exponential backoff: src/supraxis/node/peer_sync.py
- NodeService request handler incl peers: src/supraxis/node/service.py
- Spec: docs/node/phase44_peer_discovery_and_peerdb.md

## Phase 45 additions
- Global anti-spam limits + quotas: src/supraxis/p2p/antispam.py
- Transport hardening: max conns, global rate limit, global quotas
- Protocol fuzz/regression tests: tests/test_phase45_fuzz.py
- Spec: docs/node/phase45_antispam_hardening_and_fuzz.md

## Phase 46 additions
- Hardened persistence helpers (atomic + checksum): src/supraxis/node/storage_io.py
- NodeDB snapshot versioning + corruption checks: src/supraxis/node/db.py
- Spec: docs/node/phase46_persistence_hardening.md

## Phase 47 additions
- Snapshot chunking + verification: src/supraxis/node/snapshot_chunks.py
- Snapshot meta/chunk protocol: src/supraxis/p2p/protocol.py
- Node snapshot serving: src/supraxis/node/service.py
- Snapshot sync client: src/supraxis/node/snapshot_sync.py
- Spec: docs/node/phase47_snapshot_chunking_and_verification.md

## Phase 48 additions
- Transaction format + hashing: src/supraxis/tx.py
- Fee estimation: src/supraxis/fees.py
- Mempool with limits/eviction: src/supraxis/mempool.py
- TX gossip protocol + service: src/supraxis/node/tx_service.py
- Spec: docs/node/phase48_transactions_mempool_fees.md

## Phase 49 additions
- Block format + hashing: src/supraxis/netblock.py
- Block builder/proposer: src/supraxis/node/block_builder.py
- Block gossip protocol + service: src/supraxis/node/block_gossip.py
- NodeService handles new_block: src/supraxis/node/service.py
- Spec: docs/node/phase49_block_builder_and_block_gossip.md

## Phase 50 additions
- Evidence model + verification: src/supraxis/consensus/evidence.py
- Evidence store + slashed registry: src/supraxis/node/evidence_store.py
- Evidence persistence (atomic+checksum): NodeDB evidence.json
- Evidence P2P protocol + Node handlers: src/supraxis/node/evidence_service.py
- Spec: docs/node/phase50_slashing_evidence_plumbing.md

## Phase 51 additions
- Governance engine (timelock + emergency brake): src/supraxis/governance.py
- Governance P2P service + persistence: src/supraxis/node/governance_service.py
- Validator set + slashing adapter hooks: src/supraxis/consensus/stake_accounting.py, src/supraxis/node/slash_adapter.py
- Spec: docs/node/phase51_governance_hardening.md

## Phase 52 additions
- Genesis + network config: src/supraxis/genesis.py, src/supraxis/config.py
- Bootstrap scripts: scripts/supraxis_genesis.py, scripts/supraxis_run_node.py
- Example artifacts: artifacts/example_validators.json, artifacts/example_params.json
- Spec: docs/node/phase52_genesis_seed_bootstrap.md

## Phase 53 additions
- HTTP/JSON RPC server: src/supraxis/rpc/server.py
- Minimal CLI client: scripts/supraxis_cli.py
- run_node starts RPC alongside P2P: scripts/supraxis_run_node.py
- Spec: docs/node/phase53_rpc_api_and_cli.md

## Phase 55 additions
- Deterministic ledger + state root: src/supraxis/ledger_state.py
- State persistence + node state service: src/supraxis/node/state_service.py
- RPC state endpoints + run_node wiring
- Spec: docs/node/phase55_state_machine_ledger.md

## Phase 56 additions
- Block state_root compute/verify/apply: src/supraxis/node/block_builder.py
- NetBlock helper: src/supraxis/netblock.py
- Spec: docs/node/phase56_block_state_root.md

## Phase 61 additions
- Snapshot system: src/supraxis/snapshot.py + NodeDB save/load snapshot + RPC/CLI
- Verified snapshot restore in StateService
- Spec: docs/node/phase61_snapshot_system.md

## Phase 62 additions
- Block persistence to NodeDB + /sync/plan endpoint
- Spec: docs/node/phase62_fast_sync_plan.md
