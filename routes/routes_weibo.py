from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    Template,
    current_user,
    html_response,
    login_required,
    json_response)
from utils import log


def index(request):
    """
    weibo 首页的路由函数
    """
    u = current_user(request)
    weibos = Weibo.find_all(user_id=u.id)
    body = Template.render('weibo_index.html', weibos=weibos, user=u)
    return html_response(body)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    return redirect('/weibo/index')


def delete(request):
    """
    用于删除 weibo 的路由函数
    """
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    """
    用于编辑 weibo 的路由函数
    """
    weibo_id = int(request.query['id'])
    w = Weibo.find_by(id=weibo_id)
    body = Template.render('weibo_edit.html', weibo=w)
    return html_response(body)


def update(request):
    """
    用于更新 weibo 的路由函数
    """
    form = request.form()
    weibo_id = int(form['id'])
    content = form['content']
    Weibo.update(weibo_id, content=content)
    return redirect('/weibo/index')


def same_user_required(route_function):
    """
    验证同一用户
    """
    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def comment_add(request):
    """
    用于增加 comment 的路由函数
    """
    u = current_user(request)
    form = request.form()
    weibo = Weibo.find_by(id=int(form['weibo_id']))
    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo.id
    c.save()
    log('comment add', c, u, form)
    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    """
    用于判断是否微博所属用户
    """
    def f(request):
        u = current_user(request)
        if request.method == 'GET':
            weibo_id = request.query['id']
        else:
            form = request.json()
            weibo_id = form['id']
        w = Weibo.find_by(id=int(weibo_id))
        if w.user_id == u.id:
            return route_function(request)
        else:
            d = dict(
                verify="权限不足"
            )
            return json_response(d)
    return f


def comment_owner_required(route_function):
    """
    用于判断是否评论所属用户
    """
    def f(request):
        u = current_user(request)
        # 拿到评论的 ID
        if request.method == 'GET':
            comment_id = request.query['id']
        else:
            form = request.json()
            comment_id = form['id']
        c = Comment.find_by(id=int(comment_id))
        # 拿到所属微博的 ID，然后再拿到微博所属用户
        weibo_id = c.weibo_id
        w = Weibo.find_by(id=int(weibo_id))
        # 判断是否 评论的所属用户 或 微博的所属用户
        if (c.user_id == u.id) or (w.user_id == u.id):
            return route_function(request)
        else:
            d = dict(
                verify="权限不足"
            )
            return json_response(d)
    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(same_user_required(delete)),
        '/weibo/edit': login_required(same_user_required(edit)),
        '/weibo/update': login_required(same_user_required(update)),
        '/weibo/index': login_required(index),
        '/comment/add': login_required(comment_add),
    }
    return d
