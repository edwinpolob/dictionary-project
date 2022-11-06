from flask import Flask, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, json, pprint
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dictionary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db=SQLAlchemy(app)

class Word (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    word=db.Column(db.String(20))
    definition=db.Column(db.String(300))
    image=db.Column(db.String(300))



@app.route('/')
def index():
    image=os.path.join('static', 'YouWord.jpg')
    return render_template('index.html', image=image, imagen1=image, imagen2=image, imagen3=image)


@app.route("/", methods=['GET', 'POST'])
def search_word():
    search = request.form['word']
    if search != "":
        url= "https://owlbot.info/api/v4/dictionary/"
        headers= {"Authorization": "Token 0f08124df3c64f57bf147caa8eb247dae3d9e6d0"}
        r= requests.get(url+search, headers=headers)
        if r.status_code==200:
            datos = json.loads(r.content)
            definition=datos['definitions'][0]['definition']
            emoji=datos['definitions'][0]['emoji']
            example=datos['definitions'][0]['example']
            
            if datos['definitions'][0]['image_url'] != None:
                image=datos['definitions'][0]['image_url']
            else:
                image=os.path.join('static', 'No_Image_Available.jpg')
            type=datos['definitions'][0]['type']
            pronunciation=datos['pronunciation']
            Objectword=Word(word=search, definition=definition, image=image)
            db.session.add(Objectword)
            db.session.commit()
            wordlist=Word.query.all()
            palabra1=wordlist[-2:][0].word
            definicion1=wordlist[-2:][0].definition
            imagen1=wordlist[-2:][0].image
            palabra2=wordlist[-3:][0].word
            definicion2=wordlist[-3:][0].definition
            imagen2=wordlist[-3:][0].image
            palabra3=wordlist[-4:][0].word
            definicion3=wordlist[-4:][0].definition
            imagen3=wordlist[-4:][0].image
            flash(u'Word sucessfully found!', 'success')
            return render_template('index.html', search = search, definition=definition, image=image, palabra1=palabra1, definicion1=definicion1, imagen1=imagen1, palabra2=palabra2, definicion2=definicion2, imagen2=imagen2, palabra3=palabra3, definicion3=definicion3, imagen3=imagen3)
        else:
            if r.status_code== 404:
                flash(u'Word not found!', 'error')
                return render_template('index.html')

    else:
        flash(u'Introduce a word!', 'nodata')
        return render_template('index.html')
        


    
if __name__ == '__main__':
    app.run(debug=True)