from flask import *
from datetime import datetime
from dbModel import *
import json
import jieba
import codecs
import jieba.analyse
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """
    data = "Deploying a Flask App To Heroku"
    
    data_UserData = UserData.query.all()
    history_dic = {}
    history_list = []
    for _data in data_UserData:
        history_dic['Name'] = _data.Name
        history_dic['Id'] = _data.Id
        history_dic['Description'] = _data.Description
        history_dic['CreateDate'] = _data.CreateDate.strftime('%Y/%m/%d %H:%M:%S')
        history_list.append(history_dic)
        history_dic = {}
    """
    return render_template('index.html')

@app.route('/wall')
def wall():
    return render_template('wall.html')

@app.route('/test')
def test():
    return json.dumps(getComplains())

@app.route('/testj',methods = ['POST', 'GET'])
def testj():
    print("斷詞中...")
    jieba.load_userdict("userdict.txt")
    jieba.analyse.set_stop_words("stopword.txt")
    hash = {}
    for paragraph in getComplains():
        #print(paragraph["complain_content"])
        seg_list = jieba.analyse.extract_tags(paragraph["complain_content"])#jieba.cut(paragraph["complain_content"],cut_all=False)
        for word in seg_list:
            if word in hash:
                hash[word]+=1
            else:
                hash[word] = 1
                #print(word)
    return str(hash)

@app.route('/testj2',methods = ['POST', 'GET'])
def testj2():
    print("斷詞中...")
    jieba.load_userdict("userdict.txt")
    jieba.analyse.set_stop_words("stopword.txt")
    hash = {}
    id = 0
    for paragraph in getComplains():
        id+=1
        #print(paragraph["complain_content"])
        seg_list = jieba.analyse.extract_tags(paragraph["complain_content"])#jieba.cut(paragraph["complain_content"],cut_all=False)
        for word in seg_list:
            if word in hash:
                hash[word][0]+=(1+0.5*paragraph["agree_number"])
                if paragraph["agree_number"]>=hash[word][2]:
                    hash[word][1]=id
                    hash[word][2]=paragraph["agree_number"]
            else:
                hash[word] = [(1+0.5*paragraph["agree_number"]),id,paragraph["agree_number"]]
                #print(word)
    return str(hash)

@app.route('/texts',methods = ['POST','GET'])
def texts():
    try:
        tex_id = int(request.args.get('name_id'))
        whole_data = getComplains()
        content = whole_data[tex_id-1]["complain_content"]
        agree_num = whole_data[tex_id-1]["agree_number"]
        return render_template('text.html',name_id = tex_id, text = content, agree = agree_num)
    except:
        return render_template('text0.html')
@app.route('/API/add_data', methods=['POST'])
def add_data():
    name = request.form['name']
    description = request.form['description']
    if name != "" and description != "":
        add_data = UserData(
            Name=name,
            Description=description,
            CreateDate=datetime.now()
        )
        db.session.add(add_data)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
