# coding:utf-8
# 将本文件放在modern2poem下
# 将website中的translate.py拷贝一份到modern2poem下
# 在modern2poem文件夹内建立文件夹'myresult'
# '....my/dir/to/fengguang.json'位于sourcePoems/veer里
# 或许要install synonyms库

import json,codecs
import association
from translate import *

with open('/Users/markdana/Desktop/EECourse-Poem-Project/sourcePoems/veer/fengguang/fengguang.json')as fin:
    oneList=json.load(fin)

with open('labelDict.json')as fin:
    label = json.load(fin)

associator=association.Associator()

# myinitstart=0#for dhy
#myinitstart=50000 for chp
#myinitstart=100000 for ljy
myinitstart=150000 #for wzy

# myend=50000#for dhy
#myend=100000 for chp
#myend=150000 for ljy
myend=198800 #for wzy

def working(mystart=myinitstart):
    Alllist=[]
    for myitr in range(mystart,myend):
        dict = oneList[myitr]

        newdict={}
        newdict['img']=dict['imgurl']
        desc=dict['alt']

        try:
            chdesc=sg_en_to_zn_translate(desc)
            syns=associator.assoSynAll(chdesc)

            print(newdict['img'])
            print(desc)
            print(chdesc)
            print(syns)

            newdict['asso']=syns
            newdict['desc']=chdesc
        except:
            newdict['desc'] = desc
            newdict['asso'] = []
            print('woooooooooo')
            continue

        Alllist.append(newdict)

        if(len(Alllist)==1000):
            with codecs.open('myresult/imgasso%d.json'%(myitr+1), 'w') as f:
                json.dump(Alllist, f, ensure_ascii=False, indent=4)
            Alllist=[]

    if Alllist:
        with codecs.open('myresult/imgasso%d.json'%myend, 'w') as f:
            json.dump(Alllist, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    working()
    #如果中途要退出，直接终止即可。
    #继续运行时，查看myresult中最大的json数据，比如'imgasso30000.json'
    #则运行working(30000)
    #全部跑完后（约5-6小时），请将myresult打包发给我








