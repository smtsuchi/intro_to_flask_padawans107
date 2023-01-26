from flask import Blueprint, request
from ..models import Post
from ..apiauthhelper import basic_auth_required, token_auth_required

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
@token_auth_required
def createPost(user):
    data = request.json

    title = data['title']
    caption = data['caption']
    img_url = data['img_url']

    ## for now, accept the user_id parameter from the JSON body
    ### HOWEVER, this is not the correct way, we need to authenticate them somehow
    #### we will cover this in BASIC/TOKEN auth

    post = Post(title, img_url, caption, user.id)
    post.saveToDB()
    
    return {
        'status': 'ok',
        'message': 'Succesfullly created post!'
    }

# @api.route('/api/posts/update/<post_id>', methods = ["POST"])
# @basic_auth_required
# def updatePost(user, post_id):
#     data = request.json

#     title = data['title']
#     caption = data['caption']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     post = Post(title, img_url, caption, user.id)
#     post.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly created post!'
#     }