from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from .models import User,Post,Comment,Saved
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/perspective")

def home():
    return render_template("perspective.html")

#@views.route("posts/homefeed.html")
@views.route("/homefeed")
@views.route("/homefeed.html")

@login_required
def homefeed():
     posts=Post.query.order_by(Post.date_created.desc())
     #posts=Post.query.all()
     return render_template("homefeed.html",user=current_user,posts=posts)

@views.route("/second.html")
@views.route("perspective/second")
def second():
    return render_template("second.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/about.html")
def about():
    return render_template("about.html")

@views.route("/help.html")
def help():
    return render_template("help.html")

@views.route("/terms.html")
def terms():
    return render_template("terms.html")

 

@views.route("/myprofile.html")
@views.route("perspective/myprofile")
#@views.route("posts/myprofile.html")
@login_required
def myprofile():
    user=current_user
    return render_template("myprofile.html",user=current_user,posts=user.posts)

@views.route("/search.html", methods=['GET','POST'])
@login_required
def search():
    
    if request.method=='POST':
        tags=request.form.get('tags').strip()
        if not tags:
            flash('Search item cannot be empty', category='error') 
        else:
            posts=Post.query.all()
            return render_template("search.html",user=current_user,posts=posts,tags=tags)
    
    return render_template("search.html",user=current_user)

#@views.route("/searchresult.html")

@views.route("/write.html", methods=['GET','POST'])
@views.route("perspective/write",  methods=['GET','POST'])
#@views.route("posts/write.html")
@login_required 
def write():
    if request.method=='POST':
        heading=request.form.get('heading')
        text=request.form.get('text')
        formatting=request.form.get('formatting')
        tags=request.form.get('tags').strip()

        if not heading:
            flash('Heading cannot be empty', category='error')
        if not text:
            flash('Post cannot be empty', category='error')
        if not tags:
            flash('Tag cannot be empty', category='error')
        else:
            post=Post(heading=heading, text=text,formatting=formatting, tags=tags, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('New post created!', category='success')
            return redirect(url_for('views.homefeed'))



    return render_template("write.html",user=current_user)

 

@views.route("/<name>",methods=['GET','POST'])
 
def manythings(name):
        if request.method=='POST':
            text=request.form.get('text')
            if not text:
                flash('Comment cannot be empty', category='error')

            else:
                posts=Post.query.filter_by(heading=name).first()
                id2=posts.id
                comment=Comment(text=text,author=current_user.id,post_id=id2)
                db.session.add(comment)
                db.session.commit()
                posts=Post.query.all()
                comments=Comment.query.all()
                 
                user=User.query.filter_by(name=name).first()
                flash('Comment added', category='success')
                return render_template("post.html",user=user,posts=posts,heading=name,comments=comments )
            
   
        user=User.query.filter_by(name=name).first()
        if name==current_user.name:
            return render_template("myprofile.html",user=current_user,posts=user.posts)
        elif user is None:
            posts=Post.query.all()
            comments=Comment.query.all()
             
         
            return render_template("post.html",user=current_user,posts=posts,heading=name,comments=comments )
        else:
           posts=user.posts
           return render_template("profile.html",user=user,posts=posts)

@views.route("/tosave/<name>")
@login_required
def save(name):

        posts=Post.query.filter_by(heading=name).first()
        id2=posts.id
        saveds=Saved.query.filter_by(author=current_user.id,post_id=id2).first()
        if saveds is None:
            
            flash('Post Saved',category='success')
           
        else:
            db.session.delete(saveds)
            db.session.commit()
            flash("Post is already saved",category='success')
        
        saveds=Saved(author=current_user.id,post_id=id2)
        db.session.add(saveds)
        db.session.commit()
         
        return redirect(url_for('views.saved'))
    
@views.route("/saved.html")
def saved():
    saveds=Saved.query.order_by(Saved.date_created.desc())
    
    return render_template("saved.html",saveds=saveds,user=current_user)


