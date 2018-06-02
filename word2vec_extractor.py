import numpy as np
import nltk
import string
from nltk.corpus import stopwords
import gensim
import os
import time

stops = set(stopwords.words("english"))
punct = set(string.punctuation)

class Word2vecExtractor:

    def __init__(self, w2vecmodel):
        # self.w2vecmodel=gensim.models.Word2Vec.load_word2vec_format(w2vecmodel, binary=True)
        self.w2vecmodel = gensim.models.KeyedVectors.load_word2vec_format(w2vecmodel, binary=True)

    def sen2vec(self,sentence):
        words = [word for word in nltk.word_tokenize(sentence) if word not in stops and word not in punct]
        res = np.zeros(self.w2vecmodel.vector_size)
        count = 0
        for word in words:
            if word in self.w2vecmodel:
                count += 1
                res += self.w2vecmodel[word]

        if count != 0:
            res /= count

        return res 

    def doc2vec(self, doc):
        count = 0    
        res = np.zeros(self.w2vecmodel.vector_size)
        for sentence in nltk.sent_tokenize(doc):
            for word in nltk.word_tokenize(sentence):
                if((word not in stops) and (word not in punct)):
                    if word in self.w2vecmodel:
                        count += 1
                        res += self.w2vecmodel[word]

        if count != 0:
            res /= count

        return res 

    def get_doc2vec_feature_dict(self, doc):  
        vec = self.doc2vec(doc)  

        number_w2vec=vec.size    
        feature_dict = {}

        for i in range(0, number_w2vec):
            feature_dict.update({"Word2VecfeatureGoogle_"+ str(i):vec[i]})
           
        return feature_dict
    
    def word2v(self, word):
        res = np.zeros(self.w2vecmodel.vector_size)
        if word in self.w2vecmodel:
            res += self.w2vecmodel[word]
        return res

if __name__ == "__main__":
        start = time.time()
        W2vecextractor = Word2vecExtractor("GoogleNews-vectors-negative300.bin")
        end = time.time()
        print("time ellapsed: %s" %(end - start))
        
        print("starting")
        doc = "A fisherman was catching fish by the sea. A monkey saw him, and wanted to imitate what he was doing. The man went away into a little cave to take a rest, leaving his net on the beach. The monkey came and grabbed the net, thinking that he too would go fishing. But since he didn't know anything about it and had not had any training, the monkey got tangled up in the net, fell into the sea, and was drowned. The fisherman seized the monkey when he was already done for and said, 'You wretched creature! Your lack of judgment and stupid behaviour has cost you your life!'"

        start = time.time()
        feature_dict = W2vecextractor.get_doc2vec_feature_dict(doc)
        end = time.time()
        print("time ellapsed: %s" %(end - start))

        doc = "An excellent restaurant. The food was wonderful, the service friendly and attentive, and the atmosphere warm and homey. It was the best Valentine's dinner I ever had!"

        start = time.time()
        feature_dict = W2vecextractor.get_doc2vec_feature_dict(doc)
        end = time.time()
        print("time ellapsed: %s" %(end - start))

        doc = "I got a splinter. It’s not something I do often.   Actually, I can’t recall the last time I did. This one was a doosie. I tried to push it out the way it came in, but it was resistant. So, I did what I used to do. I got the alcohol, cotton ball and needle, sterilized it and went to work. This brought back a flood of memories.   I have long been fascinated with the human body: brilliant, miraculous machine that it is—along with everything else that lives. So much so, that when I was 6, I announced to my parents (after watching open heart surgery on the discovery channel) that I wanted to be a surgeon. This pleased them greatly, especially my father. He would work out in the yard, gardening or building something and have me “operate” on his splinters; encouraging me and telling me what skill and aptitude I possessed at such a young age.   Time has marched on, and I was an artistic soul it turns out, and not a scientist-doctor. My father has passed on as well, but when the memories flooded in during my  operation  on this latest splinter, I realized that I am a surgeon of sorts—a surgeon of the soul. My calling is to rightly divide the word of truth in such a way that it actually matters and answers the deep divide within every human being…where soul meets body, the flesh and tangible pitting itself against that which truly satisfies the eternal soul.   And though my father did not live to see me realize my calling, I hope he is rejoicing somewhere in the work I do, which far outlasts the fleshly veil, and gives hope and purpose to those who realize that they are much more than their bodies can ever promise them—much more than this life alone can ever give them."

        start = time.time()
        feature_dict = W2vecextractor.get_doc2vec_feature_dict(doc)
        end = time.time()
        print("time ellapsed: %s" %(end - start))







	
        
