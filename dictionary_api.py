from flask import Flask, render_template, request, flash, url_for
import requests, json, pprint
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def index():
    image=os.path.join('static', 'YouWord.jpg')
    return render_template('index.html', image=image)


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
            flash(u'Word sucessfully found!', 'success')
            return render_template('index.html', search = search, definition=definition, emoji=emoji, example=example, image=image, type=type, pronunciation=pronunciation)
        else:
            if r.status_code== 404:
                flash(u'Word not found!', 'error')
                return render_template('index.html')

    else:
        flash(u'Introduce a word!', 'nodata')
        return render_template('index.html')
        
    
    
if __name__ == '__main__':
    app.run(debug=True)