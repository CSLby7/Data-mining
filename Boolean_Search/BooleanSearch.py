
class BooleanSearch:
    def __init__(self):
        self.m_sDocDir = "E:\PycharmProjects\Boolean_Search\Index_File\Files"
        self.m_sDocIndexFile = "E:\PycharmProjects\Boolean_Search\Index_File\doc_index.txt"
        self.m_sWordIndexFile = "E:\PycharmProjects\Boolean_Search\Index_File\word_index.txt"
        self.m_docWord2List = {}
        self.m_docDocID2Path = {}

    def PageLoad(self):
        for line in open(self.m_sWordIndexFile, 'r'):  # 打开文件
            rs = line.rstrip('\n')  # 移除行尾换行符
            file = rs.split('\t')
            sWord = file[0]
            htDocIDs = {}
            for i, element in enumerate(file):
                if (i > 0) and (element not in htDocIDs) and element != '':
                    htDocIDs[element] = None
            self.m_docWord2List[sWord] = htDocIDs

        for line in open(self.m_sDocIndexFile, 'r'):  # 打开文件
            rs = line.rstrip('\n')  # 移除行尾换行符
            file = rs.split('\t')
            self.m_docDocID2Path[file[0]] = file[1]

    def SearchWithSingleKeyword(self, sKeyWord):
        pList4Return = []
        if sKeyWord in self.m_docWord2List:
            htDocIDs = self.m_docWord2List[sKeyWord]
            for sDocId in htDocIDs:
                 if not sDocId in pList4Return:
                     pList4Return.append(sDocId)

        return pList4Return

    def ConstructQueryTree(self, sQuery):
        saElements = sQuery.split(' ')
        firstGroup = []
        i = 0
        while i < len(saElements):
            obNode = []
            if saElements[i] == 'and':
                obNode.append('AND')
                obPreNode = firstGroup[len(firstGroup) - 1]
                obNode.append(obPreNode)
                del firstGroup[len(firstGroup) - 1]
                obRightNode = []
                obRightNode.append(saElements[i+1])
                obRightNode.append(None)
                obRightNode.append(None)
                obNode.append(obRightNode)
                i = i + 1
            else:
                obNode.append(saElements[i])
                obNode.append(None)
                obNode.append(None)
            i = i + 1
            firstGroup.append(obNode)

        obLastNode = firstGroup[0]
        j = 1
        while j < len(firstGroup):
            obCurrentNode = firstGroup[j]
            obORNode = []
            obORNode.append('OR')
            obORNode.append(obLastNode)
            obORNode.append(obCurrentNode)
            obLastNode = obORNode
            j = j + 1
        return obLastNode

    def SearchWithBinaryTree(self, obRootNode):
        firstResult2Return = []
        sNodeValue = obRootNode[0]
        if sNodeValue == 'AND':
            firstLefChildResults = self.SearchWithBinaryTree(obRootNode[1])
            firstRightChildResults = self.SearchWithBinaryTree(obRootNode[2])
            i = 0
            while i <len(firstLefChildResults):
                if(firstLefChildResults[i] in firstRightChildResults):
                    firstResult2Return.append(firstLefChildResults[i])
                i = i + 1
        elif sNodeValue == 'OR':
            firstLefChildResults = self.SearchWithBinaryTree(obRootNode[1])
            firstRightChildResults = self.SearchWithBinaryTree(obRootNode[2])
            i = 0
            while i < len(firstLefChildResults):
                if not firstLefChildResults[i] in firstResult2Return:
                    firstResult2Return.append(firstLefChildResults[i])
                i = i + 1
            i = 0
            while i < len(firstRightChildResults):
                if not firstRightChildResults[i] in firstResult2Return:
                    firstResult2Return.append(firstRightChildResults[i])
                i = i + 1
        else:
            return self.SearchWithSingleKeyword(sNodeValue)
        return firstResult2Return

    def Search(self, sQuery):
        self.PageLoad()
        firstIDs = self.SearchWithBinaryTree(self.ConstructQueryTree(sQuery))
        # print('firstIDs:'+str(firstIDs))
        Content = ""
        result = "Resulting IDs: "
        for ID in firstIDs:
            result += str(ID) + "\t"
            sPath = self.m_docDocID2Path[ID]
            f = open(sPath, "r")
            textcontent = f.read()
            Content += "Document\t" + str(ID) + "<br>"
            Content += "Path\t" + str(sPath) + "<br>"
            Content += "--------------------------------------------------------" + "<br>"
            Content += textcontent
            Content += "<br><br>"
            f.close()
        if result == 'Resulting IDs: ':
            result = "No results returned!"
        return result, Content

# 测试使用
if __name__ == "__main__":
    booleansearch = BooleanSearch()
    result, content = booleansearch.Search('exercise ')
    print(result)
    print(content)
