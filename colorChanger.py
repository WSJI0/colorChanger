from tkinter import filedialog
from tkinter import Button
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import *
from math import floor
import binascii
import os

window=Tk()
window.title("ColorChanger")
window.geometry("1600x900+160+90")
window.resizable(False, False)

def openFile():
    global leng,newdir,mod
    filename=filedialog.askopenfilename(initialdir="C:/")
    with open(filename, 'rb') as f:
        content=f.read()
    mod=binascii.hexlify(content).decode()

    filenameArr=filename.split("/")
    filenameArr[len(filenameArr)-1]='temp.txt'
    newdir=str('/'.join(filenameArr))
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

    b[o]=Button(window, overrelief="flat", width=10, height=5, command=lambda c=o:changeColor3(b[c].cget("text")), background=color[1], text=o)
    b[o].grid(column=o%20,row=o//20)

def confirmChange3():
    global mod,newdir,plte
    newmod=open(newdir,'w')
    newmod.write(str(mod[0:mod.index("504c5445")+8])+str(''.join(plte))+str(mod[mod.index("49444154")-16:len(mod)]))
    newmod.close()
    
b=[]
def showColor3(co):
    global b,fillArr,plte
    plte=[]
    start=0
    while start!=leng:
        plte.append(co[start:start+2])
        start+=2

    fillArr=[]
    for k in range(0,len(plte),3):
        fillArr.append([plte[k],plte[k+1],plte[k+2]])

    for j in window.grid_slaves():
        j.destroy()
    b=[]
    for i in range(len(fillArr)):
        color=str("#")+str(fillArr[i][0])+str(fillArr[i][1])+str(fillArr[i][2])
        b.append(Button(window, overrelief="flat", width=10, height=5, command=lambda c=i:changeColor3(b[c].cget("text")), background=color, text=i))
        b[-1].grid(column=i%20,row=i//20)


menuBar=Menu(window)
menu1=Menu(menuBar, tearoff=0)
menu1.add_command(label="열기", command=openFile)
menu1.add_separator()
menu1.add_command(label="저장", command=confirmChange3)
menu1.add_command(label="다른 이름으로 저장")
menuBar.add_cascade(label="파일", menu=menu1)

menu2=Menu(menuBar, tearoff=0)
menu2.add_command(label="버전 알림", command=lambda:messagebox.showwarning("정보", "미완성"))
menuBar.add_cascade(label="정보", menu=menu2)

window.config(menu=menuBar)

window.mainloop()