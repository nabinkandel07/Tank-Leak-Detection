"""Mass-balance tank leak detector using deterministic simulation."""

import csv
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def make_svg(rows):
    width, height, margin = 800, 430, 45
    max_level = max(r[4] for r in rows)
    def point(step, value):
        x = margin + step / (len(rows) - 1) * (width - 2 * margin)
        y = height - margin - value / max_level * (height - 2 * margin)
        return f"{x:.1f},{y:.1f}"
    level = " ".join(point(r[0], r[4]) for r in rows)
    residual = " ".join(point(r[0], r[5] * 20) for r in rows)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><text x="45" y="25" font-family="sans-serif" font-size="16">Tank level and scaled mass-balance residual</text>
<polyline points="{level}" fill="none" stroke="#2563eb" stroke-width="3"/><polyline points="{residual}" fill="none" stroke="#dc2626" stroke-width="2"/>
<line x1="{margin + 120 / (len(rows)-1)*(width-2*margin):.1f}" y1="35" x2="{margin + 120 / (len(rows)-1)*(width-2*margin):.1f}" y2="{height-margin}" stroke="#111827" stroke-dasharray="5 5"/>
<text x="610" y="25" fill="#2563eb" font-family="sans-serif">level</text><text x="660" y="25" fill="#dc2626" font-family="sans-serif">residual x20</text></svg>'''


def simulate(threshold=0.22, seed=23):
    rng = random.Random(seed)
    level = 55.0
    rows = []
    predictions = []
    persistence = 0
    for step in range(240):
        inflow = 1.1 + 0.25 * math.sin(step / 18)
        outflow = 0.95 + 0.18 * math.cos(step / 25)
        leak = 0.0 if step < 120 else 0.42
        next_level = level + inflow - outflow - leak
        measured_next = next_level + rng.gauss(0, 0.035)
        residual = level + inflow - outflow - measured_next
        persistence = persistence + 1 if residual > threshold else 0
        detected = persistence >= 3
        truth = step >= 120
        predictions.append((truth, detected))
        rows.append((step, inflow, outflow, leak, measured_next, residual, int(detected)))
        level = measured_next
    return rows, predictions


def evaluate(predictions):
    tp = sum(t and p for t, p in predictions)
    fp = sum((not t) and p for t, p in predictions)
    fn = sum(t and (not p) for t, p in predictions)
    first_detection = next((i for i, (_, predicted) in enumerate(predictions) if predicted), None)
    return tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn), first_detection


def threshold_sweep_svg(rows):
    width, height, margin = 720, 420, 50
    def point(threshold, value):
        x = margin + (threshold - rows[0][0]) / (rows[-1][0] - rows[0][0]) * (width - 2 * margin)
        y = height - margin - value * (height - 2 * margin)
        return f"{x:.1f},{y:.1f}"
    precision = " ".join(point(row[0], row[1]) for row in rows)
    recall = " ".join(point(row[0], row[2]) for row in rows)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/><text x="50" y="25" font-family="sans-serif" font-size="16">Alarm-threshold sensitivity</text>
<line x1="50" y1="370" x2="670" y2="370" stroke="#111"/><line x1="50" y1="50" x2="50" y2="370" stroke="#111"/>
<polyline points="{precision}" fill="none" stroke="#2563eb" stroke-width="3"/><polyline points="{recall}" fill="none" stroke="#dc2626" stroke-width="3"/>
<text x="535" y="25" fill="#2563eb" font-family="sans-serif">precision</text><text x="615" y="25" fill="#dc2626" font-family="sans-serif">recall</text></svg>'''


def main():
    RESULTS.mkdir(exist_ok=True)
    rows, predictions = simulate()
    precision, recall, first_detection = evaluate(predictions)
    sweep = []
    for threshold_percent in range(10, 51, 5):
        threshold = threshold_percent / 100
        _, threshold_predictions = simulate(threshold)
        threshold_precision, threshold_recall, detection = evaluate(threshold_predictions)
        sweep.append((threshold, threshold_precision, threshold_recall, "" if detection is None else detection - 120))
    metrics = {
        "samples": len(rows),
        "precision": precision,
        "recall": recall,
        "leak_start_step": 120,
        "first_detection_step": first_detection,
        "detection_delay_steps": first_detection - 120,
        "data": "deterministic synthetic tank mass-balance simulation",
    }
    with (RESULTS / "simulation.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["step", "inflow", "outflow", "true_leak", "measured_level", "residual", "detected"])
        writer.writerows(rows)
    with (RESULTS / "threshold_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["threshold", "precision", "recall", "detection_delay_steps"])
        writer.writerows(sweep)
    (RESULTS / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (RESULTS / "simulation.svg").write_text(make_svg(rows), encoding="utf-8")
    (RESULTS / "threshold_sweep.svg").write_text(threshold_sweep_svg(sweep), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
