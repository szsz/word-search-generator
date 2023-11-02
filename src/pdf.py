
import wordSearchGenerator
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, PageBreak,TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.styles import TA_CENTER, ParagraphStyle, _baseFontNameB, _baseFontName
from reportlab.pdfgen import canvas 
import sys
import copy
    
if __name__ == '__main__':

    font_file = 'Symbola.ttf'
    symbola_font = TTFont('Symbola', font_file)
    pdfmetrics.registerFont(symbola_font)
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))



    doc = SimpleDocTemplate("simple_table.pdf", pagesize=A4,topMargin=1.0,bottomMargin=1.0,leftMargin=1.0,rightMargin=1.0)
    flowables = []
    g = wordSearchGenerator.WordSearch("./tests/sample_data_hun.txt")

    NUM = 40
    gl = [copy.deepcopy(g) for i in range(0, NUM*5)] 
    for i in gl:
        try:
            i.generate_word_search(1)
            print(".")
        except:
            i.bv = -1

    sl = sorted(gl, key=lambda x: x.bv, reverse=True)
    skl = []
    sylehn = ParagraphStyle(name='Normal',
                                  fontName=_baseFontName,
                                  fontSize=10,
                                  leading=12)
    
    syleh = ParagraphStyle(name='Title',
                                  parent=sylehn,
                                  fontName = 'Verdana',
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=6)
    sylea = ParagraphStyle(name='Title',
                                  parent=sylehn,
                                  fontName = 'Symbola',
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=6)
    sylee = ParagraphStyle(name='end',
                                  parent=sylehn,
                                  fontName = 'Verdana',
                                  fontSize=12,
                                  leading=22,
                                  alignment=TA_CENTER,
                                  spaceAfter=6,
                                  underlineColor="black",
                                  underlineWidth=1)
    for i in range(0,NUM):
        g = sl[i]
        p = Paragraph("Találd meg a szavakat!",syleh)

        flowables.append(p)
        p = Paragraph("",syleh)
        flowables.append(p)
        
        p = Paragraph("&#129120 &#129124 &#129121 &#129125 &#129122 &#129126 &#129123 &#129127 (v " +str(i+1)+")",sylea)
        flowables.append(p)
        
        p = Paragraph("",syleh)
        flowables.append(p)
        flowables.append(p)
        (sk, w,b,k) = g.get_res()
        skl.append("megoldás "+str(i+1)+"\n"+"\n".join(sk))

        x = [w[i:i + 3] for i in range(0, len(w), 3)] 

        tbl = Table(x)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",8.0),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)

        
        flowables.append(p)
        flowables.append(p)
        tbl = Table(b)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",6.0),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        tbl.setStyle(TableStyle([("FONT",(1,1),(-1,-1),"Verdana",10.0),
                                ("VALIGN",(1,1),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)


        p = Paragraph("",syleh)
        flowables.append(p)
        flowables.append(p)        
        p = Paragraph("",syleh)
        flowables.append(p)
        flowables.append(p)
        p = Paragraph("Ismerd meg a könyvecskék mesekönyveket!",syleh)
        flowables.append(p)        
        flowables.append(p)
        p = Paragraph("<u>konyvecskek.hu</u>",syleh)
        flowables.append(p)

        flowables.append(PageBreak())

        #tbl = Table(k)
        #tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana"),
        #                        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        #flowables.append(tbl)
        #flowables.append(PageBreak())
    
    
    
    x = [skl[i:i + 5] for i in range(0, len(skl), 5)] 

    tbl = Table(x)
    tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana",5.5),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    flowables.append(tbl)

    
    flowables.append(PageBreak())
    for i in range(0,NUM):
        g = sl[i]
        p = Paragraph("Megoldás "+ str(i+1),syleh)
        flowables.append(p)
        (sk, w,b,k) = g.get_res()
        tbl = Table(k)
        tbl.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Verdana"),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        flowables.append(tbl)
        flowables.append(PageBreak())


    doc.build(flowables)