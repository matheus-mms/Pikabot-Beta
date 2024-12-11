# Introdução
Esse software se trata de uma versão beta para automatizar algumas funções relacionadas a pesca no jogo do PokexGames, por se tratar de uma versão beta o bot pode não funcionar corretamente atualmente, sendo necessário ajustar o código no arquivo "Beta.py".

Utilizando bibliotecas como a Pyautogui para as capturas de tela, e a importando o arquivo "my_keyboard" que utiliza a API do windows para gerar cliques e movimento do mouse, foi possível automatiza ações como a de pescar, atacar os pokemons que aparecem na aba de battle, curar o pokemon usando as potions, entre outras.

# Configurações
No repositório possui o executável onde ao abri-lo será disponível a interface gráfica onde será realizado a configuração dos parâmetros para o Bot funcionar dentro do jogo. Segue abaixo imagem da Interface gráfica:
![Interface grafica da versão Beta](https://i.postimg.cc/g0Gw5Tm6/Captura-de-tela-2024-12-10-132148.png)

### Hotkeys
Nos combobox da imagem abaixo serão configurados em qual tecla será utilizado a função de "Love" para agradar o pokemon, a tecla para coletar os recursos do pokemon abatido, a tecla para usar a vara de pescar na água e a tecla para usar a pokebola para capturar os pokemons abatidos.

![Hotkey](https://i.postimg.cc/jj9hbT5F/Hotkeys.png)

### Heal
Nessas opções serão configurados as opções para healar o pokemon, o botão "Life position" será utilizado para configurar a posição e cor do pixel da vida de seu pokemon no battle para utilizar as potions ou habilidades quando o pixel atingir as condições (O recomendado é deixar o pixel "cinza" quando fica sem a cor da barra de vida nesse ponto). Após isso nos campos seguinte você pode usar os checkbuttons para ativar para usar uma habilidade de cura caso o pokemon possua, e colocar em qual tecla essa habilidade está pelo combobox, o mesmo para a opções ao lado só que essa seria para o uso de potions. A opção "wait potion" é o tempo que será aguardado após o uso da potion antes de iniciar a pesca novamente.

![Heal](https://i.postimg.cc/PJsPDgS5/Life.png)


### Minigame
Nesse Scale do minigame será usado para configurar a sensibilidade para que os elementos do minigame sejam reconhecidos corretamente em seu monitor.

![minigame](https://i.postimg.cc/VLFp3jQ7/minigame.png)

### Catch
Essa é a lista de pokemons você vai configurar para jogar as pokebolas para capturar. No Entry coloque o nome do pokemon ou o nome que preferir, ao clicar em "ADD" você vai tirar print de uma parte do pokemon abatido sem capturar elementos do mapa, em seguida ao print vai aparecer o pokemon na lista com o nome que você inseriu no entry. A opção "Remove" é para retirar esse pokemon da lista, e a opção "Load" abre uma janela na pasta onde ficou salvo um arquivo Json que pode ser selecionado para inserir esse pokemon na lista novamente sem precisar refazer o processo com print.

![catch](https://i.postimg.cc/cCLw6yCt/catch.png)

### Target
Essa opção é a lista de pokemons para atacar na aba de battle do jogo, o entry as teclas "Add", "Remove" e "Load" fazem o mesmo que na lista de catch, porém nesse caso você deve tirar print do nome do pokemon no battle.

![Target](https://i.postimg.cc/rwx0VFjY/target.png)

### Lista de habilidades
A lista de spells pode ser vistas as opções de habilidades do jogo até o M12, você vai remover ou adicionar a lista essas habilidades conforme seu pokemon e como preferir, o checkbutton acima dela serve para aplicar um delay de 2s entre as habilidades se necessário. A lista de Spells Backup quando selecionado o checkbutton acima dela será ativada, nesse caso serve para colocar alguma habilidade para ser utilizada apenas se o pokemon não morrer com as habilidades da primeira lista (Por exemplo quando lurar um pokemon shiny).

![habilidades](https://i.postimg.cc/s20vKQgx/habilidades.png)

### Setup
Após realizado todas as configurações anteriores é necessário clicar na tecla "Save" para concluir a programação, a tecla "Save file" permite salvar um arquivo json com as configurações atuais, a tecla "Load file" permite ler um arquivo json para setar as programações, após ler as programações será necessário clicar na tecla "Save" para concluir também e por último a tecla "Start bot" que vai iniciar o bot. Existem teclas de atalho para iniciar e finalizar o bot sendo elas F11 inicia e F12 finalizar.

![Setup](https://i.postimg.cc/9fSQZ6Lq/Play.png)

# Considerações finais
Caso seja editado algum parametro no arquivo "Beta.py" esses parametros não vão ser consideradas no executavel. Nessa situação será necessario executar o arquivo através de alguma IDE como por exemplo o VS code com a extensão de Python, além disso será necessario instalar o Python e todas as dependencias e bibliotecas necessarias em sua maquina para conseguir executar o aquivo dessa forma.
