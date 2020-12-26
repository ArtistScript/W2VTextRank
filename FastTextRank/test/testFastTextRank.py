from FastTextRank.FastTextRank4Word import FastTextRank4Word
import codecs
import datetime

# mod = FastTextRank4Word(tol=0.0001,window=2)
# with open("text1.txt", "r", encoding='utf-8') as myfile:
# old_time = datetime.datetime.now()
def demo():
    mod = FastTextRank4Word(use_stopword=True, tol=0.0001,window=2)

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


def get_keywords_and_keyphrase2jsonfile(filein, fileout, nlines_per_content=100, min_occur_num=2):
    '''

    :param filein: text file ,one subject content text per line in file
    :param fileout: json file, ["keywords":[(k1,s1),(k2,s2),...], "phrase":[p1,p2,...]]
    :return: None
    '''
    mod = FastTextRank4Word(use_stopword=True, tol=0.0001,window=2)
    with codecs.open(filein, "rb", encoding='utf-8') as fin:
        line_cnt = 0
        line_cache = []
        for line in fin:
            line = line.strip()
            if line_cnt < nlines_per_content:
                line_cnt += 1
                line_cache.append(line)
                continue
            else:
                line_cnt = 0
                text = ' '.join(line_cache)
                keywords_score_list = mod.get_keywords(text)
                # print('keywords num=%d:' % len(keywords_score_list))
                # for keyword,score in keywords_score_list:
                #     print(keyword,score)

                keywordslist = [k for k,s in keywords_score_list]
                keyphrases = mod.get_keyphrases_according_to_keywords(keywordslist,min_occur_num)
                print('keyphrases num=%d:' % len(keyphrases))
                for keyphrase in keyphrases:
                    print(keyphrase)

                line_cache = []
        if line_cache:#
            text = ' '.join(line_cache)
            keywords_score_list = mod.get_keywords(text)
            # print('keywords num=%d:' % len(keywords_score_list))
            # for keyword,score in keywords_score_list:
            #     print(keyword,score)

            keywordslist = [k for k,s in keywords_score_list]
            keyphrases = mod.get_keyphrases_according_to_keywords(keywordslist,min_occur_num)
            print('keyphrases num=%d:' % len(keyphrases))
            for keyphrase in keyphrases:
                print(keyphrase)


if __name__ == "__main__":
    # demo() # read a whole file to get a subject text content

    # one subject content text per line in file
    filein = "test.txt"#"test.txt"#"text1.txt"
    fileout = "key1.json"
    get_keywords_and_keyphrase2jsonfile(filein, fileout, nlines_per_content=1, min_occur_num=2)
