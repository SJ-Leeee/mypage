from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where() 
client = MongoClient('mongodb+srv://sparta:test@cluster0.ixlq5pz.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca) 
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/members", methods=["POST"])
def members_post():
    name_receive = request.form['name_give']
    mbti_receive = request.form['mbti_give']
    motive_receive = request.form['motive_give']
    blog_receive = request.form['blog_give']
    github_receive = request.form['github_give']

    doc = {
        'name':name_receive,
        'mbti':mbti_receive,
        'motive':motive_receive,
        'blog':blog_receive,
        'github':github_receive,
    }
    db.members.insert_one(doc)

    return jsonify({'msg':'저장완료'})

@app.route("/members", methods=["GET"])
def web_members_get():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result': all_members})

@app.route('/secondpage') # guestbooks로 했을 때 오류
def guestbooks():
    return render_template('secondpage.html')

@app.route("/guestbooks", methods=["POST"])
def guestbooks_post():
    name_receive = request.form['name_give']
    guestbook_receive = request.form['guestbook_give']

    doc = {
        'name':name_receive,
        'guestbook':guestbook_receive
    }
    db.guestbooks.insert_one(doc)

    return jsonify({'msg':'저장완료'})

@app.route("/guestbooks", methods=["GET"])
def web_guestbooks_get():
    all_guestbooks = list(db.guestbooks.find({},{'_id':False}))
    return jsonify({'result': all_guestbooks})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)