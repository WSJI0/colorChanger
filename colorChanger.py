from tkinter import filedialog
from tkinter import Button
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import Frame
from tkinter import Label
from tkinter import *
from math import floor
import binascii
import os

window=Tk()
window.iconbitmap(default='icon.ico')
window.title("ColorChanger")
window.geometry("1600x900+160+40")
window.resizable(False, False)

frame=Frame(window, width=1600, height=900, bd=1, relief='solid')
frame.pack(side="left", fill="both", expand=False)

'''
frame2=Frame(window, width=100, height=900, bd=1, relief='solid')
frame2.pack(side="right", fill="both", expand=False)
'''


MODE=3

def openFile():
    global leng,newdir,mod,MODE,fn_ext
    filename=filedialog.askopenfilename(initialdir="C:/")
    with open(filename, 'rb') as f:
        content=f.read()
    mod=binascii.hexlify(content).decode()

    fn_ext=os.path.splitext(filename)

    newdir=fn_ext[0]+'-colormodified.txt'
    oldmod=open(newdir,'w')
    oldmod.write(mod)
    oldmod.close()

    if mod[0:16]=="89504e470d0a1a0a": #png signature
        if mod[mod.index("49484452")+26:mod.index("49484452")+28]=="03": #indexed-color
            leng=int(str(mod[mod.index("504c5445")-8:mod.index("504c5445")]),16)*2
            if mod.count("504c5445")!=1: #PLTE
                messagebox.showwarning("불러올 수 없음", "손상된 png 파일입니다.")
                os.remove(newdir)
            else:
                MODE=3
                showColor3(mod[mod.index("504c5445")+8:mod.index("504c5445")+8+leng])
        elif mod[mod.index("49484452")+26:mod.index("49484452")+28]=="02": #truecolor
            pass
        elif mod[mod.index("49484452")+26:mod.index("49484452")+28]=="04": #grayscale with alpha
            pass
        elif mod[mod.index("49484452")+26:mod.index("49484452")+28]=="06": #truecolor with alpha
            pass
        elif mod[mod.index("49484452")+26:mod.index("49484452")+28]=="00": #grayscale
            pass

        else:
            messagebox.showwarning("불러올 수 없음", "아직은 불러올 수 없는 png 파일입니다.")
            os.remove(newdir)
    else:
        messagebox.showwarning("불러올 수 없음", "해당 파일은 (.png)형식의 파일이 아니거나 손상되었습니다.")
        os.remove(newdir)

def changeColor3(o):
    global fillArr,b,plte
    color=colorchooser.askcolor(color=str("#")+str(fillArr[o][0])+str(fillArr[o][1])+str(fillArr[o][2]))

    plte[o*3]=str("{0:x}".format(floor(color[0][0])).zfill(2))
    plte[o*3+1]=str("{0:x}".format(floor(color[0][1])).zfill(2))
    plte[o*3+2]=str("{0:x}".format(floor(color[0][2])).zfill(2))

    b[o]=Button(frame, overrelief="flat", command=lambda c=o:changeColor3(b[c].cget("text")), background=color[1], text=o)
    b[o].place(x=50*(o%32), y=50*(o//32), width=50, height=50)

def confirmChange(mode):
    global mod,newdir,plte,fn_ext
    newmod=open(newdir,'w')
    if mode==3: 
        new=bytearray.fromhex(str(mod[0:mod.index("504c5445")+8])+str(''.join(plte))+str(mod[mod.index("49444154")-16:len(mod)])).hex()
        new2=binascii.a2b_hex(new)
        with open(fn_ext[0]+'-colormodified.png', 'wb') as png:
            png.write(new2)
    newmod.close()
    os.remove(newdir)
    messagebox.showinfo("저장", "저장되었습니다.")

def reverseColor():
    global fillArr,b,plte
    for o in range(len(fillArr)):
        plte[o*3]=str("{0:x}".format(floor(255-int(fillArr[o][0],16))).zfill(2))
        plte[o*3+1]=str("{0:x}".format(floor(255-int(fillArr[o][1],16))).zfill(2))
        plte[o*3+2]=str("{0:x}".format(floor(255-int(fillArr[o][2],16))).zfill(2))

        newReColor=str('#')+str(plte[o*3])+str(plte[o*3+1])+str(plte[o*3+2])

        b[o]=Button(frame, overrelief="flat", command=lambda c=o:changeColor3(b[c].cget("text")), background=newReColor, text=o)
        b[o].place(x=50*(o%32), y=50*(o//32), width=50, height=50)
    
b=[]
def showColor3(co):
    global b,fillArr,plte,fn_ext,window
    plte=[]
    start=0
    while start!=leng:
        plte.append(co[start:start+2])
        start+=2

    fillArr=[]
    for k in range(0,len(plte),3):
        fillArr.append([plte[k],plte[k+1],plte[k+2]])

    for j in frame.place_slaves():
        j.destroy()
    b=[]
    for i in range(len(fillArr)):
        color=str("#")+str(fillArr[i][0])+str(fillArr[i][1])+str(fillArr[i][2])
        b.append(Button(frame, overrelief="flat", command=lambda c=i:changeColor3(b[c].cget("text")), background=color, text=i))
        b[-1].place(x=50*(i%32), y=50*(i//32), width=50, height=50)

    reColor=Button(frame, overrelief="flat", command=reverseColor, background='#c3c3c3', text='색 반전')
    reColor.place(x=50, y=50*(len(fillArr)//32)+50, width=100, height=50)

    fN=fn_ext[0]+'-colormodified.png'
    photo=ImageTK.photoImage(Image.open(fN))
    label=Label(window, image=photo)
    label.place(x=150, y=50*(len(fillArr)//32)+50, width=100, height=100)
    

    
    

menuBar=Menu(window)
menu1=Menu(menuBar, tearoff=0)
menu1.add_command(label="열기", command=openFile)
menu1.add_separator()
menu1.add_command(label="저장", command=lambda:confirmChange(MODE))
menu1.add_command(label="다른 이름으로 저장")
menuBar.add_cascade(label="파일", menu=menu1)

menu2=Menu(menuBar, tearoff=0)
menu2.add_command(label="버전 알림", command=lambda:messagebox.showwarning("정보", "미완성"))
menuBar.add_cascade(label="정보", menu=menu2)

window.config(menu=menuBar)

window.mainloop()