# AutoClicker-Linux

Auto Clicker para Linux com suporte a X11 e Wayland.

## Status

🚧 Em desenvolvimento

## Recursos atuais

✅ Controle de mouse no X11 usando pynput  
✅ Controle de mouse no Wayland usando ydotool  
✅ Detecção da sessão gráfica  

## Tecnologias

- Python 3
- pynput
- ydotool
- GTK4 (planejado)

## Compatibilidade

Testado inicialmente em:

- Pop!_OS 24.04 LTS
- GNOME X11
- COSMIC Wayland

## Estrutura

- main.py
- gui.py
- clicker.py
- mouse.py
- config.py

## Próximos passos

- Interface gráfica GTK4
- Botão iniciar/parar
- Configuração de intervalo
- Atalhos de teclado
- Pacote .deb
- AppImage
