from backend.bot import bot


def main() -> None:
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()

