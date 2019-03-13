#!/usr/bin/python3
"""Main file for Capinibal another anticapitalist images generator."""

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color


import sys
import random
import subprocess
import time
import os, tempfile
import argparse

# liblo - see http://das.nasophon.de/pyliblo/examples.html
import liblo

################### FABRIQUE
# ~ class CasNormal :
    # ~ def uneMethode(self) :
        # ~ print("normal")

# ~ class CasSpecial :
    # ~ def uneMethode(self) :
        # ~ print("special")


# ~ def casQuiConvient(estNormal=True) :
    # ~ """Fonction fabrique renvoyant une classe."""
    # ~ if estNormal :
        # ~ return CasNormal()
    # ~ else :
        # ~ return CasSpecial()


# ~ def cpb_generator (gen_type):
    # ~ if (gen_type == "color") :
        # ~ return cpb_gen_color ()
    # ~ else if (gen_type == "size") :
        # ~ return cpb_gen_color ()


# ~ class cpb_gen_color :
    # ~ def __init__ (self) :

class Capinibal:
    duration = 0
    frame = 0
    fps = 24
    speed = 200
    port = 1234
    outputfile = ""
    verbose = False

#cpb_pattern = "CA{}I{}AL"
#cpb_textes = ['CABINAL', 'CAPIBAL', 'CATINAL', 'CANIBAL', 'CABITAL', 'CAPITAL', 'CABIPAL', 'CATIPAL', 'CAPINAL', 'CATIBAL']

#############
#
# Utils
#
############################

verbose = False
speed = 200
port = 1234
fps = 24
image_width = 1024
image_height = 576
# image = None

def cpb_setspeed(s) :
    global speed, verbose
    speed=int(1000.0*float(s)/float(fps))
    if (speed < 1): speed=1
    if (speed > 1000): speed=1000
    if (verbose):
        print("Speed:", float(s), "changes/s becomes", speed, "changes/1000 frames")

class CpbServer(liblo.ServerThread):
    def __init__(self):
        liblo.ServerThread.__init__(self, port)

    @liblo.make_method('/cpb/speed', 'f')
    def speed_callback(self, path, args):
        global speed, verbose
        if(verbose):
            print("received OSC message '%s' with argument: %f" % (path, args[0]))
        if(verbose): print("Old speed:", speed)
        cpb_setspeed(args[0])

    @liblo.make_method(None, None)
    def fallback(self, path, args):
        print("received unknown OSC message '%s'" % path)

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

def cpb_text_gen_full (n=10):
    txt_list = []
    for i in range (0, n) :
        txt_list.append (cpb_text_gen_solo())
    return txt_list

def cpb_get_text_metrics ( text_to_mesure , draw ):

    dummy_image = Image(filename='wizard:')
    metrics = draw.get_font_metrics( dummy_image, text_to_mesure )

    return metrics

# toss : give kind of rand rythm
def cpb_text_color_gen (ctx, coin = 1) :
    if (cpb_toss (coin)) :
        # ~ color FFFFFF -> 16777215
        color = random.randrange(0, 16777215, 15)
        red = color >>16
        green = ( color >> 8 ) & 0xFF
        blue = color & 0xFF
        # ~ print ("color 0x%x , r 0x%x , g 0x%x , b 0x%x" % (color, red , green , blue))
        ctx.fill_color = Color('rgb({0},{1},{2})'.format(red,green,blue))

def cpb_toss (coin) :
    coin = int(coin)
    if (coin <= 1) : return True
    if (random.randrange(1, coin) == 1) :
        return True
    return False
    
#############
#
# Image generation routines
#
############################
def cpb_img_gen_matrix (cpb_textes, ctx, align_center = False):
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
#    global image
#    with image.clone() as img:
    with cpb_img_gen_matrix.image.clone() as img:
        half_width = int(image_width / 2)
        if (verbose): print(img)
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

def cpb_img_gen_matrix_line (cpb_textes, ctx, img, align_center = False):
    if (verbose): print(img)
    # FIXME rows and columns should be parameters
    cols=2
    rows=5
    grid_len = rows * cols
    col_width = image_width // cols
    row_height = image_height // rows
    textes_len = len (cpb_textes)
    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if (cpb_img_gen_matrix.step==0):
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            # cpb_img_gen_matrix.image=Image(width=image_width, height=image_height, background=Color('lightblue'))
            clone_ctx.composite('clear', 0, 0, image_width, image_height, img)
        y=cpb_img_gen_matrix.step
        texte_num = cols * y
        for x in range (0, cols):
            metrics = cpb_get_text_metrics ( cpb_textes[texte_num], ctx ) # text size
            w=int(metrics.text_width)
            h=int(metrics.ascender)
            hmargin=1
            if (align_center) :
                hmargin=(col_width-w)//2
            if (hmargin<0):
                print('Alignment problem:', cpb_textes[texte_num], 'width:', w)
                hmargin=0
            vmargin=(row_height-h)//2
            if (vmargin<0):
                print('Alignment problem:', cpb_textes[texte_num], 'height:', h)
                vmargin=0
            clone_ctx.text(x*col_width+hmargin, y*row_height+vmargin+h, cpb_textes[texte_num])                
            texte_num +=1 
        clone_ctx(img)
    cpb_img_gen_matrix.step+=1
    if (cpb_img_gen_matrix.step>=rows): cpb_img_gen_matrix.step=0
    #~ return img.clone()

def cpb_img_gen_matrix_grid (cpb_textes, ctx, img, align_center = False):
    #~ with image as img: # Causes the image to be closed!
    if (verbose): print(img)
    # FIXME rows and columns should be parameters
    cols=2
    rows=5
    grid_len = rows * cols
    col_width = image_width // cols
    row_height = image_height // rows
    textes_len = len (cpb_textes) # may be different from grid_len

    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if (cpb_img_gen_matrix.step==0):
            cpb_img_gen_matrix_grid.cells_num = list(range(0, grid_len))
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            clone_ctx.composite('clear', 0, 0, image_width, image_height, img)
        k = random.randrange(0, len(cpb_img_gen_matrix_grid.cells_num))
        i = cpb_img_gen_matrix_grid.cells_num[k]
        cpb_img_gen_matrix_grid.cells_num.pop(k)
        x= i % cols
        y= i // cols
        texte_num = i % textes_len # in case there are less texts than cells
        metrics = cpb_get_text_metrics ( cpb_textes[texte_num], ctx ) # text size
        w=int(metrics.text_width)
        h=int(metrics.ascender)
        hmargin=1
        if (align_center) :
            hmargin=(col_width-w)//2
        if (hmargin<0):
            print('Alignment problem:', cpb_textes[texte_num], 'width:', w)
            hmargin=0
        vmargin=(row_height-h)//2
        if (vmargin<0):
            print('Alignment problem:', cpb_textes[texte_num], 'height:', h)
            vmargin=0
        clone_ctx.text(x*col_width+hmargin, y*row_height+vmargin+h, cpb_textes[texte_num])
        clone_ctx(img)
    cpb_img_gen_matrix.step+=1
    if (cpb_img_gen_matrix.step>=grid_len): cpb_img_gen_matrix.step=0
    #~ return img.clone()

# currently unused
def cpb_seq_gen_matrix (cpb_textes, ctx, pipe) :
    textes_len = len (cpb_textes)
    coord_len = int(textes_len * 4)
    candidate_coord = []
    for i in range (0, coord_len) :
        candidate_coord.append(i)

    clone_ctx = Drawing(drawing=ctx)
    with Image(width=image_width, height=image_height, background=Color('lightsalmon')) as img:
        quarter_width = image_width / 4
        deci_height = int(image_height / 10)
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

def cpb_img_gen_solo_centered (cpb_texte, ctx):
    metrics = cpb_get_text_metrics ( cpb_texte, ctx ) # FIXME all texts are not same length, loop to get max widht ?
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
    with Image(width=image_width, height=image_height, background=Color('lightgreen')) as img:
        if (verbose): print(img)
        textes_len = int(len (cpb_texte) / 2)
        with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
            clone_ctx.text(int((img.width - metrics.text_width )/2), int((img.height+metrics.ascender)/2), cpb_texte)
            clone_ctx(img)

        return img.clone()
        # ~ display(img)

def cpb_img_gen_solo_rdn_size_centered (cpb_texte, ctx, coin=1) :
    old_size = ctx.font_size
    if (cpb_toss (coin)) :
        ctx.font_size = int (random.randrange(55, 200, 15))
        if(verbose): print ("font size " , ctx.font_size)

    img = cpb_img_gen_solo_centered(cpb_texte, ctx)
    ctx.font_size = old_size
    return img

###############################
#
# MainLoop (will be slot machine) and Main
#
#########################################
def cpb_capinibal ( pipe, frames):
    ctx1=Drawing()
    ctx1.font = './Sudbury_Basin_3D.ttf' #FIXME !
    ctx1.font_size = 107
    ctx1.fill_color = Color('black')
    ctx2=Drawing()
    ctx2.font = './Sudbury_Basin.ttf' #FIXME !
    ctx2.font_size = 107
    ctx2.fill_color = Color('black')
    ctxs=[ctx1, ctx2]
    while False:
        cpb_text_color_gen (ctx, 3)
        cpb_textes = cpb_text_gen_solo()
        blob = cpb_img_gen_solo_rdn_size_centered(cpb_textes, ctx, 5).make_blob('RGB')
        pipe.stdin.write ( blob )

#        return

    step = 1 if (frames>0) else 0 # 0 => infinite loop
    in_loop = 0 # number of matrix image
    in_blink = 5 # number of matrix(s) loop
    in_matrix = False
    matrix_align = False
    phase = 0
    blob = None
    first_time = True

    global image
    image=Image(width=image_width, height=image_height, background=Color('lightblue'))
    #~ cpb_img_gen_matrix.image=Image(width=image_width, height=image_height, background=Color('lightblue'))
    cpb_img_gen_matrix.step=0
    
    try:
        # Loop over frames
        while (frames>=0):
            frames -= step
            phase += speed
            if (verbose): print ("frames:", frames, " in_loop:", in_loop, " in_blink:", in_blink, " in_matrix:", in_matrix, " matrix_align:", matrix_align, " phase:", phase )
            if (phase >= 1000) or (first_time):
                if (verbose): print("new image")
                ctx=ctxs[random.randrange(0, len(ctxs))] # FIXME!
                first_time = False
                phase=phase%1000
                cpb_text_color_gen (ctx, 3)
                if (in_matrix == False):
                    cpb_textes = cpb_text_gen_solo()
                    blob = cpb_img_gen_solo_rdn_size_centered(cpb_textes, ctx, 5 ).make_blob('RGB')
                else:
                    cpb_textes = cpb_text_gen_full()
                    #~ blob = cpb_img_gen_matrix(cpb_textes, ctx, matrix_align).make_blob('RGB')
                    #~ cpb_img_gen_matrix_grid(cpb_textes, ctx, image, matrix_align)
                    cpb_img_gen_matrix_line(cpb_textes, ctx, image, matrix_align)
                    blob = image.make_blob('RGB')

                in_loop += 1
                if (in_loop > 24): # 1 s @ 24 fps
                    in_matrix = True if (in_matrix == False) else False
                    in_blink = in_blink - 1
                    if (in_blink > 0):
                        in_loop = 0
                    else:
                        if (in_blink < - 20):
                            matrix_align = True if (matrix_align == False) else False
                            in_blink = 5

            pipe.stdin.write( blob )

        print("All frames generated")
    except KeyboardInterrupt: # Use this instead of signal.SIGINT
        print("Interrupted, exiting!")
#        except SystemExit as e:
    except BrokenPipeError:
        print("Pipe broken, exiting!")
    return


# main
if __name__=="__main__":

    capinibal = Capinibal()

    parser = argparse.ArgumentParser(description='Generate another anticapitalist moving images to a named pipe...or not.')
    parser.add_argument('-o', '--output', dest='outputfile',
                       help='Output file')
    parser.add_argument('-r', '--rate', dest='fps', default='24',
                       help='Frames per second (default: 24)')
    parser.add_argument('-d', '--duration', dest='duration', default='0',
                       help='Seconds, 0 for infinite (default: 0)')
    parser.add_argument('-s', '--speed', dest='speed_of_change', default='4',
                       help='Speed of change per second (default: 4)')
    parser.add_argument('-p', '--pipe', dest='pipename',
                       help='Name of the pipe to stream to (default: generated name)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable debug output (default: off)')
    args = vars(parser.parse_args())
    if args['verbose'] :
        sorted_by_key = sorted(args.items(), key=lambda x: x[0])
        print ('Arguments:\n', sorted_by_key, '\n')

    capinibal.fps = args['fps']
    fps=args['fps']
    capinibal.verbose=args['verbose']
    verbose=args['verbose']
    capinibal.duration=args['duration']
    duration=args['duration']
    capinibal.frames = int(float(fps) * float(duration))
    frames = int(float(fps) * float(duration))
    capinibal.outputfile=args['outputfile']
    outputfile=args['outputfile']

    encoder = None
    status, result = subprocess.getstatusoutput("avconv")
    if (status == 1):
        encoder='avconv'
    status, result = subprocess.getstatusoutput("ffmpeg")
    if (status == 1):
        encoder='ffmpeg'
    if (encoder is None):
        print("Missing dependency : You need to install ffmpeg or avconv.")
        exit ()

    if (verbose) : print ('Encoder selected:', encoder, '\n')

    cpb_setspeed(args['speed_of_change'])

    random.seed()

    print('Generating', frames, 'frames for', duration, 'seconds at', fps, 'fps, change every', 1000/speed, 'frame, with', encoder, 'as encoder.')

    try:
        server = CpbServer()
    except (liblo.ServerError):
        print ("OSC failure!")
        sys.exit()
        
    if (outputfile is None):
        # No output file, use a pipe
        if (args['pipename'] is None):
            tmpdir = tempfile.mkdtemp()
            filename = os.path.join(tmpdir, 'myfifo')
        else:
            tmpdir = None
            filename=args['pipename']
        print ("The fifo is on :\n%s" % filename, file=sys.stderr)

        try:
            os.mkfifo(filename)
        except OSError as e:
            print ("Failed to create FIFO: %s" % e, file=sys.stderr)
            quit()

        try:
            fifo = open(filename, 'w')
        except KeyboardInterrupt: # Use this instead of signal.SIGINT
            print("Interrupted, exiting!")
            sys.exit()


        cmdstring = [encoder,
                    '-loglevel', 'warning',
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', str(image_width)+'x'+str(image_height), # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', fps, # frames per second
                    '-i', '-', # The input comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-pix_fmt', 'yuv420p',
                    '-f', 'yuv4mpegpipe',
                    filename ]
    else:
        # Use given output file
        print ("The output file is :\n%s" % outputfile, file=sys.stderr)
        # No infinite duration!
        if (frames<1):
            print("Non-zero duration required when using -o, aborting.", file=sys.stderr)
            sys.exit()
        cmdstring = [encoder,
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', str(image_width)+'x'+str(image_height), # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', fps, # frames per second
                    '-i', '-', # The input comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-c:v', 'mjpeg',
                    '-q', '1',
                    outputfile ] # Unique name

    pipe = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    time.sleep(1)

    server.start()
    
    # Here we loop

    cpb_capinibal (pipe, frames)

    if (args['outputfile'] is None):
        print("Cleaning pipe stuff...", file=sys.stderr)
        fifo.close()
        os.remove(filename)
        if(tmpdir): os.rmdir(tmpdir)
    print("Terminated normally")


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
