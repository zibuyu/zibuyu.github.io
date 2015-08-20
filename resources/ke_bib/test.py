'''
This is for trans .ris to html.
This is for Chinese word segmentation bib

author: Kaixu@thunlp.cn
'''


from datetime import date
def load_source(file):
    reflist=[]
    state=0
    f=open(file,'r',encoding='utf-8')
    if(f.read(1)!='\ufeff'):
        f.seek(0)
    for line in f:
        if(state==1):
            if(line[2:5]=="  -"):
                state=0
            else:
                reflist[len(reflist)-1]["note"]=reflist[len(reflist)-1]["note"]+line[6:len(line)-1]
        if (state==0):
            if(line[0:2]=="TY"):
                reflist.append({})
                reflist[-1]["author"]=set()
                reflist[-1]["note"]=""
                reflist[-1]["JF"]=""
            if(line[0:2]=="T1"):
                reflist[-1]["title"]=line[6:len(line)-1]
            if(line[0:2]=="A1"):
                reflist[-1]["author"].add(line[6:len(line)-1])
            if(line[0:2]=="JF"):
                reflist[-1]["JF"]=line[6:len(line)-1]
            if(line[0:2]=="PY"):
                reflist[-1]["year"]=line[6:10]
            if(line[0:2]=="N1"):
                reflist[-1]["note"]=line[6:]
                state=1
    return reflist

def printHtml(reflist,f):
    print('''<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<link href="css.css" rel="stylesheet" type="text/css" />
<script src="js.js"></script>
<title>中文分词文献列表 Bibliography of Chinese Word Segmentation</title>
<div class="header"><div class="pic"></div>
中文分词文献列表 Bibliography of Chinese Word Segmentation<br/>
由<a href="http://nlp.csai.tsinghua.edu.cn/~zkx">张开旭</a>维护<br/>
如有意见与建议，欢迎联系作者:)<br/>''',file=f)
    d=str(date.today()).split('-')
    print('页面生成日期： '+d[0]+'年'+d[1]+'月'+d[2]+'日',file=f)
    f.write('</div>\n')
    year=3000
    for i,ref in enumerate(reflist):
        if(year!=ref["year"]):
            print('</div>','<div class="year">',
                  '<div class="year_number">'+ref["year"]+'</div><br/>',
                  sep='\n',file=f)
            year=ref["year"]
        
        f.write('<div class="paper">\n')
        f.write('<div class="bib">\n')
        
        authors=' '.join(['<div class="author">'+au+'</div>'for au in ref["author"]])
        authors='<div class="authors">'+authors+'</div>'
        
        title='<div class="title" onclick="turn_note('+str(i)+')">'+ref["title"]+'</div>'
        jf='<div class="JF">'+ref["JF"]+'</div>'
        
        f.write(title+authors+jf+'</div>\n')
        

        f.write('<div class="note" id="note_'+str(i)+'" style="display:none">')
        if(len(ref["note"])>1):
            f.write(ref["note"]+'\n')
        f.write('</div>\n')#div of note
        
        f.write('</div>\n')
    f.flush()

reflist=load_source('导出的条目.ris')
print(len(reflist))
printHtml(reflist,open('bib.html','w',encoding='utf-8'))

