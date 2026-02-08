from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)


def load_blog_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)


def save_blog_posts(posts):
    with open("blog_posts.json", "w") as file:
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

        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
        }

        posts.append(new_post)
        save_blog_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):

    posts = load_blog_posts()
    posts = [post for post in posts if post["id"] != post_id]

    save_blog_posts(posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):

    posts = load_blog_posts()

    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break

    if post is None:
        return "Post not found", 404

    if request.method == "POST":

        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")

        save_blog_posts(posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
