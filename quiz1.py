from bs4 import BeautifulSoup
import requests
import nltk#for tokenising

def checkurl(s):
    if "www" in s:
        return s
    else:
        return "www."+s

def crawl(url):         #fetches the code in that url
    r  = requests.get(url, "lxml")
    data = r.text
    soup = BeautifulSoup(data)
    return soup

H = {}#storing urls and no. of times url appeared
dict_tokens = {}#dict:- tokens: urls and no of times the token is present
n = 0
urls = []#store all the read urls in a list
search_list=[]

def crawler(url):
    global urls
    global n
    global dict_tokens

    n = n+1
    if (n <= 10) :
        crawlresult = crawl(url)
        for script in crawlresult(["script", "style"]):#removing unnecessary part
            script.extract()

        text = crawlresult.get_text()#it has only useful data which is text
        lines = (line.strip() for line in text.splitlines())
        #str.strip() is used to remove the extra white spaces around the string
        #str.splitlines() is used to split the string having \n and append each line as an element in a list
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # print(text)
        tokens = nltk.word_tokenize(text)#list of tokens

        domain = url.split('/')[2]

        for token in tokens:
            if token in dict_tokens.keys():
                if domain in dict_tokens[token].keys():
                    dict_tokens[token][domain] = dict_tokens[token][domain] + 1
                else:
                    dict_tokens[token][domain] = 1
            else:
                dict_tokens[token] = {}
                dict_tokens[token][domain] = 1
        print("The dictionary of tokens: ")
        print(dict_tokens)

        for link in crawlresult.find_all('a'):#all the links are with tag 'a'
            webad = link.get('href')#href=web adderss
            if "http" in str(webad):
                parts = webad.split("/")
                addr = checkurl(str(parts[2]))
                if addr in H:
                    H[addr] = int(H[addr]) + 1
                else:
                    H[addr] = 1
                    if addr in url:
                        pass
                    else:
                        urls.append(webad)
                        crawler(webad)

crawler('https://www.apple.com')

mat = {}

for key in dict_tokens.keys():
    mat[key] = []
    # print(key, dict_tokens[key])
    for dom in urls[0:9]:
        k = dom.split('/')[2]
        if k in dict_tokens[key].keys():
            mat[key].append(dict_tokens[key][k])
        else:
            mat[key].append(0)

print("All the urls gatehered: ")
print("=======================================")
inp1=input("Enter a single charecter <x>")
inp2=input("Enter a single charecter <y>")
search=inp1+inp2
print("searching for: ",search,"in all tokens")
print("------------------SEARCH---------------")
for token in dict_tokens.keys():
    if search in token:
        search_list.append(token)

print("The list of words containing the entered charecters by user: ")
print(search_list)
print("")
