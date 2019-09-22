from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import operator

finLinks = []
allLinksVisited = set()

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    if newUrl not in allLinksVisited:
                        self.links = self.links + [newUrl]
                        allLinksVisited.add(newUrl)
    
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        #print(response)
        allLinksVisited.add(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]



        
def spider(url, words, maxPages):  
    pagesToVisit = [url]
    pagesFound = 0
    numberVisited = 0
    foundWord = False
    while pagesFound < maxPages and pagesToVisit != []:
        #print(pagesToVisit)
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]

        parser = LinkParser()
        data = ""
        links = []
        try:    
            data, links = parser.getLinks(url)
        except:
            pass
        s = set()
        for word in words:
            if data.find(word)>-1 and url not in s:
                pagesFound = pagesFound + 1
                print(pagesFound, "Visiting:", url)
                s.add(url)
                finLinks.extend([url])
                foundWord = True
                with open(str(pagesFound)+'.txt','w',encoding="utf-8") as f:
                    f.write(cleanHtml(data))
                #print(url)
                pagesToVisit = pagesToVisit + links
        
            
    if not foundWord:
        print("Word never found")


def cleanHtml(html):
    soup = BeautifulSoup(html,'html.parser') 
    for script in soup(["script", "style"]): 
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text



def stopWordRemoval(fileName):
    with open(fileName,'r', encoding="utf-8") as f:
        text = f.read()    
        
    stop_words = set(stopwords.words('english'))
    stop_words.add('.')
    stop_words.add(',')
    stop_words.add('!')

    word_tokens = word_tokenize(text)

    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    return filtered_sentence


def main():
    query = ['secure','dreamhost','Virtual', 'Private', 'Servers']
    n = 50
    spider('https://www.dreamhost.com',query,n)
    a = dict()
    b = dict()
    lengthdocuments = dict()
    lengthd = 0
    for i in range(len(finLinks)):
        lengthd = 0
        filtered_sentence = stopWordRemoval(str(i+1)+'.txt')
        for x in filtered_sentence:
            w = x.lower()
            if w in a.keys():
                if a[w][-1][0] == i+1:
                    a[w][-1][1] = a[w][-1][1]+1
                    b[w][-1][1] = math.log10(a[w][-1][1])+1
                else:
                    a[w].append([i+1,1])
                    b[w].append([i+1,1])
            else:
                a[w] = []
                b[w] = []
                b[w].append([i+1,1])
                a[w].append([i+1,1])
        for x in filtered_sentence:
            lengthd += b[x.lower()][-1][1]**2
        lengthdocuments[i+1] = math.sqrt(lengthd)
    
    #print(a)
    #print(b)
    
    idf=dict()
    for w in query:
        x = w.lower()
        idf[x]=math.log10(n/len(a[x]))
    
    for w in query:
        x = w.lower()
    
    querytf = dict()
    for w in query:
        x = w.lower()
        if x in querytf.keys():
            querytf[x]=math.log10(querytf[x])+1
        else:
            querytf[x]=1
    #print(querytf)
    
    #print(idf)
    
    for w in querytf:
        querytf[w] = idf[w]*querytf[w]
    #print(querytf)
    
    lengthquery = 0
    for w in querytf:
        lengthquery += querytf[w]**2
    lengthquery = math.sqrt(lengthquery)
    #print(lengthquery)
    

    wt = dict()
    for w in query:
        x = w.lower()
        for doc in b[x]:
            if x in wt.keys():
                wt[x].append([doc[0],idf[x]*doc[1]])
            else:
                wt[x] = []
                wt[x].append([doc[0],idf[x]*doc[1]])
    #print(wt)
    
    
    result = dict()
    for w in querytf:
        for x in wt[w]:
            if x[0] in result.keys():
                result[x[0]] += querytf[w]*x[1]
            else:
                result[x[0]] = querytf[w]*x[1]
    
    for w in result:
        result[w] = result[w]/(lengthquery * lengthdocuments[w])
        #print(lengthdocuments[w])
    
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    sorted_result.reverse()
    print()
    i=0
    for x,y in sorted_result:
        if i==10:
            break
        print(str(finLinks[x-1])+'\t'+str(y))
        i+=1
    #print(result)
        
main()
