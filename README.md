# Video Perception Pipeline

## Table of Contents

- [Video Perception Pipeline](#video-perception-pipeline)
  - [Table of Contents](#table-of-contents)
  - [1. Project Overview](#1-project-overview)
  - [2. Problem Understanding](#2-problem-understanding)
  - [3. Selected Videos](#3-selected-videos)
  - [4. Methodology](#4-methodology)
    - [Video Download and Validation](#video-download-and-validation)
    - [Frame Sampling](#frame-sampling)
    - [Object Detection](#object-detection)
    - [Temporal Tracking](#temporal-tracking)
    - [Prediction Export](#prediction-export)
    - [Visualization](#visualization)
    - [Evaluation](#evaluation)
  - [5. Pipeline Architecture](#5-pipeline-architecture)
  - [6. Tracking Logic](#6-tracking-logic)
  - [7. Evaluation Methodology](#7-evaluation-methodology)
  - [8. Reviewer Feedback Loop](#8-reviewer-feedback-loop)
  - [9. Bounded Improvement](#9-bounded-improvement)
  - [10. Results and Analysis](#10-results-and-analysis)
  - [11. Failure Analysis](#11-failure-analysis)
  - [12. Assumptions](#12-assumptions)
  - [13. Limitations](#13-limitations)
  - [14. Future Work](#14-future-work)
  - [15. Repository Structure](#15-repository-structure)
  - [16. Environment Setup](#16-environment-setup)
  - [17. Reproduction Steps](#17-reproduction-steps)
  - [18. Outputs](#18-outputs)
  - [19. Conclusion](#19-conclusion)

## 1. Project Overview

This project implements a lightweight video perception pipeline for egocentric task videos. The pipeline ingests selected videos, samples frames, applies baseline object detection, associates detections over time, exports structured predictions, generates visualizations, and evaluates the results against a small human-reviewed subset.

## 2. Problem Understanding

Video perception extends object detection into the temporal domain. The objective is not only to detect objects in individual frames but also to maintain consistent object identities over time and produce outputs that can be reviewed and evaluated.

## 3. Selected Videos

| Video ID | Category          | Target Object |
| -------- | ----------------- | ------------- |
| 165895   | Food Preparation  | Wooden Spoon  |
| 839878   | Repair / Assembly | Hairdryer     |

Reasons for selection:

- Object manipulation
- Hand interactions
- Partial occlusions
- Object re-entry
- Viewpoint changes
- Temporal reasoning challenges

## 4. Methodology

### Video Download and Validation

Videos are downloaded and validated before processing.

### Frame Sampling

One frame is sampled every second.

Timestamp computation:

```text
timestamp_sec = original_frame_index / fps
```

### Object Detection

YOLOv8n (Ultralytics) is used as the baseline detector.

### Temporal Tracking

A custom IoU-based tracker associates detections across frames.

### Prediction Export

Predictions are exported to:

```text
outputs/predictions.jsonl
```

### Visualization

Annotated visualizations are generated for inspection.

### Evaluation

Evaluation is performed on a manually reviewed frame subset.

## 5. Pipeline Architecture

```text
Video
  ↓
Frame Sampling
  ↓
YOLOv8n Detection
  ↓
IoU Tracking
  ↓
Prediction Export
  ↓
Visualization + Evaluation
```

## 6. Tracking Logic

1. Load detections.
2. Compare with active tracks.
3. Match by class.
4. Compute IoU.
5. Associate if threshold passes.
6. Create new track otherwise.
7. Allow limited missed frames.
8. Close expired tracks.

## 7. Evaluation Methodology

Metrics:

- Precision
- Recall
- False positives
- Missed detections
- Track fragmentation
- ID switches

## 8. Reviewer Feedback Loop

Simulated reviewer feedback focuses on:

- Missed detections
- Occlusions
- Track fragmentation
- Viewpoint changes
- Re-entry failures

## 9. Bounded Improvement

Very small detections are removed before tracking and export.

Observed outcome:

- Removes low-value detections.
- Reduces clutter.
- Evaluation changes very little.
- Demonstrates workflow rather than major performance gains.

## 10. Results and Analysis

The pipeline successfully produces detections, tracks, visualizations, exports, and evaluation artifacts. Performance remains limited because the detector is not specialized for the selected target objects.

## 11. Failure Analysis

Observed failure modes:

- Missed detections
- Occlusions
- Track fragmentation
- Viewpoint changes
- Re-entry failures

## 12. Assumptions

- One frame per second is sufficient.
- Generic YOLOv8n is acceptable as a baseline.
- IoU tracking is sufficient for demonstration.
- Small evaluation subset is acceptable for analysis.

## 13. Limitations

- YOLOv8n is not specialized for wooden spoons or hairdryers.
- Occlusions remain difficult.
- IoU-only tracking is fragile.
- No appearance-based re-identification.
- No segmentation.
- Small evaluation subset.

## 14. Future Work

- Appearance embeddings
- DeepSORT / ByteTrack
- CLIP or DINO embeddings
- Segment Anything
- Open-vocabulary detection
- Larger evaluation set

## 15. Repository Structure

```text
video-perception-pipeline/
├── configs/
├── data/
├── docs/
├── outputs/
├── src/
├── README.md
├── requirements.txt
└── .gitignore
```

## 16. Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 17. Reproduction Steps

```bash
python3 src/download_videos.py
python3 src/sample_frames.py
python3 src/run_baseline_detection.py
python3 src/track_detections.py
python3 src/export_predictions_jsonl.py
python3 src/generate_visualizations.py
python3 src/evaluate_predictions.py
```

## 18. Outputs

```text
outputs/frames/
outputs/detections/
outputs/predictions.jsonl
outputs/visualizations/
outputs/evaluation/
```

## 19. Conclusion

This project demonstrates a complete lightweight video perception workflow including ingestion, detection, tracking, export, visualization, evaluation, reviewer feedback, and bounded improvement. The pipeline serves as a reproducible baseline and highlights opportunities for future improvements in detection and tracking quality.
