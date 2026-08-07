AutoClicker-Linux
=================

Automação de cliques de mouse para Linux com suporte a X11 e Wayland.

Arquivos incluídos
------------------
  autoclicker          Binário standalone (não requer Python instalado)
  icon.png             Ícone do aplicativo (256x256)
  autoclicker.desktop   Arquivo .desktop para integração com o menu do sistema
  install.sh           Script de instalação automática
  README.txt           Este arquivo

Instalação automática
---------------------
  ./install.sh

O script instala o aplicativo em ~/.local/opt/autoclicker/ e registra
o .desktop no diretório do usuário.

Instalação manual
-----------------
  1. Copie os arquivos para um diretório de sua preferência:

     mkdir -p ~/.local/opt/autoclicker
     cp autoclicker icon.png ~/.local/opt/autoclicker/
     chmod +x ~/.local/opt/autoclicker/autoclicker

  2. Instale o .desktop:

     mkdir -p ~/.local/share/applications
     sed 's|/opt/autoclicker|$HOME/.local/opt/autoclicker|g' \
         autoclicker.desktop > ~/.local/share/applications/autoclicker.desktop
     chmod +x ~/.local/share/applications/autoclicker.desktop
     update-desktop-database ~/.local/share/applications 2>/dev/null

Desinstalação
-------------
  rm -rf ~/.local/opt/autoclicker
  rm ~/.local/share/applications/autoclicker.desktop
  update-desktop-database ~/.local/share/applications 2>/dev/null

Arquivo de configuração
-----------------------
As preferências são salvas em:

  ~/.config/autoclicker/config.json

Repositório
-----------
  https://github.com/JotinhaGamer22/AutoClicker-Linux

Licença
-------
Projeto open source. Veja o repositório para mais detalhes.
