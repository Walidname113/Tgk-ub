#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'

installed_libs=()
failed_libs=()

check_installed() {
    if pip show "$1" &>/dev/null; then
        installed_libs+=("$1")
        return 0
    else
        failed_libs+=("$1")
        return 1
    fi
}

install_library() {
    if check_installed "$1"; then
        return 0
    else
        echo -e "${YELLOW}Установка $1...${NC}"
        if ! pip install "$1" >/dev/null 2>&1; then
            echo -e "${RED}Ошибка установки $1. (Exit code: 1)${NC}"
            return 1
        fi
    fi
}

attempt_install() {
    if install_library "$1"; then
        echo -e "${GREEN}$1 установлена.${NC}"
    else
        echo -e "${RED}Библиотека $1 не может быть установлена.${NC}"
        if [ "$2" == "optional" ]; then
            echo -e "${YELLOW}Пропуск установки $1.${NC}"
        else
            return 1
        fi
    fi
}

attempt_install "requests" &&
attempt_install "telebot" &&
attempt_install "asyncio" &&
attempt_install "psutil" &&
attempt_install "Telegraph" &&
attempt_install "telethon" || {
    echo -e "${YELLOW}Обновление libexpat успешно. Повторная установка библиотек...${NC}"
    pkg update libexpat > /dev/null 2>&1
    attempt_install "requests" "optional" || return 1
    attempt_install "telebot" "optional" || return 1
    attempt_install "asyncio" "optional" || return 1
    attempt_install "psutil" "optional" || return 1
    attempt_install "Telegraph" "optional" || return 1
    attempt_install "telethon" "optional" || return 1
}
clear

echo -e "${GREEN}Успешно установленны библиотеки.${NC}"
echo -e "${YELLOW}Попытка воиспроизвести програму...${NC}"
clear
cd
cd KVARCEVIEhelp
python3 amain.py
