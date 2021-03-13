import PySimpleGUI as sg
import os
import youtube_dl as yt

def my_hook(d):       
    if d['status'] == 'downloading':
        window['-PROGRESS_BAR-'].update( str(d['_percent_str']) )

def _down(url:str, path:str):
    
    ydl_opts = {
                'format': 'bestaudio/best',    
                'outtmpl': f'{path}/%(title)s-%(id)s.%(ext)s',
                'progress_hook':[my_hook]
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
        
    info = dict(filter( lambda x:x[0] in ['title','uploader','release_date','upload_date','duration'],info.items()))  
    
    def _formata(title=None,uploader=None,release_date=None,upload_date=None,duration=None ):

        _info = f'title: {title}\nUploader: {uploader}\nupload  date: {upload_date}'

        return _info        
    
    return _formata(**info)   

options = [
    [
        sg.Text("Folder:"),
        sg.In(size=(25,1),enable_events=True,key='-FOLDER-'),
        sg.FolderBrowse()
        
    ],
    [
        sg.Text("url",key='-url-'),
        sg.In(size=(25,1),enable_events=True,key='-URL-'),
        sg.Button('check',key='-check-')
    ]

]   
resume = [
    [sg.Text("Info:",visible=True)],
    [sg.Text (text="",key='-info-',auto_size_text=True,size=(20,20))],
    [sg.HSeparator()],
    [sg.Button('dowload',key='-DOWNLOAD-')],
    [sg.Text(text='---', key='-PROGRESS_BAR-',text_color='green',auto_size_text=True)]
 ]

#layout
layout = [
    [
        sg.Column(options),
        sg.VSeparator(),
        sg.Column(resume)
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
        _down(values['-URL-'],values['-FOLDER-'],window)
        
     
    if event == sg.WIN_CLOSED:
        break

window.close()

