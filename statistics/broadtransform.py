import os

class BroadTransform(object):

    en_file_path = 'data/en_broad.txt'
    ch_file_path = 'data/ch_broad.txt'

    def get_broad(self, broad_en):
        path = os.path.split(os.path.realpath(__file__))[0]
        en_broad_list = self.get_broad_list(os.path.join(path, self.en_file_path))
        ch_broad_list = self.get_broad_list(os.path.join(path, self.ch_file_path))
        return ch_broad_list[en_broad_list.index(broad_en)]

    def get_broad_list(self, file_path):
        broad_list = []
        f = open(file=file_path, encoding='utf-8')
        for line in f:
            for name in line.split(','):
                broad_list.append(name.strip())
        f.close()
        return broad_list


if __name__ == '__main__':
    transform = BroadTransform()
    print(transform.get_broad('buptdiscount'))