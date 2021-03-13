# dict = {'title':'abc',
#         'autor':'vior'}

# # info = ''''''
# # for x,y in dict.items():
# #     info += f''' {x} {y}\nduration'''

# # print(info)    
# # 

# def _for(title=None,autor=None):
#     text = f'ti:{teitle},\naut:{autor}'

#     return text    

# print(_for(**dict))
import youtube_dl

def my_hook(d):
    # if d['status'] == 'downloading':
    #     print(d['filename'], d['_percent_str'], d['_eta_str'])
    ...



ydl_opts = {
    'format': 'bestaudio/best',    
    'outtmpl': '//home//junin//Área de Trabalho//%(title)s-%(id)s.%(ext)s',
    'progress_hooks':[my_hook]
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=FZUfiW3W1KY&t=263s'],)