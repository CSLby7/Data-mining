import os
import math
import pandas as pd
import re


class VectorSpaceTool:
    def __init__(self):
        self.m_sDocDir = "E:\PycharmProjects\Vector_Search\Files"
        self.m_sDocIndexFile = "E:\PycharmProjects\Vector_Search\Index_File\doc_index.txt"
        self.m_sWordIndexFile = "E:\PycharmProjects\Vector_Search\Index_File\word_index.txt"
        self.sVectorFolder = "E:\PycharmProjects\Vector_Search\Vector_File"
        self.sTermFrequencyFile = "E:\PycharmProjects\Vector_Search\Vector_File\\termFrequency.txt"
        self.sVectorFile = "E:\PycharmProjects\Vector_Search\Vector_File\\termFrequency.txt"
        self.sTfIdfFile = "E:\PycharmProjects\Vector_Search\Vector_File\TfIdf.txt"
        self.sBasisFile = "E:\PycharmProjects\Vector_Search\Vector_File\sBasis.txt"
        self.dicWord2DocFrequency = {}
        self.m_firstBasisWords = []
        self.dicDocId2Vector = {}
        self.m_docDocID2Pah = {}
        self.m_docWord2List = {}

    def BuildTermFrequencyFile(self):
        if not os.path.exists(self.sVectorFolder):
            os.makedirs(self.sVectorFolder)
        for line in open(self.m_sWordIndexFile, 'r'):  # 打开文件
            rs = line.rstrip('\n')  # 移除行尾换行符
            saInfo= rs.split('\t')
            del saInfo[len(saInfo) - 1]
            dicDocID2Count = {}
            i = 1
            while i < len(saInfo):
                if saInfo[i] in dicDocID2Count:
                    dicDocID2Count[saInfo[i]] += 1
                else:
                    dicDocID2Count[saInfo[i]] = 1
                i += 1

            f = open(self.sTermFrequencyFile, "a+")
            f.write(saInfo[0] + '\t')
            for sDocId in dicDocID2Count:
                f.write(sDocId+'-'+str(dicDocID2Count[sDocId])+'\t')

            f.write('\n');
            f.close()

    def BuildTfIdfVectorFile(self):
        dicWord2DocFrequency = {}
        dicTermFrequency = {}
        dicDocument2Length = {}
        firstWords = []
        f = open(self.sTermFrequencyFile, 'r')
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            saInfo = rs.split('\t')
            dicWord2DocFrequency[saInfo[0]] = len(saInfo) - 2
            firstWords.append(saInfo[0])

            i = 1
            while i < len(saInfo)-1:
                print(saInfo)
                saSplited = saInfo[i].split('-')
                dicTermFrequency[saInfo[0]+'@'+saSplited[0]] = int(saSplited[1])
                if saSplited[0] in dicDocument2Length:
                    dicDocument2Length[saSplited[0]] += int(saSplited[1])
                else:
                    dicDocument2Length[saSplited[0]] = int(saSplited[1])
                i += 1
        f.close()
        print(dicWord2DocFrequency)

        # if not os.path.exists(self.sTfIdfFile):
        f2 = open(self.sTfIdfFile, "a+")
        for sDocID in dicDocument2Length:
            daTfIdf = []
            i = 0
            while i < len(firstWords):
                sPairKey = firstWords[i] + '@' + sDocID
                dTf = float(dicTermFrequency[sPairKey]) if sPairKey in dicTermFrequency else 0
                dTf /= float(dicDocument2Length[sDocID])
                dIdf = math.log10(float(len(dicDocument2Length))/dicWord2DocFrequency[firstWords[i]])
                daTfIdf.append(dIdf * dTf)
                i += 1
            f2.write(sDocID+'\t')
            i = 0
            while i < len(daTfIdf):
                f2.write(str(daTfIdf[i]) + '\t')
                i += 1
            f2.write('\n')
        f2.close()

        f3 = open(self.sBasisFile, "w+")
        i = 0
        while i < len(firstWords):
            f3.writelines(firstWords[i]+'\n')
            i += 1
        f3.close()

    def VectorSpaceSearch(self):
        f = open(self.sTermFrequencyFile, 'r')
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            saInfo = rs.split('\t')
            del saInfo[len(saInfo)-1]
            self.dicWord2DocFrequency[saInfo[0]] = len(saInfo) - 1
        f.close()

        f = open(self.sBasisFile, 'r')
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            self.m_firstBasisWords.append(rs)
        f.close()

        f = open(self.sTfIdfFile, 'r')
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            saInfo = rs.split('\t')
            del saInfo[len(saInfo)-1]
            i = 1
            daVector = []
            while i < len(saInfo):
                daVector.append(float(saInfo[i]))
                i += 1
            self.dicDocId2Vector[saInfo[0]] = daVector
        f.close()

        f = open(self.m_sDocIndexFile, 'r')
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            saInfo = rs.split('\t')
            self.m_docDocID2Pah[saInfo[0]] = saInfo[1]

        f.close()

        f = open(self.m_sWordIndexFile, 'r')  # 打开文件
        for line in f:
            rs = line.rstrip('\n')  # 移除行尾换行符
            file = rs.split('\t')
            sWord = file[0]
            htDocIDs = {}
            for i, element in enumerate(file):
                if (i > 0) and (element not in htDocIDs) and element != '':
                    htDocIDs[element] = None
            self.m_docWord2List[sWord] = htDocIDs

    def RepresentQueryAsVector(self, sQuery):
        saTerms = sQuery.split(' ')
        dDocLength = len(saTerms)
        dicWord2Count = {}
        i = 0
        while i < len(saTerms):
            if saTerms[i] in dicWord2Count:
                dicWord2Count[saTerms[i]] += 1
            else:
                dicWord2Count[saTerms[i]] = 1
            i += 1

        daQVector = []
        i = 0
        while i < len(self.m_firstBasisWords):
            daQVector.append(0)
            i += 1
        i = 0

        while i < len(self.m_firstBasisWords):
            sCurrentBasisWord = self.m_firstBasisWords[i]
            if not sCurrentBasisWord in dicWord2Count:
                i += 1
                continue
            dTf =dicWord2Count[sCurrentBasisWord]
            dTf /= dDocLength
            dIdf = math.log10(float(len(self.m_docDocID2Pah)+1)/float(self.dicWord2DocFrequency[sCurrentBasisWord]+1))
            daQVector[i] = dTf * dIdf
            i += 1

        return daQVector

    def GetVectorSimilarity(self, daVector1, daVector2):
        dLengthVector1 = 0
        i = 0
        while i < len(daVector1):
            dLengthVector1 += math.pow(daVector1[i], 2)
            i += 1
        if dLengthVector1 == 0:
            return 0
        dLengthVector1 = math.sqrt(dLengthVector1)

        dLengthVector2 = 0
        i = 0
        while i < len(daVector2):
            dLengthVector2 += math.pow(daVector2[i], 2)
            i += 1
        if dLengthVector2 == 0:
            return 0
        dLengthVector2 = math.sqrt(dLengthVector2)

        dInnerProduct = 0
        i = 0
        while i < len(daVector1):
            dInnerProduct += daVector1[i] * daVector2[i]
            i += 1
        return  dInnerProduct/(dLengthVector1 * dLengthVector2)

    def Search(self, sQuery):
        self.VectorSpaceSearch()
        daQueryVector = self.RepresentQueryAsVector(sQuery)
        print(daQueryVector)
        daSimilarities = []
        saDocIds = []
        for sDocId in self.dicDocId2Vector:
            daDoVector = self.dicDocId2Vector[sDocId]
            daSimilarities.append(self.GetVectorSimilarity(daQueryVector, daDoVector))
            saDocIds.append(sDocId)
        print(daSimilarities)

        length = len(daSimilarities)
        while length > 0:
            length -= 1
            cur = 0
            while cur < length:  # 拿到当前元素
                if daSimilarities[cur] < daSimilarities[cur + 1]:
                    daSimilarities[cur], daSimilarities[cur + 1] = daSimilarities[cur + 1], daSimilarities[cur]
                    saDocIds[cur], saDocIds[cur + 1] = saDocIds[cur + 1], saDocIds[cur]
                cur += 1

        Content = ""
        result = "Resulting IDs: "
        for ID in saDocIds:
            result += str(ID) + "\t"
            sPath = self.m_docDocID2Pah[ID]
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


if __name__ == "__main__":
    a = VectorSpaceTool()
    # a.BuildTermFrequencyFile()
    # a.BuildTfIdfVectorFile()
    # a.VectorSpaceSearch()
    # v.RepresentQueryAsVector('aa d v s')
    result, Content = a.Search('formulate new conjectures')
    print(result)