import os.path

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log

import random
import json


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class Template:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=xxx
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': url,
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers, 302)
    r = header + '\r\n'
    return r.encode()


def html_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data, headers=None):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    """
    验证用户
    """
    def f(request):
        log('login_required')
        u = current_user(request)
        if u.is_guest():
            # d = dict(
            #     verify="游客用户"
            # )
            # return json_response(d)
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('登录用户', route_function)
            return route_function(request)

    return f
