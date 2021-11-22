import requests
from bs4 import BeautifulSoup

start = 1
#URL = f"http://www.jobkorea.co.kr/Search/?stext=python&tabType=recruit"

def get_last_page(URL):
  result = requests.get(f"{URL}&Page_No={start}")
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class" : "tplPagination"}).find("ul")
  links = pagination.find_all('a')
  pages = []

  for link in links:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page

def extract_jobs(html):
  #find_all("span", recursive = false)  //모든 span 태그를 가져오는 걸 방지, span안에 span이 들어있을 때 사용(첫 리스트만 반환)
  #만약 find_all("span")이 두 개의 리스트를 가져온다면? company와 location이 하나의 div안에 들어있다면? company, location = html.find("div", {"class" : "company"}.find_all("span", recursive = false)) 이런식으로 한번에 지정해줄 수 있다.(unpacking)

  div = html.find("div", {"class" : "post"})
  info = div.find("div", {"class" : "post-list-info"})
  company = div.find("div", {"class" : "post-list-corp"})
  title = info.find("a", {"class" : "title"})["title"]
  company_name = company.find("a", {"class" : "name"})["title"]
  location = info.find("p", {"class" : "option"}).find("span", {"class" : "loc long"}).string #여기서 개행문자를 제거하려면 .strip("\n") 또는 .strip("\r")을 해주면 된다.
  '''exp = info.find("p", {"class" : "option"}).find("span", {"class" : "exp"}).string
  edu = info.find("p", {"class" : "option"}).find("span", {"class" : "edu"})
  if edu is None:
    edu = "미지정"
  else:
    edu = edu.string
  day = info.find("p", {"class" : "option"}).find("span", {"class" : "date"}).string'''''
  job_id = html["data-gno"]
  link = f"http://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}?Oem_Code=C1&logpath=1"

  return {'title': title, 'company': company_name, 'location': location, 'link': link}

def extract_jobkorea_jobs(last_page, URL):
  jobs = []

  for page in range(last_page):
    print(f"Scrapping jobkorea Page: {page}")
    result = requests.get(f"{URL}&Page_No={start + page}")
    soup = BeautifulSoup(result.text, "html.parser")
    body = soup.find("div", {"class" : "recruit-info"})
    results = body.find_all("li", {"class" : "list-post"})

    for result in results:
      job = extract_jobs(result)
      jobs.append(job)
  
  return jobs

def get_jobs(word):

  URL = f"http://www.jobkorea.co.kr/Search/?stext={word}&tabType=recruit"

  last_page = get_last_page(URL)

  jobs = extract_jobkorea_jobs(last_page, URL)

  return jobs