from bs4  import BeautifulSoup
import requests
import math

# crawl_link="http://www.amazon.com"
crawl_link="http://www.sridhama.com"

links=[]#list to store all the links crawled
links.append(crawl_link)
dict_out={}#key:val is link:links in the link
indegree={}#link:indegree
outdegree={}
d=0

def getdomain(link):
    if "http" in link:
        parts=link.split("/")
        link= parts[2]
    return link

# def checkwwwurl(s):
#     if "www" in s:
#         return s
#     else:
#         parts=s.split("//")
#         part1=parts[0]
#         part2="www."+parts[1]
#         return part1+"//"+part2

def crawl(url):
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    dict_out[url]=[]
    for link in soup.find_all('a'):
        addr=link.get('href')
        addr=str(addr)
        try:
            if(addr[:4]=="http"): # and (len(links)<=1000):
                links.append(addr)
                dict_out[url].append(addr)
                # print("added")
            else:
                continue
        except Exception as e:
            print(addr)
            print(e)
    return dict_out

for link in links:
    if(d<=100):
        d=d+1
        crawl(link)

for link in links:#to get how many links point to link in dict
    indegree[link]=0
    for key in dict_out.keys():
        if key!=link:
            if link in dict_out[key]:
                indegree[link]+=1

for link in links:
    outdegree[link]=0
    for key in dict_out.keys():
        if key==link:
            outdegree[link]=len(key)

print(dict_out)
# print("====================")
print("LINKS: ")
print(links)
print("==============")
print("INDEGREES: ")
print(indegree)
print("==============")
print("OUTDEGREES:")
print(outdegree)

quiz={k:None for k in outdegree.keys()}

for link in links:
    try:
        quiz[link]=(indegree[link]/outdegree[link])
    except ZeroDivisionError:
        quiz[link]=math.inf

print("============")

for i in sorted(quiz, key=quiz.get,reverse=True):
    print(i,quiz[i])
