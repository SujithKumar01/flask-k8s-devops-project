from flask import Flask, render_template, request, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

notes = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", notes=notes)


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()

    results = []
    if query:
        results = [
            note for note in notes
            if query in note["title"].lower()
            or query in note["content"].lower()
        ]

    return render_template("search.html", notes=results, query=query)


@app.route("/add", methods=["POST"])
def add_note():
    global next_id

    title = request.form.get("title")
    content = request.form.get("content")

    if title and content:
        notes.append({
            "id": next_id,
            "title": title,
            "content": content
        })
        next_id += 1

    return redirect(url_for("index"))


@app.route("/edit/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    title = request.form.get("title")
    content = request.form.get("content")

    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["content"] = content
            break

    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    global notes
    notes = [note for note in notes if note["id"] != note_id]
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)