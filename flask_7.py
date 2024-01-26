
from flask import Flask, redirect, url_for, template_rendered, render_template, request, flash, render_template_string, make_response
app = Flask(__name__)
app.secret_key='secret key'
import movie_5
import pandas as pd
import db

@app.route('/', methods=['POST', 'GET'])
def movieRecommendation():
    if request.method == 'POST':
        userID = request.form.get('userID')
        print(userID)
        movieInput = request.form.get('movie')
        print(movieInput) 
        # flash(str(movie_4.movie(movie)))
        result = movie_5.MovieReccomendation.movie(movieInput)
        print(result)
        print(type(result))
        db.insertData(userID= userID, movieInput=movieInput)

        # db.displayDB()
        if isinstance(result, pd.DataFrame):
            return render_template('index_4.html',  tables=[result.to_html(classes='data')], titles=result.columns.values)
        
        elif isinstance(result, movie_5.movieNameLength):
            # return render_template('index_2.html',  data='Sorry no movies found in DataBase')
            flash('The Entered Movie length name exceeded 50 characters please retry...')
            return render_template('index_4.html')
        
        elif isinstance(result, Exception):
            # return render_template('index_2.html',  data='Sorry no movies found in DataBase')
            flash(f'The Movie {result} is not in the Database Please retry... ')
            return render_template('index_4.html')

    return render_template('index_4.html')

@app.route('/forward', methods=['POST', 'GET'])
def displayData():
    display = db.displayDB()
    print(display)
    print(type(display))
    # flash(display)
    # db.displayDB()

    if isinstance(display, pd.DataFrame):
        return render_template('index_4.html',  tables=[display.to_html(classes='data')], titles=display.columns.values)
    return render_template('index_4.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)