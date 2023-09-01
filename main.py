import ttkbootstrap as ttb
from PIL import Image,ImageTk
from random import randint
import threading
import pygame

root=ttb.Window(themename='darkly',resizable=(False,False),title='AMONGUS')

botoes=[]
luzes=[]
sequencia=[]
pos=0

def reiniciarluzes():
    for luz in luzes:
        luz.configure(image=imagem_luz)

def reiniciarbotoes():
    for bot in botoes:
        bot.configure(image=imagem_botao)

def acertou(fim=False):
    global botoes,sequencia,pos
    estadobotoes()
    luzes[len(sequencia)-1].configure(image=imagem_luz_green)
    if fim:
        task_complete.play()
        for bot in botoes:
            bot.configure(image=imagem_botao_green)
        botao_iniciar.configure(state='normal')
    else:
        pos=0
        sequencia.append(randint(0,8))
        for bot in botoes:
            bot.configure(image=imagem_botao_green)
        root.update()
        root.after(1000,reiniciarbotoes)
        root.after(1500,ligarbotao)

def perdeu():
    fail_sound.play()
    estadobotoes()
    for bot in botoes:
        bot.configure(image=imagem_botao_pink)
    botao_iniciar.configure(state='normal')

def estadobotoes(desligado=True):
    if desligado:
        for bot in botoes:
            bot.configure(command=0)
    else:
        for bot in botoes:
            bot.configure(command=lambda e=bot:click(e))

def desligarbotao(botao:ttb.Button,index:int):
    botao.configure(image=imagem_botao)
    root.update()
    root.after(500,lambda:ligarbotao(index+1))

def ligarbotao(index=0):
    global sequencia
    if len(sequencia)<=index:
        estadobotoes(desligado=False)
        return
    else:
        clicked_sound.play()
        botao_atual=botoes[sequencia[index]]
        botao_atual.configure(image=imagem_botao_blue)
        root.update()
        root.after(1000,lambda:desligarbotao(botao_atual,index))

def iniciar():
    global sequencia,pos
    pos=0
    sequencia=[]
    reiniciarluzes()
    reiniciarbotoes()
    botao_iniciar.configure(state='disabled')
    sequencia.append(randint(0,8))
    ligarbotao()

def click(botao:ttb.Button):
    global sequencia,pos,botoes,luzes
    posicao_certa=True if sequencia[pos]==botoes.index(botao) else False
    limite=len(sequencia)
    clicked_sound.play()
    if posicao_certa and pos+1<limite:
        pos+=1
        botao.configure(image=imagem_botao_blue,command=0)
        threading.Timer(1,lambda:botao.configure(command=lambda e=botao:click(e),image=imagem_botao)).start()
    elif posicao_certa and pos+1==limite and limite<5:
        acertou()
    elif posicao_certa and pos+1==limite and limite==5:
        acertou(fim=True)
    else:
        perdeu()

pygame.init()
pygame.mixer.init()
clicked_sound=pygame.mixer.Sound('_audios\Start_Reactor_begin.ogg')
fail_sound=pygame.mixer.Sound('_audios\Start_Reactor_fail.ogg')
task_complete=pygame.mixer.Sound('_audios\Task_completion_sound.ogg')

estilo=ttb.Style()
estilo.configure('new.TLabel',background='#A2A3A2')
estilo.configure('TFrame',background='#A2A3A2')
estilo.configure('TButton',foreground='#A2A3A2',background='#A2A3A2',relief='solid',bordercolor='#A2A3A2',focuscolor='#A2A3A2')
estilo.map('TButton',background=[('active','#A2A3A2')])

imagem_base_pil=Image.open(r'_imagens\base.png')
imagem_base_pil=imagem_base_pil.resize((450,500))
imagem_base=ImageTk.PhotoImage(imagem_base_pil)

imagem_botao_pil=Image.open(r'_imagens\button.png')
imagem_botao_pil=imagem_botao_pil.resize((80,80))
imagem_botao=ImageTk.PhotoImage(imagem_botao_pil)

imagem_luz_pil=Image.open('_imagens\light.png')
imagem_luz_pil=imagem_luz_pil.resize((30,30))
imagem_luz=ImageTk.PhotoImage(imagem_luz_pil)

imagem_botao_blue_pil=Image.open(r'_imagens\button_blue.png')
imagem_botao_blue_pil=imagem_botao_blue_pil.resize((80,80))
imagem_botao_blue=ImageTk.PhotoImage(imagem_botao_blue_pil)

imagem_botao_pink_pil=Image.open(r'_imagens\button_pink.png')
imagem_botao_pink_pil=imagem_botao_pink_pil.resize((80,80))
imagem_botao_pink=ImageTk.PhotoImage(imagem_botao_pink_pil)

imagem_botao_green_pil=Image.open(r'_imagens\button_green.png')
imagem_botao_green_pil=imagem_botao_green_pil.resize((80,80))
imagem_botao_green=ImageTk.PhotoImage(imagem_botao_green_pil)

imagem_luz_green_pil=Image.open('_imagens\light_green.png')
imagem_luz_green_pil=imagem_luz_green_pil.resize((30,30))
imagem_luz_green=ImageTk.PhotoImage(imagem_luz_green_pil)

ttb.Label(root,image=imagem_base).pack()

frame_luzes=ttb.Frame(root)
frame_luzes.place(x=95,y=55)

luz_um=ttb.Label(frame_luzes,image=imagem_luz,style='new.TLabel')
luz_dois=ttb.Label(frame_luzes,image=imagem_luz,style='new.TLabel')
luz_tres=ttb.Label(frame_luzes,image=imagem_luz,style='new.TLabel')
luz_quatro=ttb.Label(frame_luzes,image=imagem_luz,style='new.TLabel')
luz_cinco=ttb.Label(frame_luzes,image=imagem_luz,style='new.TLabel')

luz_um.grid(row=0,column=0,padx=10)
luz_dois.grid(row=0,column=1,padx=10)
luz_tres.grid(row=0,column=2,padx=10)
luz_quatro.grid(row=0,column=3,padx=10)
luz_cinco.grid(row=0,column=4,padx=10)

luzes=[luz_um,luz_dois,luz_tres,luz_quatro,luz_cinco]

frame_principal=ttb.Frame(root)
frame_principal.place(x=75,y=170)

botao_um=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_um))
botao_dois=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_dois))
botao_tres=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_tres))
botao_quatro=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_quatro))
botao_cinco=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_cinco))
botao_seis=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_seis))
botao_sete=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_sete))
botao_oito=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_oito))
botao_nove=ttb.Button(frame_principal,image=imagem_botao,command=lambda:click(botao_nove))

botao_um.grid(row=0,column=0)
botao_dois.grid(row=0,column=1)
botao_tres.grid(row=0,column=2)
botao_quatro.grid(row=1,column=0)
botao_cinco.grid(row=1,column=1)
botao_seis.grid(row=1,column=2)
botao_sete.grid(row=2,column=0)
botao_oito.grid(row=2,column=1)
botao_nove.grid(row=2,column=2)

botoes=[botao_um,botao_dois,botao_tres,botao_quatro,botao_cinco,botao_seis,botao_sete,botao_oito,botao_nove]

botao_iniciar=ttb.Button(root,width=10,text='Iniciar',bootstyle='info outline',command=iniciar)
botao_iniciar.pack(pady=10,anchor='center')

estadobotoes()

root.mainloop()