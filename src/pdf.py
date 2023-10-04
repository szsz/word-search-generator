
import wordSearchGenerator
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, PageBreak,TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas 
import sys
import copy
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
    
if __name__ == '__main__':


    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))



    doc = SimpleDocTemplate("simple_table.pdf", pagesize=A4,topMargin=1.0,bottomMargin=1.0,leftMargin=1.0,rightMargin=1.0)
    flowables = []
    g = wordSearchGenerator.WordSearch("./tests/sample_data_hun.txt")

    gl = [copy.deepcopy(g) for i in range(0, 200)] 
    for i in gl:
        try:
            i.generate_word_search(1)
        except:
            i.bv = -1

    sl = sorted(gl, key=lambda x: x.bv, reverse=True)
    NUM = 40
    skl = []
    for i in range(1,NUM):
        g = sl[i]
        p = Paragraph("Találd meg a szavakat "+ str(i),styleH)
        flowables.append(p)
        (sk, w,b,k) = g.get_res()
        skl.append("megoldás"+str(i)+"\n"+"\n".join(sk))

        x = [w[i:i + 3] for i in range(0, len(w), 3)] 

        tbl = Table(x)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",8.0),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)
        tbl = Table(b)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",6.0),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        tbl.setStyle(TableStyle([("FONT",(1,1),(-1,-1),"Verdana",10.0),
                                ("VALIGN",(1,1),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)
        flowables.append(PageBreak())

        #tbl = Table(k)
        #tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana"),
        #                        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        #flowables.append(tbl)
        #flowables.append(PageBreak())
    
    
    
    x = [skl[i:i + 5] for i in range(0, len(skl), 5)] 

    tbl = Table(x)
    tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",4.0),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    flowables.append(tbl)

    
    flowables.append(PageBreak())
    for i in range(1,NUM):
        g = sl[i]
        p = Paragraph("Megoldás "+ str(i),styleH)
        flowables.append(p)
        (sk, w,b,k) = g.get_res()
        tbl = Table(k)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana"),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)
        flowables.append(PageBreak())


    doc.build(flowables)