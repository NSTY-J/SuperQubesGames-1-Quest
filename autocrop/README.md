# Autocrop-Vertical Service

Smart video converter using YOLOv8 and FFmpeg to convert horizontal video to vertical 9:16 format for social media.

## Features

- **Content-Aware Cropping**: Uses YOLOv8 model to detect people and automatically centers the vertical frame on them
- **Automatic Letterboxing**: If multiple people are too far apart for a vertical crop, automatically adds black bars
- **Scene-by-Scene Processing**: All decisions are made per-scene for consistent editing
- **High Performance**: Processing offloaded to FFmpeg via direct pipe for fast encoding

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "autocrop"
}
```

### Convert Video
```
POST /convert
```

Request body:
```json
{
  "input_path": "/tmp/input.mp4",
  "output_path": "/tmp/output_vertical.mp4"
}
```

Response:
```json
{
  "success": true,
  "output_path": "/tmp/output_vertical.mp4",
  "message": "Video converted successfully",
  "log": "..."
}
```

## Technical Details

- **YOLOv8**: For person detection
- **PySceneDetect**: For scene cut detection
- **OpenCV**: For frame manipulation and face detection
- **FFmpeg**: For video encoding
- **Flask**: For HTTP API

## Credits

Based on [Autocrop-vertical](https://github.com/kamilstanuch/Autocrop-vertical) by Kamil Stanuch
