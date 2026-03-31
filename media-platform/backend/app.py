"""Flask application – multimedia processing platform backend."""

import os
import datetime
import threading
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from db import get_db, init_db
from processors import (
    process_image, process_audio, process_video,
    IMAGE_FORMATS, AUDIO_FORMATS, VIDEO_FORMATS,
    UPLOAD_DIR, OUTPUT_DIR, ensure_dirs,
    MAX_ERROR_LENGTH,
)

app = Flask(__name__)
CORS(app)

MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

ensure_dirs()
init_db()


# ─── Helper ───────────────────────────────────────────────────────

def _save_upload(file_storage):
    """Save an uploaded file and return its path + original filename."""
    filename = secure_filename(file_storage.filename) or "untitled"
    dest = os.path.join(UPLOAD_DIR, filename)
    # Avoid overwriting: add a timestamp suffix
    if os.path.exists(dest):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{int(datetime.datetime.now().timestamp())}{ext}"
        dest = os.path.join(UPLOAD_DIR, filename)
    file_storage.save(dest)
    return dest, filename


def _create_task(filename, media_type, operation, input_path, output_format, quality=None):
    """Insert a new task row and return its id."""
    conn = get_db()
    file_size = os.path.getsize(input_path)
    cur = conn.execute(
        """INSERT INTO tasks
           (filename, media_type, operation, status, input_path, output_format, quality, file_size_before)
           VALUES (?, ?, ?, 'processing', ?, ?, ?, ?)""",
        (filename, media_type, operation, input_path, output_format, quality, file_size),
    )
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return task_id


def _complete_task(task_id, output_path):
    conn = get_db()
    file_size = os.path.getsize(output_path)
    conn.execute(
        """UPDATE tasks SET status='completed', output_path=?, file_size_after=?,
           completed_at=CURRENT_TIMESTAMP WHERE id=?""",
        (output_path, file_size, task_id),
    )
    conn.commit()
    conn.close()


def _fail_task(task_id, error_msg):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET status='failed', error_message=? WHERE id=?",
        (str(error_msg)[:MAX_ERROR_LENGTH], task_id),
    )
    conn.commit()
    conn.close()


def _task_to_dict(row):
    return {
        "id": row["id"],
        "filename": row["filename"],
        "mediaType": row["media_type"],
        "operation": row["operation"],
        "status": row["status"],
        "outputFormat": row["output_format"],
        "quality": row["quality"],
        "fileSizeBefore": row["file_size_before"],
        "fileSizeAfter": row["file_size_after"],
        "createdAt": row["created_at"],
        "completedAt": row["completed_at"],
        "errorMessage": row["error_message"],
    }


# ─── Routes ───────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/formats", methods=["GET"])
def formats():
    return jsonify({
        "image": IMAGE_FORMATS,
        "audio": AUDIO_FORMATS,
        "video": VIDEO_FORMATS,
    })


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    return jsonify([_task_to_dict(r) for r in rows])


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(_task_to_dict(row))


@app.route("/api/process/image", methods=["POST"])
def process_image_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    output_format = request.form.get("format", "jpg")
    quality = int(request.form.get("quality", 85))
    operation = request.form.get("operation", "convert")

    if output_format not in IMAGE_FORMATS:
        return jsonify({"error": f"Unsupported format: {output_format}"}), 400

    input_path, filename = _save_upload(file)
    task_id = _create_task(filename, "image", operation, input_path, output_format, quality)

    try:
        output_path = process_image(input_path, output_format, quality, operation)
        _complete_task(task_id, output_path)
    except Exception as e:
        _fail_task(task_id, e)
        return jsonify({"error": str(e)}), 500

    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify(_task_to_dict(row))


@app.route("/api/process/audio", methods=["POST"])
def process_audio_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    output_format = request.form.get("format", "mp3")
    bitrate = request.form.get("bitrate", "128k")
    operation = request.form.get("operation", "convert")

    if output_format not in AUDIO_FORMATS:
        return jsonify({"error": f"Unsupported format: {output_format}"}), 400

    input_path, filename = _save_upload(file)
    task_id = _create_task(filename, "audio", operation, input_path, output_format)

    def _run(task_id=task_id, input_path=input_path, output_format=output_format,
             bitrate=bitrate, operation=operation):
        try:
            output_path = process_audio(input_path, output_format, bitrate, operation)
            _complete_task(task_id, output_path)
        except Exception as e:
            _fail_task(task_id, e)

    threading.Thread(target=_run, daemon=True).start()

    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify(_task_to_dict(row)), 202


@app.route("/api/process/video", methods=["POST"])
def process_video_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    output_format = request.form.get("format", "mp4")
    crf = int(request.form.get("crf", 28))
    resolution = request.form.get("resolution", "")
    operation = request.form.get("operation", "convert")

    if output_format not in VIDEO_FORMATS:
        return jsonify({"error": f"Unsupported format: {output_format}"}), 400

    input_path, filename = _save_upload(file)
    task_id = _create_task(filename, "video", operation, input_path, output_format, crf)

    def _run(task_id=task_id, input_path=input_path, output_format=output_format,
             crf=crf, resolution=resolution, operation=operation):
        try:
            output_path = process_video(input_path, output_format, crf, resolution or None, operation)
            _complete_task(task_id, output_path)
        except Exception as e:
            _fail_task(task_id, e)

    threading.Thread(target=_run, daemon=True).start()

    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    return jsonify(_task_to_dict(row)), 202


@app.route("/api/download/<int:task_id>", methods=["GET"])
def download(task_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Task not found"}), 404
    if row["status"] != "completed":
        return jsonify({"error": "Task not completed"}), 400
    if not row["output_path"] or not os.path.exists(row["output_path"]):
        return jsonify({"error": "Output file not found"}), 404
    return send_file(row["output_path"], as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
