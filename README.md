# AutoClicker-Linux

Auto Clicker para Linux com suporte a X11 e Wayland.

Projeto desenvolvido em Python com foco em compatibilidade com diferentes ambientes gráficos Linux.

---

## Status

🚧 Em desenvolvimento

Versão atual: **v0.6.0**

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
✅ Interface gráfica em GTK4  
✅ Tratamento de erros (mouse indisponível, ydotool ausente, config corrompida)  
✅ Atalho global de teclado para iniciar/parar (F1-F12, Pause, Scroll Lock)  

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

| Dependência | Tipo | Finalidade |
|---|---|---|
| Python 3 | Runtime | Linguagem principal |
| pynput | pip | Controle de mouse/teclado no X11 |
| python-xlib | pip | Bindings X11 (dependência do pynput) |
| evdev | pip | Leitura de dispositivos de entrada no Wayland |
| six | pip | Compatibilidade Python 2/3 |
| GTK4 (PyGObject) | **sistema** | Interface gráfica |
| ydotool | **sistema** | Controle de mouse no Wayland |

---

# Compatibilidade

Testado em:

- Pop!_OS 24.04 LTS (GNOME X11 / COSMIC Wayland)
- Fedora 44 (GNOME Wayland)

---

# Instalação

## 1. Clone o projeto

```bash
git clone https://github.com/JotinhaGamer22/AutoClicker-Linux.git
cd AutoClicker-Linux
```

## 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instale as dependências Python (pip)

```bash
pip install -r requirements.txt
```

## 4. Instale as dependências do sistema

O projeto depende de pacotes que **não são instaláveis via pip**: os bindings do GTK4 (interface gráfica) e o `ydotool` (controle de mouse no Wayland). Escolha seu gerenciador de pacotes:

<details>
<summary><b>Ubuntu / Pop!_OS / Debian</b></summary>

```bash
sudo apt install python3-gi gir1.2-gtk-4.0 ydotool
sudo systemctl enable --now ydotool
```

</details>

<details>
<summary><b>Fedora</b></summary>

```bash
sudo dnf install python3-gobject gtk4 ydotool
sudo systemctl enable --now ydotool
```

</details>

<details>
<summary><b>Arch Linux / Manjaro</b></summary>

```bash
sudo pacman -S python-gobject gtk4 ydotool
sudo systemctl enable --now ydotool
```

</details>

<details>
<summary><b>openSUSE</b></summary>

```bash
sudo zypper install python3-gobject gtk4 ydotool
sudo systemctl enable --now ydotool
```

</details>

## 5. Permissão de input (Wayland)

Se você usa Wayland, o `evdev` precisa ler os dispositivos de entrada em `/dev/input`. Adicione seu usuário ao grupo `input`:

```bash
sudo usermod -aG input $USER
```

Faça **logout/login** para a mudança ter efeito.

> **Nota:** No X11 essa etapa não é necessária.

---

# Executando a interface gráfica

```bash
python3 -m app.main
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

# Troubleshooting

## `ModuleNotFoundError: No module named 'gi'`

O módulo `gi` (PyGObject) é um pacote do sistema, não é instalável via pip. Se o ambiente virtual não tem acesso aos pacotes do sistema, esse erro ocorre ao executar o programa.

**Solução:** Recrie o venv com a flag `--system-site-packages`:

```bash
rm -rf venv
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```

Ou, se o venv já existe, edite o arquivo `venv/pyvenv.cfg` e altere:

```
include-system-site-packages = false
```

para:

```
include-system-site-packages = true
```

---

# Próximos passos

## Melhorias futuras

- Perfis de configuração
- Ícone na bandeja do sistema
- Pacote `.deb`
- AppImage
- Testes automatizados com pytest

---

# Atalho global de teclado

O atalho funciona mesmo com a janela sem foco:

- **X11** → via `pynput`
- **Wayland** → leitura direta dos dispositivos em `/dev/input` via `evdev` (o Wayland não permite escuta global de teclado por questões de segurança, então essa é a forma de contornar)

Veja a seção [5. Permissão de input (Wayland)](#5-permissão-de-input-wayland) nas instruções de instalação para configurar os direitos de acesso.

---

# Licença

Projeto em desenvolvimento.