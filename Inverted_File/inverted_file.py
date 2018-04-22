import os
import sys


def build_document_index(path):
    files = os.listdir(path) # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
            file_name = path + "\\" +file
            s.append(file_name)

    index_path = path[:-5] + 'Index_File\\'   #获取到当前文件的目录，并检查是否有文件夹，如果不存在则自动新建文件
    if not os.path.exists(index_path):
        os.makedirs(index_path)

    f=open(index_path+"\\doc_index.txt", "w+")
    for i in s:
        f.writelines(str(s.index(i))+"\t"+i+"\n")
    f.close()

    return index_path+"\\doc_index.txt"


def build_word_index(path):
    dictionary = {}
    for line in open(path, 'r'):  #打开文件
        rs = line.rstrip('\n')  # 移除行尾换行符
        file = rs.split('\t')
        file_index = file[0]
        file_name = file[1]
        print(file_name)
        for line_2 in open(file_name, 'r'):  # 按行打开文件
            rs2 = line_2.rstrip('\n')  # 移除行尾换行符
            words = rs2.split( )
            for word in words:
                if word not in dictionary:
                    article = []
                    dictionary[word] = article
                dictionary[word].append(file_index)
    print(dictionary)

    f = open(path[:-13]+"\\word_index.txt", "w+")
    for key in dictionary:
        f.writelines(key+"\t")
        for j in dictionary[key]:
            f.writelines(j+'\t')
        f.write("\n")
    f.close()


class SearchEngine:
    def __init__(self):
        self.Word_List = {}
        self.IDPath = {}

    def Page_Load(self):
        for line in open("E:\PycharmProjects\Inverted_File\Index_File\\word_index.txt", 'r'):  # 打开文件
            rs = line.rstrip('\n')  # 移除行尾换行符
            file = rs.split('\t')
            sWord = file[0]
            htDocIDs = {}
            for i, element in enumerate(file):
                if (i > 0) and (element not in htDocIDs) and element != '':
                    htDocIDs[element] = None
            self.Word_List[sWord] = htDocIDs

        for line in open("E:\PycharmProjects\Inverted_File\Index_File\\doc_index.txt", 'r'):  # 打开文件
            rs = line.rstrip('\n')  # 移除行尾换行符
            file = rs.split('\t')
            self.IDPath[file[0]] = file[1]

    def Match(self, query):
        Content = ""
        if query in self.Word_List:
            result = "Resulting IDs: "
            htDocIDs = self.Word_List[query]
            for ID in htDocIDs:
                result += ID + "\t"
                sPath = self.IDPath[ID]

                f = open(sPath, "r")
                textcontent = f.read()

                Content += "Document\t" + str(ID) + "<br>"
                Content += "Path\t" + str(sPath) + "<br>"
                Content += "--------------------------------------------------------" + "<br>"
                Content += textcontent
                Content += "<br><br>"

                f.close()
        else:
            result = "No results returned!"
        return result, Content

    def Print(self):
        print(self.IDPath)
        print('\n')
        print(self.Word_List)


if __name__ == "__main__":
    path = sys.path[0]+'\Files'
    namelist = []
    doc_index_path = build_document_index(path)
    build_word_index(doc_index_path)

