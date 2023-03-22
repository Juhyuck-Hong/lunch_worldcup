from flask import Flask, render_template, request, jsonify
import random
from pymongo import MongoClient
from pprint import pprint
import json

with open('mongoDB_auth.json', 'r') as j:
    auth = json.load(j)

id = list(auth.keys())[0]
pw = auth[id]

client = MongoClient(f'mongodb+srv://{id}:{pw}@juhyukhong.q0dawlr.mongodb.net/?retryWrites=true&w=majority')
db = client.lunch_worldcup

app = Flask(__name__)

foods = {'감자탕': 'https://health.chosun.com/site/data/img_dir/2021/01/26/2021012602424_0.jpg',
 '고등어구이': 'https://recipe1.ezmember.co.kr/cache/recipe/2019/10/14/eafe70f3fbb6b6cdfbc8f8a1283f0c011.jpg',
 '김밥': 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Gimbap_%28pixabay%29.jpg',
 '돈까스': 'https://cdn.clien.net/web/api/file/F01/7262338/14b0f13e08ca3f.jpg',
 '돈부리': 'https://rimage.gnst.jp/livejapan.com/public/article/detail/a/00/05/a0005066/img/ko/a0005066_main.jpg',
 '떡볶이': 'https://funshop.akamaized.net/products/0000098549/vs_image800.jpg',
 '라면': 'https://img.insight.co.kr/static/2017/12/13/2000/9mg762010d3cw399d659.jpg',
 '만두국': 'https://recipe1.ezmember.co.kr/cache/recipe/2021/02/06/d0d6c059f08600bb14b23ed917b064141.jpg',
 '백반': 'https://cloudfront-ap-northeast-1.images.arcpublishing.com/chosun/P4YBXVVUCMS3P7KDH2IKMGELC4.jpg',
 '버거': 'https://cloudfront-ap-northeast-1.images.arcpublishing.com/chosunbiz/T76RHKX27GOS5BHD6LCD5W6DNQ.jpg',
 '볶음밥': 'https://i.ytimg.com/vi/S_glK_h78xI/maxresdefault.jpg',
 '불고기': 'https://recipe1.ezmember.co.kr/cache/recipe/2019/03/03/11baafbe81803965b17c3ab42a5992cb1.jpg',
 '비빔밥': 'https://i.pinimg.com/originals/d5/b3/ba/d5b3ba6572223074aed75a6daf945d5a.jpg',
 '삼겹살': 'https://mp-seoul-image-production-s3.mangoplate.com/mango_pick/uker6u9xhkr1m8.jpg',
 '샌드위치': 'https://recipe1.ezmember.co.kr/cache/recipe/2021/12/23/8f1022f46829257d51b21cf1d08d72241.jpg',
 '샐러드': 'https://src.hidoc.co.kr/image/lib/2021/2/17/1613545788294_0.jpg',
 '샤브샤브': 'https://www.elandretail.com/upload/20170828170024_0.jpg',
 '수제비': 'https://recipe1.ezmember.co.kr/cache/recipe/2016/07/28/f563617e4c5f769e84377e0ee4668e621.jpg',
 '스테이크': 'https://recipe1.ezmember.co.kr/cache/recipe/2017/07/09/6741acc7f6bf0f7d04245851fb365c311.jpg',
 '쌀국수': 'https://i.pinimg.com/originals/bd/7f/a4/bd7fa4ec8ea81665e4608df059d940be.jpg',
 '야채볶음': 'https://recipe1.ezmember.co.kr/cache/recipe/2019/04/07/d50dbf8eb8668092c11828dc9d39260d1.jpg',
 '짜장면': 'https://recipe1.ezmember.co.kr/cache/recipe/2021/10/26/8f82be9c22ec2f4f9ab25363cc611b141.jpg',
 '짬뽕': 'https://recipe1.ezmember.co.kr/cache/recipe/2017/06/19/2756808e5603db7a18c4f5ee9a699ee41.jpg',
 '초밥': 'https://watermark.lovepik.com/photo/50053/3820.jpg_wh1200.jpg',
 '치킨 텐더': 'https://recipe1.ezmember.co.kr/cache/recipe/2017/12/19/e0df7cee9917c1e0bb31bd9645d0d3791.jpg',
 '콩국수': 'https://src.hidoc.co.kr/image/lib/2019/7/25/20190725103200889_0.jpg',
 '타코': 'https://recipe1.ezmember.co.kr/cache/recipe/2020/06/17/41f36e22404c059d9750b8eabcddb77f1.jpg',
 '탕수육': 'https://homecuisine.co.kr/files/attach/images/142/073/002/99b983892094b5c6d2fc3736e15da7d1.JPG',
 '파니니': 'https://www.newiki.net/w/images/thumb/f/ff/Panini.jpg/1200px-Panini.jpg',
 '파스타': 'https://recipe1.ezmember.co.kr/cache/recipe/2019/04/01/f8b3042c80a214dd7cc60fa2027cdc9d1.jpg',
 '피자': 'https://recipe1.ezmember.co.kr/cache/recipe/2022/08/04/8f6d10f605eb2f763bf8c0a94947c81f1.jpg',
 '햄버거 스테이크': 'https://recipe1.ezmember.co.kr/cache/recipe/2015/09/22/6308008dd029eb6235a02d7f339e5796.jpg'}

rivers_set = 32

def choose_random(pool, num_pick=1, not_to_pick=[]):

    if len(not_to_pick) >= len(pool)-1:
        return {}
    else:
        pick = []
        while len(pick) < num_pick:
            pick_one = random.choice(list(pool.keys()))
            if pick_one in not_to_pick:
                pass
            else:
                pick.append(pick_one)
            pick = list(set(pick))

        candidate = {i: foods[i] for i in pick}

        return candidate


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/worldcup')
def worldcup():
   return render_template('worldcup.html')

@app.route("/autosave", methods=["POST"])
def autosave_post():
    new_chosen = request.form["new_chosen"]
    new_dropped = request.form["new_dropped"]
    
    # 선택한 메뉴 업데이트 
    chosen = request.form["chosen"]
    if chosen:
        chosen = chosen.split(',') + [new_chosen]
    else:
        chosen = [new_chosen]
    chosen = list(set(chosen))

    # 비선택 메뉴 업데이트
    dropped = request.form["dropped"]
    if dropped:
        dropped = dropped.split(',') + [new_dropped]
    else:
        dropped = [new_dropped]
    dropped = list(set(dropped))  

    # 새로운 메뉴 2개 추출 {name1: url1, name2: url2}
    # 선택과 비선택 합계가 rivers_set과 같으면 해당 차수 종료
    if len(chosen) + len(dropped) == rivers_set and len(chosen) == 1:    
        msg = "done"
    elif len(chosen) + len(dropped) == rivers_set:    
        rivers = str(rivers_set - len(dropped))
        chosen = []
        msg = f"{rivers}강 시작!"
    else:
        msg = "playing"
    
    # POST 돌려보낼 Json
    res = {"chosen":  ','.join(chosen),
           "dropped": ','.join(dropped),
           "candidate": choose_random(foods, num_pick=2, not_to_pick=dropped+chosen)}
    # 같이 보낼 메시지 추가
    res.update({"msg": msg})
    
    print("chosen:", len(chosen), chosen)
    print("dropped:", len(dropped), dropped)

    return jsonify(res)

@app.route("/autosave", methods=["GET"])
def autosave_get():
    return jsonify(choose_random(foods, num_pick=2))

@app.route("/results", methods=["POST"])
def result_post():
    user_name = request.form["user_name"]
    chosen_name = request.form["chosen_name"]
    doc = {'name': user_name,
           'result': chosen_name}
    db.results.insert_one(doc)
    return jsonify({'msg': '점심메뉴 월드컵 완료!'})

@app.route("/results", methods=["GET"])
def result_get():
    all_list = list(db.results.find({}, {'_id':False}))
    res = []
    for i in all_list:
        temp = i.update({"url": foods[i["result"]]})
        res.append(i)
    return jsonify({'results': res})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)