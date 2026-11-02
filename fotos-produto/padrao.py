"""Padrão Modestino de foto de produto: fundo cinza de estúdio, sombra leve, mais claridade."""
import sys, glob, os
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
R=os.path.dirname(os.path.abspath(__file__))
NOMES={'778c1ef8':'preta-frente-bracos-atras','f236a50d':'preta-frente','a54b8329':'preta-inteira','0c95d702':'preta-frente-2',
 '9c5418d2':'offwhite-34','aa88a432':'offwhite-frente','98cc85d2':'offwhite-frente-2','68dc03e2':'offwhite-detalhe-ombro',
 '91f8f944':'mapple-lado','45101948':'mapple-frente','662aecb7':'mapple-gola','d1d8bcbd':'mapple-gola-2','4becd4b1':'mapple-manga',
 '8a59f98c':'mapple-inteira','3df4786a':'preta-ombro','5a0a2e81':'preta-frente-close'}
TOPO={'a54b8329':.115,'0c95d702':.115,'8a59f98c':.10,'9c5418d2':.085,'5a0a2e81':.11}
COR=np.array((236,235,232),float)
def fundo(W,H):
    yy,xx=np.mgrid[0:H,0:W]; r=np.hypot(xx/W-.5,yy/H-.42)
    bg=np.clip(COR+10*np.exp(-(r/.35)**2)[...,None]-14*(r**2)[...,None],0,255)
    return Image.fromarray(bg.astype('uint8')).convert('RGBA')
def tratar(s):
    a=np.array(s).astype(float); rgb=a[...,:3]
    azul=(rgb[...,2]>rgb[...,0]+35)&(rgb[...,2]>rgb[...,1]+25)   # luz azul (isqueiro/celular)
    if azul.sum()>50:
        from scipy import ndimage as ndi
        d=ndi.binary_dilation(azul,iterations=12); m=np.clip(ndi.gaussian_filter(d.astype(float),6)*1.5,0,1)
        w=(~d).astype(float); viz=np.dstack([ndi.gaussian_filter(rgb[...,c]*w,25)/np.maximum(ndi.gaussian_filter(w,25),1e-3) for c in range(3)])
        rgb=rgb*(1-m[...,None])+viz*m[...,None]
    rgb=(rgb/255)**0.88*255
    img=Image.fromarray(np.clip(rgb,0,255).astype('uint8'))
    img=ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(1.04)).enhance(1.06).filter(ImageFilter.UnsharpMask(2,40,3))
    out=img.convert('RGBA'); out.putalpha(s.split()[3]); return out
def ndi_blur(m):
    from scipy import ndimage as ndi
    return np.clip(ndi.gaussian_filter(ndi.binary_dilation(m>0,iterations=12).astype(float),6)*1.5,0,1)
def ndi_med(rgb):
    from scipy import ndimage as ndi
    return np.dstack([ndi.median_filter(rgb[...,c],size=61) for c in range(3)])
def compor(s,W,H):
    al=np.array(s.split()[3])>128; ys,xs=np.nonzero(al)
    cx=(xs.min()+xs.max())/2
    k=max(W/s.width, H/s.height); S=s.resize((int(s.width*k)+1,int(s.height*k)+1),Image.LANCZOS)
    ox=int(W/2-cx*k); ox=min(0,max(W-S.width,ox)) if S.width>=W else ox
    f=fundo(W,H); a=S.split()[3]
    pad=Image.new('L',(W,H),0); pad.paste(a,(ox+int(.01*W),-int(.023*H))); pad.paste(a.crop((0,0,S.width,int(.04*H))),(ox+int(.01*W),0))
    sh=Image.new('RGBA',(W,H),(30,28,26,0)); sh.putalpha(pad.point(lambda v:v*.2).filter(ImageFilter.GaussianBlur(W*.019))); f.alpha_composite(sh)
    f.alpha_composite(S,(ox,0)); return f.convert('RGB')
for f in sorted(glob.glob(R+'/recortes/*.png')):
    k=os.path.basename(f)[:8]; s=Image.open(f).convert('RGBA')
    t=TOPO.get(k,0); s=s.crop((0,int(s.height*t),s.width,s.height)); s=tratar(s); n=NOMES[k]
    compor(s,1600,2000).save(f'{R}/final/{n}_ecommerce_1600x2000.jpg',quality=92)
    compor(s,1200,1200).save(f'{R}/final/{n}_mercadolivre_1200x1200.jpg',quality=92)
    compor(s,1080,1350).save(f'{R}/final/{n}_instagram_1080x1350.jpg',quality=92)
    print(n)
