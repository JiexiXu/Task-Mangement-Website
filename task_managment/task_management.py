import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = b'H\xaf\xe5B\x04\xab&\xa1\x90\xec\x1e\xf3\xbe\xad\x95!\xd1r\x17N!0va'


# 创建一个函数用来获取数据库链接
def get_db_connection():
    # 创建数据库链接到database.db文件
    conn = sqlite3.connect('database.db')
    # 设置数据的解析方法，有了这个设置，就可以像字典一样访问每一列数据
    conn.row_factory = sqlite3.Row
    return conn

# 根据post_id从数据库中查询获取post记录
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    return post


@app.route('/') 
def index():
    # 调用上面定义的函数，获取链接
    conn = get_db_connection()
    # 查询所有数据，放到变量posts中
    posts_a = conn.execute('SELECT * FROM posts where ttype="Important, Urgent" limit 5').fetchall()
    posts_b = conn.execute('SELECT * FROM posts where ttype="Important, Not Urgent" limit 5').fetchall()
    posts_c = conn.execute('SELECT * FROM posts where ttype="Urgent, Not Important" limit 5').fetchall()
    posts_d = conn.execute('SELECT * FROM posts where ttype="Not Important, Not Urgent" limit 5').fetchall()
    conn.close()

    void_num_a = 5-len(posts_a)
    void_num_b = 5-len(posts_b)
    void_num_c = 5-len(posts_c)
    void_num_d = 5-len(posts_d)


    tuple_a=(posts_a,void_num_a)
    tuple_b=(posts_b,void_num_b)
    tuple_c=(posts_c,void_num_c)
    tuple_d=(posts_d,void_num_d)
    #把查询出来的posts传给网页
    #return render_template('index.html', tuple_a=tuple_a, posts_b=posts_b, posts_c=posts_c, posts_d=posts_d)
    #return render_template('index.html', posts_a=posts_a, posts_b=posts_b, posts_c=posts_c, posts_d=posts_d)
    return render_template('index.html', tuple_a=tuple_a, tuple_b=tuple_b, tuple_c=tuple_c, tuple_d=tuple_d)


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        title = request.form['title-tmp']
        content = request.form['conten-tmp']
        ttype = request.form['ttype-tmp']

        if not title:
            flash('The title should not be void!')
        elif not content:
            flash('The content should not be void')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, ttype) VALUES (?, ?, ?)',
                         (title, content, ttype))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('new.html')


@app.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    # 进行数据库操作（连接、SELECT查询、关闭），根据id从数据库查询到要编辑的这条记录信息
    post = get_post(id)

    # 从index进入此函数时不进入下面的分支，直接执行后面的render_template，进入edit页面(edit.html)
    # 在edit页面点击了提交后才进入下面的分支
    if request.method == 'POST':
        title = request.form['title-tmp']
        content = request.form['conten-tmp']
        ttype = request.form['ttype-tmp']

        if not title:
            flash('Title is required!')
        else:
            # 进行数据库操作（连接、UPDATE更新、提交、关闭）
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?, ttype = ?'
                         ' WHERE id = ?',
                         (title, content, ttype, id))
            conn.commit()
            conn.close()
            # 提交完成跳转回主页
            return redirect(url_for('index'))

    # 跳转到edit页面，同时传入从数据库获取的记录信息作为参数输入给edit页面
    return render_template('edit.html', post=post)


@app.route('/posts/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" Deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=='__main__':
    #app.run(debug = True)
    app.run(host='127.0.0.1', port=80)
    #app.run(host='192.168.1.8', port=80)
    #app.run(host='192.168.1.100', port=80)
