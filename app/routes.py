from app import app
from flask import render_template, request, redirect, url_for
from .forms import PostForm
from .models import Post
from flask_login import current_user, login_required

@app.route('/')
def homePage():
    people = ['name', "Brandt", "Aubrey","Nicole"]
    text = "SENDING THIS FROM PYTHON!!!"
    return render_template('index.html', people = people, my_text = text )


@app.route('/contact')
def contactPage():
    return render_template('contact.html')







@app.route('/posts/create', methods=["GET","POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.data
            
            post = Post(title, img_url, caption, current_user.id)
            post.saveToDB()
    return render_template('createpost.html', form = form)


@app.route('/posts', methods=["GET"])
def getPosts():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)



@app.route('/posts/<int:post_id>', methods=["GET"])
def getPost(post_id):
    post = Post.query.get(post_id)
    return render_template('singlepost.html', post=post)

@app.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def updatePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        return redirect(url_for('getPosts'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title=form.title.data
            img_url=form.img_url.data
            caption=form.caption.data
            post.title = title
            post.img_url = img_url
            post.caption = caption
            post.saveChanges()
            return redirect(url_for('getPost', post_id=post.id))
    return render_template('updatepost.html', post=post, form= form)


@app.route('/posts/<int:post_id>/delete', methods=["GET"])
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        return redirect(url_for('getPosts'))

    post.deleteFromDB()
    
    
    return redirect(url_for('getPosts'))