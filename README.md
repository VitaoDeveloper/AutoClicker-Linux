Auto Clicker para Linux com suporte a X11 e Wayland.

Projeto desenvolvido em Python com foco em compatibilidade com diferentes ambientes gráficos Linux.

---

## Status

🚧 Em desenvolvimento

Versão atual: **v0.7.0**

---

## Changelog

### v0.7.0

- **Corrigido:** clicker no Wayland não funcionava de fato (vários bugs em cadeia)
  - `--repeat`/`--next-delay` não existiam na versão de `ydotool` disponível
  - Erro real estava sendo engolido por `stderr=DEVNULL`
  - Binário `ydotool` do snap tinha overhead alto por chamada — agora **vendorizado** (compilado do source) em `vendor/ydotool/`
  - Mismatch de caminho de socket entre cliente e daemon
  - `ydotoold` agora sobe **automaticamente**, detectando e limpando sockets órfãos
  - Mapa de botão do mouse corrigido: `ydotool` espera códigos hexadecimais de tecla-mouse (`0xC0`=esquerdo, `0xC1`=direito, `0xC2`=meio), não números decimais simples
- Resultado: clique estável no Wayland, ~14 cliques/segundo pela interface gráfica (antes: travado em 0)

### v0.6.0 e anteriores

- Base funcional com suporte X11/Wayland, interface GTK4, atalho global de teclado

---

## Recursos atuais

✅ Controle de mouse no X11 usando `pynput`  
✅ Controle de mouse no Wayland usando `ydotool` (binário vendorizado, com auto-start do daemon)  
✅ Detecção automática da sessão gráfica  
✅ Motor de cliques independente da interface gráfica  
✅ Sistema de callbacks para eventos  
✅ Controle de estados do programa  
✅ Configuração salva em `~/.config/autoclicker/config.json` (XDG)  
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
- Wayland → `ydotool` (binário vendorizado em `vendor/ydotool/`, com daemon `ydotoold` iniciado automaticamente quando necessário)

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
- Gerenciar o arquivo de configuração
- Migrar config de caminhos legados para o diretório XDG

O arquivo de configuração é armazenado em `~/.config/autoclicker/config.json` (seguindo a XDG Base Directory Specification).

---

# Estrutura do projeto

```
JCL-Clicker

├── app/
│   ├── __init__.py
│   ├── clicker.py
│   ├── config.py
│   ├── gui.py
│   ├── main.py
│   ├── mouse.py
│   └── state.py
│
├── vendor/
│   └── ydotool/
│       ├── ydotool                  (cliente, compilado do source)
│       └── ydotoold                 (daemon, compilado do source)
│
├── packaging/
│   ├── autoclicker.desktop
│   ├── postinst.sh
│   ├── icons/
│   │   └── autoclicker.png          (256x256, a ser adicionado)
│   └── standalone/
│       ├── autoclicker.desktop
│       └── install.sh
│
├── scripts/
│   ├── build-packages.sh            (.deb / .rpm)
│   └── build-standalone.sh          (binário standalone + tar.gz)
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
| ydotool | **vendorizado** (`vendor/ydotool/`) | Controle de mouse no Wayland |

---

# Compatibilidade

Testado em:

- Pop!_OS 24.04 LTS (GNOME X11 / COSMIC Wayland)
- Fedora 44 (GNOME Wayland)

---

# Instalação

O JCL Clicker pode ser instalado de três formas: pacote `.deb`, pacote `.rpm` ou binário standalone.

## Via pacote `.deb` (Debian / Ubuntu / Pop!_OS)

Baixe o arquivo `.deb` da release e instale:

```bash
sudo dpkg -i jcl-clicker_*.deb
sudo apt-get install -f   # resolve dependências, se necessário
```

## Via pacote `.rpm` (Fedora / RHEL / openSUSE)

Baixe o arquivo `.rpm` da release e instale:

```bash
sudo rpm -i jcl-clicker-*.rpm
```

## AppImage (qualquer distro)

> 🚧 Ainda não disponível — nos planos, ver [Próximos passos](#próximos-passos).

## Binário standalone (qualquer distro)

Baixe o arquivo `jcl-clicker-linux-*-standalone.tar.gz` da release e extraia:

```bash
tar -xzf jcl-clicker-linux-*-standalone.tar.gz -C /tmp/
cd /tmp/jcl-clicker
chmod +x install.sh
./install.sh
```

## A partir do código-fonte (desenvolvimento)

### 1. Clone o projeto

```bash
git clone https://github.com/JotinhaGamer22/AutoClicker-Linux.git
cd AutoClicker-Linux
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
```

### 3. Instale as dependências Python (pip)

```bash
pip install -r requirements.txt
```

### 4. Instale as dependências do sistema

O projeto depende de pacotes que **não são instaláveis via pip**: os bindings do GTK4 (interface gráfica). O `ydotool`/`ydotoold` já vêm vendorizados no repositório (`vendor/ydotool/`), não precisa instalar separadamente.

<details>
<summary><b>Ubuntu / Pop!_OS / Debian</b></summary>

```bash
sudo apt install python3-gi gir1.2-gtk-4.0
```

</details>

<details>
<summary><b>Fedora</b></summary>

```bash
sudo dnf install python3-gobject gtk4
```

</details>

<details>
<summary><b>Arch Linux / Manjaro</b></summary>

```bash
sudo pacman -S python-gobject gtk4
```

</details>

<details>
<summary><b>openSUSE</b></summary>

```bash
sudo zypper install python3-gobject gtk4
```

</details>

### 5. Permissão de input (Wayland)

Se você usa Wayland, o `ydotoold` precisa acessar `/dev/uinput`. Crie a regra `udev` e adicione seu usuário ao grupo `input`:

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/80-uinput.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -aG input $USER
```

Faça **logout/login** (ou reinicie) para a mudança de grupo ter efeito.

> **Nota:** No X11 essa etapa não é necessária.

---

## Localização do arquivo de configuração

As preferências são salvas em `~/.config/autoclicker/config.json`, seguindo a XDG Base Directory Specification.

Se existir um `config.json` ao lado do executável (versão antiga), ele será migrado automaticamente para o novo local na primeira execução.

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

## Clicker "roda" mas não clica em nada no Wayland

Verifique se o socket do `ydotoold` está de fato aceitando conexões e não é um arquivo órfão:

```bash
rm -f /tmp/.ydotool_socket
python3 -m app.main
```

O app sobe o daemon vendorizado automaticamente na primeira tentativa de clique.

---

# Próximos passos

## Rebranding (em andamento)

- [x] Escolher novo nome: **JCL Clicker** (J = Jônatas, C = Corinthians, L = Linux)
- [ ] Atualizar `app_id` do GTK, `APP_NAME` do config, nome de pacote no `build-packages.sh`, `.desktop`, ícone
- [ ] Renomear repositório no GitHub

## Interface gráfica

- [ ] Redesenho visual da GUI (estilo próprio, além do GTK4 padrão)
- [ ] Ícone na bandeja do sistema

## Empacotamento

- [ ] Gerar `.deb` (script já existe em `scripts/build-packages.sh`, precisa atualizar nome/versão)
- [ ] Gerar `.rpm`
- [ ] AppImage

## Funcionalidades

- [ ] Perfis de configuração

---

# Atalho global de teclado

O atalho funciona mesmo com a janela sem foco:

- **X11** → via `pynput`
- **Wayland** → leitura direta dos dispositivos em `/dev/input` via `evdev` (o Wayland não permite escuta global de teclado por questões de segurança, então essa é a forma de contornar)

Veja a seção [5. Permissão de input (Wayland)](#5-permissão-de-input-wayland) nas instruções de instalação para configurar os direitos de acesso.

---

# Licença

Projeto em desenvolvimento.