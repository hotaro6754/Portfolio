from PIL import Image
import os

def mk_trans(f):
    if not os.path.exists(f): return
    img = Image.open(f).convert('RGBA')
    # Use standard list comprehension over getdata()
    datas = list(img.getdata())
    new_data = []
    # threshold for black
    for item in datas:
        if item[0] < 30 and item[1] < 30 and item[2] < 30:
            new_data.append((255, 255, 255, 0)) # transparent
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save('trans_' + f)

mk_trans('real_jin.png')
mk_trans('real_shimura.png')
