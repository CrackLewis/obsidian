
```python
import sys,subprocess,math
try:
 from PIL import Image
except ImportError:
 subprocess.check_call([sys.executable,'-m','pip','install','pillow','-q'])
 from PIL import Image

M=255*256*256
C=64
D=22
def e(f,o):
 d=open(f,'rb').read()
 p=len(d).to_bytes(8,'big')+d
 p+=b'\0'*(-len(p)%C)
 a=[]
 for i in range(0,len(p),C):
  n=int.from_bytes(p[i:i+C],'big');t=[0]*D
  for j in range(D-1,-1,-1):n,t[j]=divmod(n,M)
  a+=t
 c=len(a)
 w=math.ceil(math.sqrt(c+1))
 h=math.ceil((c+1)/w)
 pix=[(0,0,0)]*(w*h)
 for i,x in enumerate(a):
  q,b=divmod(x,255)
  pix[i]=(q>>8,q&255,b+1)
 im=Image.new('RGB',(w,h))
 im.putdata(pix)
 im.save(o)

def d(f,o):
 im=Image.open(f).convert('RGB')
 a=[]
 for r,g,b in im.getdata():
  if b==0:break
  a.append(((r<<8)|g)*255+b-1)
 p=bytearray()
 for i in range(0,len(a),D):
  blk=a[i:i+D];blk+=[0]*(D-len(blk))
  n=0
  for x in blk:n=n*M+x
  p+=n.to_bytes(C,'big')
 l=int.from_bytes(p[:8],'big')
 open(o,'wb').write(p[8:8+l])

(e if sys.argv[1]=='e' else d)(sys.argv[2],sys.argv[3])
```