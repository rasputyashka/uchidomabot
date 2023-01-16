def get_image(path) -> str:
    return "https://www.cheapshark.com" + path


def redirect(path) -> str:
    return f"https://www.cheapshark.com/redirect?dealID={path}"


def get_metacritic(path) -> str:
    return f"https://www.metacritic.com{path}"


def get_steam_page(game_id) -> str:
    return f"https://store.steampowered.com/app/{game_id}"
