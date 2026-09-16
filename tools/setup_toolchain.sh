#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; TOOLS="$ROOT/.tools"; BIN="$TOOLS/bin"; SRC="$TOOLS/src"; DL="$TOOLS/downloads"; EMU="$TOOLS/emulators"; GHIDRA_DIR="$TOOLS/ghidra"; mkdir -p "$BIN" "$SRC" "$DL" "$EMU"
log(){ printf '[gen7-3ds] %s\n' "$*"; }; have(){ command -v "$1" >/dev/null 2>&1; }
install_system_deps(){ if ! have apt-get; then return 0; fi; local SUDO=""; if [ "$(id -u)" -ne 0 ]; then if have sudo; then SUDO=sudo; else return 0; fi; fi; $SUDO apt-get update; $SUDO apt-get install -y --no-install-recommends ca-certificates git curl unzip make cmake ninja-build build-essential pkg-config python3 python3-pip clang llvm lldb binutils-arm-none-eabi openjdk-21-jdk libssl-dev libcurl4-openssl-dev zlib1g-dev; }
clone_or_update(){ local url="$1" dst="$2"; if [ -d "$dst/.git" ]; then git -C "$dst" fetch --depth=1 origin; git -C "$dst" reset --hard origin/HEAD; else git clone --depth=1 --recursive "$url" "$dst"; fi; }
download_verify(){ local url="$1" dst="$2" sha="$3"; [ -f "$dst" ] || curl -fL --retry 3 --retry-delay 2 "$url" -o "$dst"; printf '%s  %s\n' "$sha" "$dst" | sha256sum -c -; }
install_ctr(){ local d="$SRC/Project_CTR"; clone_or_update https://github.com/3DSGuy/Project_CTR.git "$d"; make -C "$d" -j"$(nproc)"; local ctr maker; ctr="$(find "$d" -type f -name ctrtool -perm -111 | head -n1 || true)"; maker="$(find "$d" -type f -name makerom -perm -111 | head -n1 || true)"; [ -n "$ctr" ] && [ -n "$maker" ]; install -m755 "$ctr" "$BIN/ctrtool"; install -m755 "$maker" "$BIN/makerom"; }
install_3dstool(){ local d="$SRC/3dstool"; clone_or_update https://github.com/dnasdw/3dstool.git "$d"; cmake -S "$d" -B "$d/build" -DCMAKE_BUILD_TYPE=Release -DUSE_DEP=ON; cmake --build "$d/build" -j"$(nproc)"; local exe; exe="$(find "$d/bin" "$d/build" -type f -name 3dstool -perm -111 2>/dev/null | head -n1 || true)"; [ -n "$exe" ]; install -m755 "$exe" "$BIN/3dstool"; }
install_ghidra(){ local zip="$DL/ghidra_12.1.3_PUBLIC_20260817.zip"; download_verify https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.3_build/ghidra_12.1.3_PUBLIC_20260817.zip "$zip" 93a5d11a9ad510622acaaf908c556a7b9b764d338e78a7567f3689bf5081fd54; rm -rf "$GHIDRA_DIR"; mkdir -p "$GHIDRA_DIR"; unzip -q "$zip" -d "$GHIDRA_DIR"; local home; home="$(find "$GHIDRA_DIR" -mindepth 1 -maxdepth 1 -type d | head -n1)"; ln -sfn "$home/ghidraRun" "$BIN/ghidraRun"; ln -sfn "$home/support/analyzeHeadless" "$BIN/analyzeHeadless"; }
install_azahar(){ local dst="$EMU/azahar.AppImage"; download_verify https://github.com/azahar-emu/azahar/releases/download/2126.1.1/azahar.AppImage "$dst" e445dabc18fe7665867e24a18a78e24e133261a9cc320fae6a4a45bd2e7c4783; chmod +x "$dst"; ln -sfn "$dst" "$BIN/azahar"; }
install_system_deps; for c in git curl cmake make python3 unzip sha256sum java; do have "$c" || exit 1; done; install_ctr; install_3dstool; install_ghidra; install_azahar
cat > "$TOOLS/env.sh" <<'ENV'
#!/usr/bin/env bash
_TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; export PATH="$_TOOLS_DIR/bin:$PATH"; unset _TOOLS_DIR
ENV
chmod +x "$TOOLS/env.sh"; printf 'platform=nintendo-3ds\nghidra=12.1.3\nazahar=2126.1.1\n' > "$TOOLS/versions.txt"; log "done. Run: source .tools/env.sh"
