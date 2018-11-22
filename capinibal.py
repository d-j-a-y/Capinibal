#!/usr/bin/python3
"""Main file for Capinibal the another anticapitalist images generator."""

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

import random
import subprocess
import time
import os, tempfile
import argparse

#cpb_pattern = "CA{}I{}AL"
#cpb_textes = ['CABINAL', 'CAPIBAL', 'CATINAL', 'CANIBAL', 'CABITAL', 'CAPITAL', 'CABIPAL', 'CATIPAL', 'CAPINAL', 'CATIBAL']

#############
#
# Utils
#
############################

def cpb_text_gen_solo ():
    candidate_letter = ['P', 'B', 'T', 'N']
    txt = "CA"
    cddt_index = random.randrange(0, len(candidate_letter))
    txt = txt + candidate_letter[cddt_index]
    candidate_letter.pop(cddt_index)
    txt = txt + "I"
    txt = txt + candidate_letter[random.randrange(0, len(candidate_letter))]
    txt = txt + "AL"
    return txt

def cpb_text_gen_full ():
    txt_list = []
    for i in range (0, 10) :
        txt_list.append (cpb_text_gen_solo())
    return txt_list

def cpb_get_text_metrics ( text_to_mesure , draw ):

    dummy_image = Image(filename='wizard:')
    metrics = draw.get_font_metrics( dummy_image, text_to_mesure )

    return metrics

# toss : give kind of rand rythm
def cpb_text_color_gen (ctx, toss) :
    toss = int(toss)
    if (toss < 1) : toss = 1
    if (random.randrange(1, toss) == 1) :
        # ~ color FFFFFF -> 16777215
        color = random.randrange(0, 16777215, 15)
        red = color >>16
        green = ( color >> 8 ) & 0xFF
        blue = color & 0xFF
        # ~ print ("color 0x%x , r 0x%x , g 0x%x , b 0x%x" % (color, red , green , blue))
        ctx.fill_color = Color('rgb({0},{1},{2})'.format(red,green,blue))

#############
#
# Image generation routines
#
############################
def cpb_img_gen_matrix (cpb_textes, ctx, align_center):
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
    with Image(width=1024, height=576, background=Color('lightblue')) as img:
        half_width = 512;
        print(img)
        textes_len = int(len (cpb_textes) / 2)
        with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
            for i in range (0, textes_len) :
                metrics = cpb_get_text_metrics ( cpb_textes[i], ctx ) # left side text size
                if (align_center) :
                    clone_ctx.text(half_width - int(metrics.text_width) - 1 , (1+i)*int(metrics.ascender), cpb_textes[i])
                    clone_ctx.text(half_width + 1, (1+i)*int(metrics.ascender), cpb_textes[i+textes_len])
                else :
                    clone_ctx.text(5, (1+i)*int(metrics.ascender), cpb_textes[i])
                    clone_ctx.text(int(metrics.text_width), (1+i)*int(metrics.ascender), cpb_textes[i+textes_len])
                clone_ctx(img)

        return img.clone()
        # ~ display(img)

def cpb_seq_gen_matrix (cpb_textes, ctx, pipe) :
    textes_len = len (cpb_textes)
    coord_len = int(textes_len * 4)
    candidate_coord = []
    for i in range (0, coord_len) :
        candidate_coord.append(i)

    clone_ctx = Drawing(drawing=ctx)
    with Image(width=1024, height=576, background=Color('lightsalmon')) as img:
        quarter_width = 256
        deci_height = 57
        for i in range (0, coord_len) :
            print(img)
            coord_index = random.randrange(0, len(candidate_coord))
            coord = candidate_coord[coord_index]
            candidate_coord.pop(coord_index)
            y = int(coord / 4)
            x = coord
            if (coord > 4 ) :
                x = coord % 4
            print (coord, '  :  ' , x , ' - ' , y)
            cddt_text = random.randrange(0, textes_len)
            clone_ctx.text(x * quarter_width, (1+y) * deci_height, cpb_textes[cddt_text])
            clone_ctx(img)
            pipe.stdin.write(img.make_blob('RGB'))

def cpb_img_gen_solo (cpb_texte, ctx):
    metrics = cpb_get_text_metrics ( cpb_texte, ctx ) # FIXME all texts are not same lenght, loop to get max widht ?
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
    with Image(width=1024, height=576, background=Color('lightgreen')) as img:
        print(img)
        textes_len = int(len (cpb_texte) / 2)
        with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
            clone_ctx.text(int((img.width - metrics.text_width )/2), int((img.height+metrics.ascender)/2), cpb_texte)
            clone_ctx(img)

        return img.clone()
        # ~ display(img)

def cpb_img_gen_solo_any_size_center (cpb_texte, ctx) :
    old_size = ctx.font_size
    ctx.font_size = int (random.randrange(55, 200, 15))
    print ("font size " , ctx.font_size)
    img = cpb_img_gen_solo(cpb_texte, ctx)
    ctx.font_size = old_size
    return img

###############################
#
# MainLoop (will be slot machine) and Main
#
#########################################
def cpb_capinibal ( pipe ):
    with Drawing() as ctx :
        ctx.font = '/home/carotte/Sources/OF/examples/sound/soundPlayerExample/bin/data/Sudbury_Basin_3D.ttf'
        ctx.font_size = 110
        ctx.fill_color = Color('black')

        while False:
            cpb_text_color_gen (ctx)
            cpb_textes = cpb_text_gen_solo()
            blob = cpb_img_gen_solo_any_size_center(cpb_textes, ctx).make_blob('RGB')
            pipe.stdin.write ( blob )

        in_loop = 0 # number of matrix image
        in_blink = 5 # number of matrix(s) loop
        in_matrix = False
        matrix_align = False
        try:
            while True:
                cpb_text_color_gen (ctx, 3)
                if (in_matrix == False):
                    cpb_textes = cpb_text_gen_solo()
                    blob = cpb_img_gen_solo(cpb_textes, ctx).make_blob('RGB')
                else:
                    cpb_textes = cpb_text_gen_full()
                    blob = cpb_img_gen_matrix(cpb_textes, ctx, matrix_align).make_blob('RGB')

                pipe.stdin.write( blob )

                in_loop += 1
                if (in_loop > 24): # 24 -> fps
                    in_matrix = True if (in_matrix == False) else False
                    in_blink = in_blink - 1
                    if (in_blink > 0):
                        in_loop = 0
                    else:
                        if (in_blink < - 20):
                            matrix_align = True if (matrix_align == False) else False
                            in_blink = 5

        except SystemExit as e:
            return


# main
if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Generate another anticapitalist moving images to a named pipe...or not.')
    parser.add_argument('-r', '--record', action='store_true',
                       help='Record has video file')
#    parser.add_argument('-p', '--pipe', action='store_true',
 #                      help='Name of the pipe to stream to, if missing, name is generated')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable debug output (default: off)')
    args = vars(parser.parse_args())

    random.seed()

#    rate = 1
    fps, duration = 24, 5

    if (args['record'] == True):
        cmdstring = ['ffmpeg',
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', '1024x576', # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', '8', # frames per second
                    '-i', '-', # The imput comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-c:v', 'mjpeg',
                    '-q', '1',
                    'my_output_videofile.mp4' ]
#    else if (args['image'] == True):
    else:
        tmpdir = tempfile.mkdtemp()
        filename = os.path.join(tmpdir, 'myfifo')
        print ("The fifo is on :\n%s" % filename)

        try:
            os.mkfifo(filename)
        except OSError as e:
            print ("Failed to create FIFO: %s" % e)
            quit()

        fifo = open(filename, 'w')

        cmdstring = ['ffmpeg',
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', '1024x576', # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', '8', # frames per second
                    '-i', '-', # The imput comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-pix_fmt', 'yuv420p',
                    '-f', 'yuv4mpegpipe',
                    filename ]

    pipe = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)


    time.sleep(1)

    frames = duration * fps #FIXME fps same has for ffmpeg string
#    for i in range(frames):

    # Here we loop
    cpb_capinibal ( pipe )

    if (args['record'] == False):
        if (args['debug']):
            print("Cleaning pipe stuff...")
        fifo.close()
        os.remove(filename)
        os.rmdir(tmpdir)


#  has clone          cpb_create_image(cpb_textes, ctx).save(filename="cani_"+str(i)+".png")



#  cat can*.png | ffmpeg -y -f image2pipe -r 25 -vcodec png -i - out.mp4


# ~ https://creativegeekery.wordpress.com/2017/02/06/wrapping-text-with-imagemagick/
# ~ words = para.split(" ")
# ~ lines = []
# ~ with Image(height=10, width=10) as img:
  # ~ line = words.pop(0)
  # ~ for word in words:
    # ~ line_width = draw.get_font_metrics(img,
      # ~ line + " " + word).text_width
    # ~ if line_width < max_width:
      # ~ line = line + " " + word
    # ~ else:
      # ~ lines.append(line)
      # ~ line = word
  # ~ if line != "":
    # ~ lines.append(line)
# ~ return lines
