# AutoClicker-Linux

Auto Clicker para Linux com suporte a X11 e Wayland.

Projeto desenvolvido em Python com foco em compatibilidade com diferentes ambientes gráficos Linux.

---

## Status

🚧 Em desenvolvimento

Versão atual: **v0.4.1**

---

## Recursos atuais

✅ Controle de mouse no X11 usando `pynput`  
✅ Controle de mouse no Wayland usando `ydotool`  
✅ Detecção automática da sessão gráfica  
✅ Motor de cliques independente da interface gráfica  
✅ Sistema de callbacks para eventos  
✅ Controle de estados do programa  
✅ Configuração salva em JSON  
✅ Execução em thread separada  

---

# Arquitetura

O projeto foi dividido em módulos para facilitar manutenção e evolução.

## Motor principal

### `clicker.py`

Responsável pela lógica do AutoClicker:

- Controle do intervalo entre cliques
- Quantidade de cliques
- Execução em segundo plano
- Sistema de eventos
- Controle de iniciar/parar

---

## Controle do mouse

### `mouse.py`

Responsável pela comunicação com o sistema:

- X11 → `pynput`
- Wayland → `ydotool`

O programa detecta automaticamente qual sessão gráfica está sendo usada.

---

## Estados do programa

### `state.py`

Controle dos estados do AutoClicker:

```
        IDLE
          |
       start()
          |
          v
       RUNNING
       /     \
      /       \
FINISHED     STOPPED
```

Estados disponíveis:

- `IDLE` → aguardando iniciar
- `RUNNING` → executando cliques
- `FINISHED` → terminou a quantidade configurada
- `STOPPED` → interrompido pelo usuário

---

## Configurações

### `config.py`

Responsável por:

- Ler configurações
- Salvar configurações
- Gerenciar o arquivo `config.json`

---

# Estrutura do projeto

```
AutoClicker-Linux

├── app/
│   ├── __init__.py
│   ├── clicker.py
│   ├── config.py
│   ├── gui.py
│   ├── main.py
│   ├── mouse.py
│   └── state.py
│
├── tests/
│   ├── test_click.py
│   ├── test_clicker.py
│   ├── test_config.py
│   ├── test_mouse.py
│   ├── test_save_config.py
│   ├── test_stop.py
│   └── test_x11.py
│
├── config.json
├── README.md
└── requirements.txt
```

---

# Tecnologias

- Python 3
- pynput
- ydotool
- python-xlib
- GTK4 (planejado)

---

# Compatibilidade

Testado inicialmente em:

- Pop!_OS 24.04 LTS
- GNOME X11
- COSMIC Wayland

---

# Instalação

Clone o projeto:

```bash
git clone https://github.com/JotinhaGamer22/AutoClicker-Linux.git
```

Entre na pasta:

```bash
cd AutoClicker-Linux
```

Crie o ambiente virtual:

```bash
python3 -m venv venv
```

Ative:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Executando testes

Exemplo:

```bash
python3 -m tests.test_clicker
```

Outros testes:

```bash
python3 -m tests.test_config

python3 -m tests.test_stop

python3 -m tests.test_mouse
```

---

# Próximos passos

## Interface gráfica

- Interface GTK4
- Botões iniciar/parar
- Configuração de intervalo
- Seleção do botão do mouse

## Melhorias futuras

- Atalhos globais de teclado
- Perfis de configuração
- Ícone na bandeja do sistema
- Pacote `.deb`
- AppImage
- Testes automatizados com pytest

---

# Licença

Projeto em desenvolvimento.