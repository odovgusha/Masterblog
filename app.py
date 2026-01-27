from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)

@app.route('/add', methods=['GET', 'POST'])
@app.route('/add', methods=['GET', 'POST'])
def add():

    # If the user submitted the form
    if request.method == 'POST':


        posts = load_blog_posts()

        # Read form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')


        new_id = len(posts) + 1

        #new post
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }


        posts.append(new_post)
        save_blog_posts(posts)


        return redirect(url_for('index'))


    return render_template('add.html')

def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

def load_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=2)

if __name__ == '__main__':
    app.run(debug=True)

