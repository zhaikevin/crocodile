import pandas as pn
import matplotlib.pyplot as plt
import os
import broadtransform


class BroadStatistics(object):

    # 统计数据
    def statistics(self, data_path):
        rows = pn.read_csv(data_path)
        broads = {}
        for index, row in rows.iterrows():
            broad = row[5]
            if broad not in broads:
                broads[broad] = 1
            else:
                broads[broad] = broads[broad] + 1
        return broads

    def draw_pie_chart(self, data_path):
        broads = self.statistics(data_path)
        #plt.figure(figsize=(10, 10))
        labels = []
        transform = broadtransform.BroadTransform()
        for key in broads.keys():
            labels.append(transform.get_broad(key))
        plt.pie(x=broads.values(), labels=labels, autopct='%1.2f%%')
        plt.rcParams['font.sans-serif']=['SimHei']
        #plt.legend(loc="upper right",fontsize=10,bbox_to_anchor=(1.1,1.05),borderaxespad=0.3)
        plt.axis('equal')
        plt.show()



if __name__ == '__main__':
    statistics = BroadStatistics()
    path = os.path.split(os.path.realpath(__file__))[0]
    statistics.draw_pie_chart(os.path.join(path, 'data/top_ten_de-duplication.csv'))