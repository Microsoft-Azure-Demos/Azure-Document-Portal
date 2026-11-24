import os
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB upload limit

STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "documents")



def get_container_client():
    if not STORAGE_ACCOUNT_NAME:
        raise RuntimeError("Set AZURE_STORAGE_ACCOUNT_NAME in your environment.")
    account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    service_client = BlobServiceClient(account_url=account_url, credential=credential)
    return service_client.get_container_client(CONTAINER_NAME)



@app.route("/", methods=["GET"])
def index():
    try:
        container_client = get_container_client()
        documents = sorted(container_client.list_blobs(), key=lambda blob: blob.name.lower())
        return render_template("index.html", documents=documents, container_name=CONTAINER_NAME)
    except Exception as exc:
        app.logger.exception("Unable to list blobs")
        flash(f"Storage connection error: {exc}", "error")
        return render_template("index.html", documents=[], container_name=CONTAINER_NAME), 500



@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file or not uploaded_file.filename:
        flash("Choose a file to upload.", "error")
        return redirect(url_for("index"))

    safe_name = secure_filename(uploaded_file.filename)
    if not safe_name:
        flash("That filename is not valid.", "error")
        return redirect(url_for("index"))

    try:
        container_client = get_container_client()
        blob_client = container_client.get_blob_client(safe_name)
        blob_client.upload_blob(uploaded_file.stream, overwrite=False)
        flash(f"Uploaded '{safe_name}' successfully.", "success")
    except Exception as exc:
        app.logger.exception("Upload failed")
        flash(f"Upload failed: {exc}", "error")
    return redirect(url_for("index"))



@app.route("/download/<path:blob_name>", methods=["GET"])
def download(blob_name):
    try:
        container_client = get_container_client()
        blob_client = container_client.get_blob_client(blob_name)
        data = blob_client.download_blob().readall()
        return send_file(
            BytesIO(data),
            as_attachment=True,
            download_name=os.path.basename(blob_name),
        )
    except Exception as exc:
        app.logger.exception("Download failed")
        flash(f"Download failed: {exc}", "error")
        return redirect(url_for("index"))



@app.route("/delete/<path:blob_name>", methods=["POST"])
def delete(blob_name):
    try:
        container_client = get_container_client()
        container_client.delete_blob(blob_name)
        flash(f"Deleted '{blob_name}'.", "success")
    except Exception as exc:
        app.logger.exception("Delete failed")
        flash(f"Delete failed: {exc}", "error")
    return redirect(url_for("index"))



@app.errorhandler(413)
def file_too_large(_error):
    flash("File is too large. The upload limit is 25 MB.", "error")
    return redirect(url_for("index")), 413



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
