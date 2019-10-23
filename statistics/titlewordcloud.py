import pandas as pn
import jieba
import collections
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 帖子标题词云
class TitleWordCloud(object):

    # 加载停用词表
    def stop_words_list(self, path):
        stop_words = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
        return stop_words
    
    # 分词
    def segmentation(self, data_path, stop_words_path, user_dict_path):
        jieba.load_userdict(user_dict_path)
        rows = pn.read_csv(data_path)
        stop_words = self.stop_words_list(stop_words_path)
        segments = []
        for index, row in rows.iterrows():
            content = row[2]
            words = jieba.cut(content, cut_all=False)
            for word in words:
                if word not in stop_words:
                    segments.append(word)
        word_counts = collections.Counter(segments) 
        return word_counts

    # 绘制词云图
    def word_cloud(self, data_path, stop_words_path, font_path, user_dict_path):
        wc = WordCloud(
            font_path=font_path,
            width=1980,
            height=1680,
            max_words=30, 
            max_font_size=400
        )
        word_counts = self.segmentation(data_path, stop_words_path, user_dict_path)
        wc.generate_from_frequencies(word_counts)
        plt.imshow(wc)
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    word_cloud = TitleWordCloud()
    path = os.path.split(os.path.realpath(__file__))[0]
    word_cloud.word_cloud(os.path.join(path, 'data/top_ten_de-duplication.csv'), os.path.join(path, 'data/stop_words.txt'),\
         os.path.join(path, 'font/simhei.ttf'), os.path.join(path, 'data/user_dict.txt'))