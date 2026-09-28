
from PIL import Image
import sys
before = Image.open(sys.argv[1]); after = Image.open(sys.argv[2])
crops = {'horizon': (0, 430, 256, 256), 'foreground': (340, 700, 256, 256), 'moon': (700, 0, 256, 256), 'sky': (300, 0, 256, 256)}
for name,(x,y,w,h) in crops.items():
    b = before.crop((x,y,x+w,y+h)).resize((512,512), Image.NEAREST)
    a = after.crop((x,y,x+w,y+h)).resize((512,512), Image.NEAREST)
    combo = Image.new('RGB',(1024,512))
    combo.paste(b,(0,0)); combo.paste(a,(512,0))
    combo.save('compare_'+name+'.png')
    print('wrote compare_'+name+'.png')
