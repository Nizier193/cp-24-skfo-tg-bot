# Телеграм-клиент для RuStore
**Uses PyTelegrambotApi**

## Features:
- Поддержка загрузки файлов в систему
- Поддержка получения ответа от RAG-системы
- Получения Config системы
- Опциональное использование RagApp или RagFlow
- Удобная конфигурация с помощью config.Config и config.Providers

## Описание
Телеграм бот способен отвечать на любые вопросы в контексте RAG.
Ему можно отправлять любые файлы и он проанализирует данные и сможет отвечать
по заданному контексту.

### Requirements
Использует развёрнутый функционал RagApp или RagFlow (Опционально).

requirements.txt

### Развёртывание

```commandline
git clone https://github.com/Nizier193/05-07-Hackatone-TGBot.git
python3 main.py
```