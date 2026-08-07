# Auto Clicker para Linux — v0.7.0

Auto Clicker com suporte a **X11** e **Wayland**, interface GTK4 e atalho global de teclado.

---

## Destaques desta versão

### 🎯 Clicker finalmente funciona no Wayland

Esta versão corrige uma cadeia de bugs que travava o clique no Wayland em 0 cliques/segundo:

- **`ydotool` vendorizado** (`vendor/ydotool/`), compilado do source — o binário do snap tinha overhead alto por chamada e era a causa do travamento;
- **`ydotoold` com auto-start**: o daemon agora sobe automaticamente na primeira tentativa de clique, detectando e limpando sockets órfãos;
- **Correção do caminho de socket** entre cliente e daemon;
- **Mapa de botões corrigido**: o `ydotool` espera códigos hexadecimais de tecla-mouse (`0xC0` = esquerdo, `0xC1` = direito, `0xC2` = meio), não decimais;
- **Erros reais não são mais engolidos** (removido `stderr=DEVNULL`);
- **`--repeat`/`--next-delay` removidos**, pois não existem na versão de `ydotool` disponível.

**Resultado:** clique estável no Wayland, ~14 cliques/segundo pela interface gráfica.

---

## Mudanças

### Correções
- Clicker no Wayland não funcionava de fato (múltiplos bugs em cadeia) — corrigido
- Mapa de botões do mouse para o `ydotool` (hexadecimal)
- Mismatch de caminho de socket entre cliente e daemon
- Daemon `ydotoold` agora inicia automaticamente e limpa sockets órfãos
- Testes sem travamento (`test_clicker.py` não fica mais pendurado)
- UI atualiza imediatamente ao parar o clicker
- Modo infinito (quantidade = 0) agora persiste no Wayland

### Empacotamento
- Scripts de build para `.deb`, `.rpm` e binário standalone (`scripts/`)
- `pyinstaller` e dependências adicionados ao `requirements.txt`
- Config migrada para `~/.config/autoclicker/config.json` (XDG Base Directory), com migração automática de configs legados

---

## Instalação

Baixe os artefatos da release:

- **`.deb`** (Debian / Ubuntu / Pop!_OS):
  ```bash
  sudo dpkg -i autoclicker_*.deb && sudo apt-get install -f
  ```
- **`.rpm`** (Fedora / RHEL / openSUSE):
  ```bash
  sudo rpm -i autoclicker-*.rpm
  ```
- **Binário standalone** (qualquer distro):
  ```bash
  tar -xzf autoclicker-linux-*-standalone.tar.gz && ./autoclicker/install.sh
  ```

> **Wayland:** o `ydotoold` precisa acessar `/dev/uinput`. Crie a regra udev e adicione seu usuário ao grupo `input` (veja o README, seção *Permissão de input (Wayland)*). No X11 isso não é necessário.

---

## Compatibilidade

Testado em:

- Pop!_OS 24.04 LTS (GNOME X11 / COSMIC Wayland)
- Fedora 44 (GNOME Wayland)

---

## Notas / Em progresso

- Rebranding para **JCL Clicker** em andamento (nome ainda não aplicado ao `app_id`, pacotes e ícone)
- AppImage ainda não disponível
- Redesenho visual da GUI e bandeja do sistema nos próximos passos
