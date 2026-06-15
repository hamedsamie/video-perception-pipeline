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
    - [Detection Performance](#detection-performance)
    - [Tracking Performance](#tracking-performance)
    - [Interpretation](#interpretation)
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

Manual labels were created through visual inspection of a subset of sampled frames. A target object was considered present when it was visually identifiable in the frame, including cases where the object was partially visible or partially occluded. Because visibility judgments can be subjective in ambiguous frames, the resulting metrics should be interpreted as approximate indicators of performance rather than definitive benchmark measurements.

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

The pipeline successfully completed frame sampling, object detection, temporal tracking, prediction export, visualization generation, and evaluation.

### Detection Performance

Evaluation was performed on a manually reviewed subset containing 100 annotated target-object instances.

| Metric            | Value |
| ----------------- | ----: |
| True Positives    |     6 |
| False Positives   |     0 |
| Missed Detections |    94 |
| Precision         |  1.00 |
| Recall            |  0.06 |

No target-object false positives were observed within the manually reviewed subset, resulting in a measured precision of 1.00. However, this metric only reflects evaluation of the selected target objects and should not be interpreted as overall detector precision. Visual inspection showed that the detector occasionally produced incorrect detections for non-target classes.

Recall remained very low, with most target-object instances not detected by the baseline model. The detector therefore behaved conservatively: it generated few target-object false positives but frequently failed to detect the target object when it was present.

The dominant failure mode was missed detections rather than incorrect target-object detections.

### Tracking Performance

| Video ID | Target Object | Track Fragmentation | ID Switches |
| -------- | ------------- | ------------------: | ----------: |
| 165895   | Wooden Spoon  |                   4 |           4 |
| 839878   | Hairdryer     |                   0 |           0 |

Tracking quality varied between the two selected videos.

The wooden spoon sequence produced multiple track fragmentations and identity switches. These failures were caused by intermittent detections, partial occlusions, object motion, and viewpoint changes. When detections disappeared and later reappeared, the IoU-based tracker frequently created a new track instead of reconnecting the object to its previous identity.

The hairdryer sequence exhibited more stable tracking behavior within the reviewed subset and did not produce fragmentation or identity-switch events.

### Interpretation

The evaluation suggests that the primary limitation of the pipeline is object detection rather than track association.

Because the tracker relies on incoming detections, missed detections directly reduce tracking quality. Sparse detections lead to fragmented tracks and unstable identities, even when the tracking logic itself behaves correctly.

The results are consistent with expectations for a lightweight baseline built using a generic YOLOv8n detector and a simple IoU-based tracker.

## 11. Failure Analysis

Observed failure modes:

- Missed detections
- Occlusions
- Track fragmentation
- Viewpoint changes
- Re-entry failures

The selected target objects frequently appear under challenging conditions such as hand occlusion, motion blur, partial visibility, and changing viewpoints. These conditions reduce detector confidence and contribute directly to tracking instability.

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
- Manual annotations were not independently validated and may contain subjective judgments in ambiguous frames.
- Simulated reviewer feedback provides qualitative observations rather than definitive explanations of detector failures.

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
python3 src/run_tracking.py
python3 src/export_predictions_jsonl.py
python3 src/visualize_predictions.py
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

This project demonstrates a complete lightweight video perception workflow including video ingestion, frame sampling, object detection, temporal tracking, prediction export, visualization, evaluation, reviewer feedback, and bounded improvement.

The evaluation highlighted several challenges associated with the selected videos, particularly missed detections, occlusions, viewpoint changes, and tracking instability. While the baseline detector successfully identified some target-object instances, many remained undetected, which in turn affected tracking performance.

The reported metrics and reviewer observations provide a useful indication of system behavior, although they are based on a relatively small manually reviewed subset and should be interpreted accordingly.

Overall, the project establishes a reproducible baseline pipeline and demonstrates an end-to-end evaluation and improvement workflow. The results also highlight several directions for future work, including stronger object representations, appearance-based tracking, segmentation, and larger-scale evaluation.
