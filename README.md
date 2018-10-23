# My-blog

### Key words
Flask, python, Mysql, HTML, CSS

## ABSTRACT 
In this project, I created a personal web blog. Except for the basic functions like register, add and edit articles, find back the password, I created a few customized modules like stock information visualization and prediction, social network app usage visualization in China and a recommendation system.
The project was created mainly by Flask+python(back-end), HTML, CSS and Javascript(front-end), the database related tools are Mysql, JSON(from yahoo API) and simple self-made B+ tree.

## 1. AN OVERVIEW ON BLOG LOGIC
### 1.1  Registeration module
The Home page of the RAINBOW Blog is as follow:
![aa](https://github.com/ch812248495/My-blog/blob/master/image/1.png)

Fig.1. The home page of rainbow blog 

Basically, establishing a personal blog was one of my wishes. Main functions and modules are defined roughly in the navigation bar: Homepage, Articles page, Dashboard page, Stock page, Visualization page and Recommendation page.
To utilize the functions provided by the blog, we have to register first, otherwise clicking any functions will lead to the Sign-up page with a red error message:
![aa](https://github.com/ch812248495/My-blog/blob/master/image/2.png)
Fig.2. The login page of rainbow blog 
If you have an account you can login now; if not, click the “Register” button on the Home page or the sentence “Have not registered” and you will be redirected to the register page:
![aa](https://github.com/ch812248495/My-blog/blob/master/image/3.png)

Fig.3. The register page of rainbow blog 
Here you can register for an account for yourself. I will use my own account “ch” for demonstration.
Moreover, if you forget your username and password, you may click the sentence “Forgot your account” to enter your Email:
![aa](https://github.com/ch812248495/My-blog/blob/master/image/4.png)

Fig.4. The find back password page of rainbow blog 
After submitting the request, the backend will search for the Email in the Mysql database, if you submit the correct Email, your username and password will be sent to the Email address; if not, an error message will appear.
![a](https://github.com/ch812248495/My-blog/blob/master/image/5.png)

Here I did some simplification, the password should not be sent simply as plain text for security concern.
The mail sent from the backend is like this:
![a](https://github.com/ch812248495/My-blog/blob/master/image/6.png)

Fig.5. The password Email 
Now we can login and experience the service supported by blog.
### 1.2  ARTICLE MODULE

Blogs are primarily created for recording and article sharing, so an article module should be included.
After logging in, the page will be redirected to the dashboard:
![a](https://github.com/ch812248495/My-blog/blob/master/image/7.png)

Fig.6. The dashboard page of rainbow blog 
here I have added two articles already.
	Click the “ADD ARTICLE” button to the article edit page:
![a](https://github.com/ch812248495/My-blog/blob/master/image/8.png)

Fig.7. The add article page of rainbow blog 
We can add articles and graphs on this page. Submit the article by clicking the button. The page will be redirected to the dashboard and refresh it with the successful message:
![a](https://github.com/ch812248495/My-blog/blob/master/image/17.png)

Fig.8. Article created successfully 
Edit and delete the article by clicking the button, too.
Click the “ARTICLES” on the navigation bar to read the articles:
![a](https://github.com/ch812248495/My-blog/blob/master/image/10.png)

Fig.9. The articles page of rainbow blog 
Click the title of each article:


![a](https://github.com/ch812248495/My-blog/blob/master/image/18.png)

Fig.10. The article page of rainbow blog 

## 1.3  STOCK MODULE
The initial page of stock module:
![a](https://github.com/ch812248495/My-blog/blob/master/image/19.png)

Fig.11. The initial stock page of rainbow blog 
Theoretically, all stocks’ information could be searched by stock id since the data is from yahoo API, I just listed a few frequently-discussed stock exchanges(Shanghai, Shenzhen, Hongkong and America markets).
After entering the stock code, the k-line graph will be demonstrated (“AAPL” for example):
![a](https://github.com/ch812248495/My-blog/blob/master/image/20.png)

Fig.12. The stock info visualization
Adjust the size of the window below to change the view.
The backend is able to do some simple prediction for the coming 10 days (3 methods which will be discussed later):
![a](https://github.com/ch812248495/My-blog/blob/master/image/21.png)

Fig.13. Stock price predication

## 1.4  DATA VISUALIZATION MODULE
In this module, I grabbed some data from Baidu’s “hot search terms” make a data visualization demo to show the popularities of different social network app:



![a](https://github.com/ch812248495/My-blog/blob/master/image/22.png)

Fig.14. The data visualization 

1.5 RECOMMENDATION SYSTEM
The preference for each critic:
![a](https://github.com/ch812248495/My-blog/blob/master/image/23.png)

Fig.15. The data visualization 
By analyzing these data, I draw a few conclusion:

# 2  REALIZATION
The realizations of register and article module are ordinary work about the interaction between flask backend and web frontend. So I will skip their technical detail and focus on the realization of predicting stock price, data visualization and recommendation system instead.
## 2.1 Stock data processing
I use the yahoo finance api as the data source:
```
def to_csv(stock_num):
    start = dt.datetime.now() + dt.timedelta(-500)
    end = dt.datetime.today()
    try:
        df = web.DataReader(stock_num,'yahoo',start,end)
    except:
        row_data = 0
        date = 0
        return row_data,date
    df.to_csv('stock.csv')
```
Use the web.DataReader() method to get the stock information in last 500 days, reconstruct it to be another data format and plot the k-line graph using pyecharts and javascript.
Afterwards, I adopted 3 methods to predict the stock price. 
The main idea of stock price prediction is: can we use the historical data to fit the future data? Or simply in another word, is the stock market predictable? 
In fact, this is a very interesting topic and is argued frequently among economists and mathematicians. For example, some economists take a skeptical attitude towards stock prediction. “Give a monkey enough darts and they’ll beat the market.” So says a draft article by Research Affiliates highlighting the simulated results of 100 monkeys throwing darts at the stock pages in a newspaper. The average monkey outperformed the index by an average of 1.7 percent per year since 1964.
But other mathematicians believe that stock market is predictable with machine learning and deep learning, they believe that history keeps repeating itself, we can find the rule and regular pattern of the stock market. That is an important assumption for the follow-on Work.
Personally, I know that stock behavior is random but I still believe that stock market is predictable to some extent. There are two patterns to explain the stock behavior. One pattern is the random fluctuation (price rise or fall less than 1% for example), machine learning works just fine in this scenario, great algorithms’ accuracy may reach 70% or even higher. The other pattern is wild swings: the extreme trend influenced by the whole environment and news. If Ma Yun decide to acquire a company, everyone knows the result of its stock price. Machine learning behaves badly to follow such trend.
	1) Linear Regression:
	Main idea: fit today’s price by last 10 days’.
	The simplest linear regression form is binary linear regression adopting least square method. For example, with the observed one-dimensional dataset y(price at time T) and X(price at time T-10), we assume:

parameters (a, b) could be estimated by the least square method:


This is the simplest situation, to increase the model accuracy and correlation between y and X, we set the X as matrix (price at time T-1, T-2……T-10):

to fit the model:

	The estimation of (a,b) is complicated so I skip their mathematical form.	
	Using the linear regression method to forecast the future prices (the red one)
![a](https://github.com/ch812248495/My-blog/blob/master/image/24.png)

Fig.16. Predication

	2) SVM:
	Main idea: project the (y,X) to a higher-dimensional space to draw a plane to fit them.
	Basically, the SVM (support vector machine) is utilized for classification and regression analysis.
	The basic intention for SVM is separating 2 groups of points, if we find it hard to separate them in low-dimensional space with one line, we will project them (by kernel function) to a high-dimensional space and then separate them with a plane:
![a](https://github.com/ch812248495/My-blog/blob/master/image/25.png)

Fig.17. The SVM sketch map
	The key problem is, how to map the low-dimensional space to high-dimensional space? There are several kernel functions to do the mapping:
Linear: 
Poly: 
Rbf: 
Here I use as the input space (only 2 dimensional, in order to decrease the computing time) and adopted the poly function(n=3) to do the mapping and the fitting (the black one and the green one):
Fig.15. Predication
	3) Neural network:
	Main idea: The probability of a certain event happening partially depends on what happened before it. 
	Here I use the LSTM(long short term network) to do the predication, there will be three types of layers: input layer, hidden layer, output layer.


![a](https://github.com/ch812248495/My-blog/blob/master/image/14.png)

Fig.16. Three layers
The input layer will be

the hidden layer is set to be

the output layer is

As a result, the previous price will influence the output, the fitting task is to calculate the parameters W and U.
![a](https://github.com/ch812248495/My-blog/blob/master/image/15.png)


Fig.17. Predication

## 2.2 Recommendation system
Here is the dataset I use:
critics = 
	   {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
	   'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}
           
This simple dataset records different critics’ preference for different movies, each critic’s preference is saved in the B+ tree(will be discussed later).
Pearson correlation score: three conclusions are based on Pearson correlation score, which is a measure of the linear correlation between two variables X and Y. It has a value between +1 and −1, where 1 is total positive linear correlation, 0 is no linear correlation, and −1 is total negative linear correlation. 
Matching tastes: we adopt the Pearson correlation score to evaluate every two critics’ taste and correlation, so we can draw the conclusion that Toby and Lisa Rose are of the similar taste. 
Recommending items: for each movie Toby has not watched before, add up other critics’ (score × Pearson score) and return the highest one, as a result, The night listener is highly recommended.
Matching Products: just like matching tastes, exchange critics’ name and the movie name to compute the Person correlation score.
# 3  UNDERLYING DATA STORAGE
I used three methods to organize the underlying data storage: Mysql, json and B+ tree.
The register information and the articles are stored in the Mysql database, take the registeration process as a typical example:
```
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
```

Above codes show the interaction between database and front end. The submitted form passes the name, email, username and password to Mysql, I used the “INSERT” command to insert the user information into the database. 	
	In the stock part, the stock information returned by the yahoo finance API is JSON, I saved it as a .csv file and processed the data to get the open, close, high and low price in a day.
with open("stock.csv", 'r') as csvfile:
```
            csvFileReader = csv.reader(csvfile)
            next(csvFileReader)
            for row in csvFileReader:
                data = []
                data.append(round(float(row[1]),1)) #open price
                data.append(round(float(row[5]),1)) #close price
                data.append(round(float(row[3]),1)) #high price
                data.append(round(float(row[2]),1)) #low price
                row_data.append(data)
```
In the recommendation part, I saved different critics’ ranking for each movie in a B+ Tree. By the way, initially I intended to establish one of my own database, but soon I found it really time-consuming so I abandoned that plan. Building a B+ tree is not that easy, too. In fact, the simulation of the B+ tree requires disk I/O, which should be done by C/C++, I choose to simplify the B+ tree at last, build the tree based on list. I defined three classes to simulate the B+ tree: BPTree, BPTreeNode, BPTreeLeaf.
So, Lisa’s preference could be stored like this:	
```
Lisa = BPTree(3)
Lisa.insert({'Lady in the Water': 2.5})
Lisa.insert({'Snakes on a Plane': 3.5})
Lisa.insert({'Just My Luck': 3.0})
Lisa.insert({'Superman Returns': 3.5})
Lisa.insert({'You, Me and Dupree': 2.5})
Lisa.insert({'The Night Listener': 3.0})
```
# 4  SUMMARY
To be honest, I regretted about building this blog as the project since mastering the usage of Flask, HTML and CSS cost me too much time, although I learnt a lot from overcoming problems about web logic and web layout again and again. I spent almost half of the time making the web to be more beautiful (still ugly, however), so I am in such a hurry to realize the core functions and write this report.
Moreover, I have tried to realize so many functions (register, find back password, B+ tree, etc.), so I am unable to delve into one function (maybe this is what I want now). If a second chance offered me, I may delve into the stock function, adding more features and using more ideas to predict the price.
Anyway, I spent a lot of time on this project and do learn a lot, thanks for reading.



