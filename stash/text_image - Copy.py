__author__ = 'Wei Cao'

from PIL import Image
import sys

# def six_step_gray(x):
#     # if 0 <= x && x <= 41
#     #     return ''
#     # if 41 < x && x <= 83 
#     #     return ''
#     if x < 62:
#         return ' '
#     elif x >= 62 and x < 124:
#         return '|'
#     elif x > 124 and x < 186:
#         return '%'
#     else:
#         return '&'

def six_step_gray(x):
    # if 0 <= x && x <= 41
    #     return ''
    # if 41 < x && x <= 83 
    #     return ''
    if x < 41:
        return ' '
    elif x >= 41 and x < 83:
        return '|'
    elif x > 83 and x < 124:
        return '*'
    elif x > 124 and x < 165:
        return '%'
    elif x > 165 and x < 206:
        return '$'
    elif x > 206 and x < 247:
        return '&'
    else:
        return '&'

def rgb2gray(argb):
    return 0.299 * argb[0] + 0.587 * argb[1] + 0.114 * argb[2]

def avg_gray(pix, row, line, pixels_in_block_row, pixels_in_block_line):
    print("avg_gray start", row, line, pixels_in_block_row, pixels_in_block_line)
    pixels_in_block_row = int(pixels_in_block_row)
    pixels_in_block_line = int(pixels_in_block_line)
    gray = pixels = 0
    for i in range(pixels_in_block_row):
        for j in range(pixels_in_block_line):
            pixels += 1
            # print row * pixels_in_block_row + i, line * pixels_in_block_line + j
            gray += rgb2gray(pix[row * pixels_in_block_row + i, line * pixels_in_block_line + j])

    return gray / pixels

def display_jgp(file, blocks = 10):
    try:
        im = Image.open(file)
        w, h = im.size
        # print w, h
        pix = im.load()
        import PIL.ExifTags
        exif = {}
        try:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in im._getexif().items()
                    if k in PIL.ExifTags.TAGS
            }
        except AttributeError as e:
            exif['Orientation'] = 1

        if exif['Orientation'] == 1:
            for j in range(0, blocks):
                print("")
                for i in range(0, blocks):
                    sys.stdout.write(six_step_gray(avg_gray(pix, i, j, w / blocks, h / blocks)))
        else:
            for i in range(0, blocks):
                print("")
                for j in range(0, blocks):
                    sys.stdout.write(six_step_gray(avg_gray(pix, i, j, w / blocks, h / blocks)))
        
    except IOError as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: %s image_file \n" % sys.argv[0])\
    
    display_jgp(sys.argv[1])