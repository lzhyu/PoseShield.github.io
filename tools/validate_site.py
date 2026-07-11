#!/usr/bin/env python3
"""Validate PoseShield website content and local assets.

This is intentionally lightweight so it can run on the static GitHub Pages
repository without installing Node or browser tooling. Final acceptance should
run this script without --allow-partial-motion after motion-100 has completed.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODE_REPO = PROJECT_ROOT.parent / "PoseShield"


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value for key, value in attrs if value is not None}
        for key in ("src", "href", "poster"):
            value = attr_map.get(key)
            if value and value.startswith("./static/"):
                path = value[2:].split("?", 1)[0]
                self.refs.append(path)
                if tag == "img":
                    self.images.append(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--code-root", type=Path, default=DEFAULT_CODE_REPO)
    parser.add_argument("--expected-motion-total", type=int, default=100)
    parser.add_argument("--allow-partial-motion", action="store_true")
    parser.add_argument("--screenshot", action="append", type=Path, default=[])
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def check(condition: bool, message: str, errors: list[str]) -> None:
    if condition:
        ok(message)
    else:
        fail(message, errors)


def load_html(site_root: Path) -> str:
    index = site_root / "index.html"
    if not index.is_file():
        raise FileNotFoundError(index)
    return index.read_text(encoding="utf-8")


def check_static_refs(site_root: Path, html: str, errors: list[str]) -> RefParser:
    parser = RefParser()
    parser.feed(html)
    missing = [ref for ref in parser.refs if not (site_root / ref).is_file()]
    check(not missing, f"all {len(parser.refs)} local static refs exist", errors)
    if missing:
        print("       missing: " + ", ".join(missing))
    check_css_refs(site_root, parser.refs, errors)
    return parser


def check_css_refs(site_root: Path, refs: list[str], errors: list[str]) -> None:
    css_refs = [site_root / ref for ref in refs if ref.endswith(".css")]
    checked = 0
    missing: list[str] = []
    for css_path in css_refs:
        if not css_path.is_file():
            continue
        css = css_path.read_text(encoding="utf-8")
        for match in re.findall(r"url\(([^)]+)\)", css):
            raw = match.strip().strip("\"'")
            if not raw or raw.startswith(("data:", "http://", "https://", "#")):
                continue
            target = (css_path.parent / raw).resolve()
            checked += 1
            if not target.is_file():
                try:
                    missing.append(str(target.relative_to(site_root)))
                except ValueError:
                    missing.append(str(target))
    check(not missing, f"all {checked} local CSS url refs exist", errors)
    if missing:
        print("       missing CSS refs: " + ", ".join(missing))


def check_required_content(html: str, errors: list[str]) -> None:
    required_text = [
        "PoseShield: Neural Collision Fields for Human Self-Collision Resolution",
        "Pose Examples",
        "Human Motion Examples",
        "Humans with Collisions Data Examples",
        "Pose-Level Evaluation",
        "Failure Cases",
        "Limitations",
        "Resources",
        "BibTeX",
        "MotionFix",
        "SAField",
        "red",
        "green",
    ]
    for text in required_text:
        check(text in html, f"required text present: {text}", errors)

    section_requirements = {
        "pose gallery GLB viewers": len(re.findall(r"static/models/(?:pose_candidates/)?pose_\d+_before_after\.glb", html)) >= 6,
        "pose viewer static pair previews removed": not re.search(r"pose_examples/pose_\d+_pair", html) and "pose-viewer-poster" not in html,
        "viewer fallback paths are CSS-relative": "url('./static/images/viewer_fallbacks/" not in html,
        "motion Blender videos": len(re.findall(r"static/videos/motionfix_\d+_135_blender\.(?:mp4|webm)", html)) >= 6,
        "motion GIFs removed from homepage": not re.search(r"static/videos/motionfix_\d+_135_blender\.gif", html),
        "motion scrub sliders present": len(re.findall(r"data-motion-slider", html)) >= 6,
        "motion play buttons present": len(re.findall(r"data-motion-toggle", html)) >= 6,
        "motion videos do not loop by default": "<video" in html and " loop " not in html,
        "HwC GLB viewers": len(re.findall(r"static/models/hwc_(?:collision|free)_\d+\.glb", html)) >= 6,
        "HwC camera uses pose-example front view": "camera-orbit=\"90deg" not in html and "camera-orbit=\"-90deg" not in html,
        "HwC static previews removed": "hwc-viewer-poster" not in html and not re.search(r"hwc_examples/hwc_(?:collision|free)_\d+\.jpg", html),
        "HwC uses pose card classes": all(token not in html for token in ["hwc-viewer-grid", "hwc-viewer-shell", "hwc-example-viewer"]),
        "HwC paper-source dataset scale": all(text in html for text in ["931k SMPL-H poses", "531k self-colliding", "399k collision-free", "57%", "43%", "9:1"]),
        "old HwC local-derived count removed": "1,489,294" not in html,
        "local model-viewer script": "static/js/model-viewer.min.js" in html,
        "weighted-distance plot removed": "pose_correlation_tradeoff.png" not in html,
        "pose resolution plot present": "pose_resolution_rates.png" in html,
        "classifier baseline text removed": "Classifier baseline" not in html,
        "paper table annotation removed": "Paper Table 1" not in html,
        "motion captions hide internal metrics": not re.search(
            r"exact-FCL|sim change|wrist mean distance|\d+\s*frames",
            html,
            flags=re.IGNORECASE,
        ),
        "resource links": all(
            link in html
            for link in [
                "https://github.com/lzhyu/PoseShield",
                "https://huggingface.co/ZYYY99/PoseShield",
                "https://drive.google.com/drive/folders/1gLdFy4OTfYaKeaZ3olqShyh3kF2m5ogf?usp=sharing",
                "https://github.com/lzhyu/PoseShield.github.io",
            ]
        ),
        "arXiv BibTeX": "@article{li2026poseshield" in html,
    }
    for label, condition in section_requirements.items():
        check(condition, label, errors)

    fallback_files = re.findall(r"static/images/viewer_fallbacks/([a-z0-9_/]+\.jpg)", html)
    check(len(set(fallback_files)) >= 12, "viewer fallback posters referenced for pose and HwC cards", errors)
    for filename in sorted(set(fallback_files)):
        check((PROJECT_ROOT / "static/images/viewer_fallbacks" / filename).is_file(), f"viewer fallback exists: {filename}", errors)


def check_pose_candidate_page(site_root: Path, errors: list[str]) -> None:
    page = site_root / "pose_candidates.html"
    check(page.is_file(), f"pose candidate page exists: {page}", errors)
    if not page.is_file():
        return
    html = page.read_text(encoding="utf-8")
    parser = RefParser()
    parser.feed(html)
    missing = [ref for ref in parser.refs if not (site_root / ref).is_file()]
    check(not missing, f"all {len(parser.refs)} pose candidate static refs exist", errors)
    if missing:
        print("       missing candidate refs: " + ", ".join(missing))

    candidate_glbs = set(re.findall(r"static/models/pose_candidates/pose_\d+_before_after\.glb", html))
    candidate_posters = set(re.findall(r"static/images/viewer_fallbacks/pose_candidates/pose_\d+_before_after\.jpg", html))
    check(len(candidate_glbs) >= 15, "pose candidate page has at least 15 GLB viewers", errors)
    check(len(candidate_posters) >= 15, "pose candidate page has at least 15 fallback posters", errors)
    check("near-contact highlight" not in html, "pose candidate page avoids near-contact wording", errors)
    check("contact vertex" in html, "pose candidate page explains contact vertex highlighting", errors)


def check_hwc_candidate_page(site_root: Path, errors: list[str]) -> None:
    page = site_root / "hwc_candidates.html"
    check(page.is_file(), f"HwC candidate page exists: {page}", errors)
    if not page.is_file():
        return
    html = page.read_text(encoding="utf-8")
    parser = RefParser()
    parser.feed(html)
    missing = [ref for ref in parser.refs if not (site_root / ref).is_file()]
    check(not missing, f"all {len(parser.refs)} HwC candidate static refs exist", errors)
    if missing:
        print("       missing HwC candidate refs: " + ", ".join(missing))

    collision_glbs = set(re.findall(r"static/models/hwc_collision_\d+\.glb", html))
    free_glbs = set(re.findall(r"static/models/hwc_free_\d+\.glb", html))
    collision_posters = set(re.findall(r"static/images/viewer_fallbacks/hwc_collision_\d+\.jpg", html))
    free_posters = set(re.findall(r"static/images/viewer_fallbacks/hwc_free_\d+\.jpg", html))
    check(len(collision_glbs) >= 10, "HwC candidate page has at least 10 collision GLB viewers", errors)
    check(len(free_glbs) >= 10, "HwC candidate page has at least 10 free GLB viewers", errors)
    check(len(collision_posters) >= 10, "HwC candidate page has at least 10 collision fallback posters", errors)
    check(len(free_posters) >= 10, "HwC candidate page has at least 10 free fallback posters", errors)
    check("HC01-HC10" in html and "HF01-HF10" in html, "HwC candidate page exposes selection codes", errors)
    check("contact vertex" in html, "HwC candidate page explains contact vertex highlighting", errors)


def check_motion_candidate_page(site_root: Path, errors: list[str]) -> str:
    page = site_root / "motion_candidates.html"
    check(page.is_file(), f"motion candidate page exists: {page}", errors)
    if not page.is_file():
        return ""
    html = page.read_text(encoding="utf-8")
    parser = RefParser()
    parser.feed(html)
    missing = [ref for ref in parser.refs if not (site_root / ref).is_file()]
    check(not missing, f"all {len(parser.refs)} motion candidate static refs exist", errors)
    if missing:
        print("       missing motion candidate refs: " + ", ".join(missing))

    videos = set(re.findall(r"static/videos/motionfix_\d+_135_blender\.(?:mp4|webm)", html))
    check(len(videos) >= 22, "motion candidate page has at least 22 local videos", errors)
    check(len(re.findall(r"data-motion-toggle", html)) >= 22, "motion candidate page has at least 22 play buttons", errors)
    check(len(re.findall(r"data-motion-slider", html)) >= 22, "motion candidate page has at least 22 scrub sliders", errors)
    check("M01-M22" in html, "motion candidate page exposes selection codes", errors)
    check(
        not re.search(r"exact-FCL|sim change|wrist mean distance|\d+\s*frames", html, flags=re.IGNORECASE),
        "motion candidate captions hide internal metrics",
        errors,
    )
    return html


def check_slider_script(site_root: Path, errors: list[str]) -> None:
    script = site_root / "static/js/index.js"
    check(script.is_file(), f"motion slider script exists: {script}", errors)
    if not script.is_file():
        return
    js = script.read_text(encoding="utf-8")
    check("data-motion-slider" in js, "motion slider JS binds sliders", errors)
    check("video.currentTime" in js and "slider.value" in js, "motion slider JS seeks video currentTime", errors)
    check("video.play().catch" in js and "togglePlayback" in js, "motion playback is user-triggered", errors)
    check("DOMContentLoaded" in js and "video.play().catch" in js and "toggle.addEventListener" in js, "motion autoplay is not used on load", errors)


def check_motion_aggregate(
    code_root: Path,
    html: str,
    expected_total: int,
    allow_partial: bool,
    errors: list[str],
) -> None:
    aggregate = code_root / "tmp/website_runs/selection/motion100_aggregate.json"
    check(aggregate.is_file(), f"motion aggregate exists: {aggregate}", errors)
    if not aggregate.is_file():
        return
    rows = json.loads(aggregate.read_text(encoding="utf-8"))
    complete = sum(1 for row in rows if row.get("status") == "complete")
    clean = sum(1 for row in rows if row.get("exact_collision_free") is True)
    full = len(rows) >= expected_total and complete >= expected_total
    message = (
        f"motion aggregate rows={len(rows)}/{expected_total}, "
        f"complete={complete}, exact-clean={clean}"
    )
    if full:
        ok(message)
    elif allow_partial:
        ok(message + " (partial allowed)")
    else:
        fail(message + " (full complete motion-100 required)", errors)

    candidate_report = code_root / "tmp/website_runs/selection/motion_website_candidates.json"
    check(candidate_report.is_file(), f"motion candidate report exists: {candidate_report}", errors)
    if candidate_report.is_file():
        report = json.loads(candidate_report.read_text(encoding="utf-8"))
        check(report.get("num_rows") == len(rows), "candidate report is fresh for current aggregate row count", errors)
        check(report.get("num_complete") == complete, "candidate report is fresh for current complete-output count", errors)
        if full:
            check(report.get("is_full_run") is True, "candidate report was generated from full motion-100", errors)
            referenced_stems = set(re.findall(r"static/videos/(motionfix_\d+_135)_blender\.(?:mp4|webm)", html))
            row_by_stem = {row.get("stem"): row for row in rows}
            contact_root = code_root / "tmp/website_runs/website_assets/motion_contacts_all"
            invalid: list[str] = []
            for stem in sorted(referenced_stems):
                row = row_by_stem.get(stem)
                summary_path = contact_root / f"{stem}_contact_summary.json"
                mask_path = contact_root / f"{stem}_contact_masks.npz"
                if row is None:
                    invalid.append(f"{stem}: missing aggregate row")
                    continue
                if row.get("exact_collision_free") is not True:
                    invalid.append(f"{stem}: optimized output is not exact-clean")
                if not summary_path.is_file():
                    invalid.append(f"{stem}: missing original contact summary")
                    continue
                if not mask_path.is_file():
                    invalid.append(f"{stem}: missing original contact mask")
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                if int(summary.get("num_collision_frames", 0)) <= 0:
                    invalid.append(f"{stem}: original has no TOPO=40 collision frames")
            check(
                not invalid,
                "referenced motion videos have exact-clean outputs and TOPO=40 original collision masks",
                errors,
            )
            if invalid:
                print("       invalid motion refs: " + "; ".join(invalid))
        elif allow_partial:
            ok("candidate report is partial, as expected for current run state")


def check_screenshots(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        check(path.is_file(), f"screenshot exists: {path}", errors)


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    html = load_html(args.site_root)
    check_static_refs(args.site_root, html, errors)
    check_required_content(html, errors)
    check_pose_candidate_page(args.site_root, errors)
    check_hwc_candidate_page(args.site_root, errors)
    motion_candidate_html = check_motion_candidate_page(args.site_root, errors)
    check_slider_script(args.site_root, errors)
    check_motion_aggregate(args.code_root, html + "\n" + motion_candidate_html, args.expected_motion_total, args.allow_partial_motion, errors)
    check_screenshots(args.screenshot, errors)
    if errors:
        print(f"\nValidation failed with {len(errors)} issue(s).")
        return 1
    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
