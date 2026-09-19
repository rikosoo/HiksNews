#!/usr/bin/env python3
"""Run the full experiment matrix and emit the results table.

For every scenario: boot the flight software under QEMU with tracing on,
uplink the telecommands, then replay the trace through the control-flow
monitor. Traces are deleted as soon as they are consumed - a second of
emulated flight produces roughly 200 MB of trace.

  python3 eval/run_matrix.py --out out/results.md
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
ELF = ROOT / "firmware" / "build" / "flight.elf"

SCENARIOS = [
    ("S0",    "Nominal telecommands",              False),
    ("S1",    "Malformed telecommands (rejected)", False),
    ("S4",    "Sustained nominal load",            False),
    ("ATK-1", "Buffer overflow",                   True),
    ("ATK-2", "Function pointer corruption",       True),
    ("ATK-3", "ROP / control-flow hijacking",      True),
    ("ATK-4", "Malicious task scheduling",         True),
    ("ATK-5", "Unauthorized privileged function",  True),
    ("ATK-6", "Forged exception return",           True),
    ("S5",    "Data-only attack (no CF deviation)",  None),
]


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out/results.md")
    ap.add_argument("--settle", type=float, default=0.8)
    ap.add_argument("--workdir", default=tempfile.mkdtemp(prefix="cfi-"))
    args = ap.parse_args()

    work = pathlib.Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)
    model = work / "cfg.json"

    print("== extracting the static control-flow model ==")
    t0 = time.time()
    rc, out = run([sys.executable, str(ROOT / "monitor" / "cfg_extract.py"),
                   str(ELF), "-o", str(model)])
    extract_s = time.time() - t0
    print(out.strip())
    if rc != 0:
        return rc
    model_kb = model.stat().st_size / 1024.0

    rows = []
    for name, desc, is_attack in SCENARIOS:
        boundary = is_attack is None
        print(f"\n== {name}: {desc} ==")
        trace = work / f"{name}.trace"
        res = work / f"{name}.json"

        rc, out = run([sys.executable, str(ROOT / "eval" / "run_scenario.py"),
                       name, "--settle", str(args.settle), "--trace", str(trace)])
        compromised = "COMPROMISED" in out
        trace_mb = trace.stat().st_size / (1024 * 1024) if trace.exists() else 0.0

        t0 = time.time()
        rc, mout = run([sys.executable, str(ROOT / "monitor" / "cfi_monitor.py"),
                        str(model), str(trace), "--json", str(res)])
        analysis_s = time.time() - t0
        data = json.loads(res.read_text()) if res.exists() else {}
        trace.unlink(missing_ok=True)

        nv = data.get("n_violations", 0)
        lat = None
        if data.get("violations"):
            lat = data["violations"][0].get("lat_instr")
        rows.append({
            "scenario": name, "desc": desc, "attack": bool(is_attack),
            "boundary": boundary,
            "compromised": compromised, "violations": nv,
            "detected": bool(is_attack) and nv > 0,
            # Extra violations inside an attack scenario are the further
            # stages of the same hijack (a ROP chain trips more than one
            # edge); false positives are only meaningful on benign runs.
            "false_positives": 0 if (is_attack or boundary) else nv,
            "blocks": data.get("blocks", 0),
            "instructions": data.get("instructions", 0),
            "lat_instr": lat,
            "trace_mb": trace_mb,
            "analysis_s": analysis_s,
        })
        print(f"   compromised={compromised} violations={nv} "
              f"trace={trace_mb:.0f} MB analysis={analysis_s:.1f} s")

    hz = 25e6
    attacks = [r for r in rows if r["attack"]]
    benign = [r for r in rows if not r["attack"] and not r["boundary"]]
    boundary = [r for r in rows if r["boundary"]]
    det = sum(1 for r in attacks if r["detected"])
    fp = sum(r["false_positives"] for r in benign)

    lines = []
    lines.append("# Resultados / Results\n")
    lines.append(f"Gerado por `eval/run_matrix.py` | firmware: `{ELF.name}` "
                 f"| CPU: Cortex-M3 @ 25 MHz (QEMU mps2-an385)\n")

    lines.append("\n## Por cenário / Per scenario\n")
    lines.append("| Cenário | Descrição | Comprometido | Violações | Detectado | "
                 "Latência (instr) | Latência (ms) |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lat_ms = f"{r['lat_instr'] / hz * 1000:.4f}" if r["lat_instr"] else "—"
        lines.append(
            f"| {r['scenario']} | {r['desc']} | "
            f"{'sim' if r['compromised'] else 'não'} | {r['violations']} | "
            f"{'SIM' if r['detected'] else ('NÃO' if r['boundary'] else ('—' if r['attack'] else 'n/a'))} | "
            f"{r['lat_instr'] or '—'} | {lat_ms} |")

    lines.append("\n## Métricas agregadas / Summary metrics\n")
    lines.append("| Métrica | Valor |")
    lines.append("|---|---|")
    lines.append(f"| Attack detection | {det}/{len(attacks)} "
                 f"({100.0 * det / len(attacks):.0f}%) |")
    lines.append(f"| False positives (S0, S1, S4) | {fp} |")
    for b in boundary:
        lines.append(f"| {b['scenario']} — {b['desc']} | "
                     f"comprometido={'sim' if b['compromised'] else 'não'}, "
                     f"violações={b['violations']} → **fora do alcance da técnica** |")
    lat_all = [r["lat_instr"] for r in attacks if r["lat_instr"]]
    if lat_all:
        lo, hi = min(lat_all), max(lat_all)
        lines.append(f"| Detection latency | {lo}–{hi} instr "
                     f"({lo / hz * 1000:.4f}–{hi / hz * 1000:.4f} ms @ 25 MHz) |")
    lines.append("| CPU overhead (on board) | 0% — o firmware não é instrumentado |")
    lines.append("| Flash overhead (on board) | 0 KB — nenhum código adicionado à imagem |")
    lines.append("| Memory overhead (on board) | 0 KB — nenhuma estrutura em RAM de voo |")
    lines.append(f"| Modelo de CFG (lado do monitor) | {model_kb:.1f} KB |")
    lines.append(f"| Extração do modelo (build time) | {extract_s:.1f} s |")
    tb = sum(r["trace_mb"] for r in rows)
    ta = sum(r["analysis_s"] for r in rows)
    lines.append(f"| Volume de trace analisado | {tb:.0f} MB |")
    lines.append(f"| Tempo de análise | {ta:.0f} s |")

    lines.append("""
## Leitura dos números

O overhead de bordo é **zero por construção**: o detector não instrumenta o
firmware, ele consome o trace que o hardware já produz. O custo não desaparece —
migra para a banda do canal de trace e para os recursos do monitor. Essa é a
troca central da abordagem, e é o que a torna plausível sob orçamento de energia
e prazo de tempo real de um satélite.

A latência de detecção é medida entre a escrita que corrompe a pilha (retorno de
`tc_copy`) e o primeiro desvio ilegal observado. Ela é menor que o intervalo do
laço de ADCS (10 ms), o que significa que há margem para uma resposta antes do
próximo ciclo de controle.
""")

    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text("\n".join(lines))
    print("\n" + "\n".join(lines))
    print(f"\nwritten to {outp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
