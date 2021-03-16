import PySimpleGUI as sg
import os
import youtube_dl as yt
import textwrap


def my_hook(d):       
    if d['status'] == 'downloading':
        _progress = float(d['_percent_str'][:-1].replace('%',''))
        window['-PROGRESS_BAR-'].UpdateBar(_progress)
        
    if d['status'] == 'finished':
        sg.popup('finished',location=(720,180))


def _down(url:str, path:str):   
    ydl_opts = {
                'format': 'bestaudio/best',  
                 'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'm4a',
                                    'preferredquality': '192',
                                    }],  
                'outtmpl': f'{path}/%(title)s-%(id)s.%(ext)s',
                'progress_hooks':[my_hook]
    }
    
    with yt.YoutubeDL(ydl_opts) as ydl: 
        try:
            ydl.download([str(url)])
                   
        except:
            sg.popup('Error...',location=(720,180))


def ext_info(url:str):
    info = {}
    with yt.YoutubeDL({}) as ydl:
        try:
            info = ydl.extract_info(url=url,download=False)
            
        except:
            sg.popup('Url invalida!...',location=(720,180))
        
        else:
            info = dict(filter( lambda x:x[0] in ['title','uploader','release_date','upload_date','duration'],info.items()))  
    
            def _formata(title=None,uploader=None,release_date=None,upload_date=None,duration=None ):
                _info = f'''Title: {title}
                    Uploader: {uploader}
                    Upload_date: {upload_date}
                    Duration: { float(int(duration)/60):10.2f}min~'''
                wrapper = textwrap.TextWrapper(width=50,subsequent_indent='\n')

                return wrapper.fill(text=_info)        
    
            return _formata(**info)   

options = [
    [
        sg.Text("Folder:"),
        sg.In(size=(25,1),enable_events=True,key='-FOLDER-'),
        sg.FolderBrowse()
        
    ],
    [
        sg.Text("URL",key='-url-'),
        sg.In(size=(25,1),enable_events=True,key='-URL-'),
        sg.Button('check',key='-check-')
    ]

]   
resume = [
    [
        sg.Text("INFO:", visible=True,font=12)
    ],
    [
        sg.Text (text="",key='-info-', auto_size_text=True, size=(20,20), font=10)
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Button('dowload',key='-DOWNLOAD-' )
    ],
    [
        sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_BAR-')
    ]
 ]

#layout
layout = [
    [
        sg.Column(options),
        sg.VSeparator(),
        sg.Column(resume, justification='center')
    ]
]


# Create the window
window = sg.Window("Youtube Download", layout,location=(720,180))


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "-check-":
        window['-info-'].update( ext_info(values['-URL-']))


    if event == "-DOWNLOAD-":
        _down(values['-URL-'],values['-FOLDER-'])
        
     
    if event == sg.WIN_CLOSED:
        break

window.close()

