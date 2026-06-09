# syntax=docker/dockerfile:1
# Containerized Enterprise Agent OS core: Rust fabric-core + Python reference +
# SurrealQL + spec. Build context = repo root:
#   docker build -f deploy/fabric/Dockerfile -t fabric-core:local .

# --- stage 1: build + test the Rust core ---------------------------------
FROM rust:1-slim AS rust-build
WORKDIR /build
COPY crates/fabric-core/Cargo.toml crates/fabric-core/Cargo.toml
COPY crates/fabric-core/src crates/fabric-core/src
RUN cargo test --release --manifest-path crates/fabric-core/Cargo.toml \
 && cargo build --release --manifest-path crates/fabric-core/Cargo.toml

# --- stage 2: runtime (reference + benchmarks + surql + spec) ------------
FROM python:3.13-slim AS runtime
WORKDIR /fabric
COPY scripts/ scripts/
COPY experiments/fabric/ experiments/fabric/
COPY docs/ docs/
COPY --from=rust-build /build/crates/fabric-core/target/release/fabric-core /usr/local/bin/fabric-core
RUN useradd -m fabric && chown -R fabric /fabric
USER fabric

# Prove the Rust core resolves, then run the full (deterministic) benchmark suite.
CMD ["bash", "-lc", "fabric-core && bash scripts/run_benchmarks.sh"]
