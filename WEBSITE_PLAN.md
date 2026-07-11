# PoseShield Project Website Plan

This document tracks design direction, source links, asset provenance, and
implementation notes for the PoseShield project website.

## Repositories

- Website repo: https://github.com/lzhyu/PoseShield.github.io
- Code repo: https://github.com/lzhyu/PoseShield
- Local website checkout: `/group/bera89/data/li5280/project/code-release-verify/PoseShield.github.io`
- Local code checkout: `/group/bera89/data/li5280/project/code-release-verify/PoseShield`
- Possible local asset/source fallback:
  `/group/bera89/data/li5280/project/code-release/PoseShield`

## Paper Metadata

- Title: PoseShield: Neural Collision Fields for Human Self-Collision Resolution
- Venue: ECCV 2026
- arXiv: https://arxiv.org/abs/2606.29686
- arXiv status checked: v2, last revised 2026-07-01
- Paper source files:
  https://drive.google.com/file/d/1meYYIs_ag3L3DfOspiSHUFSPemYc5LtL/view?usp=sharing
- Authors: Zhengyuan Li, Zeyun Deng, Yifan Shen, Liangyan Gui, Miaolan Xie,
  Joseph Campbell, Xifeng Gao, Kui Wu, Zherong Pan, Aniket Bera
- Institutions:
  - Purdue University
  - LightSpeed Studios
  - University of Illinois Urbana-Champaign

## Citation

```bibtex
@article{li2026poseshield,
  title={PoseShield: Neural Collision Fields for Human Self-Collision Resolution},
  author={Li, Zhengyuan and Deng, Zeyun and Shen, Yifan and Gui, Liangyan and Xie, Miaolan and Campbell, Joseph and Gao, Xifeng and Wu, Kui and Pan, Zherong and Bera, Aniket},
  journal={arXiv preprint arXiv:2606.29686},
  year={2026}
}
```

## Visual And Design Direction

Primary style target: Nerfies-style academic project page.

Reference:
- Website: https://nerfies.github.io/
- Source: https://github.com/nerfies/nerfies.github.io

Design principles:
- Keep the familiar computer vision paper page structure: title, authors,
  institution line, resource buttons, large teaser, abstract, method, results,
  BibTeX.
- Preserve the clean Bulma/Nerfies rhythm already present in this repo.
- Replace Nerfies content fully and remove the original Google Analytics tag.
- Keep a footer acknowledgement for the Nerfies template, as requested by the
  original template license note.
- Make the first viewport immediately communicate the problem: input human
  poses/motions contain self-collisions; PoseShield repairs them post-hoc.
- Prefer visual before/after evidence over decorative design.

Color semantics:
- Red means colliding / self-collision present.
- Green means collision-free / self-collision resolved.
- Apply this consistently across pose examples, human motion examples, HwC data
  examples, captions, overlays, legends, and quantitative charts.
- Avoid reusing red or green for unrelated categories so the visual language
  stays unambiguous.

## Current Implementation Checkpoint

2026-07-11 candidate and contact-visualization pass:

- Pose Examples now have a separate `pose_candidates.html` preview page with 15
  local GLB before/after candidates. Use the stable page codes `P01-P15` when
  selecting final homepage examples.
- The six homepage pose viewers reuse the same GLB/poster style as the
  candidate page. The current homepage selection is `P15`, `P13`, `P11`,
  `P07`, `P09`, and `P10`; the remaining pose examples stay available on the
  candidate page. Red is the colliding input, green is the PoseShield output.
- Collision marking is implemented as a yellow surface patch on the red input
  mesh from precomputed contact vertex sets. Current pose/HwC GLBs use a
  3-ring surface expansion and no floating sphere markers.
- HwC now has a separate `hwc_candidates.html` preview page with 20 local GLB
  candidates: `HC01-HC10` for red self-colliding samples and `HF01-HF10` for
  green collision-free samples. The export ranks for readable upright bodies
  and uses a simple pose-space diversity heuristic before selecting samples.
- The homepage HwC section remains concise but links to the 20-candidate page
  for manual selection.
- Human Motion Examples now use twelve local WebM video candidates with custom
  Play buttons and scrub sliders. They do not autoplay or loop. The render
  style follows the provided reference video's clean grey/white studio setting
  while preserving the website's red/green semantics.
- Motion examples must be selected from original sequences with at least one
  exact self-collision frame. "Clean" applies only to the optimized green
  PoseShield result, not to the red input sequence.
- Motion contact highlighting must use precomputed exact original-motion
  contact masks exported with the repo's `deps/distances.pkl` topology filter.
  A temporary low-threshold renderer produced false-positive yellow regions on
  legs and must not be used for final website videos.
- Motion videos should show the natural sequence from the beginning rather than
  cropping to the most visibly colliding interval; yellow contact patches appear
  only on frames where the exact mask contains contact faces.
- Earlier motion review renders used aggressive frame sampling for quick
  iteration; final website candidates should follow the current exact-mask
  rendering pass below.
- Current motion selection pass uses twelve 960x540 WebM videos rendered from
  the start of each sequence with stride-3 sampling, TOPO=40 exact contact
  masks on the red input, and no yellow overlay on the green output:
  `motionfix_005317_135`, `motionfix_005348_135`, `motionfix_004448_135`,
  `motionfix_005315_135`, `motionfix_002395_135`, and
  `motionfix_005350_135`, plus `motionfix_005454_135`,
  `motionfix_005406_135`, `motionfix_005718_135`,
  `motionfix_005652_135`, `motionfix_005334_135`, and
  `motionfix_005859_135`. Each referenced original has at least one TOPO=40
  self-collision frame, and each optimized output is exact-clean. Candidate
  visual sheet: `/tmp/poseshield_motion_12_candidates_sheet.jpg`.
- Follow-up Motion-20 pass keeps those twelve videos on the homepage and adds a
  separate `motion_candidates.html` page for `M01-M20`. The eight added
  candidates are:
  `motionfix_005355_135`, `motionfix_005403_135`,
  `motionfix_005398_135`, `motionfix_006076_135`,
  `motionfix_005424_135`, `motionfix_005399_135`,
  `motionfix_004450_135`, and `motionfix_005610_135`. Selection priority is:
  TOPO=40 exact original contact plus exact-clean optimized output first,
  visual diversity second, then marker visibility and motion preservation.
- Follow-up exact-FCL diagnosis found that `motionfix_004422_135` and
  `motionfix_005783_135` were incorrectly summarized as clean because contact
  collection was capped before TOPO=40 pairs appeared. After raising the contact
  cap, both originals have TOPO=40 collision frames and are added to
  `motion_candidates.html` as M21 and M22.
- Homepage motion selection was later narrowed to six reader-facing examples:
  M02 (`motionfix_005348_135`), M11 (`motionfix_005334_135`), M17
  (`motionfix_005424_135`), M18 (`motionfix_005399_135`), M21
  (`motionfix_004422_135`), and M22 (`motionfix_005783_135`). M06, M08, and
  M14 were removed after visual review.
- M11 was re-exported with a larger `num_max_contacts=5_000_000` cap and
  frame-stride-3 processing to match the displayed website video frames. The
  old M11 mask had a raw contact-face maximum of 87 per frame; the fixed export
  reaches 1028, confirming that the earlier visualization was contact-list
  truncated before the TOPO=40 filter saw the full contact set.
- Pose and HwC viewer assets were also regenerated after the same contact-cap
  fix. The export script now uses `num_max_contacts=1_000_000` for pose/HwC
  exact-FCL contact faces, and the current P01-P15 order was re-exported
  explicitly to avoid drifting from the manually reviewed candidate page.
- M12 (`motionfix_005859_135`) and M16 (`motionfix_006076_135`) are now used as
  failure cases: they satisfy the collision-resolution evidence requirement,
  but the optimized green motion changes the apparent action semantics more
  than desired.
- Follow-up diagnostics found that older visually pleasing candidates
  `motionfix_004422_135` and `motionfix_005783_135` do contain TOPO=40
  original self-collisions. Their earlier zero-frame contact summaries were an
  export bug: `self_collision_contact_faces()` capped FCL contacts at 20k, so
  near-topology contacts filled the result before far-topology contacts were
  returned. The helper now uses the same 1,000,000 contact cap as exact-FCL for
  standard website exports, with the M11 audit using 5,000,000 contacts.
- Motion clips may still show visually close hand/body or limb/body regions
  without a yellow patch in some frames. This is expected under the final
  website rule:
  yellow is drawn only where the precomputed original-motion mask has FCL
  contact with penetration greater than `1e-6` and topological face distance at
  least 40. Near contact, screen-space overlap, or visually plausible contact is
  not manually painted.
- Homepage Pose Examples currently show only the final local 3D before/after
  viewer for the selected `P15`, `P13`, `P11`, `P07`, `P09`, and `P10` poses.
  Optimization-path GIFs were removed from the homepage at user request; any
  trajectory assets should remain auxiliary unless explicitly reintroduced.
- Homepage captions are reader-facing visual descriptions. Internal ids,
  exact-FCL status, similarity deltas, wrist distances, and frame counts should
  remain in reports/plan files, not in the public demo captions.

## Project-Specific Story

Core message:

PoseShield is a generator-agnostic, post-hoc self-collision resolver for
SMPL-H poses and human motion sequences. It uses a neural collision field in
pose space as a differentiable constraint, enabling collision repair without
retraining or knowing the upstream pose/motion generator.

Important claims to surface:
- Neural collision field defined directly in SMPL pose space.
- Eikonal-style regularization for stable gradients near the collision boundary.
- Works for single poses and motion sequences.
- Post-hoc and generator-agnostic.
- Reported 95.8% success rate on the constructed SMPL pose benchmark.

## Required Content Sections

These sections should be treated as required for the first complete website
draft.

1. Pose Examples
   - Goal: show single-pose self-collision repair.
   - Required source run: run collision resolution on the pose test set, then
     select website examples from those resolved test-set outputs.
   - Suggested layout: side-by-side "Input" and "PoseShield" panels, plus a
     short rendered optimization trajectory GIF for each example.
   - Render pose examples with Blender rather than relying only on raw HTML or
     screenshot outputs.
   - During pose solving, record the collision-resolution trajectory so each
     final example can show how the pose moves from colliding to resolved.
   - Emphasize colliding regions visually when available.
   - Include 3-6 examples so the page demonstrates robustness across different
     body configurations.

2. Human Motion Examples
   - Goal: show temporal self-collision repair on full human motion sequences.
   - Required source run: run collision resolution on the motion-100 set, then
     select website examples from those resolved motion outputs.
   - Suggested layout: before/after videos or GIFs in a carousel or compact
     grid.
   - Show that PoseShield removes collisions while preserving the original
     action, hand motion, and global dynamics.
   - Generation/selection plan:
     - Run the current default motion-resolution algorithm.
     - Use exact-FCL validation to filter for examples where collisions are
       fully or nearly fully resolved.
     - Rank candidates by high similarity/preservation to the source motion.
     - Use VLM-assisted visual screening to choose examples that are clean,
       attractive, easy to understand, and free of obvious artifacts.
   - If the intended section name is "Human Examples" rather than "Human Motion
     Examples", keep the visual content motion-focused and use the shorter
     label on the page.

3. HwC Data Examples
   - Goal: explain and visually sample the Humans with Collisions dataset.
   - Suggested layout: a small dataset strip with Blender-rendered colliding
     pose samples, collision-free counterparts or labels if available, and a
     concise caption.
   - Render pose dataset examples with Blender for visual consistency with the
     Pose Examples section.
   - Mention that part of the source data comes from MotionFix:
     https://motionfix.is.tue.mpg.de/
   - Include dataset scale/splits only if final numbers are ready; otherwise
     link to the release assets and README.

Additional sections that are strongly recommended:

4. Main Teaser
   - A large first-screen visual combining the most persuasive pose and motion
     before/after example.
   - This is separate from the detailed example sections; it should make the
     contribution obvious within a few seconds.

5. Method Overview
   - Use `assets/pipeline.png`.
   - Keep it short and visual: neural collision field, Eikonal regularization,
     post-hoc optimization.

6. Pose-Level Evaluation
   - Scope: pose-level results only.
   - Do not use a table for the main presentation.
   - Prefer a compact bar chart or similar visual summary for success rate and
     any key pose-level metric selected from the paper.
   - Also consider one small visual about correlation/trade-off if the final
     data is available:
     - Correlation plot: learned collision-field score or constraint status vs.
       exact-FCL collision-free outcome / collision severity.
     - Trade-off plot: collision-resolution success vs. pose preservation,
       pose change, or similarity under different thresholds/cost weights.
   - These plots should be figure-like and intuitive, not dense tables.
   - This should support the demos without turning the page into a full paper.

7. Failure Cases / Limitations
   - A short, honest section can increase credibility.
   - Useful especially because body-shape generalization and non-neutral SMPL-H
     assumptions are important limitations.
   - Follow the paper wording closely.
   - Mention that we tried SAField / adding shape condition, and that adding
     shape conditioning seems feasible rather than fundamentally difficult.
   - Do not present SAField as a standalone demo section in the first public
     website version.

## Asset Sources

From code repo:
- Main teaser candidate: `assets/PoseShield_demo.gif`
- Pipeline figure: `assets/pipeline.png`
- Experimental SAField image:
  `assets/safield_experimental_shape_demo_blender.png` for possible limitations
  context only, not as a dedicated demo section.
- Public SAField text links to:
  `https://github.com/lzhyu/PoseShield/tree/main/experimental/safield_demo`.
- Additional generated examples can be produced later from scripts under:
  - `demos/demo_pose.py`
  - `demos/demo_motion.sh`
  - `tools/generate_motion_html.py`
  - `tools/render_motion_blender.py`
  - `tools/blender_render.py`

Institution logos:
- Borrow Purdue and UIUC logos from the SimMotionEdit project page:
  https://lzhyu.github.io/SimMotionEdit.github.io/
- That page includes visible Purdue University and University of Illinois logo
  assets. Copy or recreate local static image assets later instead of hotlinking.
- Tencent/LightSpeed logo candidate:
  - Original local asset: `static/images/logos/tencent_logo_original.png`
  - Upscaled local asset: `static/images/logos/tencent_logo_4x.png`
  - Use only if the institution/logo row should include the Tencent or
    LightSpeed affiliation visually.

External resource buttons:
- Paper/arXiv: https://arxiv.org/abs/2606.29686
- Code: https://github.com/lzhyu/PoseShield
- Model/checkpoints: https://huggingface.co/ZYYY99/PoseShield
- Website: https://github.com/lzhyu/PoseShield.github.io

Required run assets:
- Before running pose test-set or motion-100 resolution, run
  `python tools/check_assets.py` in the code repo.
- First try to reuse available checkpoints/data from the local fallback path:
  `/group/bera89/data/li5280/project/code-release/PoseShield`.
- If required assets are missing locally, download the release packages specified
  in the PoseShield README from the PoseShield Google Drive folder:
  - `PoseShield_release_dependencies_20260628.zip`
  - `PoseShield_release_pose_data_20260628.zip`
  - `PoseShield_release_motion_data_20260708.zip`
- Required for pose examples:
  - `ckpts/poseshield/model.pth`
  - `ckpts/poseshield/config.yaml`
  - `data/dataset_test/` benchmark files
- Required for motion examples:
  - `data/motion_canonical/motionfix_*_135.npy` motion-100 files
  - motion collision field / HY-Motion assets checked by `tools/check_assets.py`

## Current Implementation Status

Updated 2026-07-10:

- Pose500 run completed under the code repo:
  `tmp/website_runs/pose_test_full/pose_test_full.log`
  - Parsed samples: 500
  - Exact-FCL collision-free outputs: 417 / 500
  - Exact-FCL collision-free rate: 83.4%
  - Solver success rate: 45.4%
  - Learned-field constraint satisfied rate: 27.4%
- Pose candidate visual screening notes:
  `tmp/website_runs/selection/visual_screening_notes.md`
- Pose examples exported with recorded SLSQP trajectories:
  `tmp/website_runs/website_assets/pose_examples/`
- Current website draft:
  - Uses the PoseShield teaser GIF.
  - Uses local Purdue, Tencent, and UIUC logos.
  - Uses the pipeline figure from the code repo.
  - Uses six local GLB-backed `<model-viewer>` cards in the Pose Examples
    section, with no visible static preview overlay.
  - Blender-rendered trajectory GIFs remain available under
    `static/images/pose_examples/` but are not shown on the homepage draft.
  - Uses no-shadow Blender-rendered motion MP4 files copied to
    `static/videos/`. The videos use Standard Blender color management,
    stronger opaque red/green materials, and 5 fps playback, with a custom
    timeline slider below each video for time scrubbing.
  - Uses one pose-only quantitative plot under `static/images/plots/`; the
    current plot removes the classifier baseline and does not include the
    previous paper-table / MVD annotation.
  - Uses a six-card local GLB-backed `<model-viewer>` HwC gallery with three
    red colliding samples and three green collision-free samples, with no
    visible static preview overlay.
  - The HwC section now states release-level dataset scale from the local data
    split: 1,489,294 labeled SMPL-H poses across train/test raw release files,
    with a nearly balanced colliding / collision-free mix.
  - Pose-Level Evaluation was redesigned on 2026-07-10 to use values from the
    paper source table `tables/result_merged.tex`: PoseShield reaches HwC SCC
    0.958, PDR 0.982, and MVD 0.059, compared with the strongest baseline
    COAP at SCC 0.446, PDR 0.832, and MVD 0.106.
  - The weighted-distance ablation plot was removed from the homepage after
    visual review; the Pose-Level Evaluation now keeps only the main pose
    resolution-rate figure.
  - Pose trajectory GIFs were slowed from 120 ms/frame to 210 ms/frame and kept
    as reusable assets, but the homepage now shows only the clearer red/green
    before-after render for each pose.
  - Human Motion Examples are now a vertical gallery with reader-facing visual
    captions. Internal sample ids, exact-FCL status, similarity change, frame
    counts, and wrist distances are kept out of the page text.
  - HwC examples were re-exported as local 3D viewers using
    `tools/export_hwc_viewer_assets.py`; the homepage now relies on the GLB
    viewers directly rather than the rendered poster images.
- Completed website asset updates:
  - Six selected pose examples now have visible Blender trajectory GIFs:
    `pose_379`, `pose_074`, `pose_352`, `pose_288`, `pose_057`,
    `pose_207`.
  - HwC data examples are exported from three `label = -1` colliding frames
    and three `label = 1` collision-free frames in the HwC test split. The
    selected files/frames are recorded in
    `static/images/hwc_examples/hwc_viewer_examples.json`.
  - Browser-native 3D viewer exploration:
    - There is no true browser-native HTML element for SMPL/GLB mesh viewing
      comparable to `<img>` or `<video>`.
    - Practical GitHub Pages options are `<model-viewer>` or Three.js, but both
      require JavaScript and exported GLB/OBJ assets; they are feasible if we
      decide to vendor the dependency and export curated meshes.
    - The site now uses `<model-viewer>` with a locally vendored JS module at
      `static/js/model-viewer.min.js`, so the page does not depend on a runtime
      CDN fetch for the viewer code.
    - The six homepage pose examples each have a local GLB exported from the
      selected pose example's red `input.obj` and green `resolved.obj`.
    - The homepage viewer cards now load the local GLB directly, without a
      static overlay that hides the interactive viewer.
- Current motion100 status:
  - Final aggregation found 100 stage2 outputs, 100 complete exact-FCL outputs,
    and 87 exact collision-free outputs.
  - Original motion100 array `13368002` and retry array `13378374` are complete.
  - Retry array `13378374` reran original indices 75, 80, and 82
    (`motionfix_005652_135`, `motionfix_005737_135`,
    `motionfix_005764_135`), which previously failed immediately with
    CUDA-busy errors and left empty stage2 directories. All three retry tasks
    completed and filled the missing stage2 and exact-FCL outputs.
  - Task 81 wrote a valid exact-FCL JSON but remained colliding
    (76 / 120 collision frames), so it is complete but not a clean website
    candidate. Task 85 also wrote a valid exact-FCL JSON but remained colliding
    (8 / 90 collision frames), so it is complete but not a clean website
    candidate. Task 84 finished exact-FCL cleanly
    (`motionfix_005783_135`, 0 / 121 collision frames) and is now counted as a
    clean complete output. Task 86 also finished exact-FCL cleanly
    (`motionfix_005859_135`, 0 / 120 collision frames). Task 87 finished
    exact-FCL cleanly (`motionfix_005867_135`, 0 / 120 collision frames), while
    task 88 wrote a valid but collided exact-FCL JSON
    (`motionfix_005945_135`, 27 / 90 collision frames). Task 89 finished
    exact-FCL cleanly (`motionfix_005998_135`, 0 / 90 collision frames). Task
    90 finished exact-FCL cleanly (`motionfix_005999_135`, 0 / 120 collision
    frames). Tasks 91 and 92 also finished exact-FCL cleanly
    (`motionfix_006003_135`, 0 / 119 collision frames;
    `motionfix_006004_135`, 0 / 120 collision frames). Tasks 94 and 95 finished
    exact-FCL cleanly (`motionfix_006008_135`, 0 / 90 collision frames;
    `motionfix_006074_135`, 0 / 90 collision frames). Task 93 finished
    exact-FCL cleanly (`motionfix_006006_135`, 0 / 119 collision frames).
    Task 96 finished exact-FCL cleanly (`motionfix_006076_135`,
    0 / 120 collision frames). Task 98 finished exact-FCL cleanly
    (`motionfix_007540_135`, 0 / 90 collision frames).
    Task 97 finished exact-FCL cleanly (`motionfix_006080_135`,
    0 / 120 collision frames). Original task 99 wrote a valid collided
    exact-FCL JSON (`motionfix_007768_135`, 109 / 120 collision frames). Retry
    task 75 finished exact-FCL cleanly (`motionfix_005652_135`,
    0 / 90 collision frames). Retry tasks 80 and 82 also finished exact-FCL
    cleanly (`motionfix_005737_135`, 0 / 120 collision frames;
    `motionfix_005764_135`, 0 / 119 collision frames).
  - Full motion100 completion is now satisfied; final motion examples have been
    selected from the full exact-FCL clean candidate report.
  - Some Slurm array tasks may be marked failed because strict exact-FCL
    validation raises an error after writing `exact_fcl_results.json` when
    collisions remain. These are valid collided outputs for aggregation, not
    missing infrastructure runs, as long as the final exact-FCL JSON exists.
  - `tools/evaluate_exact_fcl.py` now supports
    `--allow-collisions-exit-zero`, and the motion100 Slurm script uses it for
    future/retry website production runs so collided samples are recorded
    without making the task fail.
  - Final completion evidence: aggregate reached 100 motion rows and
    100 complete exact-FCL outputs, with fresh full-run candidate selection
    generated from the full aggregate.
- Motion website candidate prefilter:
  - `tools/select_motion_website_examples.py` ranks complete exact-FCL clean
    motion outputs by preservation metrics and a light diversity heuristic.
  - Current final reports:
    `tmp/website_runs/selection/motion_website_candidates.json` and
    `tmp/website_runs/selection/motion_website_candidates.md`.
  - The report records `is_full_run: true`.
  - Final top-three candidates are `motionfix_004425_135`,
    `motionfix_005303_135`, and `motionfix_004524_135`; all three have local
    Blender GIFs and are referenced by the website motion gallery.
- Local preview server:
  - No long-running preview server is currently required; start a temporary
    `python -m http.server` from the website repo when taking fresh screenshots.
- Visual validation performed with headless Firefox screenshots:
  - `/tmp/poseshield_home_desktop.png`
  - `/tmp/poseshield_home_desktop_v2.png`
  - `/tmp/poseshield_home_desktop_v3.png`
  - `/tmp/poseshield_home_mobile.png`
  - `/tmp/poseshield_home_desktop_full.png`
  - `/tmp/poseshield_home_mobile_full2.png`
  - `/tmp/poseshield_home_desktop_motion004425.png`
  - `/tmp/poseshield_home_desktop_motion004425_004524.png`
  - `/tmp/poseshield_home_desktop_motion_top3_grid_v2.png`
  - `/tmp/poseshield_home_mobile_motion_top3_v2.png`
  - `/tmp/poseshield_review_desktop_final_hwc.png`
  - `/tmp/poseshield_review_mobile_final_hwc.png`
  - Final validator command:
    `python tools/validate_site.py --screenshot /tmp/poseshield_review_desktop_final_hwc.png --screenshot /tmp/poseshield_review_mobile_final_hwc.png`
  - Final validation passed after checking local refs, six pose GLB viewers,
    six HwC GLB viewers, motion MP4 videos, no weighted-distance plot, no internal
    motion metrics in captions, full motion-100 aggregate/candidate freshness,
    and the two final browser screenshots.
  - `/tmp/poseshield_home_desktop_quant_width.png`
  - `/tmp/poseshield_home_mobile_quant_width.png`
  - `/tmp/poseshield_home_desktop_resources.png`
  - `/tmp/poseshield_home_mobile_resources.png`
  - Current desktop and real 390px mobile screenshots show no obvious overlap,
    missing local assets, or horizontal overflow after the pose trajectory and
    HwC grid updates.
- Static acceptance helper:
  - `tools/validate_site.py` checks required page sections, local static asset
    references, local CSS `url(...)` references, pose/motion/HwC visual counts,
    BibTeX, MotionFix/SAField text, motion aggregate coverage,
    candidate-report freshness, and screenshot files.
  - Current interim command passed with partial motion explicitly allowed:
    `python tools/validate_site.py --allow-partial-motion --screenshot /tmp/poseshield_home_desktop_motion004425_004524.png --screenshot /tmp/poseshield_home_mobile_full2.png`
  - A later interim run also passed with:
    `/tmp/poseshield_home_desktop_motion_top3_grid_v2.png` and
    `/tmp/poseshield_home_mobile_motion_top3_v2.png`.
  - Browser request-log review after removing the unused Font Awesome CSS link
    showed no remaining local static 404s from missing webfont files.
  - Latest interim static validation on 2026-07-10 passed with
    `--allow-partial-motion`; the motion gate reported 90 aggregate rows,
    81 complete exact-FCL outputs, and 71 exact-clean outputs.
  - Later interim validations passed after refreshing to 46 aggregate rows,
    40 complete exact-FCL outputs, and 34 exact-clean outputs; 47 aggregate
    rows, 41 complete exact-FCL outputs, and 35 exact-clean outputs; 48
    aggregate rows, 42 complete exact-FCL outputs, and 36 exact-clean outputs;
    and 51 aggregate rows, 45 complete exact-FCL outputs, and 39 exact-clean
    outputs; and 52 aggregate rows, 46 complete exact-FCL outputs, and
    40 exact-clean outputs; and 55 aggregate rows, 49 complete exact-FCL
    outputs, and 43 exact-clean outputs; and 57 aggregate rows,
    51 complete exact-FCL outputs, and 45 exact-clean outputs; and
    60 aggregate rows, 54 complete exact-FCL outputs, and 48 exact-clean
    outputs; and 61 aggregate rows, 55 complete exact-FCL outputs, and
    49 exact-clean outputs; and 63 aggregate rows, 57 complete exact-FCL
    outputs, and 51 exact-clean outputs; and 67 aggregate rows,
    61 complete exact-FCL outputs, and 55 exact-clean outputs; and
    69 aggregate rows, 63 complete exact-FCL outputs, and 56 exact-clean
    outputs; and 72 aggregate rows, 66 complete exact-FCL outputs, and
    58 exact-clean outputs; and 75 aggregate rows, 69 complete exact-FCL
    outputs, and 61 exact-clean outputs; and 78 aggregate rows,
    72 complete exact-FCL outputs, and 64 exact-clean outputs; and
    79 aggregate rows, 72 complete exact-FCL outputs, and 64 exact-clean
    outputs.
  - The 90-row / 81-complete interim validation still requires
    `--allow-partial-motion`; it is not final acceptance evidence.
  - The latest screenshot review also motivated a small CSS update so
    quantitative plots fill their columns on desktop and mobile.
  - A Resources section was added after limitations and visually checked on
    desktop and mobile; `tools/validate_site.py` now checks the section and
    links to code, models, data assets, and the website repository.
  - Final acceptance must run the same script without `--allow-partial-motion`
    after motion-100 reaches the expected 100 rows.
  - Latest full static validation on 2026-07-10 passed without
    `--allow-partial-motion`:
    `python tools/validate_site.py`.
    The check confirmed 37 local static refs, all required sections, all
    pose/motion/HwC assets, resource links, BibTeX, motion aggregate
    rows=100/100, complete=100, exact-clean=87, fresh full-run candidate report,
    and referenced motion GIFs coming from selected exact-clean candidates.
  - Final validation with screenshot existence checks also passed:
    `python tools/validate_site.py --screenshot /home/li5280/poseshield_home_desktop_current.png --screenshot /home/li5280/poseshield_home_desktop_tall_current.png --screenshot /home/li5280/poseshield_home_mobile_current.png`.
  - Fresh headless Firefox screenshots were generated after starting the local
    preview server with escalation:
    - `/home/li5280/poseshield_home_desktop_current.png`
    - `/home/li5280/poseshield_home_desktop_tall_current.png`
    - `/home/li5280/poseshield_home_mobile_current.png`
  - Visual review of the screenshots found the header/logos, teaser, method,
    pose cards, vertical motion examples, and larger HwC examples readable with
    no obvious overlap or horizontal overflow. Updated plot assets and HwC
    renders were also inspected directly with `view_image`.
  - After adding the 3D viewer, the local GLB and local model-viewer JS are
    both validated by `tools/validate_site.py`. Headless Firefox screenshots
    are useful for layout but may not render WebGL/model-viewer content.
  - Final static acceptance passed without `--allow-partial-motion`:
    `python tools/validate_site.py --screenshot /tmp/poseshield_home_desktop_motion_top3_grid_v2.png --screenshot /tmp/poseshield_home_mobile_motion_top3_v2.png`
    The motion gate reported 100 aggregate rows, 100 complete exact-FCL
    outputs, 87 exact-clean outputs, a full-run candidate report, and verified
    that the referenced motion GIFs come from the full-run exact-clean
    candidate report.
  - A final VLM-style visual review of the desktop and 390px mobile screenshots
    found the page readable and visually coherent, with no obvious overlap,
    missing local assets, or horizontal overflow.
  - Follow-up visual review on 2026-07-10 was triggered by concerns that the
    previous check was too static and did not sufficiently judge aesthetics.
    Revisions from that review:
    - Removed the prediction-accuracy style quantitative plot. This interim
      pass briefly used a weighted-distance SCC/MVD ablation, which was later
      removed from the homepage during the pose-viewer credibility pass.
    - Enlarged the Pose Examples gallery with a wider dedicated container and
      clearer red/green before-after render assets.
    - Added a screenshot-visible poster overlay to the local GLB viewer; the
      overlay fades on hover/focus so the locally hosted `<model-viewer>` scene
      remains interactive on GitHub Pages.
    - Reduced the mobile 3D viewer height so the poster no longer floats in a
      large blank frame.
  - Latest full-page visual review artifacts:
    - `/home/li5280/poseshield_review_desktop_full_v1.png`
    - `/home/li5280/poseshield_review_mobile_full_v1.png`
    - Asset-level plot review also inspected
      `static/images/plots/pose_resolution_rates.png` and
      `static/images/plots/pose_correlation_tradeoff.png`.
  - Latest final validation with screenshot existence checks passed:
    `python tools/validate_site.py --screenshot /home/li5280/poseshield_review_desktop_full_v1.png --screenshot /home/li5280/poseshield_review_mobile_full_v1.png`
  - Remaining polish note: the single quantitative plot is coherent on desktop
    but still small on a 390px mobile screenshot. A future pass could add a
    mobile-specific simplified plot image if mobile chart readability becomes a
    priority.
  - Pose viewer credibility pass on 2026-07-10:
    - Removed the weighted-distance plot from the homepage entirely.
    - Replaced the static Pose Examples gallery and standalone 3D viewer with
      six local GLB-backed pose viewer cards:
      `pose_379`, `pose_074`, `pose_352`, `pose_288`, `pose_057`, `pose_207`.
    - Rewrote motion captions as visual descriptions and added validator checks
      that reject `exact-FCL`, `sim change`, `wrist mean distance`, and
      frame-count wording in page text.
    - Re-rendered the three motion GIFs with softer no-shadow Blender lighting
      and no GIF dithering, which removed most visible shadow speckling.
    - Latest visual review screenshots:
      `/home/li5280/poseshield_review_desktop_poseviewers_v1.png` and
      `/home/li5280/poseshield_review_mobile_poseviewers_v1.png`.
    - Latest validation command:
      `python tools/validate_site.py --screenshot /home/li5280/poseshield_review_desktop_poseviewers_v1.png --screenshot /home/li5280/poseshield_review_mobile_poseviewers_v1.png`
- Blender dependency:
  - Downloaded portable Blender 4.2.11 LTS to
    `/tmp/blender-4.2.11-linux-x64/blender`
  - Verified Blender-rendered motion GIF generation.
  - System `ffmpeg` is unavailable in the current shell. Motion video output
    now falls back to OpenCV `VideoWriter` MP4 encoding in
    `tools/render_motion_blender.py` after Blender renders PNG frames.

Open polish items:

- Optionally add mobile-specific simplified quantitative plot assets if chart
  label readability on narrow phones becomes important.
- Optionally convert the teaser GIF and repeated GIF demos to compressed video
  assets later if page weight becomes a problem.

## Proposed Page Structure

1. Hero / metadata
   - Title, venue, author list, institution line, optional institution logos.
   - Buttons: Paper, arXiv, Code, Hugging Face, Data/Assets if desired.

2. Teaser
   - Use a large before/after motion or pose visual.
   - Use the existing `PoseShield_demo.gif` from the code repo for the initial
     website teaser.
   - If possible, convert GIF to compressed MP4/WebM for page performance.

3. One-sentence subtitle
   - Example draft: "PoseShield repairs self-colliding SMPL-H poses and
     motions as a post-hoc optimization step, without retraining the upstream
     generator."

4. Abstract
   - Adapt from the arXiv abstract.
   - Keep concise; avoid burying the visual result.

5. Method
   - Use `pipeline.png`.
   - Explain in three short blocks:
     - Learn a neural collision field in pose space.
     - Use Eikonal regularization for stable optimization.
     - Optimize poses or motion latents to preserve semantics while removing
       self-collisions.

6. Demo / Results
   - Pose Examples: single-pose collision resolution gallery.
   - Human Motion Examples: full-motion collision resolution gallery.
   - HwC Data Examples: visual samples from the Humans with Collisions dataset.
   - Favor side-by-side "Input" vs "Resolved" videos/images.
   - Use carousel only when each item is visually strong; otherwise use a grid.

7. Quantitative Results
   - Pose-level only.
   - Use a compact bar chart or visual metric summary rather than a table.
   - Highlight 95.8% success rate if aligned with the final paper wording.
   - Data source: use the paper results and existing result/log files in the
     project directories; rerun only if a needed plot value is missing.
   - Candidate visualizations:
     - Success-rate bar chart comparing PoseShield with baselines.
     - Correlation scatter/strip plot showing how the learned collision-field
       decision relates to exact-FCL validation.
     - Trade-off curve or grouped bars showing collision removal vs. pose
       preservation/similarity.
   - Keep the red/green semantics: red for colliding/failure, green for
     collision-free/success.

8. Resources
   - Link code repo, model/checkpoint release, and asset download locations.
   - Keep heavy data off GitHub Pages; link to Hugging Face, Google Drive, or
     GitHub Releases as appropriate.

9. BibTeX
   - Use the citation recorded above unless a final proceedings BibTeX replaces
     the arXiv entry later.

10. Acknowledgements / template credit
   - Credit Nerfies template.
   - Add institution/funding acknowledgements if needed.

## GitHub Pages Constraints

- GitHub Pages is static hosting for HTML, CSS, and JavaScript.
- Do not rely on backend inference or server-side rendering.
- Keep the published site under GitHub Pages size limits; avoid committing
  large videos directly when YouTube, Hugging Face, Google Drive, or Releases
  would be better.
- Prefer optimized MP4/WebM over large GIF files for repeated demos.
- Current website repo already uses a static Nerfies/Bulma template, which is
  suitable for GitHub Pages.
- Hosting decision: keep the main website assets locally hosted in this repo.
  This includes the teaser, selected pose/motion/HwC examples, generated plots,
  and institution logos. External links can still be used for full datasets,
  checkpoints, and supplementary large releases.

## Acceptance Criteria

- The website must be reviewed visually before delivery, not just checked for
  successful HTML loading.
- Use VLM-assisted review and/or other visual inspection tools on screenshots
  from representative desktop and mobile viewports.
- Repeat review after meaningful layout or asset changes until the page is:
  - visually coherent and aesthetically polished;
  - consistent with the Nerfies-style academic project-page direction;
  - complete with all required sections: teaser, pose examples, human motion
    examples, HwC data examples, method overview, pose-only quantitative
    visualization, limitations, resources, and BibTeX;
  - consistent in red/green collision semantics;
  - free of obvious text overflow, broken images/videos, awkward cropping,
    overlapping UI, or inconsistent spacing;
  - clear enough that a first-time reader understands the before/after
    collision-resolution story without reading the full paper.
- VLM/visual-review notes should feed back into revisions rather than being a
  one-time final check.
- Current visual baseline: match the clean Pose Examples studio style across
  Pose, Human Motion, and HwC sections: light gray/white background, clear
  red/green opaque subjects, restrained shadows, and consistent card spacing.
- Final review artifacts for the latest visual pass:
  `/tmp/poseshield_review_desktop_video_viewer_v6.png` and
  `/tmp/poseshield_review_mobile_video_viewer_v6.png`.

## Implementation Checklist

- [x] Replace README content so it describes PoseShield instead of Nerfies.
- [x] Remove original Nerfies Google Analytics snippet from `index.html`.
- [x] Replace page title, metadata, authors, institutions, and resource links.
- [x] Copy selected assets from the code repo into `static/images` or
  `static/videos`.
- [x] Remove unused Nerfies template media/assets after replacing all page
  references, so the GitHub Pages repo does not carry unnecessary large files.
- [x] Add Purdue/UIUC logo assets locally.
- [x] Build hero teaser using PoseShield before/after visual.
- [x] Use `PoseShield_demo.gif` as the first teaser asset.
- [x] Replace carousel/demo sections with PoseShield pose examples, human
  motion examples, and HwC data examples.
- [x] Run collision resolution on the pose test set and select pose examples
  from the resolved test-set outputs.
- [x] Select final specific pose, motion, and HwC examples autonomously, prioritizing
  visual diversity, clean collision resolution, consistent rendering style, and
  publication-quality appearance.
- [x] For pose examples, record optimization trajectories and export 6 local
  red/green GLB before-after scenes for homepage `<model-viewer>` cards.
  Viewer fallback posters are locally rendered in the same studio style and are
  used only for loading/no-WebGL cases.
- [x] For HwC data examples, export 6 local GLB viewer samples, including 3
  colliding red examples and 3 collision-free green examples, and add the
  MotionFix source-data note.
- [x] For human motion examples, run the default algorithm, filter with
  exact-FCL, require the red original sequence to contain self-collision,
  rank by similarity/preservation, and use VLM-assisted visual screening for
  final selection.
- [x] Run collision resolution on the motion-100 set and select motion examples
  from the resolved motion-100 outputs.
- [x] Replace abstract and method text.
- [x] Add pose-only quantitative chart.
- [x] Keep the pose-level quantitative snapshot focused on the main resolution
  plot and remove the weighted-distance ablation from the homepage.
- [x] Remove the classifier baseline and paper-table annotation from the
  quantitative snapshot.
- [x] Replace homepage motion GIFs with local WebM videos and custom scrub
  sliders.
- [x] Add failure/limitations section, including the SAField/shape-condition
  note, without making SAField a demo section.
- [x] Add Resources section with links to code, models, data assets, and the
  website repository.
- [x] Add BibTeX from this plan to `index.html`.
- [x] Verify locally in browser and check mobile layout.
- [x] Use VLM-assisted and/or visual screenshot review repeatedly until layout,
  style, and content completeness meet the acceptance criteria.
- [x] Validate static resources, viewer counts, video references, hidden
  internal motion metrics, fallback poster paths, and slider seek logic with
  `python tools/validate_site.py --screenshot /tmp/poseshield_review_desktop_video_viewer_v6.png --screenshot /tmp/poseshield_review_mobile_video_viewer_v6.png`.
- [x] Align the final Pose/HwC viewer default angles after visual review:
  `pose_288` uses a 45-degree initial orbit while the other pose examples keep
  the cleaner 0-degree front/three-quarter view; HwC uses one sample per card
  with per-sample initial orbits selected from rendered yaw contact sheets.
- [x] Re-render HwC fallback posters with the Pose-card studio style and a
  wider camera distance so the prone samples are not cropped; final visual
  review used `/tmp/poseshield_review_desktop_orient_v3_full.png`,
  `/tmp/poseshield_review_mobile_orient_v3_full.png`, and
  `/tmp/hwc_final_fallback_sheet_v4.jpg`.
- [x] Re-align Human Motion Examples with the original PoseShield repository
  teaser style instead of the earlier plain studio render: local WebM examples
  now use the README-style red/green bodies, perspective checkerboard floor,
  light gray background, and stronger scene depth while retaining the custom
  Play/scrub controls. Visual review used
  `/tmp/poseshield_motion_readme_style_sheet.jpg`.
- [x] HTTP-check representative local GLB and WebM resources from the preview
  server.
- [ ] Push to `lzhyu/PoseShield.github.io` after review.

## Open Questions

- Should LightSpeed Studios also have a logo in the institution row?
- Should the site use the arXiv BibTeX for now, or later switch to the ECCV
  proceedings BibTeX once available?

## Example Selection Policy

- Pose, motion, and HwC examples will be selected by the implementer rather than
  predetermined manually.
- Pose examples must be selected from the resolved pose test set.
- Motion examples must be selected from the resolved motion-100 set.
- Prioritize diversity across body configurations, contact types, action types,
  and collision severity.
- Keep the visual style unified: same camera convention, similar lighting,
  consistent red/green collision semantics, and comparable crop/scale.
- Prefer examples where collisions are clearly visible before resolution and
  visually clean after resolution.
- For motion examples, combine exact-FCL filtering, similarity/preservation
  scores, and VLM-assisted visual screening.
- VLM screening should judge visual cleanliness, aesthetic quality, temporal
  smoothness, absence of obvious artifacts, and whether the before/after story
  is easy to understand.
