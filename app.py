# -*- coding: UTF-8 -*-

from flask import Flask, render_template, flash, redirect, url_for, session, logging,request
from flask_mail import Message
import init
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import random
from pyecharts import Kline,Line
from pyecharts.constants import DEFAULT_HOST
from grabber import to_csv
from pyecharts import Page
from predict import predictation
from pyecharts import *
from pyecharts.constants import CITY_GEO_COORDS

[app,mysql,mail] = init.initiation()

#Check if users logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, please login','danger')
            return redirect(url_for('login'))
    return wrap


#index
@app.route('/')
def index():
    return render_template('home.html')

#about
@app.route('/about/')
def about():
    return render_template('about.html')

#articles
@app.route('/articles/')
@is_logged_in
def articles():
    cur = mysql.connection.cursor()
    result = cur.execute("use myflaskapp")
    result = cur.execute("select * from articles")
    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html',articles = articles)
    else:
        msg = 'No articles found'
        return render_template('articles.html',msg=msg)



#single article
@app.route('/article/<string:id>/')
def ab(id):
    cur = mysql.connection.cursor()
    result = cur.execute("use myflaskapp")
    result = cur.execute("select * from articles where id = %s",[id])
    article = cur.fetchone()
    return render_template('article.html',article = article)


#register form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=1,max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

#user register
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        #Create the cursor
        cur = mysql.connection.cursor()
        result = cur.execute("use myflaskapp")
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))

        #commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()
        flash('you are now registered and can log in', 'success')
        redirect(url_for('index'))

    return render_template('register.html',form=form)

#User login
@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        #get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("use myflaskapp")

        result = cur.execute("select * from users where username = %s",[username])

        if result > 0: #if any rows is found
            #get stored hash
            data = cur.fetchone() #get the first one found
            password = data['password']
            #compare passwords
            if password_candidate == password:
                #passed
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))
            else:
                error = 'Password not matched'
                return render_template('login.html',error = error)
            #close connection
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
        #do not close the cur here cause the user may want to login again
    return render_template('login.html')



#logout
@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    #flash('You are now logged out', 'success')
    return render_template('home.html')


#Find password
@app.route('/find_password/', methods=['GET', 'POST'])
def find_password():
    if request.method =='POST':
        #get form fields
        email = request.form['email']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username
        result = cur.execute("use myflaskapp")

        result = cur.execute("select * from users where email = %s",[email])

        if result > 0: #if any rows is found
            #get stored hash
            data = cur.fetchone() #get the first one found
            password = data['password']
            username = data['username']
            str = 'username:'+username+' '+'password:'+password
            msg = Message('找回密码', sender='caoheng1994@outlook.com', recipients=[email])
            msg.body = str

            with app.app_context():
                mail.send(msg)
            #close connection

            cur.close()
            msg = 'Email sent successfully'
            return render_template('login.html', msg=msg)

        else:
            error = 'User not found'
            return render_template('login.html', error=error)
        #do not close the cur here cause the user may want to login again
    return render_template('find_password.html')


#dashboard
@app.route('/dashboard/')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("use myflaskapp")
    result = cur.execute("select * from articles")
    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html',articles = articles)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html',msg=msg)


#add_articles
@app.route('/add_article',methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        result = cur.execute("use myflaskapp")

        cur.execute("insert into articles(title, body,author) values(%s, %s, %s)", (title, body, session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Article created','success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form = form)

#Edit articles
@app.route('/edit_article/<string:id>',methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("use myflaskapp")

    result = cur.execute("select * from articles where id=%s",[id])

    article = cur.fetchone()

    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']


    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()
        result = cur.execute("use myflaskapp")

        cur.execute("update articles set title=%s, body=%s where id = %s", (title,body,id))

        mysql.connection.commit()

        cur.close()

        flash('Article Updated','success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form = form)


#delete article
@app.route('/delete_article/<string:id>')
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("use myflaskapp")

    cur.execute("delete from articles where id=%s",[id])
    mysql.connection.commit()
    cur.close()

    flash('Article deleted','success')

    return redirect(url_for('dashboard'))


#Stock
@app.route('/stock/',methods=['GET','POST'])
@is_logged_in
def stock():
    page = Page()
    if request.method =='POST':
        stock_num = request.form['stock_num']
        if stock_num:
            kline = k_line(stock_num)
            page.add(kline)
            if kline==0:
                error = "No Such Stock, Check First"
                return render_template('stock.html',error = error)
            normalline = nomoral_line(stock_num)
            page.add(normalline)
            return render_template('stock.html',
                           myechart=page.render_embed(),
                           host=DEFAULT_HOST,
                           script_list=page.get_js_dependencies())
        else:
            return render_template('stock.html')
    return render_template('stock.html')


#virtualization
@app.route('/virtualization/')
def virtualization():
    page2 = Page()
    data_clound =data_cloud()
    page2.add(data_clound)
    _bar = force()
    page2.add(_bar)
    map = _map()
    page2.add(map)
    pie = _pie()
    page2.add(pie)
    return render_template('virtualization.html',
                           myechart=page2.render_embed(),
                           host=DEFAULT_HOST,
                           script_list=page2.get_js_dependencies())


@app.route('/recommendation/')
def recommendation():
    page3 = Page()
    sca = scatter()
    page3.add(sca)
    return render_template('recommendation.html',
                           myechart=page3.render_embed(),
                           host=DEFAULT_HOST,
                           script_list=page3.get_js_dependencies())


def scatter():
    attr = ['Lady in the Water', 'Snakes on a Plane', 'Just My Luck', 'Superman Returns', 'You, Me  Dupree', 'The Night Listener']
    v1 = [2.5, 3.5, 3, 3.5, 2.5, 3]
    v2 = [3,3.5,1.5,5,3.5,3]
    v3 = [2.5,3,0,3.5,4,0]
    v4 = [0,3.5,3,4,2.5,4.5]
    v5 = [3,4,2,3,2,3]
    v6 = [3,4,3,5,3.5,0]
    v7 = [0,4.5,1,4,0,0]

    bar = Bar("Preference of each critic",width=1200, height=450)
    bar.add("Lisa Rose", attr, v1)
    bar.add("Michael Phillips",attr,v3)
    bar.add("Claudia Puig",attr,v4)
    bar.add("Mick LaSalle",attr,v5)
    bar.add("Jack Matthews",attr,v6)
    bar.add("Toby",attr,v7)

    bar.add("Gene Seymour",attr,v2,is_convert=True)


    return bar


def _map():
    value = [50, 30, 100, 78, 20, 80, 190, 53, 49.6,100,38]
    attr = ["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏","浙江","黑龙江"]
    map = Map("Wechat popularity in different areas", width=800, height=500)
    map.add("", attr, value,type="heatmap", is_visualmap=True, visual_range=[0, 100], visual_text_color='#fff',is_roam=False,is_map_symbol_show=False)
    return map


def data_cloud():
    name = ['微博','QQ空间','知乎','豆瓣','贴吧','Twitter','Facebook','LinkedIn','Tumblr','微信','lofter','天涯','人人']
    index = [214370,64766,135530,52322,33802,4215,22729,3724,6715,300327,8126,22824,4479]
    wordcloud = WordCloud(width=600, height=400)
    wordcloud.add("Social app popularity", name, index, word_size_range=[20, 100])
    return wordcloud

def force():
    attr = ["under 19","20-29","30-39","40-49","above 50"]
    v1 = [2,14,54,26,4]
    v2 = [6,18,49,25,2]
    v3 = [1,20,61,16,2]
    v4 = [6,30,46,17,1]
    v5 = [9,26,46,18,1]
    bar = Bar("Populariry among all ages",width=1200, height=520)
    bar.add("WeChart", attr, v1)
    bar.add("qq Zone", attr, v2, is_convert=True)
    bar.add("LinkedIn", attr, v3, is_convert=True)
    bar.add("Zhihu", attr, v4, is_convert=True)
    bar.add("Tieba", attr, v5, is_convert=True)
    return bar


def k_line(stock_num):
    v1,date = to_csv(stock_num)
    if v1==0:
        kline=0
        return kline
    kline = Kline(stock_num,width=800,height=450)
    kline.add("Daily K Line", date, v1, mark_point=["max"], is_datazoom_show=True)
    return kline


def nomoral_line(stock_num):
    v2,v3,v4 = predictation(stock_num);
    attr = []
    for i in range(1,11):
        attr.append(i)
    predict_line = Line("Prediction")
    predict_line.add("Close price(linear regression)",attr,v2,mark_point=["max","min"])
    predict_line.add("Close price(Neural Network)",attr,v4,mark_point=["max","min"])
    predict_line.add("Close price(SVM-poly_kernal)",attr,v3,yaxis_min=round(min(min(v3),min(v2),min(v4)))-0.01*round(min(min(v3),min(v2),min(v4))),mark_point=["max","min"])
    return predict_line

def _pie():
    pie = Pie("Popularity by gender")
    pie.add("微信", ["微信男", ""], [68, 32], center=[10, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, )
    pie.add("", ["知乎男", ""], [56, 44], center=[30, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, legend_pos='left')
    pie.add("", ["空间男", ""], [47, 53], center=[50, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["天涯男", ""], [66, 34], center=[70, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["微博男", ""], [54, 46], center=[90, 30], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["领英男", ""], [67, 33], center=[10, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["豆瓣男", ""], [54, 46], center=[30, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["贴吧男", ""], [74, 26], center=[50, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["脸书男", ""], [50, 50], center=[70, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None)
    pie.add("", ["推特男", ""], [53, 47], center=[90, 70], radius=[18, 24],
            label_pos='center', is_label_show=True, label_text_color=None, is_legend_show=False, legend_top="center")
    return pie





#Article form class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Context', [validators.Length(min=30)])


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host='0.0.0.0', debug=True, port=2000)