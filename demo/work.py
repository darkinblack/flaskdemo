# import random
# random.choice('abcdefghijklmnopqrstuvwxyz')
# random.randint(4,15)
# with open('interests', 'w') as f:
#
#     for i in range(100):
#         interest = ''
#         for wordlenth in range(random.randint(4,15)):
#             interest+=random.choice('abcdefghijklmnopqrstuvwxyz')
#         f.write(interest)
#         f.write('\n')
#
#
#
#
#
# position caculate
#_________________________________________________________________________________________________________
# from haversine import haversine, Unit
#
# lyon = (45.759712, 4.842212) # (lat, lon)
# paris = (45.759716, 4.842216)
#
# print(haversine(lyon, paris))






# creat data.json
#__________________________________________________________
# import time
# import gensim.downloader
#
# vector = gensim.downloader.load('glove-twitter-25')
# print(vector.most_similar("apple"))
# t0 = time.time()
#
#
import json
# import pandas as pd
# hobbies = pd.read_csv("hobbies.csv")
# dic = {}
# for i in hobbies['HOBBIES']:
#     if i.find(" ") == -1 and i.find('/') == -1:
#         i = i.lower()
#         try:
#             dic[i] = [result[0] for result in vector.most_similar(i)]
#         except:
#             pass
# print(dic)
#
# with open('data.json', 'r') as f:
#     data = json.load(f)
#
# print(list(data.keys())[20])
# print(len(data))
# import pandas as pd
# class keywords:
#     def __init__(self):
#
#         self.data = pd.read_csv("/Users/zhaolunshi/Desktop/flaskdemo/demo/unigram_freq.csv")
#         self.interest = list(self.data['word'])
#         self.interest = [x for x in self.interest if isinstance(x,str)]
#         # self.vector = gensim.downloader.load('glove-twitter-25')
#
# n = keywords()
# for i in n.interest:
#     if not isinstance(i,str):
#         print(i,type(i))
# print(type(n.interest))

# import gensim.downloader
#
# vector = gensim.downloader.load('glove-twitter-25')
#
# similar_interest = vector.most_similar("handjobs")
# good_interest = [x[0] for x in similar_interest if x[1]>= 0.8]
# print(type(good_interest),good_interest)



#______________________________________________
# import spacy
#
# nlp = spacy.load('en_core_web_lg')
#
# print("Enter two space-separated words")
# words = input()
# print(words, type(words))
# tokens = nlp(words)
#
# for token in tokens:
#     # Printing the following attributes of each token.
#     # text: the word string, has_vector: if it contains
#     # a vector representation in the model,
#     # vector_norm: the algebraic norm of the vector,
#     # is_oov: if the word is out of vocabulary.
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)
# #
# token1, token2 = tokens[0], tokens[1]
# #
# print("Similarity:", token1.similarity(token2))



#_________________________________________________________________________
# Creat random coff
#
# import random
#
#
# coff = [[0 for i in range(200)] for k in range(200)]
# print(coff)
# for i in range(200):
#     for j in range(i,200):
#         if i!=j:
#
#             coff[i][j] = random.randint(0,1000)/1000
#             coff[j][i] = coff[i][j]
#         elif i==j:
#             coff[i][j] = 1
#
# print(coff)
# dic = {}
# for ith,hobbies in enumerate(coff):
#     hobby_dic = {}
#     for kth,hobby in enumerate(hobbies):
#         hobby_dic["hobby"+str(kth)] = hobby
#     dic["hobby"+str(ith)] = hobby_dic
# print(dic)
#
# with open("hobby_dic.json", "w") as outfile:
#     json.dump(dic, outfile)




#__________________________________________________________________________




