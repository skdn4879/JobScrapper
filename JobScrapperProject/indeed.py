import requests
from bs4 import BeautifulSoup

LIMIT = 50
#URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"
#URL = "https://kr.indeed.com/jobs?q=python&limit=50&radius=25"

def get_last_page(URL): #페이지 갯수
  '''indeed_result = requests.get("https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch")'''

  result = requests.get(URL)
  # URL 가져오기

  soup = BeautifulSoup(result.text, "html.parser")
  #URL의 전체 html 가져오기

  pargination = soup.find("ul", {"class" : "pagination-list"})
  #html에서 pagination-list라는 클래스명을 가진 ul을 가져온다.

  links = pargination.find_all('a')
  #pargination의 모든 a태그를 가져와 리스트 생성
  pages = []

  for link in links[:-1]:
    pages.append(int(link.string))
    #links의 모든 a태그에서 글자만 가져와 리스트에 넣어준다.
    #우리는 int형을 원하므로 바꿔줘야한다.

    #pages.append(link.find("span").string)
    #links의 span태그들의 글자만 가져와 리스트에 넣어준다. 위와 똑같이 동작
    #단 위와 같이 동작하려면 해당 태그와 모든 하위 태그에 string이 1개여야 함 

  #pages = pages[:-1]
  #마지막에 숫자가 아닌 부분을 제거해준다. 위처럼 애초에 조건문을 달아도된다.

  max_page = pages[-1]
  return max_page #마지막 페이지 반환

def extract_jobs(html): #일자리 목록을 받아 정보 반환
  '''title = i.find("h2", {"class" : "title"})
  #results안의 html중 class명이 title인 모든 h2태그를 받아옴
  anchor = title.find("a")["title"]
  #title안의 html중 a태그의 title속성을 받아옴'''
    
  title = html.find("h2", {"class" : "title"}).find("a")["title"]
  #위의 코드를 한줄로 만들어준 것
  #find는 첫번째로 찾은 결과를 보여준다.

  company = html.find("span", {"class" : "company"})
  if company is not None:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = company_anchor.string
    else:
      company = company.string
    company = company.strip() #맨 마지막의 개행문자 제거, ()안에 문자를 넣으면 해당 문자 제거
  else:
    company = "정보없음"

  location = html.find("div", {"class" : "recJobLoc"})["data-rc-loc"]
  #indeed의 html을 보면 알겠지만 위와 아래는 내용은 같다.
  #location = html.find("span", {"class" : "location accessible-contrast-color-location"}).string

  link = html.find("h2", {"class" : "title"}).find("a")["href"]
  #link = "https://kr.indeed.com" + link
  link = f"https://kr.indeed.com{link}"
  
  return {'title': title, 'company': company, 'location': location, 'link': link}

def extract_indeed_jobs(last_page, URL): #실제 직업들을 추출
  jobs = []

  #페이지가 넘어갈때의 규칙성을 찾아 적용
  for page in range(last_page):
    print(f"Scrapping indeed Page: {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    #페이지가 넘어갈때의 규칙성을 찾아 적용

    soup = BeautifulSoup(result.text, "html.parser") #html 문서 받아옴
    results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
    #모든 일자리를 받아옴 class명이 jobsearch-SerpJobCard인 모든 div태그를 리스트로 생성, find_all은 리스트 전부를 가져옴

    for result in results:  #위의 div리스트의 각각의 값에 result가 접근
      job = extract_jobs(result) #해당 일자리 html을 함수에 넣어줌
      jobs.append(job)

  return jobs

def get_jobs(word):

  URL = f"https://kr.indeed.com/jobs?q={word}&limit={LIMIT}&radius=25"

  last_page = get_last_page(URL)

  jobs = extract_indeed_jobs(last_page, URL)

  return jobs