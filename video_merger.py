import ffmpeg, os
from operator import itemgetter

delim = "_"

def get_video_properties(v):
    
    res = os.popen("ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {}".format(v)).read()

    width = int(res[:res.find('x')])
    height = int(res[res.find('x') + 1:-1])

    return [width, height]

def get_max_size(videos):
    max_width = 0
    max_height = 0

    for v in videos:
        props = get_video_properties(v)
        max_width = max(max_width, props[0])
        max_height = max(max_height, props[1])

    return max_width, max_height

def resize(videos, maxw, maxh):
    PAD_OPTIONS = {
        'width':'{}'.format(maxw),
        'height':'{}'.format(maxh),
        'x':'(ow-iw)/2',
        'y':'(oh-ih)/2',
    }
    for v in videos:

        (
            ffmpeg
            .input(v)
            .filter("scale", size = "{}:{}".format(maxw, maxh), force_original_aspect_ratio='decrease')
            .filter_("pad",**PAD_OPTIONS)
            .filter("setsar", 1)
            .output('{}m.mp4'.format(v[:v.find(".mp4")]))

            .global_args('-y')

            .run()
        )

#inst = instrument
def merge_inst(inst, videos, maxw, maxh, npc):
    print(videos)
    vl = len(videos)
    if vl == 0:
        pass

    ind = 0
    inp = []

    fin = []

    PAD_OPTIONS = {
        'width':'{}'.format(maxw * npc),
        'height':'{}'.format(maxh),
        'x':'(ow-iw)/2',
        'y':'(oh-ih)/2',
    }

    for i in range(vl):
        if (i != 0 and i % npc == 0):
            (
                ffmpeg
                .filter(inp, 'hstack', len(inp))
                .output('{}{}.mp4'.format(inst, ind))

                .global_args('-y')
                
                .run()

            )

            fin.append(ffmpeg.input('{}{}.mp4'.format(inst, ind)))
            
            inp = []
            ind += 1    

        inp.append(ffmpeg.input(videos[i]))


    if (len(inp) != 0):
        if (len(inp) != 1):
            (
                ffmpeg
                .filter(inp, 'hstack', len(inp))

                .filter("scale", size = "{}:{}".format(maxw * npc, maxh), force_original_aspect_ratio='decrease')
                .filter_("pad",**PAD_OPTIONS)
                .filter("setsar", 1)
                
                .output('{}{}.mp4'.format(inst, ind))

                .global_args('-y')

                .run()
            )
        else:
            
            (
                ffmpeg

                .filter(inp, "scale", size = "{}:{}".format(maxw * npc, maxh), force_original_aspect_ratio='decrease')
                .filter_("pad",**PAD_OPTIONS)
                .filter("setsar", 1)
                
                .output('{}{}.mp4'.format(inst, ind))

                .global_args('-y')

                .run()
            )

        fin.append(ffmpeg.input('{}{}.mp4'.format(inst, ind)))

    #controls space between sections
    PAD_OPTIONS = {
        'width':'{}'.format(maxw * npc),
        'height':'{}'.format(maxh * len(fin) + 30), 
        'x':'(ow-iw)/2',
        'y':'(oh-ih)/2',
    }

    #final video

    if (len(fin) > 1):
        (
            ffmpeg
            .filter(fin, 'vstack', len(fin))

            .filter("scale", size = "{}:{}".format(maxw * npc, maxh * len(fin) + 30), force_original_aspect_ratio='decrease')
            .filter_("pad",**PAD_OPTIONS)
            .filter("setsar", 1)
            
            .output('{}fin.mp4'.format(inst))

            .global_args('-y')

            .run()

        )
    else:
        (
            ffmpeg
            .filter(fin, "scale", size = "{}:{}".format(maxw * npc, maxh * len(fin) + 30), force_original_aspect_ratio='decrease')
            .filter_("pad",**PAD_OPTIONS)
            .filter("setsar", 1)
            
            .output('{}fin.mp4'.format(inst))

            .global_args('-y')

            .run()

        )
        

#npc = number of users per column
def merge_all(user_inst, maxw, maxh, npc):
    curv = []
    curinst = user_inst[0][1]

    insts = [curinst]

    for i in user_inst:
        if (i[1] != curinst):
            merge_inst(curinst, curv, maxw, maxh, npc)
            curinst = i[1]
            curv = []
            insts.append(curinst)
        curv.append(i[0] + delim + i[1] + "m.mp4")

    merge_inst(curinst, curv, maxw, maxh, npc)

    print(insts)

    inp_insts = []

    for i in range(len(insts)):
        inp_insts.append(ffmpeg.input('{}fin.mp4'.format(insts[i])))

    if (len(insts) > 1):
        #final video
        (
            ffmpeg
            .filter(inp_insts, 'vstack', len(insts))
            .output('combined.mp4')

            .global_args('-y')

            .run()

        )
    else:
        #we need to rename the file
        os.system("mv {}fin.mp4 combined.mp4".format(insts[0]))

def merge(user_inst):

    user_inst = sorted(user_inst, key=itemgetter(1))

    videos = []

    for i in user_inst:
        videos.append(i[0] + delim + i[1] + ".mp4")

    maxw, maxh = get_max_size(videos)

    resize(videos, maxw, maxh)

    merge_all(user_inst, maxw, maxh, 3)

    #add sound to combined
    os.system("ffmpeg -i combined.mp4 -i mixed.wav -c:v copy -map 0:v:0 -map 1:a:0 final.mp4")

