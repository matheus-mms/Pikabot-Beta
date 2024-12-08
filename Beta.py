from tkinter.ttk import Label,Button,Combobox,Style, Checkbutton, Scale
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
import json
from time import sleep
import my_keyboard
import pyautogui
import time
import numpy as np
import constantes
import os
import threading
import pynput
import os
import cv2
import random
from tkinter import filedialog
from pynput import mouse
from PIL import ImageGrab, Image, ImageDraw, ImageTk
from keyboard import is_pressed

main_process_pid = os.getpid()

with open('default.json', 'r') as file:
    data = json.loads(file.read())
love = data['love']['value']
loot = data['loot']['value']
road = data['road']['value']
ball = data['ball']['value']
heal = data['heal']['value']
life_pos = data['Life_pos']['position']
rgb = data['Life_pos']['rgb']

x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False
canvas = None
captured_image_window = None
x_heal = ""
y_heal = ""

room = ThemedTk(theme='arc', themebg=True)
room.title("PikaBot Fishing")
#room.geometry('500x700+650+400')
room.resizable(False, False)
style = Style()
style.configure('TBB', font=constantes.form_text)
room.iconbitmap('PikaBot.ico')
scale_var = tk.IntVar()
label_var = tk.StringVar()

def generate_widget (widget, row, column, padx=5, pady=5, stick='NSEW', columnspan=1, **kwargs ):
    my_widget = widget(**kwargs)
    my_widget.grid(row=row, column=column, padx=padx, pady=pady, stick = stick, columnspan = columnspan)
    return my_widget

def generate_checkbutton(texto, row, column, columnspan=1, sticky="S"):
    var = tk.BooleanVar()
    checkbutton = Checkbutton(room, text=texto, variable=var)
    checkbutton.grid(row=row, column=column, padx=5, pady=5, columnspan=columnspan, sticky=sticky)
    constantes.checkbutton_vars.append(var)

def clicar_no_centro_da_imagem(coordenadas):
    if not coordenadas:
            print("Nenhuma coordenada para clicar.")
            return

    primeira_coordenada = random.choice(coordenadas)

    x, y, largura, altura = primeira_coordenada["x"], primeira_coordenada["y"], primeira_coordenada["largura"], primeira_coordenada["altura"]
    centro_x, centro_y = pyautogui.center((x, y, largura, altura))

    # Clica no centro
    pyautogui.moveTo(centro_x, centro_y)
    sleep(0.5)
    my_keyboard.press(road)
    return primeira_coordenada

def procurar_imagem_na_tela_pasta(pasta_referencia, caminho_imagem_capturada):
    coordenadas_encontradas = []

    imagens_referencia = [f for f in os.listdir(pasta_referencia) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for imagem_referencia_nome in imagens_referencia:
        caminho_imagem_referencia = os.path.join(pasta_referencia, imagem_referencia_nome)

        imagem_referencia = cv2.imread(caminho_imagem_referencia, cv2.IMREAD_GRAYSCALE)

        if imagem_referencia is None:
            print(f"Erro: Não foi possível carregar a imagem de referência em '{caminho_imagem_referencia}'. Verifique o caminho e a existência do arquivo.")
            continue

        imagem_capturada = cv2.imread(caminho_imagem_capturada, cv2.IMREAD_GRAYSCALE)

        if imagem_capturada is None:
            print(f"Erro: Não foi possível carregar a imagem capturada em '{caminho_imagem_capturada}'. Verifique o caminho e a existência do arquivo.")
            continue

        resultado_correspondencia = cv2.matchTemplate(imagem_capturada, imagem_referencia, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8
        loc = np.where(resultado_correspondencia >= threshold)
        coordenadas_encontradas.extend([
            {"x": pt[0], "y": pt[1], "largura": imagem_referencia.shape[1], "altura": imagem_referencia.shape[0]}
            for pt in zip(*loc[::-1])
        ])
    return coordenadas_encontradas

def set_fishing_rod():
    while not myevent.is_set():
        screenshot = pyautogui.screenshot()
        screenshot.save('validar_pesca/set_fishing_rod.png')
        coordenadas = procurar_imagem_na_tela_pasta('water', 'validar_pesca/set_fishing_rod.png')
        coordenada_clicada = clicar_no_centro_da_imagem(coordenadas)
        wait_bolhas(coordenada_clicada)
        if coordenada_clicada:   
            break

def wait_bolhas(coordenada=None, **kwargs):
    tempo_inicial = time.time()
    sair = 0
    target_monster()
    while not myevent.is_set():
        if coordenada is None:
            return
        if sair == 1:
            break
        pasta_bolhas = 'bubbles'
        imagens_bolhas = [f for f in os.listdir(pasta_bolhas) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.PNG'))]
        x, y = coordenada["x"], coordenada["y"]
        for imagem_bolhas in imagens_bolhas:
            caminho_imagem = os.path.join(pasta_bolhas, imagem_bolhas)
            bolhas = pyautogui.locateOnScreen(caminho_imagem, confidence=0.8 , region=(x -20, y -20, 120, 120)) 
            if bolhas is not None:
                my_keyboard.press(road)
                #sleep(0.5)
                sair = 1
                break
                

        if time.time() - tempo_inicial >= 60:
            print('loop cabou')
            break
        sleep(0.1)

def minigame():
    sleep(0.5)
    fish = True
    while fish != None:
        bar = pyautogui.locateOnScreen('validar_pesca/bar.png', confidence=(constantes.var_minigame), region=constantes.MINIGAME_REGION)
        fish = pyautogui.locateOnScreen('validar_pesca/fish.png', confidence=(constantes.var_minigame), region=constantes.MINIGAME_REGION, grayscale=True)
        if bar != None and fish != None:
            peixe_top = fish[1]  # O índice 1 representa a coordenada 'top(y)' na tupla
            barra_top = bar[1]  # O índice 1 representa a coordenada 'top(y)' na tupla

            if barra_top > peixe_top:
                my_keyboard.key_down(0x39)
            else:
                my_keyboard.release_key(0x39)
        else:
            my_keyboard.key_down(0x39)
            my_keyboard.release_key(0x39)

def target_monster ():
    if len(constantes.itens_target) > 0:
        sleep(0.5)
        sair1 = 0
        while not myevent.is_set():
            if sair1 == 1:
                break
            for caminho_imagem in constantes.caminhos_arquivos_target:
                target = pyautogui.locateOnScreen(caminho_imagem, confidence=0.6)
                if target is not None:
                    target_x, target_y = pyautogui.center(target)
                    pyautogui.moveTo(target_x,target_y,0.3)
                    pyautogui.click()
                    sleep (0.5)
                    coordenadas_normalizadas1 = constantes.normalizar_coordenadas(*(963, 397, 10, 10))
                    x1,y1, largura1, altura1 = coordenadas_normalizadas1
                    pyautogui.moveTo(x1,y1, 0.5)
                    espera_poke_morrer()
                    break
            target = pyautogui.locateOnScreen(caminho_imagem, confidence=0.6)
            if target == None:
                sair1 = 1
                break
            time.sleep(0.1)

def atack_backup(checkbutton_id):
    estado = constantes.checkbutton_vars[checkbutton_id].get()
    if estado:
        if checkbutton_id == 0:
            my_atacks = constantes.spells_backup
            for atack in my_atacks:
                my_keyboard.press(atack)

def atack(checkbutton_id):
    estado = constantes.checkbutton_vars[checkbutton_id].get()
    my_atacks = constantes.spells
    for atack in my_atacks:
        my_keyboard.press(atack)
        if estado:
            if checkbutton_id == 1:
                sleep(2)

def espera_poke_morrer():
    sair = 0
    my_screen = pyautogui.screenshot(region=constantes.CONDICAO_SAIDA)
    width, height = my_screen.size
    for x in range(0, width,1):
        for y in range(0,height,1):
            r,g,b = my_screen.getpixel((x, y))

            while r == 180:
                my_screen = pyautogui.screenshot(region=(constantes.CONDICAO_SAIDA))
                r,g,b = my_screen.getpixel((x, y))
                atack(checkbutton_id=1)
                sleep(1.7)
                heal_poke(checkbutton_id=2)
                sleep(0.1)
                my_screen = pyautogui.screenshot(region=(constantes.CONDICAO_SAIDA))
                r,g,b = my_screen.getpixel((x, y))
                sleep(0.1)
                if r == 180:
                    atack_backup(checkbutton_id=0)
                sair = 1
                  
            if sair == 1:
                break
def catch():
    if len(constantes.itens_catch) > 0:
        sair = 0
        while not myevent.is_set():
            print('iniciou captura')
            if sair == 1:
                break
            for caminho_imagem in constantes.caminhos_arquivos_catch:
                catch_poke = pyautogui.locateOnScreen(caminho_imagem, confidence=0.6, region=(constantes.x_catch-400, constantes.y_catch-400, 500, 500))

                if catch_poke is not None:
                    x, y,A,L = catch_poke
                    my_keyboard.press(ball)
                    sleep(0.2)
                    center_x, center_y = pyautogui.center((x,y,A,L))
                    pyautogui.moveTo(center_x, center_y, 0.5)
                    sleep (0.2)
                    pyautogui.click()
                    break
            if catch_poke is None:
                sair = 1

def save_file():
    my_data = {
        "love": {
            'value': cbx_love.get(),
            'position': cbx_love.current()
        },
        "loot": {
            'value': cbx_loot.get(),
            'position': cbx_loot.current()
        },
        "road": {
            'value': cbx_road.get(),
            'position': cbx_road.current()
        },
        "ball": {
            'value': cbx_ball.get(),
            'position': cbx_ball.current()
        },
        "Life_pos": {
            'position': life_pos,
            'rgb': rgb
        },
        "heal": {
            'value': cbx_life.get(),
            'position': cbx_life.current()
        },
        "potion": {
            'value': cbx_potion.get(),
            'position': cbx_potion.current()
        },
        "itens_catch": constantes.itens_catch,
        "itens_target": constantes.itens_target,
        "itens_spell": constantes.itens_spells,
        "itens_spell_backup": constantes.itens_spells_backup,
        "time_potion": constantes.time_potion,
        "var_minigame": constantes.var_minigame
    }
    file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")],
            title="Salvar Arquivo JSON"
        )

    if file_path:
        with open(file_path, 'w') as file:
            file.write(json.dumps(my_data))

        print(f"Arquivo salvo em: {file_path}")
    else:
        print("Nenhum arquivo selecionado. O arquivo não foi salvo.")

def save():
    my_data = {
        "love": {
            'value': cbx_love.get(),
            'position': cbx_love.current()
        },
        "loot": {
            'value': cbx_loot.get(),
            'position': cbx_loot.current()
        },
        "road": {
            'value': cbx_road.get(),
            'position': cbx_road.current()
        },
        "ball": {
            'value': cbx_ball.get(),
            'position': cbx_ball.current()
        },
        "Life_pos": {
            'position': life_pos,
            'rgb': rgb
        },
        "heal": {
            'value': cbx_life.get(),
            'position': cbx_life.current()
        },
        "potion": {
            'value': cbx_potion.get(),
            'position': cbx_potion.current()
        },
        "itens_catch": constantes.itens_catch,
        "itens_target": constantes.itens_target,
        "itens_spell": constantes.itens_spells,
        "itens_spell_backup": constantes.itens_spells_backup,
        "time_potion": constantes.time_potion,
        "var_minigame": constantes.var_minigame
    }
    with open('interface.json', 'w') as file:
        file.write(json.dumps(my_data))

def Load_window():
    global life_pos
    global rgb
    global x_heal
    global y_heal
    global lbl_life_pos
    global lbl_cor
    global lbl_potion_time

    if lbl_life_pos is not None:
        lbl_life_pos.destroy()
        lbl_cor.destroy()

    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos JSON", "*.json")],
        title="Carregar Arquivo JSON"
    )

    if file_path:
        with open(file_path, 'r') as file:
            data = json.loads(file.read())
    cbx_love.current(data['love']['position'])
    cbx_loot.current(data['loot']['position'])
    cbx_road.current(data['road']['position'])
    cbx_ball.current(data['ball']['position'])
    cbx_life.current(data['heal']['position'])
    cbx_potion.current(data['potion']['position'])
    life_pos = data['Life_pos']['position']
    rgb = data['Life_pos']['rgb']
    constantes.time_potion = data['time_potion']
    constantes.var_minigame = data['var_minigame']
    label_var.set(f"Valor: {constantes.var_minigame}")
    scale_var.set((constantes.var_minigame*10))

    lbl_potion_time.destroy()
    lbl_potion_time = generate_widget(Label, row=4, column=3, stick='S', text=f"{constantes.time_potion} seconds", font=constantes.form_text)

    if life_pos is not None:
        x_heal = life_pos[0]
        y_heal = life_pos[1]

    lbl_life_pos = generate_widget(Label, row=4, column=0, stick='s', text=f"X: {x_heal} | Y: {y_heal}", font=constantes.form_text)
    lbl_cor = generate_widget(Label, row=5, column=0, stick='n', text=f"Color: {rgb}", font=constantes.form_text)
    
    lista_spell_backup.delete(0, tk.END)
    constantes.itens_spells_backup = []
    constantes.spells_backup = []
    lista_spell.delete(0, tk.END)
    constantes.itens_spells = []
    constantes.spells = []

    for item_data in data.get("itens_catch", []):
        nome_item = item_data.get("nome")
        caminho_arquivo = item_data.get("caminho")
        caminho_json = item_data.get("caminho_json")

        if nome_item and caminho_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_catch]:
                constantes.itens_catch.append({'nome': nome_item, 'caminho': caminho_arquivo, 'caminho_json': caminho_json})
                lista_catch.insert(tk.END, nome_item)
                constantes.caminhos_arquivos_catch.append(caminho_arquivo)

    # Adicionar itens de 'itens_target' à lista e à lista de caminhos
    for item_data in data.get("itens_target", []):
        nome_item = item_data.get("nome")
        caminho_arquivo = item_data.get("caminho")
        caminho_json = item_data.get("caminho_json")

        if nome_item and caminho_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_target]:
                constantes.itens_target.append({'nome': nome_item, 'caminho': caminho_arquivo, 'caminho_json': caminho_json})
                lista_target.insert(tk.END, nome_item)
                constantes.caminhos_arquivos_target.append(caminho_arquivo)

    for item_data in data.get("itens_spell", []):
        nome_item = item_data.get("nome")
        spell_arquivo = item_data.get("spell")
        caminho_json = item_data.get("caminho_json")

        if nome_item and spell_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_spells]:
                constantes.itens_spells.append({'nome': nome_item, 'spell': spell_arquivo, 'caminho_json': caminho_json})
                lista_spell.insert(tk.END, nome_item)
                constantes.spells.append(spell_arquivo)
    
    for item_data in data.get("itens_spell_backup", []):
            nome_item = item_data.get("nome")
            spell_arquivo_backup = item_data.get("spell_backup")
            caminho_json = item_data.get("caminho_json")

            if nome_item and spell_arquivo_backup and caminho_json:
                if nome_item not in [item.get("nome") for item in constantes.itens_spells_backup]:
                    constantes.itens_spells_backup.append({'nome': nome_item, 'spell_backup': spell_arquivo_backup, 'caminho_json': caminho_json})
                    lista_spell_backup.insert(tk.END, nome_item)
                    constantes.spells_backup.append(spell_arquivo_backup)

def Load():
    global love
    global loot
    global road
    global ball
    global heal
    global life_pos
    global rgb
    global potion
    global x_heal
    global y_heal
    global lbl_life_pos
    global lbl_cor
    global lbl_potion_time

    if lbl_life_pos is not None:
        lbl_life_pos.destroy()
        lbl_cor.destroy()

    with open('interface.json', 'r') as file:
        data = json.loads(file.read())

    cbx_love.current(data['love']['position'])
    cbx_loot.current(data['loot']['position'])
    cbx_road.current(data['road']['position'])
    cbx_ball.current(data['ball']['position'])
    cbx_life.current(data['heal']['position'])
    cbx_potion.current(data['potion']['position'])

    lista_spell_backup.delete(0, tk.END)
    constantes.itens_spells_backup = []
    constantes.spells_backup = []
    lista_spell.delete(0, tk.END)
    constantes.itens_spells = []
    constantes.spells = []

    love = data['love']['value']
    loot = data['loot']['value']
    road = data['road']['value']
    ball = data['ball']['value']
    heal = data['heal']['value']
    potion = data['potion']['value']
    life_pos = data['Life_pos']['position']
    rgb = data['Life_pos']['rgb']
    constantes.time_potion = data['time_potion']
    constantes.var_minigame = data['var_minigame']
    label_var.set(f"Valor: {constantes.var_minigame}")
    scale_var.set((constantes.var_minigame*10))

    lbl_potion_time.destroy()
    lbl_potion_time = generate_widget(Label, row=4, column=3, stick='S', text=f"{constantes.time_potion} seconds", font=constantes.form_text)

    if life_pos is not None:
        x_heal = life_pos[0]
        y_heal = life_pos[1]
    lbl_life_pos = generate_widget(Label, row=4, column=0, stick='s', text=f"X: {x_heal} | Y: {y_heal}", font=constantes.form_text)
    lbl_cor = generate_widget(Label, row=5, column=0, stick='n', text=f"Color: {rgb}", font=constantes.form_text)
    
    for item_data in data.get("itens_catch", []):
        nome_item = item_data.get("nome")
        caminho_arquivo = item_data.get("caminho")
        caminho_json = item_data.get("caminho_json")

        if nome_item and caminho_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_catch]:
                constantes.itens_catch.append({'nome': nome_item, 'caminho': caminho_arquivo, 'caminho_json': caminho_json})
                lista_catch.insert(tk.END, nome_item)
                constantes.caminhos_arquivos_catch.append(caminho_arquivo)

    # Adicionar itens de 'itens_target' à lista e à lista de caminhos
    for item_data in data.get("itens_target", []):
        nome_item = item_data.get("nome")
        caminho_arquivo = item_data.get("caminho")
        caminho_json = item_data.get("caminho_json")

        if nome_item and caminho_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_target]:
                constantes.itens_target.append({'nome': nome_item, 'caminho': caminho_arquivo, 'caminho_json': caminho_json})
                lista_target.insert(tk.END, nome_item)
                constantes.caminhos_arquivos_target.append(caminho_arquivo)

    for item_data in data.get("itens_spell", []):
        nome_item = item_data.get("nome")
        spell_arquivo = item_data.get("spell")
        caminho_json = item_data.get("caminho_json")

        if nome_item and spell_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_spells]:
                constantes.itens_spells.append({'nome': nome_item, 'spell': spell_arquivo, 'caminho_json': caminho_json})
                lista_spell.insert(tk.END, nome_item)
                constantes.spells.append(spell_arquivo)
    
    for item_data in data.get("itens_spell_backup", []):
            nome_item = item_data.get("nome")
            spell_arquivo_backup = item_data.get("spell_backup")
            caminho_json = item_data.get("caminho_json")

            if nome_item and spell_arquivo_backup and caminho_json:
                if nome_item not in [item.get("nome") for item in constantes.itens_spells_backup]:
                    constantes.itens_spells_backup.append({'nome': nome_item, 'spell_backup': spell_arquivo_backup, 'caminho_json': caminho_json})
                    lista_spell_backup.insert(tk.END, nome_item)
                    constantes.spells_backup.append(spell_arquivo_backup)
    
def main_process():
    while not myevent.is_set():
        sleep (2)
        heal_poke(checkbutton_id = 2)
        Potion_poke(checkbutton_id = 3)
        print('Pesca iniciada')
        set_fishing_rod()
        minigame()
        target_monster()
        catch()
        my_keyboard.press(loot)
        sleep(0.3)
        my_keyboard.press(love)
        sleep(0.2)

def start():
    #room.iconify()
    global data
    data = Load()
    #btn_iniciar['state'] = tk.DISABLED
    global myevent
    myevent = threading.Event()
    global start_th
    start_th = threading.Thread(target=main_process)
    start_th.start()

def key_listener():
    global myevent
    with pynput.keyboard.Listener(on_release=on_key_event) as listener:
        listener.join()

def on_key_event(Key):
    if Key == pynput.keyboard.Key.f12:
        print("Programa será encerrado pelo usuário.")
        myevent.set()
        key_thread = threading.Thread(target=key_listener)
        key_thread.start()
        return False
    elif Key == pynput.keyboard.Key.f11:
        print("Tecla F11 pressionada. Iniciando...")
        start()

key_thread = threading.Thread(target=key_listener)
key_thread.start()

def close_window():
    os.kill(main_process_pid, 9)

def adicionar_item(entry,lista):
    item = entry.get()
    if item:
        threading.Thread(target=lambda: inicia_captura(entry, lista, item)).start()

def remover_item(lista):
    if lista == lista_catch:
        selecao = lista.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            if indice_selecionado < len(constantes.itens_catch):
                item_removido = constantes.itens_catch.pop(indice_selecionado)
                constantes.caminhos_arquivos_catch.pop(indice_selecionado)
                lista.delete(indice_selecionado)
                print(constantes.caminhos_arquivos_catch)
                print(constantes.itens_catch)
                if item_removido:
                    caminho_json = item_removido.get('caminho_json')
                    if os.path.exists(caminho_json):
                        os.remove(caminho_json)
                        print(f"Arquivo removido: {caminho_json}")
                        
    elif lista == lista_target:
        selecao = lista.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            if indice_selecionado < len(constantes.itens_target):
                item_removido = constantes.itens_target.pop(indice_selecionado)
                constantes.caminhos_arquivos_target.pop(indice_selecionado)
                lista.delete(indice_selecionado)
                print(constantes.caminhos_arquivos_target)
                print(constantes.itens_target)
                if item_removido:
                    caminho_json = item_removido.get('caminho_json')
                    if os.path.exists(caminho_json):
                        os.remove(caminho_json)
                        print(f"Arquivo removido: {caminho_json}")
    
    elif lista == lista_spell:
        selecao = lista.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            if indice_selecionado < len(constantes.itens_spells):
                item_removido = constantes.itens_spells.pop(indice_selecionado)
                constantes.spells.pop(indice_selecionado)
                lista.delete(indice_selecionado)
                print(constantes.itens_spells)
                print(constantes.spells)
                if item_removido:
                    caminho_json = item_removido.get('caminho_json')
                    if os.path.exists(caminho_json):
                        os.remove(caminho_json)
                        print(f"Arquivo removido: {caminho_json}")
            
    elif lista == lista_spell_backup:
        selecao = lista.curselection()
        if selecao:
            indice_selecionado = selecao[0]
            if indice_selecionado < len(constantes.itens_spells_backup):
                item_removido = constantes.itens_spells_backup.pop(indice_selecionado)
                constantes.spells_backup.pop(indice_selecionado)
                lista.delete(indice_selecionado)
                print(constantes.itens_spells_backup)
                print(constantes.spells_backup)
                if item_removido:
                    caminho_json = item_removido.get('caminho_json')
                    if os.path.exists(caminho_json):
                        os.remove(caminho_json)
                        print(f"Arquivo removido: {caminho_json}")
            else:
                print("Erro: Índice selecionado fora dos limites.")

def adicionar_item_lista(entry, lista, item, caminho_arquivo):
    if lista == lista_catch:
        constantes.itens_catch.append({'nome': item, 'caminho': caminho_arquivo, 'caminho_json': f"{item}.json"})
        
        constantes.caminhos_arquivos_catch.append(caminho_arquivo)
        lista.insert(tk.END, item)
        salvar_configuracao_json( lista, item, caminho_arquivo)

        entry.delete(0, tk.END)
    if lista == lista_target:
        constantes.itens_target.append({'nome': item, 'caminho': caminho_arquivo, 'caminho_json': f"{item}.json"})
        constantes.caminhos_arquivos_target.append(caminho_arquivo)
        lista.insert(tk.END, item)
        salvar_configuracao_json( lista, item, caminho_arquivo)

        entry.delete(0, tk.END)

def salvar_configuracao_json(lista, item, caminho_arquivo):
    if lista == lista_catch:
        configuracao = {"item": item, "caminho_arquivo": caminho_arquivo}
        nome_arquivo_json = f"{item}.json"
        caminho_arquivo_json = os.path.join("text_catch", nome_arquivo_json)
        with open(caminho_arquivo_json, "w") as arquivo_json:
            json.dump(configuracao, arquivo_json)
    if lista == lista_target:
        configuracao = {"item": item, "caminho_arquivo": caminho_arquivo}
        nome_arquivo_json = f"{item}.json"
        caminho_arquivo_json = os.path.join("text_target", nome_arquivo_json)
        with open(caminho_arquivo_json, "w") as arquivo_json:
            json.dump(configuracao, arquivo_json)

def on_move(event):
    global x_end, y_end, drawing

    if drawing:
        x_end, y_end = event.x_root, event.y_root
        draw_rectangle()

def draw_rectangle():
    if captured_image_window:
        captured_image_window.destroy()
        
    screen_captured = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))
    mask = Image.new('L', screen_captured.size, 50)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([0, 0, x_end - x_start, y_end - y_start], fill=255)
    alpha = Image.new('L', screen_captured.size, 100)
    alpha.paste(mask, (0, 0), mask=mask)

    img = Image.composite(screen_captured, Image.new('RGB', screen_captured.size, 'white'), alpha)

    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(x_start, y_start, image=img_tk, anchor=tk.NW)  # Ajuste aqui
    canvas.img_tk = img_tk

def on_click(event):
    global x_start, y_start, drawing

    x_start, y_start = event.x_root, event.y_root
    drawing = True

def finalizar_programa(entry, lista, item):
    global x_start, y_start, x_end, y_end, captured_image_window
    x1, y1 = min(x_start, x_end), min(y_start, y_end)
    x2, y2 = max(x_start, x_end), max(y_start, y_end)
    width = x2 - x1
    height = y2 - y1
    value = {
        'left': x1,
        'top': y1,
        'width': width,
        'height': height
    }
    print(value)
    if lista == lista_catch:
        root.destroy()
        img = pyautogui.screenshot(region=(x1, y1, width, height))
        nome_arquivo = f"{item}_{int(time.time())}.png"
        caminho_arquivo = os.path.join("catch", nome_arquivo)
        img.save(caminho_arquivo)
        room.after(0, lambda: adicionar_item_lista(entry, lista, item, caminho_arquivo))
    
    if lista == lista_target:
        root.destroy()
        img = pyautogui.screenshot(region=(x1, y1, width, height))
        nome_arquivo = f"{item}_{int(time.time())}.png"
        caminho_arquivo = os.path.join("target", nome_arquivo)
        img.save(caminho_arquivo)
        room.after(0, lambda: adicionar_item_lista(entry, lista, item, caminho_arquivo))

def on_release(event, entry, lista, item):
    global drawing

    drawing = False
    finalizar_programa(entry, lista, item)

def inicia_captura(entry, lista, item):
    if lista == lista_catch:
        messagebox.showinfo(title='Play Pokeball', message='Take a screenshot of the fainted Pokemon you want to capture (Does not capture an image of the environment)')
    if lista == lista_target:
        messagebox.showinfo(title='Attack pokemon', message='Capture the name of the pokemon in your battle.')
    global canvas
    global root
    root = tk.Toplevel(room)
    root.overrideredirect(True) 
    root.attributes('-topmost', True) 
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) 
    root.attributes('-alpha', 0.5) 

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),  highlightthickness=0)
    canvas.pack()
    canvas.bind("<B1-Motion>", on_move)
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<ButtonRelease-1>", lambda event, entry=entry, lista=lista, item=item: on_release(event,entry, lista, item))
    

def carregar_item_do_json(lista, item): 
    if lista == lista_catch:
        caminho_arquivo_json = os.path.join("text_catch", f"{item}.json")
        with open(caminho_arquivo_json, "r") as arquivo_json:
            configuracao = json.load(arquivo_json)
            caminho_arquivo = configuracao["caminho_arquivo"]
        constantes.itens_catch.append({'nome': item, 'caminho': caminho_arquivo, 'caminho_json': f"{item}.json"})

        lista.insert(tk.END, item)
        constantes.caminhos_arquivos_catch.append(caminho_arquivo)
    if lista == lista_target:
        caminho_arquivo_json = os.path.join("text_target", f"{item}.json")
        with open(caminho_arquivo_json, "r") as arquivo_json:
            configuracao = json.load(arquivo_json)
            caminho_arquivo = configuracao["caminho_arquivo"]
        constantes.itens_target.append({'nome': item, 'caminho': caminho_arquivo, 'caminho_json': f"{item}.json"})
        lista.insert(tk.END, item)
        constantes.caminhos_arquivos_target.append(caminho_arquivo)

    if lista == lista_spell:
        caminho_arquivo_json = os.path.join("spells", f"{item}.json")
        with open(caminho_arquivo_json, "r") as arquivo_json:
            configuracao = json.load(arquivo_json)
            spell_arquivo = configuracao["spell"]
        constantes.itens_spells.append({'nome': item, 'spell': spell_arquivo, 'caminho_json': f"{item}.json"})
        constantes.spells.append(spell_arquivo)
        lista.insert(tk.END, item)
        print(constantes.itens_spells)
        print(constantes.spells)

    if lista == lista_spell_backup:
        caminho_arquivo_json = os.path.join("spells", f"{item}.json")
        with open(caminho_arquivo_json, "r") as arquivo_json:
            configuracao = json.load(arquivo_json)
            spell_arquivo_backup = configuracao["spell"]
        constantes.itens_spells_backup.append({'nome': item, 'spell_backup': spell_arquivo_backup, 'caminho_json': f"{item}.json"})
        constantes.spells_backup.append(spell_arquivo_backup)
        print(constantes.itens_spells_backup)
        print(constantes.spells_backup)
        lista.insert(tk.END, item)

def carregar_do_json(lista):
    if lista == lista_catch:
        arquivo_json = filedialog.askopenfilename(initialdir="text_catch", title="Select file",
                                                filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        if arquivo_json:
            nome_item = os.path.splitext(os.path.basename(arquivo_json))[0]
            carregar_item_do_json(lista, nome_item)

    if lista == lista_target:
        arquivo_json = filedialog.askopenfilename(initialdir="text_target", title="Select file",
                                                filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        if arquivo_json:
            nome_item = os.path.splitext(os.path.basename(arquivo_json))[0]
            carregar_item_do_json(lista, nome_item)
    
    if lista == lista_spell:
        arquivo_json = filedialog.askopenfilename(initialdir="spells", title="Select file",
                                                filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        if arquivo_json:
            nome_item = os.path.splitext(os.path.basename(arquivo_json))[0]
            carregar_item_do_json(lista, nome_item)
    
    if lista == lista_spell_backup:
        arquivo_json = filedialog.askopenfilename(initialdir="spells", title="Select file",
                                                filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        if arquivo_json:
            nome_item = os.path.splitext(os.path.basename(arquivo_json))[0]
            carregar_item_do_json(lista, nome_item)

def Life():
    sair = True
    global rgb
    global life_pos
    global x_heal
    global y_heal
    global lbl_life_pos
    global lbl_cor
    if lbl_life_pos and lbl_cor is not None:
        lbl_life_pos.destroy()
        lbl_cor.destroy()
    messagebox.showinfo(title='Life Position', message='Position the mouse cursor on the pokemons life bar and click the "insert" key')
    while sair:
        if is_pressed('insert'):
            x_heal_pos,y_heal_pos = pyautogui.position()
            rgb = pyautogui.screenshot().getpixel((x_heal_pos,y_heal_pos))
            x_heal = x_heal_pos
            y_heal = y_heal_pos   
            messagebox.showinfo(title='Life Result', message=f'X: {x_heal} | Y: {y_heal} - RGB: {rgb}')
            life_pos = [x_heal, y_heal]
            lbl_life_pos = generate_widget(Label, row=3, column=0, stick='w', text=f"X: {x_heal} | Y: {y_heal}", font=constantes.form_text)
            lbl_cor = generate_widget(Label, row=4, column=0, stick='w', text=f"Color: {rgb}", font=constantes.form_text)
            sair = False
            break

def heal_poke(checkbutton_id):
    global life_pos
    global heal
    global data
    global rgb
    estado = constantes.checkbutton_vars[checkbutton_id].get()
    if estado:
        if checkbutton_id == 2:
            if life_pos is not None:
                x_heal = life_pos[0]
                y_heal = life_pos[1]
                if pyautogui.pixelMatchesColor(x_heal, y_heal, tuple(rgb)):
                    if heal != 'Off':
                        my_keyboard.press(heal)

def Potion_poke(checkbutton_id):
    global life_pos
    global potion
    global data
    global rgb
    sair = 0
    estado = constantes.checkbutton_vars[checkbutton_id].get()
    if estado:
        if checkbutton_id == 3:
            while not myevent.is_set():
                if life_pos is not None:
                    x_heal = life_pos[0]
                    y_heal = life_pos[1]
                    if pyautogui.pixelMatchesColor(x_heal, y_heal, tuple(rgb)):
                        if potion != 'Off':
                            my_keyboard.press(potion)
                            pyautogui.moveTo(x_heal,y_heal,0.5)
                            pyautogui.click()
                    else:
                        sair = 1
                if sair == 1:
                    break
                if isinstance(constantes.time_potion, int):
                    print (f'tempo de espera começou: {constantes.time_potion}')
                    sleep(constantes.time_potion) 

            
def time_potion():
    global lbl_potion_time
    constantes.time_potion = entry_potion.get()
    if constantes.time_potion.isdigit():
        constantes.time_potion = int(constantes.time_potion)
        lbl_potion_time.destroy()
        lbl_potion_time = generate_widget(Label, row=3, column=3, stick='S', text=f"{constantes.time_potion} seconds", font=constantes.form_text)
        entry_potion.delete(0, tk.END)
    else:
        messagebox.showinfo(title='Wait Potion', message='The waiting time must be an integer')
        lbl_potion_time.destroy()
        lbl_potion_time = generate_widget(Label, row=3, column=3, stick='S', text=f"{constantes.time_potion} seconds", font=constantes.form_text)
        entry_potion.delete(0, tk.END)

def on_scale_change(value):
    label_var.set(f"Valor: {(int(float(value))/10)}")
    constantes.var_minigame = (int(float(value))/10)


btn_salvar = generate_widget(Button, row=0, column=1, padx= 35, text="Save", command=save)
btn_carregar = generate_widget(Button, row=1, column=1, padx= 35, text="Load file", command=Load_window)
btn_iniciar = generate_widget(Button, row=0, column=0, padx= 35, text="Start bot (F11)", command=start)
btn_salvar_arquivo = generate_widget(Button, row=1, column=0, padx= 35, text="Save file", command=save_file)
btn_Life = generate_widget(Button, row=6, column=0, padx= 35, text="Life Position", command=Life)

lbl_life_pos = generate_widget(Label, row=4, column=0, stick='s', text=f"X: {x_heal} | Y: {y_heal}", font=constantes.form_text)
lbl_cor = generate_widget(Label, row=5, column=0, stick='n', text=f"Color: {rgb}", font=constantes.form_text)

lbl_love = generate_widget(Label, row=0, column=2, stick='w', text="Hotkey love", font=constantes.form_text)
cbx_love = generate_widget(Combobox, row=1, column=2, values= constantes.Hotkey, state = 'readonly', font=constantes.form_text, width=12)

lbl_loot = generate_widget(Label, row=0, column=3, stick='w', text="Hotkey loot", font=constantes.form_text)
cbx_loot = generate_widget(Combobox, row=1, column=3, values= constantes.Hotkey, state = 'readonly', font=constantes.form_text, width=12)

lbl_road = generate_widget(Label, row=0, column=4, stick='w', text="Hotkey road", font=constantes.form_text)
cbx_road = generate_widget(Combobox, row=1, column=4, values= constantes.Hotkey, state = 'readonly', font=constantes.form_text, width=12)

lbl_ball = generate_widget(Label, row=0, column=5, stick='w', text="Hotkey Pokeball", font=constantes.form_text)
cbx_ball = generate_widget(Combobox, row=1, column=5, values= constantes.Hotkey, state = 'readonly', font=constantes.form_text, width=12)

lbl_life = generate_widget(Label, row=5, column=1, stick='S', text="Hotkey spell heal", font=constantes.form_text)
cbx_life = generate_widget(Combobox, row=6, column=1, values= constantes.Hotkey_heal, state = 'readonly', font=constantes.form_text, width=12)

lbl_potion = generate_widget(Label, row=5, column=2, stick='S', text="Hotkey Potion", font=constantes.form_text)
cbx_potion = generate_widget(Combobox, row=6, column=2, values= constantes.Hotkey, state = 'readonly', font=constantes.form_text, width=12)

entry_potion=tk.Entry(room)
entry_potion.grid(row=5, column=3, columnspan=1, pady=5)
lbl_potion_time = generate_widget(Label, row=4, column=3, stick='S', text=f"{constantes.time_potion} seconds", font=constantes.form_text)
btn_potion = generate_widget(Button, row=6, column=3, padx= 25, text="Wait Potion", command=time_potion)

def adicionar_lista(frame, lista, entry, row, column):
    frame.grid(row=row, column=column, columnspan=2, pady=5)  
    lista.grid(row=0, column=0, columnspan=2, pady=5)
    entry.grid(row=1, column=0, columnspan=2, pady=5)

def adicionar_lista_spell(frame, lista, row, column):
    frame.grid(row=row, column=column, columnspan=2, pady=5)  
    lista.grid(row=0, column=0, columnspan=2, pady=5)

frame_catch = tk.Frame(room)
lista_catch = tk.Listbox(frame_catch)
entry_catch = tk.Entry(frame_catch)

lbl_target = generate_widget(Label, row=7, column=0, stick='S', columnspan=2, text="Catch Pokémon", font=constantes.form_text)
adicionar_lista(frame_catch, lista_catch, entry_catch, row=8, column=0)

btn_adicionar_catch = generate_widget(Button, row=10, column=0, stick="E", text="Add", command=lambda: adicionar_item(entry_catch,lista_catch))
btn_remover_catch = generate_widget(Button, row=10, column=1, stick="W", text="Remove", command=lambda: remover_item(lista_catch))
btn_buscar_catch = generate_widget(Button, row=11, column=0, stick='S', columnspan=2, text="Load", command=lambda: carregar_do_json(lista_catch))

frame_target = tk.Frame(room)
lista_target = tk.Listbox(frame_target)
entry_target = tk.Entry(frame_target)

lbl_target = generate_widget(Label, row=7, column=2, stick='S', columnspan=2, text="Target Pokémon", font=constantes.form_text)
adicionar_lista(frame_target, lista_target, entry_target, row=8, column=2)

btn_adicionar_target = generate_widget(Button, row=10, column=2, stick="E", text="Add", command=lambda: adicionar_item(entry_target,lista_target))
btn_remover_target = generate_widget(Button, row=10, column=3, stick="W", text="Remove", command=lambda: remover_item(lista_target))
btn_buscar_target = generate_widget(Button, row=11, column=2, stick='S', columnspan=2, text="Load", command=lambda: carregar_do_json(lista_target))

frame_spell = tk.Frame(room)
lista_spell = tk.Listbox(frame_spell)

generate_checkbutton('If the target does not die', row=7, column=6, columnspan=2)
generate_checkbutton('Delay between spells (2s)', row=7, column=4, columnspan=2)
generate_checkbutton('Activate spell heal', row=4, column=1)
generate_checkbutton('Activate Potion', row=4, column=2)

lbl_target = generate_widget(Label, row=8, column=4, stick='N', columnspan=2, text="Spell Pokémon", font=constantes.form_text)
adicionar_lista_spell(frame_spell, lista_spell, row=8, column=4)

btn_remover_spell = generate_widget(Button, row=11, column=4, stick='S', columnspan=2, text="Remove", command=lambda: remover_item(lista_spell))
btn_buscar_spell = generate_widget(Button, row=10, column=4, stick='S', columnspan=2, text="Load", command=lambda: carregar_do_json(lista_spell))


frame_spell_backup = tk.Frame(room)
lista_spell_backup = tk.Listbox(frame_spell_backup)

label_backup = generate_widget(Label, row=8, column=6, stick='N', columnspan=2, text="Spell Backup", font=constantes.form_text)
adicionar_lista_spell(frame_spell_backup, lista_spell_backup, row=8, column=6)

generate_widget(Button, row=11, column=6, stick='S', columnspan=2, text="Remove", command=lambda: remover_item(lista_spell_backup))
generate_widget(Button, row=10, column=6, stick='S', columnspan=2, text="Load", command=lambda: carregar_do_json(lista_spell_backup))

lbl_minigame = generate_widget(Label, row=4, column=5, stick='N', columnspan=1, text="Minigame sensitivity", font=constantes.form_text)
scale = Scale(from_=0, to=10, variable=scale_var, orient="horizontal", command=on_scale_change)
scale.grid(row=4, column=5, sticky='W', padx=20, pady=30)

label_var.set("Valor: 0")

label = Label(textvariable=label_var)
label.grid(row=4, column=5, sticky='S', pady=10)

empty_label = generate_widget(Label, row=15, column=0, stick='N', text="")
btn_iniciar['command'] = lambda: (start(), empty_label.focus_set())
room.protocol("WM_DELETE_WINDOW", close_window)


def spell_backup():
    with open('spells.json', 'r') as file:
        data = json.loads(file.read())
    for item_data in data.get("itens_spell", []):
        nome_item = item_data.get("nome")
        spell_arquivo_backup = item_data.get("spell")
        caminho_json = item_data.get("caminho_json")

        if nome_item and spell_arquivo_backup and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_spells_backup]:
                constantes.itens_spells_backup.append({'nome': nome_item, 'spell_backup': spell_arquivo_backup, 'caminho_json': caminho_json})
                lista_spell_backup.insert(tk.END, nome_item)
                constantes.spells_backup.append(spell_arquivo_backup)

def spells_defalt():
    with open('spells.json', 'r') as file:
        data = json.loads(file.read())
    for item_data in data.get("itens_spell", []):
        nome_item = item_data.get("nome")
        spell_arquivo = item_data.get("spell")
        caminho_json = item_data.get("caminho_json")

        if nome_item and spell_arquivo and caminho_json:
            if nome_item not in [item.get("nome") for item in constantes.itens_spells]:
                constantes.itens_spells.append({'nome': nome_item, 'spell': spell_arquivo, 'caminho_json': caminho_json})
                lista_spell.insert(tk.END, nome_item)
                constantes.spells.append(spell_arquivo)
    return data

spells_defalt()
spell_backup()


cbx_loot.current(0)
cbx_love.current(0)
cbx_road.current(0)
cbx_ball.current(0)
cbx_life.current(0)
cbx_potion.current(0)
room.mainloop()