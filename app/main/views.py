
import os
from flask import render_template,request,redirect,url_for,abort
from flask_login import current_user, login_required
from . import main
from app.request import get_movies,get_movie,search_movie
from ..models import Review,User
from .forms import ReviewForm,UpdateProfile
from .. import db
import markdown2
from werkzeug.utils import secure_filename

import app

ALLOWED_EXTENSIONS={'png','jpg','jpeg'}
# Review=review.Review

#Views 
@main.route('/')
def index():

  '''
  View root page function that returns the index page and its data
  '''
  # message='Hello World'
  title='Home - Welcome to the best Movie Review Website Online'
  
  #Getting popular movie
  popular_movies=get_movies('popular')
  upcoming_movie=get_movies('upcoming')
  now_showing_movie=get_movies('now_playing')
  search_movie=request.args.get('movie_query')

  if search_movie:
    return redirect(url_for('main.search',movie_name=search_movie))
  else:
    return render_template('index.html',title=title,popular=popular_movies, upcoming=upcoming_movie, now_showing=now_showing_movie)

@main.route('/movie/<int:id>')
def movie(id):
  '''
  View movie page function that returns the movie details page and its data
  '''
  movie=get_movie(id)
  title=f'{movie.title}'  
  reviews=Review.get_reviews(movie.id)
  return render_template('movie.html',title=title,movie=movie,reviews=reviews)


@main.route('/search/<movie_name>')
def search(movie_name):
  '''
  View function to display the search results
  '''
  movie_name_list=movie_name.split(" ")
  movie_name_format="+".join(movie_name_list)
  searched_movies=search_movie(movie_name_format)
  title=f'search results for {movie_name}'
  return render_template('search.html',movies=searched_movies)

@main.route('/movie/review/new/<int:id>',methods=['GET','POST'])
@login_required
def new_review(id):
  form=ReviewForm()
  movie=get_movie(id)
  
  if form.validate_on_submit():
    title=form.title.data
    review=form.review.data
    # new_review=Review(movie.id,title,movie.poster,review)
    new_review=Review(movie_id=movie.id,movie_title=title,image_path=movie.poster,movie_review=review,user=current_user)
    new_review.save_review()
    return redirect(url_for('main.movie',id=movie.id))

  title=f'{movie.title} review'
  return render_template('new_review.html', title=title,review_form=form,movie=movie)

@main.route('/user/<uname>')
def profile(uname):
  user=User.query.filter_by(username=uname).first()

  if user is None:
    abort(404)

  return render_template("profile/profile.html", user=user)

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
  user=User.query.filter_by(username=uname).first()
  if user is None:
    abort(404)

  form=UpdateProfile()

  if form.validate_on_submit():
    user.bio=form.bio.data
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('.profile',uname=user.username))
  return render_template('profile/update.html',form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
  user=User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    photo=request.files['photo']
    # filename=photos.save(request.files['photo'])
    filename=secure_filename(photo.filename)
    # path=f'photos/{filename}'
    photo.save(os.path.join('app/static/photos',filename))
    user.profile_pic_path=f'photos/{filename}'
    db.session.add(user)
    db.session.commit()

  return redirect(url_for('main.profile',uname=uname))

@main.route('/review/<int:id>')
def single_review(id):
  review=Review.query.get(id)
  if review is None:
    abort(404)
  format_review=markdown2.markdown(review.movie_review,extras=["code-friendly","fenced-code-blocks"])
  return render_template('review.html',review=review,format_review=format_review)

  