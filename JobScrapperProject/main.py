from flask import Flask #flask는 파이썬으로 웹을 만드는 프레임워크
from flask import render_template #template을 렌더링 해줌
from flask import request #query argument를 받기위해 import함
from flask import redirect #경로 재설정을 위해
from flask import send_file #파일 저장을 위해
from indeed import get_jobs as get_indeed_jobs
from jobkorea import get_jobs as get_jobkorea_jobs
from exporter import save_to_file

app = Flask("SuperScrapper") #앱 생성의 기초 app = Flask("앱이름")

db = {} #매번 스크래핑을 기다릴 순 없으니 FakeDB를 만들어준다.
#이것을 이용하면 처음에만 스크래핑하고 이미 검색한 키워드를 다시 검색하면 순식간에 내용이 나오게 된다.
#route밖에 선언해야 지워지지 않는다. 안에 선언하면 매번 초기화 된다.

@app.route("/") #사용자의 입력 url에 따라 작용하는 @데코레이터
  #url path에서 /는 가장 상위의 root를 의미, 즉 여기서는 url에 접속하면 바로 나오는 메인 페이지를 의미
  #데코레이터는 자기 바로 아래의 함수를 찾는다. 데코레이터 아래에는 함수만 올 수 있다.
def home():
  return render_template("home.html") #render_template("html문서 이름") 미리 만들어둔 html문서를 불러오게 할 수 있다.

@app.route("/report") #html에서 검색어를 입력하면 report url로 이동하면서 검색어를 넘겨주니까 이동했을 때의 반응을 설정
def report():
  word = request.args.get('word') #html에서 required name = "word" 즉 검색어를 넘겨주니까 그 검색어를 받아오는 역할
  if word: #word가 존재하면
    word = word.lower()
    existingJobs = db.get(word) #이미 한번 검색한 내용이 있는지 확인
    if existingJobs: #내용이 있으면
      jobs = existingJobs #기다릴 필요없이 있는 걸 바로 출력
    else: #내용이 없으면
      indeed_jobs = get_indeed_jobs(word)
      jobkorea_jobs = get_jobkorea_jobs(word)
      jobs = indeed_jobs + jobkorea_jobs #스크래핑한 뒤
      db[word] = jobs #db에 넣어준다. db['키 값']
  else: #word가 존재하지 않으면
    return redirect("/") #메인 페이지로 이동
  return render_template("report.html", searching=word, resultsNumber=len(jobs), jobs=jobs)
  #report.html에 가면 보일텐데 report문서는 searching이라는 변수를 사용한다. 그래서 report.html에 searching값을 word로 넣어준것
  #flask는 html을 렌더링하고 {{}}안에 우리가 넣어준 변수를 보여준다.

@app.route("/export") #다운로드 페이지
def export():
  try: #처음 시도되는 부분
    word = request.args.get('word')
    if not word: #word가 존재하지 않으면
      raise Exception() #except부분 실행
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return send_file(f"{word}_jobs.csv")
  except: #try구문이 에러가 날 시 실행
    return redirect("/")

'''@app.route("/second") #사용자가 /second에 접속하면 실행
def second(): #함수의 이름은 똑같이 않아도 된다.
  return "second page"

@app.route("/<username>") #<>는 placeholder로 입력값을 사용자에게 맡긴다는 것이다.
def potato(username):
  return f"hello {username}" #<>안의 값은 사용해주어야 한다. 안그럼 에러가 발생한다.
  #이것이 dynamin Url의 기본이다. 메인페이지url/사용자입력(id) 등을 입력했을때 인스타그램 등에서 해당 계정페이지로 바로 이동할 수 있는 원리이다. (db에서 username이 일치하는 것을 찾아주는 예))'''

app.run(host="0.0.0.0") #앱 실행의 기초 host="0.0.0.0"은 repl에서 실행