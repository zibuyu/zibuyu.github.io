from collections import Counter 
from datetime import date
def gen_paper_bib(filename='ke.bib'):
    cache=[]
    for line in open(filename,encoding='utf8'):
        line=line.strip()
        if line:
            if line[0]=="@" and cache:
                
                yield cache
                cache=[]
            cache.append(line)
        
    if cache:
        yield cache


def clear_deli(s):
    return s.replace("{","").replace("}","")

def clear_annote(annote):
    if not annote:return ""
    annote=annote[:-1]
    return "<br/>\n".join(l.replace("{","").replace("}","") for l in annote)


def gen_papers(filename):
    paper_type={"inproceedings","article","phdthesis"}
    keys={"title","year","author","journal","booktitle","keywords"}
    for record in gen_paper_bib(filename):
        #print(record)
        paper={k:"" for k in keys}
        paper['annote']=""
        if record[0][0]=='@':
            type=record[0].partition("{")[0][1:]
            if type not in paper_type:continue
            paper['type']=type;
        
        annote=[]
        for i,line in enumerate(record):
            #print(i, line)
            if annote:
                annote.append(line)
                continue
            key,x,value=line.partition(" =\t")
            #print(key, x, value)
            if key in keys:
                value=value[:-1]
                value=clear_deli(value)
                #print(key+":",value)
                paper[key]=value;
            
            if line.startswith("annote"):
                line=line[9:]
                annote.append(line)
                
        paper['annote']=clear_annote(annote)
        yield paper;


def printHtml(reflist,f):
    print('''<meta http-equiv="content-type" content="text/html; charset=UTF-8"> <link href="css.css" rel="stylesheet" type="text/css" /> <script src="js.js"></script> 
	<title>Bibliography of Automatic Keyphrase Extraction</title> <div class="header"><div class="pic"></div>Bibliography of Automatic Keyphrase Extraction<br/><br/> 
	Maintained by <a href="http://nlp.csai.tsinghua.edu.cn/~lzy">Zhiyuan Liu</a><br/>''',file=f)
    d=str(date.today()).split('-')
    print('Generated on '+d[0]+'.'+d[1]+'.'+d[2]+'.',file=f)
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
        
        
        authors='<div class="authors">'+ref["author"]+'</div>'
        
        title='<div class="title" onclick="turn_note('+str(i)+')">'+ref["title"]+'</div>'
        jf='<div class="JF">'+ref["journal"]+ref["booktitle"]+'</div>'
        
        kw=' '.join(['<div class="keyword">'+k+'</div>'for k in ref["keywords"].split(",")])
        kw='<div class="keywords">'+kw+'</div>'
        #kw='<div class="keywords">'+ref["keywords"]+'</div>'
        #print(ref["keywords"])
        f.write(title+authors+jf+kw+'</div>\n')
        

        #if(ref["annote"]):
        f.write('<div class="note" id="note_'+str(i)+'" style="display:none">')
        
        f.write(ref["annote"]+'\n')
        f.write('</div>\n')#div of note
        
        f.write('</div>\n')
        
        
    
    print('''
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-23920323-3']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
          ''',file=f)
    
    f.flush()


if __name__=='__main__':
    
    papers=[p for p in gen_papers('ke.bib')]
    printHtml(papers,open('bib.html','w',encoding='utf-8'))
    
        
