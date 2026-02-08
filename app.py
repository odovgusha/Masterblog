from flask import Flask, render_template, redirect, url_for, request
import json
import os

app = Flask(__name__)

DATA_FILE = "blog_posts.json"

def load_blog_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save posts
def save_blog_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=2)

@app.route("/")
def index():
    posts = load_blog_posts()
    return render_template("index.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_blog_posts()
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        # Unique ID
        new_id = max([post["id"] for post in posts], default=0) + 1

        posts.append({
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        })

        save_blog_posts(posts)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_blog_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_blog_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_blog_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_blog_posts(posts)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
