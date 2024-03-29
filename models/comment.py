from models import Model
from models.user import User
# from models.weibo import Weibo


class Comment(Model):
    """
    评论类
    """
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    @classmethod
    def add(cls, form, user_id, weibo_id):
        c = Comment(form)
        c.user_id = user_id
        c.weibo_id = weibo_id
        c.save()
        return c

    # def weibo(self):
    #     from models.weibo import Weibo
    #     w = Weibo.find_by(id=self.weibo_id)
    #     return w
