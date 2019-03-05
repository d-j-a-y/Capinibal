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


class CpbServer(liblo.ServerThread):
    def __init__(self):
        liblo.ServerThread.__init__(self, port)

    @liblo.make_method('/cpb/speed', 'f')
    def speed_callback(self, path, args):
        global speed
        global verbose
        if(verbose): print("Old speed:", speed)
        speed=int(1000.0*float(args[0])/float(fps))
        if (speed <1): speed=1
        if (speed > 1000): speed=1000
        if(verbose): print("received OSC message '%s' with argument: %f , speed set to %d" % (path, args[0], speed))

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
    with Image(width=1024, height=576, background=Color('lightblue')) as img:
        half_width = 512;
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

# currently unused
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

def cpb_img_gen_solo_centered (cpb_texte, ctx):
    metrics = cpb_get_text_metrics ( cpb_texte, ctx ) # FIXME all texts are not same lenght, loop to get max widht ?
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
    with Image(width=1024, height=576, background=Color('lightgreen')) as img:
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
    with Drawing() as ctx :
        ctx.font = './Sudbury_Basin_3D.ttf' #FIXME !
        ctx.font_size = 110
        ctx.fill_color = Color('black')

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
        try:
            # Loop over frames
            while (frames>=0):
                frames -= step
                phase += speed
                if (verbose): print ("frames:", frames, " in_loop:", in_loop, " in_blink:", in_blink, " in_matrix:", in_matrix, " matrix_align:", matrix_align, " phase:", phase )
                if (phase >= 1000) or (first_time):
                    if (verbose): print("new image")
                    first_time = False
                    phase=phase%1000
                    cpb_text_color_gen (ctx, 3)
                    if (in_matrix == False):
                        cpb_textes = cpb_text_gen_solo()
                        blob = cpb_img_gen_solo_rdn_size_centered(cpb_textes, ctx, 5 ).make_blob('RGB')
                    else:
                        cpb_textes = cpb_text_gen_full()
                        blob = cpb_img_gen_matrix(cpb_textes, ctx, matrix_align).make_blob('RGB')

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

    parser = argparse.ArgumentParser(description='Generate another anticapitalist moving images to a named pipe...or not.')
    parser.add_argument('-o', '--output', dest='outputfile',
                       help='Output file')
    parser.add_argument('-r', '--rate', dest='fps', default='24',
                       help='Frames per second')
    parser.add_argument('-d', '--duration', dest='duration', default='0',
                       help='Seconds, 0 for infinite')
    parser.add_argument('-s', '--speed', dest='speed_of_change', default='4',
                       help='Speed of change (changes per second)')
    parser.add_argument('-p', '--pipe', dest='pipename',
                       help='Name of the pipe to stream to, if missing, name is generated')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable debug output (default: off)')
    args = vars(parser.parse_args())
    #print(args)

    random.seed()

    fps=args['fps']
    verbose=args['verbose']
    duration=args['duration']
    frames = int(float(fps) * float(duration))
    outputfile=args['outputfile']
    speed=int(1000.0*float(args['speed_of_change'])/float(fps))
    if (speed <1): speed=1
    if (speed > 1000): speed=1000
    print("speed:", float(args['speed_of_change']), ' becomes ', speed)
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
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', '1024x576', # size of one frame
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
                    '-s', '1024x576', # size of one frame
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
        os.rmdir(tmpdir)
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
