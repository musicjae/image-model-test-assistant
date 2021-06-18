import PySimpleGUI as sg
# import PySimpleGUIQt as sg
import os.path
from PIL import Image
import io
import base64
import shutil
from apilist import loadapi
from setting import args
from utils import findprepost
from subprocess import call
import os

# ## For run and set port ##
# base = os.getcwd()
#
# call([f'python main.py --p={args.p}'], cwd=base,shell=True)
# ##########################

sg.theme('Light Blue 1')
def convert_to_bytes(file_or_bytes, resize=None,passs=None,fail=None):

    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            img.thumbnail((100,100))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)
            img.thumbnail((100, 100))
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns

left_col = [[sg.Text('port'), sg.InputText(key='port'),sg.Submit()],
           [sg.Text(size=(25,1),key='port_check',font=("Bodoni", 15))],
            [sg.Text('Folder',font=("Bodoni")),sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(initial_folder=os.getcwd())],
            [sg.Listbox(values=[], enable_events=True, size=(80,40),key='-FILE LIST-')],
            [ sg.In(key='-W-', size=(0,0)), sg.In(key='-H-', size=(0,0))]]

# For now will only show the name of the file that was chosen
images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-PREIMAGE-'),
              sg.Image(key='-IMAGE-'),
              sg.Image(key='-POSTIMAGE-')],
              [sg.Text('Output: ',size=(40,1),key='result',font=("Bodoni", 25))],
              [sg.Button('Pass',size=(4,2),font=("Bodoni", 15)),sg.Button('fail',size=(4,2),font=("Bodoni", 15)),sg.Button('Exit',size=(4,2),font=("Helvetica", 15))],
              [sg.Text(size=(25,1),key='output_notification',font=("Bodoni", 15))],
              [sg.Button('Manual check',key='check',size=(6,2),font=("Bodoni", 10))]]

# ----- Full layout -----
layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------

window = sg.Window('Image Model test assistant in Dangamsoft', layout, resizable=True,font=("Bodoni"))

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:

    event, values = window.read(timeout=1)
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
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)

    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            filename_ = values['-FILE LIST-'][0]

            res = findprepost(file_list,filename_)
            prev_img = os.path.join(values['-FOLDER-'],file_list[res[0]])
            post_img = os.path.join(values['-FOLDER-'],file_list[res[1]])

            window['-TOUT-'].update(filename)

            window['-PREIMAGE-'].update(data=convert_to_bytes(prev_img), size=(100, 100))
            window['-IMAGE-'].update(data=convert_to_bytes(filename),size=(300,300))
            window['-POSTIMAGE-'].update(data=convert_to_bytes(post_img), size=(100, 100))

            filename = filename_
            result = loadapi(imgpath='images/' + filename, port=args.p)
            window['result'].update(result)

        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename


    elif event == 'Submit':
        try:
            window['port_check'].update(f"{int(values['port'])} 번 포트가 입력되었습니다.")
        except:
            window['port_check'].update('종료 후 다시 시작해주세요')

    elif event in (None,'Exit'):
        break

    elif event == 'Pass':
        print(filename_,'를 pass 폴더 내로 옮겼습니다.')
        filename = filename_
        src = 'images/'
        dir = 'pass/'
        shutil.copyfile(src+filename,dir+filename)
        window['output_notification'].update(filename_+'를 pass 폴더 내로 옮겼습니다.')



    elif event == 'fail':
        print(filename_,'를 fail 폴더 내로 옮겼습니다.')
        filename = filename_
        src = 'images/'
        dir = 'fail/'
        shutil.copyfile(src+filename,dir+filename)
        window['output_notification'].update(filename_+'를 fail 폴더 내로 옮겼습니다.')

    elif event == 'check':
        filename = filename_
        result = loadapi(imgpath='images/'+filename, port=int(values['port']))
        window['result'].update(result)



# --------------------------------- Close & Exit ---------------------------------
window.close()