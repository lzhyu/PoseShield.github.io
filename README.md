# PoseShield Project Website

This repository contains the static GitHub Pages website for:

**PoseShield: Neural Collision Fields for Human Self-Collision Resolution**

The site is built as a Nerfies-style academic project page and is intended to
host the paper overview, teaser, pose examples, human motion examples, Humans
with Collisions data examples, pose-level quantitative plots, limitations,
resources, and BibTeX.

## Local Preview

Serve the repository root with any static file server, for example:

```bash
python -m http.server 8012
```

Then open `http://127.0.0.1:8012/`.

## Main Local Inputs

- Website plan and acceptance notes: `WEBSITE_PLAN.md`
- Code and generated assets repo:
  `/group/bera89/data/li5280/project/code-release-verify/PoseShield`
- Static website assets:
  - `static/images/pose_examples/`
  - `static/images/hwc_examples/`
  - `static/images/plots/`
  - `static/videos/`

## Validation

The lightweight static validation helper checks local asset references,
required sections, generated example counts, motion-100 coverage, and visual
review screenshot artifacts:

```bash
python tools/validate_site.py --screenshot /tmp/desktop.png --screenshot /tmp/mobile.png
```

During partial motion-100 runs, use `--allow-partial-motion`. Final acceptance
should run without that flag after the full motion-100 aggregate and candidate
report are regenerated.

## Citation

```bibtex
@article{li2026poseshield,
  title={PoseShield: Neural Collision Fields for Human Self-Collision Resolution},
  author={Li, Zhengyuan and Deng, Zeyun and Shen, Yifan and Gui, Liangyan and Xie, Miaolan and Campbell, Joseph and Gao, Xifeng and Wu, Kui and Pan, Zherong and Bera, Aniket},
  journal={arXiv preprint arXiv:2606.29686},
  year={2026}
}
```

## Template Credit And License

This project page is adapted from the
[Nerfies website template](https://nerfies.github.io/).

Website content and assets are managed for the PoseShield project. Template
materials inherited from Nerfies are provided under the Creative Commons
Attribution-ShareAlike 4.0 International License.
