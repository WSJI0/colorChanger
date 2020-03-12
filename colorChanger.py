from tkinter import filedialog
from tkinter import Button
from tkinter import messagebox
from tkinter import *
import binascii
import os

window=Tk()
window.title("ColorChanger")
window.geometry("1600x900+160+90")
window.resizable(False, False)

def openFile():
    global leng
    filename=filedialog.askopenfilename(initialdir="C:/")
    with open(filename, 'rb') as f:
        content = f.read()
    mod=binascii.hexlify(content).decode()

    filenameArr=filename.split("/")
    filenameArr[len(filenameArr)-1]='temp.txt'
    newdir=str('/'.join(filenameArr))
    newmod=open(newdir,'w')
    newmod.write(mod)
    newmod.close()

    if mod[0:16]=="89504e470d0a1a0a": #png signature
        if mod[mod.index("49484452")+26:mod.index("49484452")+28]=="03": #indexed-color
            leng=int(str(mod[mod.index("504c5445")-8:mod.index("504c5445")]),16)*2
            if mod.count("504c5445")!=1: #PLTE
                messagebox.showwarning("불러올 수 없음", "손상된 png 파일입니다.")
                os.remove(newdir)
            else:
                showColor(mod[mod.index("504c5445")+8:mod.index("504c5445")+8+leng])
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
        

menuBar=Menu(window)
menu1=Menu(menuBar, tearoff=0)
menu1.add_command(label="열기", command=openFile)
menu1.add_separator()
menu1.add_command(label="저장")
menu1.add_command(label="다른 이름으로 저장")
menuBar.add_cascade(label="파일", menu=menu1)

menu2=Menu(menuBar, tearoff=0)
menu2.add_command(label="버전 알림")
menuBar.add_cascade(label="정보", menu=menu2)

window.config(menu=menuBar)

def changeColor(o):
    pass

b=[]
def showColor(co):
    global b
    plte=[]
    start=0
    while start!=leng:
        plte.append(co[start:start+2])
        start+=2

    fillArr=[]
    for i in range(0,len(plte),3):
        fillArr.append([plte[i],plte[i+1],plte[i+2]])

    for j in window.grid_slaves():
        j.destroy()
    b=[]
    for i in range(len(fillArr)):
        color=str("#")+str(fillArr[i][0])+str(fillArr[i][1])+str(fillArr[i][2])
        b.append(Button(window, overrelief="flat", width=10, height=5, command=changeColor(i), background=color))
        b[-1].grid(column=i%20,row=i//20)

window.mainloop()