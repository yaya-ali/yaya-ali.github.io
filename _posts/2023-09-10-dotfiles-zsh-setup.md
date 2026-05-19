---
title: "My Dotfiles Setup — Fast Zsh, Lazy Loading, and a 0.23s Shell Start"
date: 2023-09-10 10:00:00 +0200
categories: [Dotfiles]
tags: [linux, zsh, dotfiles, productivity, terminal]
---

## The Problem

My zsh startup time had crept up to **4.4 seconds**. Every new terminal tab felt sluggish. The culprits: NVM, conda, and pyenv all initialising eagerly on every shell launch, even when I wasn't using them.

---

## The Fix: Lazy Loading

Instead of running `eval "$(nvm.sh)"` at startup, I replaced all three with stub functions that only initialise on first use:

```zsh
# NVM — load only when nvm/node/npm is first called
nvm() {
  unfunction nvm node npm npx
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
  nvm "$@"
}
node() { nvm; node "$@"; }
npm()  { nvm; npm "$@"; }
npx()  { nvm; npx "$@"; }
```

Same pattern for `conda` and `pyenv`. The shell now starts instantly and loads the tool on first call — the 200ms delay on first use is imperceptible in practice.

---

## Result

```bash
time zsh -i -c exit
# before: 4.4s
# after:  0.23s
```

**19× faster.**

---

## OMZ Plugin Diet

Removed every heavy plugin and kept only what I actually use:

```zsh
plugins=(
  git
  sudo
  fzf
  extract
  zsh-autosuggestions
  fast-syntax-highlighting
  zsh-history-substring-search
)
```

Plugins like `kubectl`, `docker`, and `command-not-found` each add 100–300ms. Removed them all.

---

## compinit Once

OMZ calls `compinit` internally. A second call in `.zshrc` was doubling completion init time. Added a 24-hour freshness check instead:

```zsh
autoload -Uz compinit
if [[ -n ${ZDOTDIR}/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi
```

---

## Secrets Management

API keys and tokens **never** go in `.zshrc`. They live in `~/.zshrc.private`, which is gitignored and sourced at the end:

```zsh
[ -f ~/.zshrc.private ] && source ~/.zshrc.private
```

---

## Full Dotfiles

My dotfiles are structured as:

```
dotfiles/
├── zsh/
│   ├── .zshrc        # main config
│   └── .zprofile     # brew + pipx PATH
├── git/.gitconfig
├── nvim/
├── starship/
└── tmux/.tmux.conf
```

Symlinked into `$HOME` with a simple install script. If you're spending more than 0.5s waiting for your shell to start, lazy loading is worth the 30 minutes it takes to set up.
