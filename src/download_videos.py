from pathlib import Path
import json
import requests
import cv2
from tqdm import tqdm


# Repository root directory
REPO_ROOT = Path(__file__).resolve().parents[1]

# Input metadata file provided by the assignment
VIDEOS_JSON = REPO_ROOT / "data" / "videos.json"

# Directory where downloaded videos will be stored
OUTPUT_DIR = REPO_ROOT / "data" / "videos"


def load_videos():
    """
    Load video metadata from videos.json.

    Returns:
        list: List of video metadata dictionaries.
    """
    with open(VIDEOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        videos = data.get("videos", [])
    else:
        videos = data

    return videos


def get_video_id(video):
    """
    Extract a video identifier.
    """
    return str(
        video.get("video_id")
        or video.get("id")
        or video.get("clip_id")
    )


def get_video_url(video):
    """
    Extract the download URL from the Miraxis metadata.
    """
    return (
        video.get("video_download_url")
        or video.get("preview_download_url")
        or video.get("download_url")
        or video.get("preview_url")
        or video.get("url")
        or video.get("video_url")
    )


def download_file(url, output_path):
    """
    Download a video file from the given URL.
    """
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(output_path, "wb") as f:
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=output_path.name,
        ) as progress:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))


def validate_video(video_id, path):
    """
    Validate that OpenCV can open the downloaded video.
    """
    cap = cv2.VideoCapture(str(path))

    if not cap.isOpened():
        raise RuntimeError(
            f"OpenCV could not open video: {path}"
        )

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Duration in seconds
    duration = frame_count / fps if fps and fps > 0 else 0.0

    cap.release()

    return {
        "video_id": video_id,
        "path": str(path),
        "fps": round(fps, 2),
        "frame_count": frame_count,
        "duration": round(duration, 2),
    }


def main():
    """
    Main pipeline:

    1. Create output directory.
    2. Load video metadata.
    3. Download videos if missing.
    4. Validate videos with OpenCV.
    5. Print validation summary.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    videos = load_videos()

    results = []

    for video in videos:
        video_id = get_video_id(video)
        url = get_video_url(video)

        # Skip malformed entries
        if not video_id:
            print(
                f"Skipping video with missing ID: {video}"
            )
            continue

        # Skip entries without a valid URL
        if not url:
            print(
                f"Skipping {video_id}: "
                "no download or preview URL found"
            )
            continue

        output_path = OUTPUT_DIR / f"{video_id}.mp4"

        # Avoid downloading the same file twice
        if output_path.exists():
            print(
                f"Already downloaded: {output_path}"
            )
        else:
            print(
                f"Downloading {video_id} from {url}"
            )
            download_file(url, output_path)

        # Validate downloaded video
        result = validate_video(
            video_id,
            output_path
        )

        results.append(result)

    # Required Step 3 output format
    print("\nvideo_id,path,fps,frame_count,duration")

    for r in results:
        print(
            f"{r['video_id']},"
            f"{r['path']},"
            f"{r['fps']},"
            f"{r['frame_count']},"
            f"{r['duration']}"
        )


if __name__ == "__main__":
    main()