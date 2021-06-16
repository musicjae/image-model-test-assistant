import PySimpleGUI as sg
# import PySimpleGUIQt as sg
import os.path
import PIL.Image
import io
import base64
import shutil
from apilist import loadapi
from setting import args

def convert_to_bytes(file_or_bytes, resize=None,passs=None,fail=None):

    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns

left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse( initial_folder=os.getcwd())],
            [sg.Listbox(values=[], enable_events=True, size=(70,50),key='-FILE LIST-')],
            [ sg.In(key='-W-', size=(5,1)), sg.In(key='-H-', size=(5,1))]]

# For now will only show the name of the file that was chosen
images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')],
              [sg.Button('check',key='check',size=(10,5))],
              [sg.Text('결과: ',size=(40,10),key='result',font=("Helvetica", 25))]]

# ----- Full layout -----
layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c')],
          [sg.Button('Pass'),sg.Button('fail'),sg.Button('Exit')]
          ]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Image Model test assistant in Dangamsoft', layout, resizable=True)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-FOLDER-':
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            filename_ = values['-FILE LIST-'][0]
            window['-TOUT-'].update(filename)
            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                new_size = None
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=new_size))
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename

    elif event in (None,'Exit'):
        break

    elif event == 'Pass':
        print(filename_,'를 pass 폴더 내로 옮겼습니다.')
        filename = filename_
        src = 'images/'
        dir = 'pass/'
        shutil.move(src+filename,dir+filename)

    elif event == 'fail':
        print(filename_,'를 fail 폴더 내로 옮겼습니다.')
        filename = filename_
        src = 'images/'
        dir = 'fail/'
        shutil.move(src+filename,dir+filename)

    elif event == 'check':
        filename = filename_
        result = loadapi(imgpath='images/'+filename, port=args.p)
        print(result)
        window['result'].update(result)

# --------------------------------- Close & Exit ---------------------------------
window.close()