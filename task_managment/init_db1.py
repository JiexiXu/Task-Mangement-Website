import sqlite3

# 创建数据库链接
connection = sqlite3.connect('database.db')

# 执行db.sql中的SQL语句
with open('db1.sql') as f:
    connection.executescript(f.read())

# 创建一个执行句柄，用来执行后面的语句
cur = connection.cursor()

# 插入两条文章
cur.execute("INSERT INTO posts (title, content, ttype) VALUES (?, ?, ?)",
            ('任务xx', '任务1，xxxx', '重要紧急')
            )

cur.execute("INSERT INTO posts (title, content, ttype) VALUES (?, ?, ?)",
            ('任务yy', '任务2，xxxx','重要不紧急')
            )

cur.execute("INSERT INTO posts (title, content, ttype) VALUES (?, ?, ?)",
            ('任务zz', '任务3，xxxx','紧急但不重要')
            )

cur.execute("INSERT INTO posts (title, content, ttype) VALUES (?, ?, ?)",
            ('任务uu', '任务4, xxxx','不重要不紧急')
            )

# 提交前面的数据操作
connection.commit()

# 关闭链接
connection.close()
