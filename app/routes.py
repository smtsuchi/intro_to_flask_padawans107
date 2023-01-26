from app import app
from flask import render_template, request, redirect, url_for
from .forms import PostForm, SearchForm
from .models import Post, Likes, User
from flask_login import current_user, login_required
import requests
import os

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

@app.route('/')
def homePage():
    people = ['name', "Brandt", "Aubrey","Nicole"]
    text = "SENDING THIS FROM PYTHON!!!"
    return render_template('index.html', people = people, my_text = text )


@app.route('/contact')
def contactPage():
    users = User.query.all()
    if current_user.is_authenticated:
        who_i_am_following = {u.id for u in current_user.followed.all()}
        for user in users:
            if user.id in who_i_am_following:
                user.following = True
    return render_template('contact.html', users=users)






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
    # Finding likes base on User
    if current_user.is_authenticated:
        my_likes = Likes.query.filter_by(user_id=current_user.id).all()
        likes = {like.post_id for like in my_likes}

        for post in posts:
            if post.id in likes:
                post.liked = True
    #Find likes based on Post
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

@app.route('/posts/<int:post_id>/like', methods=["GET"])
@login_required
def likePost(post_id):
    like_instance = Likes(current_user.id, post_id)
    like_instance.saveToDB()    
    return redirect(url_for('getPosts'))

@app.route('/posts/<int:post_id>/unlike', methods=["GET"])
@login_required
def unlikePost(post_id):
    like_instance = Likes.query.filter_by(post_id=post_id).filter_by(user_id=current_user.id).first()
    like_instance.deleteFromDB()
    return redirect(url_for('getPosts'))


@app.route('/follow/<int:user_id>', methods=["GET"])
@login_required
def followUser(user_id):
    person = User.query.get(user_id)
    current_user.follow(person)
    return redirect(url_for('contactPage'))

@app.route('/unfollow/<int:user_id>', methods=["GET"])
@login_required
def unfollowUser(user_id):
    person = User.query.get(user_id)
    current_user.unfollow(person)
    return redirect(url_for('contactPage'))



@app.route('/news', methods = ["GET", "POST"])
def newsPage():
    my_form = SearchForm()
    
    if request.method == "POST":
        if my_form.validate():
            search_term = my_form.shoha.data
            url = f'https://newsapi.org/v2/everything?q={search_term}&apiKey={NEWS_API_KEY}&pageSize=20'
            result = requests.get(url)

            data = result.json()
            
            articles = data['articles']
            return render_template('news.html', html_form = my_form, articles = articles)

    return render_template('news.html', html_form = my_form)


@app.route('/test', methods = ["GET", "POST"])
def testFunction():
   
    
    
    posts = Post.query.all()
    posts = [p.to_dict() for p in posts]
    
    

    return render_template('test.html', posts=posts)

