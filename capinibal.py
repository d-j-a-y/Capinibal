#!/usr/bin/python3
"""Main file for Capinibal another anticapitalist images generator."""

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import wand.version 


import sys
import random
import subprocess
import time
import os, tempfile
import argparse

# liblo - see http://das.nasophon.de/pyliblo/examples.html
import liblo

################### FABRIQUE
# ~ class CasNormal:
    # ~ def uneMethode(self):
        # ~ print("normal")

# ~ class CasSpecial:
    # ~ def uneMethode(self):
        # ~ print("special")


# ~ def casQuiConvient(estNormal=True):
    # ~ """Fonction fabrique renvoyant une classe."""
    # ~ if estNormal:
        # ~ return CasNormal()
    # ~ else:
        # ~ return CasSpecial()


# ~ def cpb_generator (gen_type):
    # ~ if (gen_type == "color"):
        # ~ return cpb_gen_color ()
    # ~ else if (gen_type == "size"):
        # ~ return cpb_gen_color ()


# ~ class cpb_gen_color:
    # ~ def __init__ (self):

# see https://stackoverflow.com/questions/4092528/how-to-clamp-an-integer-to-some-range
cpb_clip = lambda x, l, u: l if x < l else u if x > u else x

class Capinibal:
    duration = 0
    frame = 0
    fps = 24
    image_width = 1024
    image_height = 576
    speed = 200
    port = 1234
    verbose = False
    texts = [
        'CAPITAL', 'CAPINAL', 'CAPIBAL',
        'CATIPAL', 'CATINAL', 'CATIBAL',
        'CANIPAL', 'CANITAL', 'CANIBAL',
        'CABIPAL', 'CABITAL', 'CABINAL'
    ]
    fonts = [
        'Sudbury_Basin_3D.ttf',
        'Sudbury_Basin.ttf'
    ]
    # The max* lists will be populated with one item per font
    max_width = []
    max_height = []
    # max_max* will be set for all fonts, all texts
    max_max_width = 0
    max_max_height = 0
    ref_font_size = 100
    min_font_size = 55
    max_font_size = 200
    hspacing = 4
    vspacing = 4

    # toss: give kind of rand rythm
    def cpb_random_color ():
        # ~ color FFFFFF -> 16777215
        color = random.randrange(0, 16777215, 15)
        red = color >>16
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        # ~ print ("color 0x%x, r 0x%x, g 0x%x, b 0x%x" % (color, red, green, blue))
        return Color('rgb({0},{1},{2})'.format(red,green,blue))

    def cpb_fill_color_gen (ctx, coin = 1):
        if (Capinibal.cpb_toss (coin)):
            ctx.fill_color = Capinibal.cpb_random_color ()

    def cpb_set_bg(ctx, bg_color):
        #~ clone_ctx.composite('clear', 0, 0, image_width, image_height, img) # set to black!
        old_color=ctx.fill_color
        ctx.fill_color=bg_color
        ctx.color(0, 0, 'reset')
        ctx.fill_color=old_color

    def cpb_toss (coin):
        coin = int(coin)
        if (coin <= 1): return True
        if (random.randrange(1, coin) == 1):
            return True
        return False

    def cpb_setspeed(speed):
        Capinibal.speed=cpb_clip(int(1000.0*float(speed)/float(Capinibal.fps)), 1, 1000)
        if Capinibal.verbose:
            print("Speed:", float(speed), "changes/s becomes", Capinibal.speed, "changes/1000 frames")

    def cpb_get_max_metrics(texts, ctx):
        max_width=0
        max_height=0
        for t in texts:
            metrics=cpb_get_text_metrics (t, ctx)
            max_width=max(max_width, metrics.text_width)
            max_height=max(max_height, metrics.text_height)
        return max_width, max_height

    class Effect_parameters:
        cols=2
        rows=5
        ctx = None
        img = None
        align_center = False
        bg_color = Color('lightblue')
        step = 0
        random_order = True
        # ~ def get_param()
        # ~ def inc_rand_param()
        # ~ def dec_rand_param()

#cpb_pattern = "CA{}I{}AL"
#cpb_textes = ['CABINAL', 'CAPIBAL', 'CATINAL', 'CANIBAL', 'CABITAL', 'CAPITAL', 'CABIPAL', 'CATIPAL', 'CAPINAL', 'CATIBAL']

#############
#
# Utils
#
############################

class CpbServer(liblo.ServerThread):
    def __init__(self):
        liblo.ServerThread.__init__(self, Capinibal.port)

    @liblo.make_method('/cpb/speed', 'f')
    def speed_callback(self, path, args):
        if(Capinibal.verbose):
            print("received OSC message '%s' with argument: %f" % (path, args[0]))
        if(Capinibal.verbose): print("Old speed:", Capinibal.speed)
        Capinibal.cpb_setspeed(args[0])

    @liblo.make_method(None, None)
    def fallback(self, path, args):
        print("received unknown OSC message '%s'" % path)

def cpb_text_gen_solo ():
    return random.choice(Capinibal.texts)
    
def cpb_text_gen_solo_alt ():
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
    for i in range (0, n):
        txt_list.append (cpb_text_gen_solo())
    return txt_list

def cpb_get_text_metrics (text_to_measure, draw):

    dummy_image = Image(filename='wizard:')
    metrics = draw.get_font_metrics(dummy_image, text_to_measure)

    return metrics

#############
#
# Image generation routines
#
############################
def cpb_img_gen_matrix (cpb_textes, ctx, img):
    # Generate complete matrix in one step
    if Capinibal.verbose: print(img)
    bg_color=Capinibal.Effect_parameters.bg_color
    align_center=Capinibal.Effect_parameters.align_center
    cols=Capinibal.Effect_parameters.cols
    rows=Capinibal.Effect_parameters.rows
    col_width = Capinibal.image_width // cols
    row_height = Capinibal.image_height // rows
    textes_len = len (cpb_textes) # may be different from grid length

    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        Capinibal.cpb_set_bg(clone_ctx, bg_color)
        # Fill grid with text
        for i in range (0, cols):
            for j in range (0, rows):
                # What about changing colors between rows/between cells?
                text = cpb_textes[(i + cols * j) % textes_len]
                metrics = cpb_get_text_metrics (text, ctx) # FIXME should be pre-computed
                a=int(metrics.ascender)
                if (align_center):
                    hmargin = (col_width-int(metrics.text_width))//2
                    vmargin = (row_height-int(metrics.text_height))//2
                else:
                    hmargin = Capinibal.hspacing // 2
                    vmargin = Capinibal.vspacing // 2
                clone_ctx.text(i*col_width+hmargin, j*row_height+vmargin+a, text) # Fill to bottom
                clone_ctx(img)

def cpb_img_gen_matrix_line (cpb_textes, ctx, img):
    # generate a matrix image, one row at a time
    if Capinibal.verbose: print(img)
    bg_color = Capinibal.Effect_parameters.bg_color
    align_center = Capinibal.Effect_parameters.align_center
    cols = Capinibal.Effect_parameters.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.Effect_parameters.rows
    row_height = Capinibal.image_height // rows
    textes_len = len (cpb_textes)
    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if Capinibal.verbose: print('step ', Capinibal.Effect_parameters.step)
        if Capinibal.Effect_parameters.step==0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, bg_color)
            cpb_img_gen_matrix_line.lines_num = list(range(0, rows))
        if Capinibal.Effect_parameters.random_order :
            k = random.randrange(0, len(cpb_img_gen_matrix_line.lines_num))
            y = cpb_img_gen_matrix_line.lines_num[k]
            cpb_img_gen_matrix_line.lines_num.pop(k)
        else:
            y = Capinibal.Effect_parameters.step
        
        for x in range (0, cols):
            text = cpb_textes[(x + cols * y) % textes_len]
            metrics = cpb_get_text_metrics (text, clone_ctx) # text size
            w = int(metrics.text_width)
            h = int(metrics.ascender)
            hmargin=Capinibal.hspacing//2
            if (align_center):
                hmargin = (col_width-w) // 2
            if (hmargin<0):
                print('Alignment problem:', text, 'width:', w)
                hmargin = 0
            vmargin=(row_height-h) // 2
            if (vmargin<0):
                print('Alignment problem:', text, 'y:', y, 'row height:', row_height,
                 'rows:', rows, 'text height:', h, 'font size:', clone_ctx.font_size)
                vmargin = 0
            clone_ctx.text(x*col_width+hmargin, y*row_height+vmargin+h, text)
        clone_ctx(img)
    Capinibal.Effect_parameters.step=(Capinibal.Effect_parameters.step+1) % rows

def cpb_img_gen_matrix_col (cpb_textes, ctx, img):
    # generate a matrix image, one column at a time
    if Capinibal.verbose: print(img)
    bg_color = Capinibal.Effect_parameters.bg_color
    align_center = Capinibal.Effect_parameters.align_center
    cols = Capinibal.Effect_parameters.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.Effect_parameters.rows
    row_height = Capinibal.image_height // rows
    textes_len = len (cpb_textes)
    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if Capinibal.verbose: print('step ', Capinibal.Effect_parameters.step)
        if Capinibal.Effect_parameters.step==0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, bg_color)
            cpb_img_gen_matrix_col.cols_num = list(range(0, cols))
        if Capinibal.Effect_parameters.random_order :
            k = random.randrange(0, len(cpb_img_gen_matrix_col.cols_num))
            x = cpb_img_gen_matrix_col.cols_num[k]
            cpb_img_gen_matrix_col.cols_num.pop(k)
        else:
            x = Capinibal.Effect_parameters.step
        
        for y in range (0, rows):
            text = cpb_textes[(x + cols * y) % textes_len]
            metrics = cpb_get_text_metrics (text, clone_ctx) # text size
            w = int(metrics.text_width)
            h = int(metrics.ascender)
            hmargin=Capinibal.hspacing//2
            if (align_center):
                hmargin = (col_width-w) // 2
            if (hmargin<0):
                print('Alignment problem:', text, 'width:', w)
                hmargin = 0
            vmargin=(row_height-h) // 2
            if (vmargin<0):
                print('Alignment problem:', text, 'y:', y, 'row height:', row_height,
                 'rows:', rows, 'text height:', h, 'font size:', clone_ctx.font_size)
                vmargin = 0
            clone_ctx.text(x*col_width+hmargin, y*row_height+vmargin+h, text)
        clone_ctx(img)
    Capinibal.Effect_parameters.step=(Capinibal.Effect_parameters.step+1) % cols

def cpb_img_gen_matrix_grid (cpb_textes, ctx, img):
    # generate a matrix image, one cell at a time
    # What about populating adjacent cells, worm-like?
    if Capinibal.verbose: print(img)
    align_center = Capinibal.Effect_parameters.align_center
    cols = Capinibal.Effect_parameters.cols
    rows = Capinibal.Effect_parameters.rows
    grid_len = rows * cols
    col_width = Capinibal.image_width // cols
    row_height = Capinibal.image_height // rows
    textes_len = len (cpb_textes) # may be different from grid_len

    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if cpb_img_gen_matrix_grid.cells_num == []:
            Capinibal.Effect_parameters.step = 0
        if Capinibal.Effect_parameters.step == 0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.Effect_parameters.bg_color)
            # FIXME! could be visually interesting to optionally keep same context for all steps
            cpb_img_gen_matrix_grid.cells_num = list(range(0, grid_len))
            #~ cpb_img_gen_matrix_grid.texts=cpb_textes
            if Capinibal.verbose: print(cpb_img_gen_matrix_grid.rows, 'rows ', cpb_img_gen_matrix_grid.row_height, 'tall.')
        #~ clone_ctx.font_size = cpb_img_gen_matrix_grid.font_size
        if Capinibal.Effect_parameters.random_order :
            k = random.randrange(0, len(cpb_img_gen_matrix_grid.cells_num))
            i = cpb_img_gen_matrix_grid.cells_num[k]
            cpb_img_gen_matrix_grid.cells_num.pop(k)
        else:
            i = Capinibal.Effect_parameters.step
        x = i % cols
        y = i // cols
        text = cpb_textes[i % textes_len]
        metrics = cpb_get_text_metrics (text, clone_ctx) # text size
        w = int(metrics.text_width)
        h = int(metrics.text_height)
        a = int(metrics.ascender)
        hmargin = 1
        if align_center:
            hmargin = (col_width-w) // 2
        if hmargin < 0:
            print('Alignment problem:', text, 'width:', w)
            hmargin = 0
        vmargin = (row_height-h) // 2
        if vmargin < 0:
            print('Alignment problem:', text, 'ascender:', a)
            vmargin = 0
        clone_ctx.text(x*col_width+hmargin, y*row_height+vmargin+a, text)
        clone_ctx(img)
    Capinibal.Effect_parameters.step = (Capinibal.Effect_parameters.step + 1) % grid_len

def cpb_img_gen_cloud (cpb_textes, ctx, img):
    if Capinibal.verbose: print(img)
    bg_color = Capinibal.Effect_parameters.bg_color
    align_center = Capinibal.Effect_parameters.align_center
    cloud_len = 15 # FIXME
    with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
        if Capinibal.Effect_parameters.step == 0:
            Capinibal.cpb_set_bg(clone_ctx, bg_color)
            cpb_img_gen_cloud.texts=cpb_textes
        text = random.choice(cpb_img_gen_cloud.texts)
        clone_ctx.font_size = int(random.randrange(Capinibal.min_font_size, Capinibal.max_font_size, 15))
        if Capinibal.verbose: print ("font size ", clone_ctx.font_size)
        metrics = cpb_get_text_metrics (text, clone_ctx) # text size
        w = int(metrics.text_width)
        a = int(metrics.ascender)
        if (align_center):
            x = (Capinibal.image_width-w)//2
        else:
            x = int(random.gauss((Capinibal.image_width-w)//2, (Capinibal.image_width-w)//6))
            x = cpb_clip(x, 0, Capinibal.image_width-w)
        y = int(random.gauss((Capinibal.image_height-a)//2, (Capinibal.image_height-a)//6))
        y = cpb_clip(y, 0, Capinibal.image_height-a)+a
        clone_ctx.text(x, y, text)
        clone_ctx(img)
    Capinibal.Effect_parameters.step = (Capinibal.Effect_parameters.step + 1) % cloud_len

# currently unused
def cpb_seq_gen_matrix (cpb_textes, ctx, pipe):
    textes_len = len (cpb_textes)
    coord_len = int(textes_len * 4)
    candidate_coord = []
    for i in range (0, coord_len):
        candidate_coord.append(i)
    clone_ctx = Drawing(drawing=ctx)
    with Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightsalmon')) as img:
        quarter_width = Capinibal.image_width / 4
        deci_height = int(Capinibal.image_height / 10)
        for i in range (0, coord_len):
            print(img)
            coord_index = random.randrange(0, len(candidate_coord))
            coord = candidate_coord[coord_index]
            candidate_coord.pop(coord_index)
            y = int(coord / 4)
            x = coord
            if coord > 4:
                x = coord % 4
            print (coord, ':  ', x, ' - ', y)
            cddt_text = random.randrange(0, textes_len)
            clone_ctx.text(x * quarter_width, (1+y) * deci_height, cpb_textes[cddt_text])
            clone_ctx(img)
            pipe.stdin.write(img.make_blob('RGB'))

def cpb_img_gen_solo_centered (cpb_texte, ctx):
    metrics = cpb_get_text_metrics (cpb_texte, ctx)
#    with Image(width=int(metrics.text_width)*2+15, height=int(metrics.text_height)*5, background=Color('lightblue')) as img:
    with Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightgreen')) as img:
        if Capinibal.verbose: print(img)
        with Drawing(drawing=ctx) as clone_ctx:  #<= Clones & reuse the parent context.
            x = int(img.width - metrics.text_width) // 2
            if x < 0: x = 0
            y = int(img.height + metrics.ascender) // 2
            if y < 0: y = 0
            clone_ctx.text(x, y, cpb_texte)
            clone_ctx(img)
        return img.clone()
        # ~ display(img)

def cpb_img_gen_solo_rdn_size_centered (cpb_texte, ctx, coin=1):
    old_size = ctx.font_size
    if (Capinibal.cpb_toss (coin)):
        ctx.font_size = int (random.randrange(Capinibal.min_font_size, Capinibal.max_font_size, 15))
        if(Capinibal.verbose): print ("font size ", ctx.font_size)
    img = cpb_img_gen_solo_centered(cpb_texte, ctx)
    ctx.font_size = old_size
    return img

###############################
#
# MainLoop (will be slot machine) and Main
#
#########################################
def cpb_capinibal (pipe, frames):
    ctxs = []
    for f in Capinibal.fonts:
        ctx = Drawing()
        ctx.font = './'+f #FIXME !
        ctx.font_size = Capinibal.ref_font_size
        ctx.fill_color = Color('black')
        max_width, max_height = Capinibal.cpb_get_max_metrics(Capinibal.texts, ctx)
        Capinibal.max_width.append(max_width)
        Capinibal.max_height.append(max_height)
        ctxs.append(ctx)
    Capinibal.max_max_width = max(Capinibal.max_width)
    Capinibal.max_max_height = max(Capinibal.max_height)
    ctx_count = len(ctxs)
    #~ print (ctxs, Capinibal.fonts, Capinibal.max_width, Capinibal.max_height)
        
    cpb_funs=[cpb_img_gen_cloud, cpb_img_gen_matrix, cpb_img_gen_matrix_line, cpb_img_gen_matrix_grid]
    #~ cpb_funs=[cpb_img_gen_matrix_col] # Use this for testing a single effect
    cpb_fun=0
    
    while False:
        Capinibal.cpb_fill_color_gen (ctx, 3)
        cpb_textes = cpb_text_gen_solo()
        blob = cpb_img_gen_solo_rdn_size_centered(cpb_textes, ctx, 5).make_blob('RGB')
        pipe.stdin.write (blob)

#        return

    step = 1 if frames > 0 else 0 # 0 => infinite loop
    in_loop = 0 # number of matrix image
    in_blink = 5 # number of matrix(s) loop
    blinking = False
    in_matrix = False # Single or multiple textx
    matrix_align = False
    phase = 1000 # Ensure first image is generated right away
    effect_images = 0
    blob = None

    image = Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightblue'))
    Capinibal.Effect_parameters.step = 0
    cpb_img_gen_matrix_grid.cells_num = []
    
    try:
        # Loop over frames
        while frames>=0:
            frames -= step
            phase += Capinibal.speed
            if Capinibal.verbose:
                print ("frames:", frames, " in_loop:", in_loop, " in_blink:", in_blink, " in_matrix:", in_matrix, " matrix_align:", matrix_align, " phase:", phase)
            if phase >= 1000: # Time to generate a new image!
                if Capinibal.verbose: print("new image")
                phase = phase % 1000
                effect_images -= 1
                if effect_images < 0 and Capinibal.Effect_parameters.step == 0: # Time to setup a new effect sequence!
                    # Also test step to avoid interrupting an effect before completion
                    # FIXME interrupting might be interesting too
                    # FIXME the probabilities below should be controllable through OSC
                    effect_images = random.randint(10, 60)
                    effect_steps = random.randint(1, 4)
                    blinking = random.random() > 0.8
                    in_matrix = random.random() > 0.5
                    matrix_align = random.random() > 0.5
                    Capinibal.Effect_parameters.random_order = random.random() > 0.5
                    if Capinibal.verbose:
                        print("new sequence for", effect_images, "images, blinking:", blinking, "in matrix:", in_matrix,".")
                    #~ Capinibal.Effect_parameters.step = 0 # Force effect re-init
                ctx_num = random.randrange(0, ctx_count) # Random context means random font
                ctx = ctxs[ctx_num]
                Capinibal.cpb_fill_color_gen(ctx, 3) # Random color... sometimes!
                if in_matrix:
                    # Multiple texts (grid or cloud)
                    Capinibal.Effect_parameters.bg_color = Capinibal.cpb_random_color()
                    # row and column count and font size need to be set prior to calling effect
                    # i.e. at step 0
                    # They must not be changed for any other step
                    if Capinibal.Effect_parameters.step == 0:
                        cpb_textes = cpb_text_gen_full()
                        cpb_fun = (cpb_fun + 1) % len(cpb_funs) # Ensures each function is used
                        if Capinibal.verbose:
                            print('Selected effect:', cpb_funs[cpb_fun], ', effect image counter:', effect_images)
                        # FIXME How do we know whether effect is multi-step or not?
                        # If multi-step, context may change between steps
                        # If using a single context, set bounds accordingly
                        #~ max_width = Capinibal.max_width[ctx_num]
                        #~ max_height = Capinibal.max_height[ctx_num]
                        # context-change safe bounds
                        max_width = Capinibal.max_max_width
                        max_height = Capinibal.max_max_height
                        Capinibal.Effect_parameters.cols = random.randrange(1, 7)
                        col_width = Capinibal.image_width/Capinibal.Effect_parameters.cols
                        scale = col_width / (max_width + Capinibal.hspacing)
                        row_height = max_height * scale + Capinibal.vspacing
                        Capinibal.Effect_parameters.rows = random.randrange(1, Capinibal.image_height // row_height)
                        if Capinibal.verbose:
                            print('Outer loop step 0,',
                              Capinibal.Effect_parameters.rows, 'rows,',
                              Capinibal.Effect_parameters.cols, 'columns,',
                              'scale:', scale
                            )
                    ctx.font_size = Capinibal.ref_font_size * scale
                    for i in range(1, effect_steps):
                        cpb_funs[cpb_fun](cpb_textes, ctx, image)
                        if Capinibal.Effect_parameters.step == 0:
                            break
                    blob = image.make_blob('RGB')
                else:
                    # Single text
                    blob = cpb_img_gen_solo_rdn_size_centered(cpb_text_gen_solo(), ctx, 5).make_blob('RGB')
                if blinking:
                    in_matrix = not in_matrix

                # Effect sequencing logic
                #~ in_loop += 1
                #~ if in_loop > 24: # 1 s @ 24 fps
                    #~ in_matrix = not in_matrix
                    #~ in_blink = in_blink - 1
                    #~ if in_blink > 0:
                        #~ in_loop = 0
                        #~ Capinibal.Effect_parameters.step=0
                    #~ else:
                        #~ if in_blink < -20:
                            #~ matrix_align = not matrix_align
                            #~ in_blink = 5

            pipe.stdin.write(blob)

        print("All frames generated")
    except KeyboardInterrupt: # Use this instead of signal.SIGINT
        print("Interrupted, exiting!")
#        except SystemExit as e:
    except BrokenPipeError:
        print("Pipe broken, exiting!")
    return


# main
if __name__=="__main__":

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
    if args['verbose']:
        sorted_by_key = sorted(args.items(), key=lambda x: x[0])
        print ('Arguments:\n', sorted_by_key, '\n')

    Capinibal.fps = args['fps']
    Capinibal.verbose = args['verbose']
    Capinibal.duration = args['duration']
    Capinibal.frames = int(float(Capinibal.fps) * float(Capinibal.duration))
    outputfile=args['outputfile']

    encoder = None
    status, result = subprocess.getstatusoutput("avconv")
    if status == 1:
        encoder='avconv'
    status, result = subprocess.getstatusoutput("ffmpeg")
    if status == 1:
        encoder='ffmpeg'
    if encoder is None:
        print("Missing dependency: You need to install ffmpeg or avconv.")
        exit ()

    if Capinibal.verbose: print ('Encoder selected:', encoder, '\n')

    Capinibal.cpb_setspeed(args['speed_of_change'])

    random.seed()
    
    print('wand version:',wand.version.VERSION)

    if Capinibal.duration:
        print('Generating', Capinibal.frames, 'frames for', Capinibal.duration, 'seconds at', Capinibal.fps, 'fps, change every', 1000/Capinibal.speed, 'frames, with', encoder, 'as encoder.')
    else:
        print('Generating frames at', Capinibal.fps, 'fps, change every', 1000/Capinibal.speed, 'frames, with', encoder, 'as encoder.')

    try:
        server = CpbServer()
    except (liblo.ServerError):
        print ("OSC failure!")
        sys.exit()
        
    if outputfile is None:
        # No output file, use a pipe
        if (args['pipename'] is None):
            tmpdir = tempfile.mkdtemp()
            filename = os.path.join(tmpdir, 'myfifo')
        else:
            tmpdir = None
            filename=args['pipename']
        print ("The fifo is on:\n%s" % filename, file=sys.stderr)

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
                    '-s', str(Capinibal.image_width)+'x'+str(Capinibal.image_height), # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', Capinibal.fps, # frames per second
                    '-i', '-', # The input comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-pix_fmt', 'yuv420p',
                    '-f', 'yuv4mpegpipe',
                    filename ]
    else:
        # Use given output file
        print ("The output file is:\n%s" % outputfile, file=sys.stderr)
        # No infinite duration!
        if Capinibal.frames<1:
            print("Non-zero duration required when using -o, aborting.", file=sys.stderr)
            sys.exit()
        cmdstring = [encoder,
                    '-y', # (optional) overwrite output file if it exists
                    '-f', 'rawvideo', #TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                    '-c:v','rawvideo',
                    '-s', str(Capinibal.image_width)+'x'+str(Capinibal.image_height), # size of one frame
                    '-pix_fmt', 'rgb24',
                    '-r', Capinibal.fps, # frames per second
                    '-i', '-', # The input comes from a pipe
                    '-an', # Tells FFMPEG not to expect any audio
                    '-c:v', 'mjpeg',
                    '-q', '1',
                    outputfile ] # Unique name

    pipe = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    time.sleep(1)

    server.start()
    
    # Here we loop

    cpb_capinibal (pipe, Capinibal.frames)

    if outputfile is None:
        print("Cleaning pipe stuff...", file=sys.stderr)
        fifo.close()
        os.remove(filename)
        if tmpdir: os.rmdir(tmpdir)
    print("Terminated normally")


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
