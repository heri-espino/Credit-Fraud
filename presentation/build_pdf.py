"""Create a searchable 16:9 PDF from the same slide data used by deck.md and slides.html.

Offline print fallback. For a genuine Marp CLI export, see README.md.
"""
from pathlib import Path
import html, json, re
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

BASE=Path(__file__).resolve().parent
PROJECT=BASE.parent
META=json.loads((BASE/'slides_metadata.json').read_text(encoding='utf8'))
MANIFEST=json.loads((BASE/'figure_manifest.json').read_text(encoding='utf8'))
LOOKUP={r['file']:r for r in MANIFEST['figures']}
FIGURE_INDEX={r['file']:i+1 for i,r in enumerate(MANIFEST['figures'])}
OUTPUT=BASE/'slides.pdf'
W,H=960,540
ink=HexColor('#1D3147'); muted=HexColor('#586B80'); teal=HexColor('#238D93'); coral=HexColor('#CF6E74')
navy=HexColor('#263D58'); bg=HexColor('#FBFCFD'); line=HexColor('#DEE6EC')
styles={
 'tiny': ParagraphStyle('tiny',fontName='Helvetica',fontSize=9.4,leading=12,textColor=ink),
 'small': ParagraphStyle('small',fontName='Helvetica',fontSize=13,leading=17,textColor=muted),
 'body': ParagraphStyle('body',fontName='Helvetica',fontSize=16,leading=20,textColor=muted),
 'box':ParagraphStyle('box',fontName='Helvetica',fontSize=14,leading=19,textColor=muted),
 'tag':ParagraphStyle('tag',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=teal),
 'heading':ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=29,leading=33,textColor=navy),
}
C=canvas.Canvas(str(OUTPUT),pagesize=(W,H),pageCompression=1)
C.setTitle('Predicting Credit Card Fraud | LDS1071')
C.setAuthor('LDS1071 Machine Learning project')
C.setSubject('59-slide visual report including 44 supplied figures')

def para(text,x,top,width,style='tiny',height=None):
 p=Paragraph(html.escape(text).replace('\n','<br/>'),styles[style]);w,h=p.wrap(width,700)
 if height and h>height:
  # Tighten text if needed (without cropping its content).
  size=styles[style].fontSize
  while h>height and size>8.1:
   size-=.3
   tmp=ParagraphStyle('fit',parent=styles[style],fontSize=size,leading=size*1.25)
   p=Paragraph(html.escape(text),tmp);w,h=p.wrap(width,700)
 p.drawOn(C,x,top-h)
 return h

def rect(x,y,w,h,fill,stroke=None,r=9):
 C.setFillColor(fill)
 if stroke:C.setStrokeColor(stroke)
 else:C.setStrokeColor(fill)
 C.roundRect(x,y,w,h,r,stroke=1 if stroke else 0,fill=1)

def title(t,x,y,maxw=850,fontsize=29):
 size=fontsize
 while C.stringWidth(t,'Helvetica-Bold',size)>maxw and size>18:size-=.7
 C.setFont('Helvetica-Bold',size); C.setFillColor(navy);C.drawString(x,y,t)

def label(t,x,y,size=10,col=teal):
 C.setFillColor(col);C.setFont('Helvetica-Bold',size);C.drawString(x,y,t.upper())

def image_in_box(path,x,y,w,h):
 rect(x,y,w,h,HexColor('#FFFFFF'),line,9)
 im=Image.open(path)
 iw,ih=im.size
 k=min((w-12)/iw,(h-12)/ih)
 rw,rh=iw*k,ih*k
 C.drawImage(ImageReader(im),x+(w-rw)/2,y+(h-rh)/2,width=rw,height=rh,mask='auto',preserveAspectRatio=True)

def note(x,y,w,h,heading,body,accent):
 fill=HexColor('#F3F8F9') if accent==teal else HexColor('#FFF7F6')
 rect(x,y,w,h,fill,None,6)
 C.setFillColor(accent);C.rect(x,y,3,h,fill=1,stroke=0)
 label(heading,x+12,y+h-15,8.5,accent)
 para(body,x+12,y+h-24,w-24,'tiny',height=h-29)

def strip():
 C.setFillColor(HexColor('#F7F9FB'));C.rect(0,0,W,H,fill=1,stroke=0)
 C.setFillColor(teal);C.rect(0,H-7,580,7,stroke=0,fill=1)
 C.setFillColor(HexColor('#5A91AD'));C.rect(580,H-7,280,7,stroke=0,fill=1)
 C.setFillColor(coral);C.rect(860,H-7,100,7,stroke=0,fill=1)

def foot(idx):
 C.setFillColor(HexColor('#91A2B3'));C.setFont('Helvetica',8.5)
 C.drawString(40,12,'LDS1071 · CREDIT CARD FRAUD')
 C.drawRightString(W-40,12,f'{idx:02d} / {len(META):02d}')

def boxes(parts,starty=410):
 for i,(h,body) in enumerate(parts):
  col=i%2;row=i//2
  x=42+col*443; y=starty-row*175-148
  rect(x,y,425,153,HexColor('#FFFFFF'),line,9)
  label(h,x+18,y+125,11)
  para(body,x+18,y+111,385,'box',height=105)

def extract_bold_tags(b):
 return re.findall(r'<b>(.*?)</b>\s*<p>(.*?)</p>',b,flags=re.S)

for ix,s in enumerate(META,1):
 strip()
 kind=s['kind']; body=s['body']; t=s.get('title') or ''
 if kind in ('cover','closing'):
  iscover=kind=='cover'
  label('LDS1071 · MACHINE LEARNING · FINAL PROJECT',52,463)
  if iscover:
   title('Predicting',52,392,830,60);title('Credit Card Fraud',52,327,850,60)
   para('A visual investigation of rare-event classification, model selection, calibration and cross-validated risk ranking.',55,281,780,'body')
   metrics=[('699,960','labeled transactions'),('1.67%','fraud prevalence'),('44','supplied figures'),('ROC AUC','primary objective')]
  else:
   title('Thank you.',52,350,850,66)
   para('Research artifacts: notebook, 44 figures, figure manifest, Marp Markdown, HTML and PDF.',55,293,850,'body')
   metrics=[('44 / 44','figures included'),('5-fold','CV framework'),('ROC AUC','competition metric')]
  for i,(v,lab) in enumerate(metrics):
   w=190 if iscover else 260;x=52+i*(w+13)
   rect(x,103,w,87,HexColor('#FFFFFF'),line,9)
   title(v,x+14,149,maxw=w-24,fontsize=25)
   para(lab,x+14,137,w-25,'tiny')
 elif kind=='section':
  code=re.search(r'SECTION (\d+)',body)
  label(f'SECTION {code.group(1) if code else ""} / 06',52,451)
  # break long chapter titles in a natural two-line form.
  words=t.split(); lines=['']
  for word in words:
   if len(lines[-1])+len(word)>19 and lines[-1]:lines.append(word)
   else:lines[-1]=(lines[-1]+' '+word).strip()
  for n,part in enumerate(lines):title(part,52,360-n*59,850,56)
  desc=re.search(r'<div class="chapter-sub">(.*?)</div>',body,re.S)
  para(html.unescape(re.sub('<.*?>','',desc.group(1))) if desc else '',52,200,820,'body')
  pts=re.findall(r'<span>(.*?)</span>',body,re.S)
  for j,p in enumerate(pts):
   x=52+j*287;rect(x,80,274,55,HexColor('#FFFFFF'),line,7)
   para(html.unescape(p),x+12,119,250,'tiny',height=32)
 elif kind=='figure':
  f=s['figure']; info=LOOKUP[f]
  label(info['chapter'],42,497,9.2)
  label(f'FIGURE {FIGURE_INDEX[f]:02d} / 44  ·  SOURCE {f[:2]}',754,497,8.5,muted)
  title(t,42,457,870,29)
  iw,ih=info['pixels'];tall=iw/ih<1.30
  path=PROJECT/'outputs'/'figures'/f
  if tall:
   image_in_box(path,42,65,648,375)
   note(703,267,216,169,'How to read',info['read'],teal)
   note(703,66,216,191,'Interpretation / limit',info['interpret']+' '+info['limitation'],coral)
  else:
   image_in_box(path,42,128,877,309)
   note(42,35,429,86,'What this shows',info['read'],teal)
   note(483,35,436,86,'Interpretation & caution',info['interpret']+' '+info['limitation'],coral)
 else:
  eyebrow=re.search(r'<div class="eyebrow">(.*?)</div>',body,re.S)
  label(html.unescape(eyebrow.group(1)) if eyebrow else 'MODEL ANALYSIS',52,470)
  title(t,52,419,850,38)
  pairs=extract_bold_tags(body)
  if len(pairs)>=4:
   boxes([(html.unescape(re.sub('<.*?>','',a)),html.unescape(re.sub('<.*?>','',b))) for a,b in pairs],starty=401)
  else:
   para(html.unescape(re.sub('<.*?>','',body)),52,340,845,'body')
  extra=re.findall(r'<div class="strip">(.*?)</div>',body,re.S)
  if extra:
   C.setFillColor(coral);C.rect(54,37,4,37,fill=1,stroke=0)
   para(html.unescape(re.sub('<.*?>','',extra[-1])),70,67,820,'small')
 foot(ix)
 C.showPage()
C.save()
print(f'PDF created: {OUTPUT}, {len(META)} pages, {len(LOOKUP)} figures')
