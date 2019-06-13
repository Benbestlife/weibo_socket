from routes.routes_weibo import (
    weibo_owner_required,
    comment_owner_required,
)
from routes import (
    json_response,
    current_user,
    login_required,
)
from models.weibo import Weibo
from models.comment import Comment


def all(request):
    weibos = Weibo.all_json()
    for w in weibos:
        weibo_id = w['id']
        comment = Comment.find_all(weibo_id=weibo_id)
        c = [c.json() for c in comment]
        w['comments'] = c
        # user_id = w['user_id']
        # user = User.find_by(id=user_id)
        # uname = user.username
        # w['user'] = uname
    return json_response(weibos)


def add(request):
    form = request.json()
    u = current_user(request)
    t = Weibo.add(form, u.id)
    return json_response(t.json())


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    comments = Comment.find_all(weibo_id=weibo_id)
    for c in comments:
        c_id = c.id
        Comment.delete(c_id)
    d = dict(
        message="成功删除 weibo"
    )
    return json_response(d)


def update(request):
    form: dict = request.json()
    weibo_id = int(form.pop('id'))
    t = Weibo.update(weibo_id, **form)
    return json_response(t.json())


def comment_add(request):
    form = request.json()
    u = current_user(request)
    weibo_id = int(form.pop('weibo_id'))
    c = Comment.add(form, u.id, weibo_id)
    return json_response(c.json())


def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除评论"
    )
    return json_response(d)


def comment_update(request):
    form = request.json()
    comment_id = int(form.pop('id'))
    c = Comment.update(comment_id, **form)
    return json_response(c.json())


def route_dict():
    d = {
        '/api/weibo/all': login_required(all),
        '/api/weibo/add': login_required(add),
        '/api/weibo/delete': login_required(weibo_owner_required(delete)),
        '/api/weibo/update': login_required(weibo_owner_required(update)),
        '/api/comment/add': login_required(comment_add),
        '/api/comment/delete': login_required(comment_owner_required(comment_delete)),
        '/api/comment/update': login_required(comment_owner_required(comment_update)),
    }
    return d
