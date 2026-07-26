# AutoClicker-Linux

Auto Clicker para Linux com suporte a X11 e Wayland.

O objetivo do projeto é criar um Auto Clicker nativo para Linux com interface gráfica, compatível com ambientes modernos como GNOME X11 e Wayland (COSMIC).

---

## Status

🚧 Em desenvolvimento

Versão atual: **v0.3**

---

# Recursos atuais

✅ Controle de mouse no X11 usando `pynput`
✅ Controle de mouse no Wayland usando `ydotool`
✅ Detecção automática da sessão gráfica
✅ Motor de cliques utilizando threads
✅ Controle de quantidade de cliques
✅ Controle de intervalo entre cliques
✅ Sistema de callbacks para eventos
✅ Gerenciamento de estados do AutoClicker

---

# Arquitetura

O projeto é dividido em camadas:

```text
AutoClicker-Linux

main.py
   |
   v
gui.py              (interface gráfica futura)
   |
   v
clicker.py          (motor de automação)
   |
   v
mouse.py            (controle do mouse)
   |
   +----------------+
   |                |
  X11            Wayland
pynput           ydotool
```

---

# Sistema de Estados

O AutoClicker utiliza estados para controlar o ciclo de execução:

```text
                 IDLE
                  |
              start()
                  |
                  v
              RUNNING
             /       \
            /         \
       quantidade      stop()
        acabou          |
          |             |
          v             v
      FINISHED       STOPPED
```

## Estados

### IDLE

Estado inicial.

O AutoClicker foi criado, mas ainda não começou a executar.

---

### RUNNING

O programa está executando os cliques automaticamente.

---

### FINISHED

Ocorre quando o AutoClicker termina a execução normalmente.

Exemplo:

* Usuário define 100 cliques
* O programa realiza todos os cliques
* Estado muda para `FINISHED`

---

### STOPPED

Ocorre quando a execução é interrompida manualmente.

Exemplo:

* Usuário inicia o AutoClicker
* Usuário utiliza o comando parar
* Estado muda para `STOPPED`

---

# Tecnologias

* Python 3
* Threading
* pynput
* ydotool
* Git
* GTK4 (planejado)

---

# Compatibilidade

Testado inicialmente em:

* Pop!_OS 24.04 LTS
* GNOME X11
* COSMIC Wayland

---

# Estrutura atual

```text
AutoClicker-Linux

├── main.py
├── gui.py
├── clicker.py
├── mouse.py
├── state.py
├── config.py
├── teste_clicker.py
└── teste_stop.py
```

---

# Próximos passos

* Sistema de configuração persistente (`config.json`)
* Interface gráfica GTK4/Libadwaita
* Botão iniciar/parar
* Configuração de intervalo
* Quantidade de cliques pela interface
* Atalhos de teclado
* Melhorias de acessibilidade
* Pacote `.deb`
* AppImage
* Testes automatizados

---

# Desenvolvimento

O projeto utiliza branches para organização:

* `main` → versões estáveis
* `develop` → desenvolvimento e novos recursos

---

## Licença

Projeto em desenvolvimento.
