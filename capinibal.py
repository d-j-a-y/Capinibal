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
import os
import tempfile
import argparse

# liblo - see http://das.nasophon.de/pyliblo/examples.html
import liblo

# TODO
# more consistent context/drawing naming
# vertical and oblique text
# connect more OSC parameters

#######
# FABRIQUE
###################
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


# see https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# see https://stackoverflow.com/questions/4092528/how-to-clamp-an-integer-to-some-range
# cpb_clip = lambda x, l, u: l if x < l else u if x > u else x
def cpb_clip(x, l, u):
    return l if x < l else u if x > u else x

#TODO remove member function cpb_ prefixe
class Capinibal:
    """Main class of the another anticapitalist images generator."""
    # FIXME use annotations to document type
    duration = 0
    frame = 0
    fps = 24
    image_width = 1024
    image_height = 576
    port = 1234
    verbose = 0
    texts = [
        'capital', 'capinal', 'capibal', #FIXME
        'catipal', 'catinal', 'catibal',
        'canipal', 'canital', 'canibal',
        'cabipal', 'cabital', 'cabinal'
    ]
    fonts = [
        'Sudbury_Basin_3D.ttf',
        'Sudbury_Basin.ttf',
        'Esteh.ttf',
        'Sheilova.ttf',
        '5yearsoldfont.ttf',
        'uwch.ttf',
        'cubicblock_s.ttf',
        'cubicblock_t.ttf'

    ]
    text_font_ref_metrics = []
    # The max* lists will be populated with one item per font
    max_width = []
    max_height = []
    # max_max* will be set for all fonts, all texts
    max_max_width = 0
    max_max_height = 0
    ref_font_size = 100
    min_font_size = 55
    max_font_size = 200
    text_font_ref_metrics = []
    hspacing = 4
    vspacing = 4
    ctx_num = 0

    def __init__(self):  # Todo
        print("in init")

    def cpb_toss(coin=2):
        """toss: give kind of rand rythm.
        """
        # fixme return and default above
        coin = int(coin)
        if (coin <= 1):
            return True
        if (random.randrange(1, coin) == 1):
            return True
        return False

#######
# COLOR UTILS
###################
    def cpb_random_color():
        #~ color FFFFFF -> 16777215
        color = random.randrange(0, 16777215, 15)
        red = color >> 16
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        #~ print ("color 0x%x, r 0x%x, g 0x%x, b 0x%x" % (color, red, green, blue))
        return Color('rgb({0},{1},{2})'.format(red, green, blue))

    def cpb_fill_color_gen(ctx, coin=1):
        if Capinibal.cpb_toss(coin):
            ctx.fill_color = Capinibal.cpb_random_color()

    def cpb_set_bg(ctx, bg_color):
        #~ clone_ctx.composite('clear', 0, 0, image_width, image_height, img) # set to black!
        old_color = ctx.fill_color
        if bg_color is None:
            bg_color = Capinibal.cpb_random_color()
        ctx.fill_color = bg_color
        ctx.color(0, 0, 'reset')
        ctx.fill_color = old_color

#######
# TEXTS GENERATION
###################
    def cpb_text_gen_solo():
        return random.choice(Capinibal.texts)

    def cpb_text_gen_solo_alt():
        candidate_letter = ['P', 'B', 'T', 'N']
        txt = "CA"
        cddt_index = random.randrange(0, len(candidate_letter))
        txt = txt + candidate_letter[cddt_index]
        candidate_letter.pop(cddt_index)
        txt = txt + "I"
        txt = txt + candidate_letter[random.randrange(0, len(candidate_letter))]
        txt = txt + "AL"
        return txt

    def cpb_text_gen_full(n=10):
        txt_list = []
        for i in range(0, n):
            txt_list.append(Capinibal.cpb_text_gen_solo())
        return txt_list

#######
# RYTHM CONTROL
###################
    def cpb_setspeed(speed):  # Speed is in changes per second
        Capinibal.FxParams.speed = cpb_clip(int(1000.0 * float(speed) / float(Capinibal.fps)), 1, 1000)
        # Internal speed is changes per frame * 1000
        # 1000 means change every frame, going faster is pointless
        if Capinibal.verbose:
            print("Speed:", float(speed),
                  "changes/s becomes", Capinibal.FxParams.speed,
                  "changes/1000 frames")

    def cpb_increase(speed):
        Capinibal.FxParams.speed = cpb_clip(Capinibal.FxParams.speed + speed, 1, 1000)
        #~ Capinibal.FxParams.speed += 1000*float(speed)/float(Capinibal.fps)  # use consistent units
        if Capinibal.verbose:
            print("Increase speed:", float(speed),
                  "changes/s becomes", Capinibal.FxParams.speed,
                  "changes/1000 frames")

    def cpb_decrease(speed):
        Capinibal.FxParams.speed = cpb_clip(Capinibal.FxParams.speed - speed, 1, 1000)
        #~ Capinibal.FxParams.speed -= 1000*float(speed)/float(Capinibal.fps)  # use consistent units
        if Capinibal.verbose:
            print("Decrase speed:", float(speed),
                  "changes/s becomes", Capinibal.FxParams.speed,
                  "changes/1000 frames")


    class FxParams:

        parameters_strenght = [50,50,50,50] #FIXME
        speed = 200
        cols = 2
        rows = 5
        ctx = None
        img = None
        valign_center = False
        halign_center = False
        # What about align_bottom?
        bg_color = Color('lightblue')
        fg_color = Color('black')
        step = 0
        random_order = True
        reverse_cols = True
        reverse_rows = True
        # ~ def get_param()
        # ~ def inc_rand_param()
        # ~ def dec_rand_param()
    #END CLASS FxParams
#END CLASS Capinibal


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
            print("Received OSC message '%s' with argument: %f" % (path, args[0]))
            print("Old speed:", Capinibal.FxParams.speed)
        Capinibal.cpb_setspeed(args[0])

    @liblo.make_method('/cpb/increase', 'i')
    def increase_callback(self, path, args):
        if(Capinibal.verbose):
            print("Received OSC message '%s' with argument: %d" % (path, args[0]))
            print("Old speed:", Capinibal.FxParams.speed)
        Capinibal.cpb_increase(args[0])

    @liblo.make_method('/cpb/decrease', 'i')
    def decrease_callback(self, path, args):
        if(Capinibal.verbose):
            print("Received OSC message '%s' with argument: %d" % (path, args[0]))
            print("Old speed:", Capinibal.FxParams.speed)
        Capinibal.cpb_decrease(args[0])

    @liblo.make_method(None, None)
    def fallback(self, path, args):
        eprint("Warning : received unknown OSC message '%s'" % path)


def cpb_text_gen_solo():
    return random.choice(Capinibal.texts)


def cpb_text_gen_solo_alt():
    candidate_letter = ['P', 'B', 'T', 'N']
    txt = "CA"
    cddt_index = random.randrange(0, len(candidate_letter))
    txt = txt + candidate_letter[cddt_index]
    candidate_letter.pop(cddt_index)
    txt = txt + "I"
    txt = txt + candidate_letter[random.randrange(0, len(candidate_letter))]
    txt = txt + "AL"
    return txt


def cpb_text_gen_full(n=10):
    txt_list = []
    for i in range(0, n):
        txt_list.append(cpb_text_gen_solo())
    return txt_list


def cpb_get_cached_text_w_h_a(text_to_measure, ctx, t=None, f=None):
    # Scaling cached metrics is close enough to exact metrics
    # tests showed results within 2 pixels of exact size
    if t is None:
        t = Capinibal.texts.index(text_to_measure)
        if Capinibal.verbose:
            print("text: ", text_to_measure, " #", str(t))
    if f is None:
        #~ f=Capinibal.fonts.index(ctx.font[2:])  #FIXME relies on font path
        f = Capinibal.ctx_num  # FIXME Hidden dependency
        if Capinibal.verbose:
            print("context: ", str(f))
    #~ print(ctx.font, f, text_to_measure, t, "font size:", ctx.font_size)
    #~ print(Capinibal.text_font_ref_metrics)
    #~ print(len(Capinibal.text_font_ref_metrics))
    try:
        m = Capinibal.text_font_ref_metrics[f][t]
    except IndexError:
        if Capinibal.verbose:
            print('metrics cache miss at', f, t)
        dummy_image = Image(filename='wizard:')
        m = ctx.get_font_metrics(dummy_image, text_to_measure)
        #~ scale = 1.0
        return int(m.text_width), int(m.text_height), int(m.ascender)
    scale = ctx.font_size / Capinibal.ref_font_size
    if Capinibal.verbose > 1:
        print('metrics cache hit at', f, t,
              'font size', ctx.font_size,
              'scale:', round(scale, 3))
    return int(m.text_width * scale + 0.5), int(m.text_height * scale + 0.5), int(m.ascender * scale + 0.5)


def cpb_get_text_metrics(text_to_measure, draw):
    dummy_image = Image(filename='wizard:')
    metrics = draw.get_font_metrics(dummy_image, text_to_measure)
    # Compare with cache results for verification
    #~ w, h, a = cpb_get_cached_text_w_h_a (text_to_measure, draw)
    # These 6 variables for testing only
    #~ if w>0:

        #~ cpb_get_text_metrics.max_delta_w = max(cpb_get_text_metrics.max_delta_w, w-metrics.text_width)
        #~ cpb_get_text_metrics.min_delta_w = min(cpb_get_text_metrics.min_delta_w, w-metrics.text_width)
        #~ cpb_get_text_metrics.max_delta_h = max(cpb_get_text_metrics.max_delta_h, h-metrics.text_height)
        #~ cpb_get_text_metrics.min_delta_h = min(cpb_get_text_metrics.min_delta_h, h-metrics.text_height)
        #~ cpb_get_text_metrics.max_delta_a = max(cpb_get_text_metrics.max_delta_a, a-metrics.ascender)
        #~ cpb_get_text_metrics.min_delta_a = min(cpb_get_text_metrics.min_delta_a, a-metrics.ascender)

        #~ print(
            #~ 'w:', metrics.text_width, w, cpb_get_text_metrics.max_delta_w, cpb_get_text_metrics.min_delta_w,
            #~ 'h:', metrics.text_height, h, cpb_get_text_metrics.max_delta_h, cpb_get_text_metrics.min_delta_h,
            #~ 'a:', metrics.ascender, a, cpb_get_text_metrics.max_delta_a, cpb_get_text_metrics.min_delta_a
            #~ )

    #~ print (metrics.text_width, metrics.text_height, metrics.ascender, cpb_get_cached_text_w_h_a (text_to_measure, draw))
    #~ print("=" * 79)
    return metrics


def cpb_fill_metrics_cache(ctxs):
    # Pre-compute metrics
    for f in range(len(Capinibal.fonts)):
        Capinibal.ctx_num = f
        ctx = Drawing()
        ctx.font = './' + Capinibal.fonts[f]  # FIXME !
        ctx.font_size = Capinibal.ref_font_size
        ctx.fill_color = Color('black')
        # Cache metrics for each text for each font
        row = []
        max_width = 0
        max_height = 0
        for t in range(len(Capinibal.texts)):
            # Capinibal.text_font_ref_metrics[f][t]=
            metrics = cpb_get_text_metrics(Capinibal.texts[t], ctx)
            max_width = max(metrics.text_width, max_width)
            max_height = max(metrics.text_height, max_height)
            row.append(metrics)
        Capinibal.text_font_ref_metrics.append(row)
        Capinibal.max_width.append(max_width)
        Capinibal.max_height.append(max_height)
        ctxs.append(ctx)
    # Max values across all fonts, all texts
    Capinibal.max_max_width = max(Capinibal.max_width)
    Capinibal.max_max_height = max(Capinibal.max_height)


def cpb_print_metrics_cache():
    print('Reference font size:', Capinibal.ref_font_size)
    for f in range(len(Capinibal.fonts)):
        for t in range(len(Capinibal.texts)):
            print('Font', f, ':', Capinibal.fonts[f],
                  'text', t, ':', Capinibal.texts[t],
                  'w:', Capinibal.text_font_ref_metrics[f][t].text_width,
                  'h:', Capinibal.text_font_ref_metrics[f][t].text_height,
                  'a:', Capinibal.text_font_ref_metrics[f][t].ascender,
                  #~ 'metrics:', Capinibal.text_font_ref_metrics[f][t]
                  )
        print('max_width:', Capinibal.max_width[f],
              'max_height:', Capinibal.max_height[f])
        print("=" * 79)


#############
#
# Image generation routines
#
############################
def cpb_put_text(cpb_textes, ctx, col, row, cols, rows, col_width, row_height):
    # Prepare context ctx for displaying a text in grid layout
    text_num = (col + cols * row) % len(cpb_textes) # Use random?
    text = cpb_textes[text_num]
    w, h, a = cpb_get_cached_text_w_h_a(text, ctx, t=text_num)
    hmargin = Capinibal.hspacing // 2
    vmargin = Capinibal.vspacing // 2
    if Capinibal.FxParams.halign_center:
        hmargin = (col_width - w) // 2
        if Capinibal.verbose > 2:
            print("h center:"
                  'col:', col,
                  'col width:', col_width,
                  'cols:', cols,
                  'text width:', w,
                  'hmargin:', hmargin,
                  'x:', col * col_width + hmargin,
                  )
    if Capinibal.FxParams.valign_center:
        vmargin = (row_height - h) // 2
        if Capinibal.verbose > 2:
            print("v center:"
                  'row:', row,
                  'row height:', row_height,
                  'rows:', rows,
                  'text height:', h, a,
                  'vmargin:', vmargin,
                  'y:', row * row_height + vmargin + a,
                  )
    if hmargin < 0:
        eprint('Alignment problem:', text, 'width:', w)
        hmargin = 0
    if vmargin < 0:
        eprint('Alignment problem:', text,
              'col:', col,
              'row height:', row_height,
              'rows:', rows,
              'text height:', h,
              'font size:', ctx.font_size)
        vmargin = 0
    if Capinibal.FxParams.reverse_cols:
        col = cols - col - 1
    if Capinibal.FxParams.reverse_rows:
        row = rows - row - 1
    ctx.text(col * col_width + hmargin,
             row * row_height + vmargin + a,
             text)


def cpb_clr_text(cpb_textes, ctx, col, row, cols, rows, col_width, row_height):
    # Prepare context ctx for clearing a text in grid layout
    # Always clear the whole cell, ignore margins
    # Caller has to set ctx.fill_color
    if Capinibal.FxParams.reverse_cols:
        col = cols - col - 1
    if Capinibal.FxParams.reverse_rows:
        row = rows - row - 1
    ctx.stroke_width = 0
    ctx.rectangle(left=col * col_width,
                  top=row * row_height,
                  width=col_width,
                  height=row_height)

def cpb_img_gen_matrix_full(cpb_textes, ctx, img):
    # Generate complete matrix in one step
    if Capinibal.verbose > 1:
        print(img)
    cols = Capinibal.FxParams.cols
    rows = Capinibal.FxParams.rows
    col_width = Capinibal.image_width // cols
    row_height = Capinibal.image_height // rows
    textes_len = len(cpb_textes)  # may be different from grid length
    Capinibal.FxParams.step = 0
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
        # Fill grid with text
        for col in range(0, cols):
            for row in range(0, rows):
                cpb_put_text(cpb_textes, clone_ctx, col, row, cols, rows, col_width, row_height)
                clone_ctx(img)
    return True # Allow clearing matrix


# FIXME The following 3 functions have much in common, should be factored out
def cpb_img_gen_matrix_line(cpb_textes, ctx, img):
    # Generate a matrix image, one row at a time
    if Capinibal.verbose > 1:
        print("gen line step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    textes_len = len(cpb_textes)
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        if Capinibal.FxParams.step == 0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
            cpb_img_gen_matrix_line.lines_num = list(range(0, rows))
        if Capinibal.FxParams.random_order:
            k = random.randrange(0, len(cpb_img_gen_matrix_line.lines_num))
            row = cpb_img_gen_matrix_line.lines_num[k]
            cpb_img_gen_matrix_line.lines_num.pop(k)
        else:
            row = Capinibal.FxParams.step % rows
        for col in range(0, cols):
            cpb_put_text(cpb_textes, clone_ctx, col, row, cols, rows, col_width, row_height)
        clone_ctx(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % rows
    return True # Allow clearing matrix


def cpb_img_gen_matrix_col(cpb_textes, ctx, img):
    # Generate a matrix image, one column at a time
    if Capinibal.verbose > 1:
        print("gen column step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    textes_len = len(cpb_textes)
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        if Capinibal.FxParams.step == 0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
            cpb_img_gen_matrix_col.cols_num = list(range(0, cols))
        if Capinibal.FxParams.random_order:
            k = random.randrange(0, len(cpb_img_gen_matrix_col.cols_num))
            col = cpb_img_gen_matrix_col.cols_num[k]
            cpb_img_gen_matrix_col.cols_num.pop(k)
        else:
            col = Capinibal.FxParams.step % cols
        for row in range(0, rows):
            cpb_put_text(cpb_textes, clone_ctx, col, row, cols, rows, col_width, row_height)
        clone_ctx(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % cols
    return True # Allow clearing matrix


def cpb_img_gen_matrix_diag(cpb_textes, ctx, img):
    # Generate a matrix image, one diagonal row at a time
    if Capinibal.verbose > 1:
        print("gen diag step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        if Capinibal.FxParams.step == 0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
        col_from = max(0, Capinibal.FxParams.step - rows + 1)
        col_to = min(cols, Capinibal.FxParams.step + 1)
        for col in range(col_from, col_to):
            # col + row is constant for one oblique line
            row = Capinibal.FxParams.step - col
            cpb_put_text(cpb_textes, clone_ctx, col, row, cols, rows, col_width, row_height)
        clone_ctx(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % (rows + cols - 1)
    return True # Allow clearing matrix


def cpb_img_gen_matrix_grid(cpb_textes, ctx, img):
    # Generate a matrix image, one cell at a time
    # What about populating adjacent cells, worm-like?
    if Capinibal.verbose > 1:
        print("gen grid step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    rows = Capinibal.FxParams.rows
    grid_len = rows * cols
    col_width = Capinibal.image_width // cols
    row_height = Capinibal.image_height // rows

    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        if cpb_img_gen_matrix_grid.cells_num == []:
            Capinibal.FxParams.step = 0
        if Capinibal.FxParams.step == 0:
            # FIXME! also keep the version without clearing, leading to a visually interesting accumulation
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
            # FIXME! could be visually interesting to optionally keep same context for all steps
            cpb_img_gen_matrix_grid.cells_num = list(range(0, grid_len))
            if Capinibal.verbose:
                print(rows, 'rows ', row_height, 'tall.')
        if Capinibal.FxParams.random_order:
            k = random.randrange(0, len(cpb_img_gen_matrix_grid.cells_num))
            i = cpb_img_gen_matrix_grid.cells_num[k]
            cpb_img_gen_matrix_grid.cells_num.pop(k)
        else:
            i = Capinibal.FxParams.step
        col = i % cols
        row = i // cols
        cpb_put_text(cpb_textes, clone_ctx, col, row, cols, rows, col_width, row_height)
        clone_ctx(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % grid_len
    return True # Allow clearing matrix


def cpb_img_clr_matrix_line(cpb_textes, ctx, img):
    # Clear a matrix image, one row at a time
    if Capinibal.verbose > 1:
        print("clr line step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    if Capinibal.FxParams.step == 0:
        cpb_img_gen_matrix_line.lines_num = list(range(0, rows))
    if Capinibal.FxParams.random_order:
        k = random.randrange(0, len(cpb_img_gen_matrix_line.lines_num))
        row = cpb_img_gen_matrix_line.lines_num[k]
        cpb_img_gen_matrix_line.lines_num.pop(k)
    else:
        row = Capinibal.FxParams.step % rows
    ctx2 = Drawing()
    ctx2.fill_color = Capinibal.FxParams.bg_color # ctx.fill_color
    for col in range(0, cols):
        cpb_clr_text(cpb_textes, ctx2, col, row, cols, rows, col_width, row_height)
    ctx2(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % rows


def cpb_img_clr_matrix_col(cpb_textes, ctx, img):
    # Clear a matrix image, one column at a time
    if Capinibal.verbose > 1:
        print("clr column step:", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    if Capinibal.FxParams.step == 0:
        cpb_img_gen_matrix_col.cols_num = list(range(0, cols))
    if Capinibal.FxParams.random_order:
        k = random.randrange(0, len(cpb_img_gen_matrix_col.cols_num))
        col = cpb_img_gen_matrix_col.cols_num[k]
        cpb_img_gen_matrix_col.cols_num.pop(k)
    else:
        col = Capinibal.FxParams.step % cols
    ctx2 = Drawing()
    ctx2.fill_color = Capinibal.FxParams.bg_color # ctx.fill_color
    for row in range(0, rows):
        cpb_clr_text(cpb_textes, ctx2, col, row, cols, rows, col_width, row_height)
    ctx2(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % cols


def cpb_img_clr_matrix_diag(cpb_textes, ctx, img):
    # Clear a matrix image, one diagonal row at a time
    if Capinibal.verbose > 1:
        print("clr diag step", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    col_from = max(0, Capinibal.FxParams.step - rows + 1)
    col_to = min(cols, Capinibal.FxParams.step + 1)
    ctx2 = Drawing()
    ctx2.fill_color = Capinibal.FxParams.bg_color # ctx.fill_color
    for col in range(col_from, col_to):
        # col + row is constant for one oblique line
        row = Capinibal.FxParams.step - col
        cpb_clr_text(cpb_textes, ctx2, col, row, cols, rows, col_width, row_height)
    ctx2(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % (rows + cols - 1)


def cpb_img_clr_matrix_grid(cpb_textes, ctx, img):
    # Clear a matrix image, one cell at a time
    if Capinibal.verbose > 1:
        print("clr grid step", Capinibal.FxParams.step, img)
    cols = Capinibal.FxParams.cols
    col_width = Capinibal.image_width // cols
    rows = Capinibal.FxParams.rows
    row_height = Capinibal.image_height // rows
    grid_len = rows * cols

    if cpb_img_clr_matrix_grid.cells_num == []:
        Capinibal.FxParams.step = 0
    if Capinibal.FxParams.step == 0:
        cpb_img_clr_matrix_grid.cells_num = list(range(0, grid_len))
        if Capinibal.verbose:
            print(rows, 'rows ', row_height, 'tall.')
    if Capinibal.FxParams.random_order:
        k = random.randrange(0, len(cpb_img_clr_matrix_grid.cells_num))
        i = cpb_img_clr_matrix_grid.cells_num[k]
        cpb_img_clr_matrix_grid.cells_num.pop(k)
    else:
        i = Capinibal.FxParams.step
    col = i % cols
    row = i // cols
    ctx2 = Drawing()
    ctx2.fill_color = Capinibal.FxParams.bg_color # ctx.fill_color
    cpb_clr_text(cpb_textes, ctx2, col, row, cols, rows, col_width, row_height)
    ctx2(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % grid_len



def cpb_img_gen_cloud(cpb_textes, ctx, img):
    # multis-step does not look very good
    # How could we prevent multistep from main loop?
    # h and v centering together don't look very good
    # We can force early exit by setting Capinibal.FxParams.step
    # This can lead to switching to a new effect only if effect_images is <0
    if Capinibal.verbose > 1:
        print(img)
    cloud_len = random.randint(6, 12)  # FIXME
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        if Capinibal.FxParams.step == 0:
            Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
        text_num = random.randrange(0, len(cpb_textes))
        text = cpb_textes[text_num]
        clone_ctx.font_size = int(random.randrange(Capinibal.min_font_size, Capinibal.max_font_size, 15))
        if Capinibal.verbose > 1:
            print("font size ", clone_ctx.font_size)
        w, h, a = cpb_get_cached_text_w_h_a(text, clone_ctx, t=text_num)
        if Capinibal.FxParams.halign_center:
            # Strict centering
            #~ x = (Capinibal.image_width - w) // 2
            # Statistical centering
            x = int(random.gauss((Capinibal.image_width - w) // 2,
                                 (Capinibal.image_width - w) // 6))
        else:
            x=random.randrange(0, Capinibal.image_width - w)
        x = cpb_clip(x, 0, Capinibal.image_width - w)
        if Capinibal.FxParams.valign_center:
            # Strict centering
            #~ y = (Capinibal.image_height - h) // 2
            # Statistical centering
            y = int(random.gauss((Capinibal.image_height - h) // 2,
                                 (Capinibal.image_height - h) // 6))
        else:
            y=random.randrange(a, Capinibal.image_height)
        y = cpb_clip(y, 0, Capinibal.image_height - a) + a
        if Capinibal.verbose > 1:
            print("Cloud:", text, "at", x, y, )
        clone_ctx.text(x, y, text)
        clone_ctx(img)
    Capinibal.FxParams.step = (Capinibal.FxParams.step + 1) % cloud_len
    return False # Don't allow clearing matrix (there is none)


# currently unused
def cpb_seq_gen_matrix(cpb_textes, ctx, pipe):
    textes_len = len(cpb_textes)
    coord_len = int(textes_len * 4)
    candidate_coord = []
    for i in range(0, coord_len):
        candidate_coord.append(i)
    clone_ctx = Drawing(drawing=ctx)
    with Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightsalmon')) as img:
        quarter_width = Capinibal.image_width / 4
        deci_height = int(Capinibal.image_height / 10)
        for i in range(0, coord_len):
            print(img)
            coord_index = random.randrange(0, len(candidate_coord))
            coord = candidate_coord[coord_index]
            candidate_coord.pop(coord_index)
            y = int(coord / 4)
            x = coord
            if coord > 4:
                x = coord % 4
            print(coord, ':  ', x, ' - ', y)
            cddt_text = random.randrange(0, textes_len)
            clone_ctx.text(x * quarter_width, (1 + y) * deci_height, cpb_textes[cddt_text])
            clone_ctx(img)
            pipe.stdin.write(img.make_blob('RGB'))


def cpb_img_gen_solo_centered(cpb_texte, ctx, img):
    w, h, a = cpb_get_cached_text_w_h_a(cpb_texte, ctx)
    if Capinibal.verbose > 1:
        print(img)
    with Drawing(drawing=ctx) as clone_ctx:  # <= Clones & reuse the parent context.
        Capinibal.cpb_set_bg(clone_ctx, Capinibal.FxParams.bg_color)
        x = int(img.width - w) // 2
        if x < 0:
            x = 0
        y = int(img.height + a) // 2
        if y < 0:
            y = 0
        clone_ctx.text(x, y, cpb_texte)
        clone_ctx(img)


def cpb_img_gen_solo_rdn_size_centered(cpb_texte, ctx, img, coin=1):
    old_size = ctx.font_size
    if Capinibal.cpb_toss(coin):
        ctx.font_size = int(random.randrange(Capinibal.min_font_size, Capinibal.max_font_size, 15))
        if Capinibal.verbose > 1:
            print("font size ", ctx.font_size)
    cpb_img_gen_solo_centered(cpb_texte, ctx, img)
    ctx.font_size = old_size


###############################
#
# MainLoop (will be slot machine) and Main
#
#########################################
def cpb_capinibal(pipe, frames):
    ctxs = []

    # These 6 variables for testing only
    #~ cpb_get_text_metrics.max_delta_w = 0
    #~ cpb_get_text_metrics.min_delta_w = 0
    #~ cpb_get_text_metrics.max_delta_h = 0
    #~ cpb_get_text_metrics.min_delta_h = 0
    #~ cpb_get_text_metrics.max_delta_a = 0
    #~ cpb_get_text_metrics.min_delta_a = 0

    cpb_fill_metrics_cache(ctxs)

    if Capinibal.verbose > 1:  # Show precomputed values
        cpb_print_metrics_cache()

    ctx_count = len(ctxs)

    # Comment lines below if a particular fill is not wanted
    # functions with a matching clr function must come first
    cpb_gen_funs = [
                cpb_img_gen_matrix_line,
                cpb_img_gen_matrix_grid,
                cpb_img_gen_matrix_col,
                cpb_img_gen_matrix_diag,
                cpb_img_gen_cloud,
                cpb_img_gen_matrix_full,
                ]
    cpb_gen_fun = 0
    cpb_clr_funs = [
                cpb_img_clr_matrix_line,
                cpb_img_clr_matrix_grid,
                cpb_img_clr_matrix_col,
                cpb_img_clr_matrix_diag,
                ]
    cpb_clr_fun = 0

    step = 1 if frames > 0 else 0  # 0 => infinite loop
    #~ in_loop = 0  # number of matrix image
    #~ in_blink = 5  # number of matrix(s) loop
    blinking = False
    clearing = False
    in_matrix = False  # Single or multiple text
    #~ Capinibal.FxParams.matrix_align = False
    Capinibal.FxParams.valign_center = False
    Capinibal.FxParams.halign_center = False
    phase = 1000  # Ensure first image is generated right away
    effect_images = 0
    blob = None

    # Use two images so that we can use one for matrices/cloud
    # and one for single text; this allows switching quickly
    # between these two effects
    image = Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightblue'))
    image2 = Image(width=Capinibal.image_width, height=Capinibal.image_height, background=Color('lightblue'))

    Capinibal.FxParams.step = 0
    cpb_img_gen_matrix_grid.cells_num = []
    cpb_img_clr_matrix_grid.cells_num = []

    while False:
        Capinibal.cpb_fill_color_gen(ctxs[0], 3)
        cpb_textes = Capinibal.cpb_text_gen_solo()
        cpb_img_gen_solo_rdn_size_centered(cpb_textes, ctxs[0], image2, 5)
        blob = image2.make_blob('RGB')
        pipe.stdin.write(blob)

    try:
        # Loop over frames
        while frames >= 0:
            frames -= step
            phase += Capinibal.FxParams.speed
            #~ if Capinibal.verbose:
                #~ print ("frames:", frames, " in_loop:", in_loop, "blinking:", blinking, " in_matrix:", in_matrix, " matrix_align:", matrix_align, " phase:", phase)
            if phase >= 1000:  # Time to generate a new image!
                if Capinibal.verbose:
                    print("New image, clearing:", clearing,
                          "step:", Capinibal.FxParams.step)
                phase = phase % 1000
                Capinibal.ctx_num = random.randrange(0, ctx_count)  # Random context means random font
                ctx = ctxs[Capinibal.ctx_num]
                #~ Capinibal.cpb_fill_color_gen(ctx, 3)  # Random color... sometimes!
                if Capinibal.cpb_toss(3):
                    Capinibal.FxParams.fg_color = Capinibal.cpb_random_color()
                ctx.fill_color = Capinibal.FxParams.fg_color

                effect_images -= 1
                if effect_images < 0 and Capinibal.FxParams.step == 0 and not clearing:
                    # Time to setup a new effect sequence!
                    # Also test step to avoid interrupting an effect
                    # before its end.
                    # FIXME interrupting might be interesting too
                    if Capinibal.verbose:
                        print("new effect")
                    # FIXME the probabilities below should be controllable through OSC
                    # FIXME the probabilities below should be effect dependant
                    # using an effect x parameter probability matrix
                    #~ clearing = False
                    effect_images = random.randint(10, 30)
                    effect_steps = random.randint(1, 4)
                    blinking = random.random() > 0.8
                    in_matrix = random.random() > 0.33
                    #~ Capinibal.FxParams.matrix_align = random.random() > 0.5
                    Capinibal.FxParams.random_order = random.random() > 0.33
                    Capinibal.FxParams.reverse_cols = random.random() > 0.5
                    Capinibal.FxParams.reverse_rows = random.random() > 0.5
                    Capinibal.FxParams.valign_center = random.random() > 0.5
                    Capinibal.FxParams.halign_center = random.random() > 0.5
                    # FIXME how can we clear image from here? Should we?
                    #~ Capinibal.cpb_fill_color_gen(ctx2) # Random background color
                    #~ ctx2.color(0, 0, 'reset')
                    #~ ctx2(image)
                    # When done with ctx, will keep resetting color at each image
                    # When done inside effects, uses cloned context, works
                    Capinibal.FxParams.bg_color = Capinibal.cpb_random_color()
                    Capinibal.FxParams.fg_color = Capinibal.cpb_random_color()
                    ctx.fill_color = Capinibal.FxParams.fg_color
                    #~ Capinibal.cpb_fill_color_gen(ctx) # Random color
                    if Capinibal.verbose:
                        print("New sequence for", effect_images, "images, ",
                              effect_steps, "steps at a time,",
                              "background:", Capinibal.FxParams.bg_color,
                              "foreground:", Capinibal.FxParams.fg_color,
                              "blinking:", blinking,
                              "in matrix:", in_matrix, "."
                              )
                #~ if Capinibal.FxParams.step == -1: # Magic value will start clearing
                    #~ ctx.fill_color = Capinibal.FxParams.bg_color
                    #~ Capinibal.FxParams.step = 0
                    #~ clearing = True

                if in_matrix:
                    # Multiple texts (grid or cloud)
                    # row and column count and font size need to be set prior to calling effect
                    # i.e. at step 0
                    # They must not be changed for any other step
                    # The same image is reused so that results of previous steps are kept
                    if Capinibal.FxParams.step == 0 and not clearing:
                        # Before image generator function is called for step 0,
                        # we initialize some random variables.
                        # If clearing, we want to use the same grid as for filling,
                        # we don't want to set new values for rows and columns.
                        cpb_textes = cpb_text_gen_full()
                        cpb_gen_fun = (cpb_gen_fun + 1) % len(cpb_gen_funs)  # Ensures each function is used (for testing)
                        #~ cpb_gen_fun = random.randrange(0, len(cpb_gen_funs))
                        if Capinibal.verbose:
                            print('Selected effect:', cpb_gen_funs[cpb_gen_fun], ', effect image counter:', effect_images)
                        # FIXME How do we know whether effect is multi-step or not?
                        # If multi-step, context may change between steps
                        # If using a single context, set bounds accordingly
                        #~ max_width = Capinibal.max_width[ctx_num]
                        #~ max_height = Capinibal.max_height[ctx_num]
                        # context-change safe bounds
                        max_width = Capinibal.max_max_width
                        max_height = Capinibal.max_max_height
                        Capinibal.FxParams.cols = random.randint(1, 7)
                        col_width = Capinibal.image_width / Capinibal.FxParams.cols
                        scale = col_width / (max_width + Capinibal.hspacing)
                        fs = int(Capinibal.ref_font_size * scale)
                        row_height = max_height * scale + Capinibal.vspacing
                        # effect_steps should be reduced for small grids
                        if effect_steps > Capinibal.FxParams.rows:
                            effect_steps = Capinibal.FxParams.rows
                        if effect_steps > Capinibal.FxParams.cols:
                            effect_steps = Capinibal.FxParams.cols
                        Capinibal.FxParams.rows = random.randint(1, Capinibal.image_height // row_height)
                        if Capinibal.verbose:
                            print('Selected effect parameters:',
                                  Capinibal.FxParams.rows, 'rows,',
                                  Capinibal.FxParams.cols, 'columns,',
                                  'scale:', scale
                                  )
                    ctx.font_size = fs
                    if Capinibal.verbose:
                        print('Effect steps per image:', effect_steps)
                    for i in range(0, effect_steps):
                        if clearing:
                            # Choose the clear function that matches the generation function
                            # Alternatively we could choose a random function
                            cpb_clr_fun = cpb_gen_fun % len(cpb_clr_funs)
                            if Capinibal.verbose > 1:
                                print('Clear effect ', cpb_clr_fun,
                                      'index', i, 'of', effect_steps, ',',
                                      Capinibal.FxParams.rows, 'row(s),',
                                      Capinibal.FxParams.cols, 'column(s),',
                                      'step', Capinibal.FxParams.step)
                            ctx.fill_color = Capinibal.FxParams.bg_color
                            cpb_clr_funs[cpb_clr_fun](cpb_textes, ctx, image)
                            clear_enable = False
                        else:  # Generating text display
                            if Capinibal.verbose > 1:
                                print('Gen effect ', cpb_gen_fun,
                                      'index', i, 'of', effect_steps, ',',
                                      Capinibal.FxParams.rows, 'row(s),',
                                      Capinibal.FxParams.cols, 'column(s),',
                                      'step', Capinibal.FxParams.step)
                            ctx.fill_color = Capinibal.FxParams.fg_color
                            clear_enable = cpb_gen_funs[cpb_gen_fun](cpb_textes, ctx, image)

                        if Capinibal.FxParams.step == 0:
                            # Effect just completed (gen or clr)
                            clearing = False
                            if Capinibal.verbose > 1:
                                print('Effect complete, exiting at step', i)
                            if clear_enable: # Capinibal.FxParams.step == -1:
                                # FIXME reverse/random/effect_steps should be randomly reset
                                clearing = random.random() > .5
                                if Capinibal.verbose:
                                    print("Clearing:", clearing)
                            break
                    blob = image.make_blob('RGB')
                else:
                    # Single text
                    # A different image is used
                    # so that blinking does not erase previous matrix effect results
                    cpb_img_gen_solo_rdn_size_centered(Capinibal.cpb_text_gen_solo(), ctx, image2, 5)
                    blob = image2.make_blob('RGB')
                if blinking:
                    in_matrix = not in_matrix

                # Effect sequencing logic
                #~ in_loop += 1
                #~ if in_loop > 24: # 1 s @ 24 fps
                    #~ in_matrix = not in_matrix
                    #~ in_blink = in_blink - 1
                    #~ if in_blink > 0:
                        #~ in_loop = 0
                        #~ Capinibal.FxParams.step=0
                    #~ else:
                        #~ if in_blink < -20:
                            #~ matrix_align = not matrix_align
                            #~ in_blink = 5

            pipe.stdin.write(blob)

        print("All frames generated")
    except KeyboardInterrupt:  # Use this instead of signal.SIGINT
        eprint("Interrupted, exiting!")
#        except SystemExit as e:
    except BrokenPipeError:
        eprint("Pipe broken, exiting!")
    return

def print_alpha():
    print('ALPHA ----- ALPHA ----- ALPHA ----- ALPHA ----- ALPHA')
    print('Your are viewing some not released work... good luck!')
    print('ALPHA ----- ALPHA ----- ALPHA ----- ALPHA ----- ALPHA\n')

# main
if __name__ == "__main__":
    print_alpha()

    parser = argparse.ArgumentParser(description='Running stand alone it generate random  \
                                                  scenes based on a repetitive pattern.\n \
                                                  The rhythm can be moderate thrue OCS messages.')
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
    parser.add_argument('-x', '--osc_and_quit', default=False, action='store_true',
                        help='Dump OSC message list and quit.')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Enable debug output (default: off)')
    args = vars(parser.parse_args())

    if args['osc_and_quit']: #FIXME
        print('OSC message dump:')
        sys.exit(0)

    Capinibal.verbose = int(args['verbose'])
    if Capinibal.verbose:
        sorted_by_key = sorted(args.items(), key=lambda x: x[0])
        print('Arguments:\n', sorted_by_key, '\n')

    Capinibal.fps = args['fps']
    Capinibal.duration = args['duration']
    Capinibal.frames = int(float(Capinibal.fps) * float(Capinibal.duration))
    outputfile = args['outputfile']

    encoder = None
    status, result = subprocess.getstatusoutput("avconv")
    if status == 1:
        encoder = 'avconv'
    status, result = subprocess.getstatusoutput("ffmpeg")
    if status == 1:
        encoder = 'ffmpeg'
    if encoder is None:
        eprint("Missing dependency: You need to install ffmpeg or avconv.")
        sys.exit(1)

    if Capinibal.verbose:
        print('Encoder selected:', encoder)
        print('verbose level:', Capinibal.verbose)

    Capinibal.cpb_setspeed(args['speed_of_change'])

    random.seed()

    print('wand version:', wand.version.VERSION)

    if Capinibal.duration:
        print('Generating', Capinibal.frames,
              'frames for', Capinibal.duration,
              'seconds at', Capinibal.fps,
              'fps, change every', 1000 / Capinibal.FxParams.speed,
              'frames, with', encoder, 'as encoder.')
    else:
        print('Generating frames at', Capinibal.fps,
              'fps, change every', 1000 / Capinibal.FxParams.speed,
              'frames, with', encoder, 'as encoder.')

    try:
        server = CpbServer()
    except (liblo.ServerError):
        eprint("OSC failure!")
        sys.exit()

    if outputfile is None:
        # No output file, use a pipe
        if args['pipename'] is None:
            tmpdir = tempfile.mkdtemp()
            filename = os.path.join(tmpdir, 'myfifo')
        else:
            tmpdir = None
            filename = args['pipename']
        print("The fifo is on:\n%s" % filename)

#FIXME PIPE FULL bug ?
# use os.O_NONBLOCK. When you do a write which would block os.write should instead return immediately with EAGAIN

        try:
            os.mkfifo(filename)
        except OSError as e:
            eprint("Failed to create FIFO: %s" % e)
            sys.exit(1)

        try:
            fifo = open(filename, 'w')
        except KeyboardInterrupt:  # Use this instead of signal.SIGINT
            eprint("Interrupted, exiting!")
            sys.exit(0)

        cmdstring = [encoder,
                     '-loglevel', 'warning',
                     '-y',  # (optional) overwrite output file if it exists
                     '-f', 'rawvideo',  # TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                     '-c:v', 'rawvideo',
                     '-s', str(Capinibal.image_width) + 'x' + str(Capinibal.image_height),  # size of one frame
                     '-pix_fmt', 'rgb24',
                     '-r', Capinibal.fps,  # frames per second
                     '-i', '-',  # The input comes from a pipe
                     '-an',  # Tells FFMPEG not to expect any audio
                     '-pix_fmt', 'yuv420p',
                     '-f', 'yuv4mpegpipe',
                     filename]
    else:
        # Use given output file
        print("The output file is:\n%s" % outputfile, file=sys.stderr)
        # No infinite duration!
        if Capinibal.frames < 1:
            eprint("Non-zero duration required when using -o, aborting.")
            sys.exit()
        cmdstring = [encoder,
                     '-y',  # (optional) overwrite output file if it exists
                     '-f', 'rawvideo',  # TODO '-f', 'image2pipe', '-vcodec', 'mjpeg' avec blob('jpeg')
                     '-c:v', 'rawvideo',
                     '-s', str(Capinibal.image_width) + 'x' + str(Capinibal.image_height),  # size of one frame
                     '-pix_fmt', 'rgb24',
                     '-r', Capinibal.fps,  # frames per second
                     '-i', '-',  # The input comes from a pipe
                     '-an',  # Tells FFMPEG not to expect any audio
                     '-c:v', 'mjpeg',
                     '-q', '1',
                     outputfile]  # Unique name

    pipe = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

    time.sleep(1)

    server.start()

    # Here we loop

    cpb_capinibal(pipe, Capinibal.frames)

    if outputfile is None:
        print("Cleaning pipe stuff...")
        fifo.close()
        os.remove(filename)
        if tmpdir:
            os.rmdir(tmpdir)
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
