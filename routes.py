import os
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash
from forms import SignupForm, LoginForm, CaptionField
from classes import user, loginuser, filesave
from werkzeug.utils import secure_filename 
from files import allowed_file
import datetime
from werkzeug.datastructures import CombinedMultiDict


UPLOAD_FOLDER = 'images'#upload folder
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])#allowedextensions
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "development-key" #used to authorize the modification of critical data 
app.debug = True
offset = 0
newuser= []

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

"""On the login page an existing user can signin or a new user can signup
The loginuser class is used to check the credentials of the user"""
@app.route("/login", methods=["GET","POST"])
def login():
  if 'email' in session: #check if session active
    return redirect(url_for('home'))
  form = LoginForm() #create a form object of class LoginForm
  if request.method=="POST": 
    if form.validate()==False: 
      return render_template('login.html', form=form)
    else:
      email = form.email.data
      password = form.password.data
      retuser = loginuser(email)
      userinfo = retuser.existcheck(email)
      if userinfo is not None:
        pwd = userinfo[3]
        pwd = pwd.strip()
      if userinfo is not None and retuser.check_password(password,pwd):
        session['email']= form.email.data
        return redirect(url_for('home'))
      else:
        print "Did not match"
        return redirect(url_for('login'))
  elif request.method=="GET":
    return render_template("login.html", form=form)

"""Home allows file uploads. The OS function .save is used to save files"""
@app.route("/home", methods=['GET','POST'])
def home():
  form = CaptionField(CombinedMultiDict((request.files, request.form)))
  if 'email' not in session:
    return redirect(url_for('login'))
  if request.method == 'POST':  
      """foldername= session['email'].split('@')[0]    
      app.config['UPLOAD_FOLDER'] = 'images/'+foldername
      print foldername"""
      f = form.photo.data
        # check if the post request has the file part
      if f is not None:  
        if allowed_file(f.filename):
          filesaver = filesave(form.caption.data)
          filesaver.storefile()
          filename = secure_filename(f.filename)
          filename = str(datetime.datetime.now()) + filename
          #if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'])):
            #os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']))
            #print "folder created"
          f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          return redirect(url_for('home'))
        print 'invalid file'
  return render_template("home.html", form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

""""A for loop has been implemented to iterate over the captions and files"""
@app.route('/preview/')
def preview():
  if 'email' not in session:
    return redirect(url_for('login'))
  """foldername= session['email'].split('@')[0]    
  app.config['UPLOAD_FOLDER'] = 'images/'+foldername"""
  captions= []
  revcaps = []
  images=[]
  global offset
  print os.path.isdir(app.config['UPLOAD_FOLDER'])
  #if os.path.exists(app.config['UPLOAD_FOLDER']):
  images = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
  images.sort(reverse=True)
  images = images[0:10]
  f = open("filecaptions.txt", "r")
  for line in f:
    captions.append(line)
  for caption in captions:
    revcaps.insert(0,caption)
  revcaps = revcaps[0:10]
  return render_template('preview.html',images_captions=zip(images,revcaps))

"""A list slicing function has been used to display only the required 10 images"""
@app.route('/preview/next/')
def previewnext():
  if 'email' not in session:
    return redirect(url_for('login'))
  captions= []
  revcaps = []
  images = []
  #if os.path.exists(app.config['UPLOAD_FOLDER']):
  images = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
  #offset=0
  global offset
  if offset+10 < len(images):
    offset=offset+10
  #offset=offset + len(images)%10
  images.sort(reverse=True)
  images = images[offset:offset+10]
  f = open("filecaptions.txt", "r")
  for line in f:
    captions.append(line)
  for caption in captions:
    revcaps.insert(0,caption)
  revcaps = revcaps[offset:offset+10]
  return render_template('preview.html',images_captions=zip(images,revcaps))

"""A list slicing function has been used to display only the required 10 images"""
@app.route('/preview/prev/')
def previewprev():
  if 'email' not in session:
    return redirect(url_for('login'))
  captions= []
  revcaps = []
  images =[]
  global offset
  if offset != 0:
    offset=offset-10
  #if os.path.exists(app.config['UPLOAD_FOLDER']):
  images = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
  images.sort(reverse=True)
  images = images[offset:offset+10]
  f = open("filecaptions.txt", "r")
  for line in f:
    captions.append(line)
  for caption in captions:
    revcaps.insert(0,caption)
  revcaps = revcaps[offset:offset+10]
  return render_template('preview.html',images_captions=zip(images,revcaps))
	#return send_from_directory('pt.html',image)

""""The send_from_directory function is used to render files from a specific directory in the server"""
@app.route('/uploads/<filename>')
def uploaded_file(filename):
  if 'email' not in session:
    return redirect(url_for('login'))
  #foldername= session['email'].split('@')[0]    
  #app.config['UPLOAD_FOLDER'] = 'images/'+foldername
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

"""Signup form is used to capture data from a new user. A session is used to prevent the user from logging in multiple times"""
@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = user(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      newuser.store()
      session['email'] = newuser.email     
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

"""On logging out the users session is ended by popping out the user's email from the session"""
@app.route("/logout", methods=["GET","POST"])
def logout():
  session.pop("email",None)
  return redirect(url_for('index'))

"""Port 5000 is used for further integration with Mongodb"""
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


