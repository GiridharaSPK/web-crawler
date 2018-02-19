from bs4  import BeautifulSoup
import requests

# crawl_link="http://www.amazon.com"
crawl_link="http://www.sridhama.com"


links=[]#list to store all the links crawled
links.append(crawl_link)
dict_out={}#key:val is link:links in the link
indegree={}#link:indegree
outdegree={}


# In[4]:


# def getdomain(link):
#     if "http" in link:
#         parts=link.split("/")
#         link= parts[2]
#     return link


# In[5]:


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
            if(addr[:4]=="http") and (len(links)<=100):
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
        quiz[link]=1000000

# for key, value in sorted(quiz.iteritems(), key=lambda (k,v): (v,k)):
#     print "%s: %s" % (key, value)

