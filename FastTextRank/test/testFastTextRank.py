from FastTextRank.FastTextRank4Word import FastTextRank4Word
import codecs
import datetime
mod = FastTextRank4Word(tol=0.0001,window=2)
# with open("text1.txt", "r", encoding='utf-8') as myfile:
old_time = datetime.datetime.now()
for i in range(1):
    text = codecs.open('test.txt', 'r', 'utf-8').read()
    text = text.strip()
    # text = codecs.open('xaa', 'rb', 'utf-8').read()
    print('keywords:')
    old_time = datetime.datetime.now()
    # keywords_score_list = mod.get_keywords(text, keywords_num = 200000)# here text should be a whole text content;not multi articles
    keywords_score_list = mod.get_keywords(text)
    print("total time:" , datetime.datetime.now() - old_time)
    print('keywords num=%d:' % len(keywords_score_list))
    for keyword,score in keywords_score_list:
        print(keyword,score)

    print('keyphrases:')
    keywordslist = [k for k,s in keywords_score_list]
    keyphrases = mod.get_keyphrases_according_to_keywords(keywordslist)
    print('keyphrases num=%d:' % len(keyphrases))
    for keyphrase in keyphrases:
        print(keyphrase)
#
# old_time = datetime.datetime.now()
# for i in range(1):
#     text = codecs.open('text' + str(i + 1) + '.txt', 'r', 'utf-8').read()
#     text = text.strip()
#     # text = codecs.open('xaa', 'rb', 'utf-8').read()
#
#     old_time = datetime.datetime.now()
#     keyphrases = mod.get_keyphrases(text, keywords_num=200000)
#     print("total time:" , datetime.datetime.now() - old_time)
#     print('keyphrases:')
#     for keyphrase in keyphrases:
#         print(keyphrase)