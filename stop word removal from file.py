from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
file=open("docc.txt","r")



example_sent =file.read()

stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(example_sent)

filtered_sentence = []

for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)
freq={}
for i in filtered_sentence:
    if i not in freq.keys():
        freq[i]=0
    freq[i]+=1
print()
print ("The frequency is:")
print()
print (freq)
    
