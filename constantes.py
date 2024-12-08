import pyautogui
import json

largura_tela, altura_tela = pyautogui.size()
x1_regiao = (largura_tela - 200)
y1_regiao = 0
CONDICAO_TARGET = (x1_regiao, y1_regiao, 200, 250)

largura_tela1, altura_tela1 = pyautogui.size()
x_regiao1 = (largura_tela1 - 200)
y_regiao1 = 50
CONDICAO_SAIDA = (x_regiao1, y_regiao1, 150, 150)


largura_tela, altura_tela = pyautogui.size()
x_centro = (largura_tela - 80) // 2
y_centro = 0
MINIGAME_REGION = (x_centro, y_centro, 80, altura_tela)

largura_catch, altura_catch = pyautogui.size()
centro_catch= pyautogui.center((0, 0, largura_catch, altura_catch))
x_catch,y_catch = centro_catch

def normalizar_coordenadas(x, y, largura, altura, resolucao_base=(1920, 1080)):
    largura_monitor, altura_monitor = pyautogui.size()

    x_normalizado = int(x * (largura_monitor / resolucao_base[0]))
    y_normalizado = int(y * (altura_monitor / resolucao_base[1]))
    largura_normalizada = int(largura * (largura_monitor / resolucao_base[0]))
    altura_normalizada = int(altura * (altura_monitor / resolucao_base[1]))

    return x_normalizado, y_normalizado, largura_normalizada, altura_normalizada

#coordenadas_normalizadas = normalizar_coordenadas(*coordenadas_originais)
#x,y, largura, altura = coordenadas_normalizadas
#pyautogui.click(x,y)
coordenadas_normalizadas = normalizar_coordenadas(*(1727, 110, 181, 40))
x,y, largura, altura = coordenadas_normalizadas
LOCATION_TARGET = (x,y, largura, altura)

with open('default.json', 'r') as file:
    data = json.loads(file.read())
love = data['love']['value']
loot = data['loot']['value']
road = data['road']['value']
ball = data['ball']['value']

Hotkey = ['Off', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'TAB', 'CAPS']
Hotkey_heal = ['Off', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
form_text = ('Roboto', 12)

itens_catch = []
itens_target = []
itens_spells = []
spells = []
itens_spells_backup = []
spells_backup = []
caminhos_arquivos_catch = []
caminhos_arquivos_target = []
checkbutton_vars = []
time_potion = 0
var_minigame = 0
