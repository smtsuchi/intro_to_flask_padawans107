from flask import Blueprint, request
from ..models import Post

api = Blueprint('api', __name__)


@api.route('/api/posts')
def getPosts():
    posts = Post.query.all()

    new_posts = []
    for p in posts:
        new_posts.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(posts),
        'posts': [p.to_dict() for p in posts]
    }

@api.route('/api/posts/<int:post_id>')
def getPost(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'totalResults': 1,
            'post': 
            post.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'The post you are looking for does not exist.'
        }

@api.route('/api/posts/create', methods = ["POST"])
def createPost():
    data = request.json

    title = data['title']
    caption = data['caption']
    img_url = data['img_url']

    user_id = data['user_id']

    ## for now, accept the user_id parameter from the JSON body
    ### HOWEVER, this is not the correct way, we need to authenticate them somehow
    #### we will cover this in BASIC/TOKEN auth

    post = Post(title, img_url, caption, user_id)
    post.saveToDB()
    
    return {
        'status': 'ok',
        'message': 'Succesfullly created post!'
    }