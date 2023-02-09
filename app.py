from flask import Flask, render_template, redirect, request, url_for, jsonify,session
from bs4 import BeautifulSoup
import requests
import sys
import crud
import json
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/', methods =["GET","POST"])
def home():
    print("1231231231")
    URL = "https://uproxx.com/movies/best-movies-on-netflix/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    show_containers = soup.find_all("div", class_="post-page")
    shows = []
    for container in show_containers:
        show_name = container.find("em").text
        shows.append(show_name)
    return render_template("index.html")

@app.route('/yours', methods =["GET","POST"])
def yours():
    if request.method == "GET":
        username = session.get('username')
        #print("print all fckers")
        #print(username)
        x = crud.show_something("name", username)
        #print(x[0][0])
        if username == x[0][0]:
            movies_list = crud.show_something("movies",username)
            #print(type(movies_list[0][0]))
            #print(movies_list[0])
            movies_list2 = movies_list[0][0].replace("[","").replace("]","").replace('"',"").split(",")
            #print(movies_list2)
            #print(type(movies_list2))
            return render_template("yours.html", movies_list = movies_list2)
        else:
            return "there is a problem with a log in"
        
    if request.method == "POST":
        if "delete" in request.form:
            delete_movie = request.form["delete"]
            username = session.get('username')
            #print(delete_movie)
            movies_list = crud.show_something("movies",username)
            movies_list2 = movies_list[0][0].replace("[","").replace("]","").replace('"',"").split(",")
            #print("fckers")
            print(movies_list2)
            #print(type(movies_list2))
            movies_list2.remove(delete_movie)
            print(movies_list2)
            movies_list3 = json.dumps(movies_list2, separators=(',',':'))
            #print(movies_list3)
            #print(type(movies_list3))
            crud.update("users","movies", movies_list3, "name", username)
            return render_template("yours.html", movies_list = movies_list2)
        
        elif "add_movie" in request.form:
            #so here basically going to be the relatively hard part where rating is going to be add app 
            add_movie = request.form["add_movie"]
            username = session.get('username')
            movies_list = crud.show_something("movies",username)
            movies_list2 = movies_list[0][0].replace("[","").replace("]","").replace('"',"").split(",")
            movies_list2.append(add_movie)
            movies_list4 = json.dumps(movies_list2, separators=(',',':'))
            crud.update("users","movies", movies_list4, "name",  username)
            tapple_movies_list = crud.select("movie","movies")
            string_movies_list = [x[0] for x in tapple_movies_list]
            print(string_movies_list)
            if add_movie in string_movies_list:
                rating_number = crud.show_something2("rating","movies","movie", add_movie)
                print(rating_number)
                print(type(rating_number))
                rating_number2 = int(rating_number[0][0]) + 1
                print(rating_number2)
                crud.update("movies", "rating", rating_number2, "movie", add_movie)
            else:
                print("it is not in the movies")
                print(add_movie)
                print(crud.select("movie","movies"))
            #if add_movie in crud.select all from column movies then select rating 
            #and plus one and then update it, if not then update movies with writing the new 
            #movie you have several problems redo the crud to make it more flex
            return render_template("yours.html", movies_list = movies_list2)
        


@app.route('/test', methods =["GET","POST"])
def test():
    x = crud.select("movie","movies")
    print(x)
    return render_template("test.html", x=x )


@app.route('/login', methods =["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        input_password = crud.check_password(name)
        input_password2 = input_password[0][0]
        if str(password) == str(input_password[0][0]):
            session['username'] = request.form["name"]
            return "sessioin created"
        else:
            return "not authorised "




@app.route('/shows', methods =["GET","POST"])
def shows():
    if request.method == "GET":
        #so this guy basicaly will show just the movies that in the table with ratings   
        return render_template("shows.html")

@app.route('/registration', methods =["GET","POST"])
def registration():
    if request.method == "GET":
        return  render_template("registration.html")
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        crud.write("users", name, password)
        return render_template("login.html")



if __name__ == '__main__':
    app.run(debug=True)
