# Video Perception Pipeline

## Objective

Build a small video perception pipeline capable of:

- Video ingestion
- Frame sampling
- Object detection
- Temporal tracking
- Prediction export
- Visualization
- Evaluation

The goal is to process egocentric task videos and generate inspectable perception outputs that can later be reviewed by humans.

---

## Dataset

The assignment provides four candidate videos from different task categories.

| Video ID | Category               | Duration (s) | Primary Object |
| -------- | ---------------------- | -----------: | -------------- |
| 767223   | Cleaning               |        384.3 | Dishes         |
| 870855   | Laundry / Garment Care |        351.5 | Clothes        |
| 165895   | Food Preparation       |        349.8 | Wooden Spoon   |
| 839878   | Repair / Assembly      |        644.5 | Hairdryer      |

---

## Repository Structure

```text
video-perception-pipeline/
├── configs/
├── data/
│   ├── videos.json
│   └── video_manifest.md
├── docs/
│   └── Computer Vision _ Video Perception Take-Home.pdf
├── outputs/
│   ├── evaluation/
│   └── visualizations/
├── src/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Metadata Files

Dataset metadata:

```text
data/videos.json
data/video_manifest.md
```

Task description:

```text
docs/Computer Vision _ Video Perception Take-Home.pdf
```

---

## Planned Pipeline

```text
Video
  │
  ▼
Frame Sampling
  │
  ▼
Object Detection
  │
  ▼
Temporal Tracking
  │
  ▼
Prediction Export (JSONL)
  │
  ▼
Visualization
  │
  ▼
Evaluation
```

---

## Planned Outputs

```text
outputs/
├── frames/
├── predictions.jsonl
├── visualizations/
└── evaluation/
```

---

## Technology Stack

- Python 3.11+
- OpenCV
- NumPy
- Ultralytics YOLO
- ByteTrack
- Pandas
- Matplotlib
