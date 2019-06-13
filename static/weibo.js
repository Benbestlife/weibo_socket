// 微博 API
// 获取所有微博
var apiWeiboAll = function(callback) {
    var path = `/api/weibo/all`
    ajax('GET', path, '', callback)
}

// 增加微博
var apiWeiboAdd = function(form, callback) {
    var path = `/api/weibo/add`
    ajax('POST', path, form, callback)
}

// 删除微博
var apiWeiboDelete = function(weiboId, callback) {
    var path = `/api/weibo/delete?id=${weiboId}`
    ajax('GET', path, '', callback)
}

// 更新微博
var apiWeiboUpdate = function(form, callback) {
    var path = `/api/weibo/update`
    ajax('POST', path, form, callback)
}

// 增加评论
var apiCommentAdd = function(form, callback) {
    var path = `/api/comment/add`
    ajax('POST', path, form, callback)
}

// 删除评论
var apiCommentDelete = function(commentId, callback) {
    var path = `/api/comment/delete?id=${commentId}`
    ajax('GET', path, '', callback)
}

// 更新评论
var apiCommentUpdate = function(form, callback) {
    var path = `/api/comment/update`
    ajax('POST', path, form, callback)
}

// 评论的 template
var commentTemplate = function(weibo) {
    var comments = weibo.comments
    var h = ''
    // 判断是否有评论
    if (comments.length > 0) {
        // 循环所有的评论
        for (var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            var c = `
                <div class="comment-cell" data-id="${comment.id}">
                    <span>评论：</span>
                    <span class="comment-content">${comment.content}</span>
                    <button class="comment-edit">编辑</button>
                    <button class="comment-delete">删除</button>
                </div>
            `
            h += c
        }
    } else {
        log('没有评论', comments)
    }
    return h
}

// 微博的 template
var weiboTemplate = function(weibo) {
    // 评论的 template，在下面和微博 template 合并
    if ('comments' in weibo) {
        var comments = commentTemplate(weibo)
    } else {
        var comments = ''
    }
    var w = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <span class="weibo-content">${weibo.content}</span>
            <button class="weibo-edit">编辑</button>
            <button class="weibo-delete">删除</button>
            <div class="comment-list">
                ${comments}
            </div>
            <div>
                <input class='comment-add-input' data-id="${weibo.id}">
                <button class='comment-add'>发表评论</button>
            </div>
        </div>
    `
    return w
}

// 更新微博的 template
var weiboUpdateTemplate = function(content) {
    var w = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}"/>
            <button class="weibo-update">更新</button>
        </div>
    `
    return w
}

// 更新评论的 template
var commentUpdateTemplate = function(content) {
    var c = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}"/>
            <button class="comment-update">更新</button>
        </div>
    `
    return c
}

// 增加评论的template
var commentAddTemplate = function(comment) {
    var c = `
        <div class="comment-cell" data-id="${comment.id}">
            <span>评论：</span>
            <span class="comment-content">${comment.content}</span>
            <button class="comment-edit">编辑</button>
            <button class="comment-delete">删除</button>
        </div>
    `
    return c
}

// 插入微博的函数
var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var weiboList = e("#id-weibo-list")
    weiboList.insertAdjacentHTML("beforeend", weiboCell)
}

// 插入评论的函数
var insertComment = function(comment, weiboCell) {
    var commentList = e('.comment-list', weiboCell)
    var commentCell = commentAddTemplate(comment)
    commentList.insertAdjacentHTML('beforeend', commentCell)
}

// 插入更新微博表单
var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

// 插入更新评论表单
var insertUpdateCommentForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}

// 加载所有的微博
var loadWeibos = function() {
    apiWeiboAll(function(weibos) {
        for (var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

// 绑定增加微博的事件
var bindEventWeiboAdd = function() {
    var b = e("#id-button-add")
    b.addEventListener("click", function() {
        var input = e("#id-input-weibo")
        var content = input.value
        log("新增加的微博", content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            insertWeibo(weibo)
        })
    })
}

// 绑定删除微博的事件
var bindEventWeiboDelete = function() {
    var weiboList = e("#id-weibo-list")
    weiboList.addEventListener('click', function(event) {
        log(event)
        var self = event.target
        log("被点击的元素", self)
        if (self.classList.contains('weibo-delete')) {
            log("点到了删除按钮")
            var weiboId = self.parentElement.dataset['id']
            apiWeiboDelete(weiboId, function(r) {
                if ('verify' in r) {
                    alert(r.verify)
                } else {
                    log('删除微博', r.message)
                    self.parentElement.remove()
                    alert(r.message)
                }
            })
        } else {
            log('点到了 todo cell')
        }
    })
}

// 绑定编辑微博的事件
var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('weibo-edit')) {
            var weiboCell = self.closest('.weibo-cell')
            var weiboSpan = e('.weibo-content', weiboCell)
            var content = weiboSpan.innerText
            insertUpdateForm(content, weiboCell)
        } else {
            log('点到了 weibo cell')
        }
    })
}

// 绑定更新微博的事件
var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('weibo-update')) {
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            var weiboInput = e('.weibo-update-input', weiboCell)
            var content = weiboInput.value
            var form = {
                id: weiboId,
                content: content,
            }
            apiWeiboUpdate(form, function(weibo) {
                log(weibo.message)
                if ('verify' in weibo) {
                    alert(weibo.verify)
                } else {
                    var weiboSpan = e('.weibo-content', weiboCell)
                    weiboSpan.innerText = weibo.content
                    var updateForm = e('.weibo-update-form', weiboCell)
                    updateForm.remove()
                    alert('更新成功')
                }
            })
        } else {
            log('点到了其它元素')
        }
    })
}

// 绑定增加评论的事件
var bindEventCommentAdd = function() {
    var weiboList = e("#id-weibo-list")
    weiboList.addEventListener('click', function() {
        var self = event.target
        log('被点击到的元素', self)
        if (self.classList.contains('comment-add')) {
            log('点到了增加评论')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            log('微博id', weiboId)
            var commentInput = e('.comment-add-input', weiboCell)
            var content = commentInput.value
            log('评论内容', content)
            var form = {
                weibo_id: weiboId,
                content: content,
            }
            apiCommentAdd(form, function(comment) {
                log('评论', comment)
                insertComment(comment, weiboCell)
            })
        } else {
            log('点到了其它元素')
        }
    })
}

// 绑定删除评论的事件
var bindEventCommentDelete = function() {
    var weiboList = e("#id-weibo-list")
    weiboList.addEventListener('click', function(event) {
        log(event)
        var self = event.target
        log("被点击的元素", self)
        if (self.classList.contains('comment-delete')) {
            log("点到了删除按钮")
            var commentId = self.parentElement.dataset['id']
            apiCommentDelete(commentId, function(r) {
                if ('verify' in r) {
                    alert(r.verify)
                } else {
                    log('删除微博', r.message)
                    self.parentElement.remove()
                    alert(r.message)
                }
            })
        } else {
            log('点到了 todo cell')
        }
    })
}

// 绑定编辑评论的事件
var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        log(event)
        var self = event.target
        if (self.classList.contains('comment-edit')) {
            log('点到了评论编辑按钮')
            var commentCell = self.closest('.comment-cell')
            var commentSpan = e('.comment-content', commentCell)
            var content = commentSpan.innerText
            insertUpdateCommentForm(content, commentCell)
        } else {
            log('点到了其它元素')
        }
    })
}

//  绑定更新评论的事件
var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('comment-update')) {
            log('点到了更新评论按钮')
            var commentCell = self.closest('.comment-cell')
            // 拿到评论的 ID
            var commentId = commentCell.dataset['id']
            // 拿到输入的评论
            var commentInput = e('.comment-update-input', commentCell)
            var content = commentInput.value
            var form = {
                id: commentId,
                content: content,
            }
            apiCommentUpdate(form, function (comment) {
                if ('verify' in comment) {
                    alert(comment.verify)
                } else {
                    var commentSpan = e('.comment-content', commentCell)
                    commentSpan.innerText = comment.content
                    var updateForm = e('.comment-update-form', commentCell)
                    updateForm.remove()
                    alert('更新成功')
                }
            })
        } else {
            log('点到了其它元素')
        }
    })
}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()