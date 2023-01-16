def get_image(path) -> str:
    """Return image from cheapshark by given path.

    `path` is a string that starts with /
    """
    return f"https://www.cheapshark.com{path}"


def redirect(deal_id) -> str:
    """Return redirecting page.

    `deal` is returned by cheapshark itself.
    """
    return f"https://www.cheapshark.com/redirect?dealID={deal_id}"


def get_metacritic(path) -> str:
    """Get metacritic review page.

    `path` is a string that starts with /
    """
    return f"https://www.metacritic.com{path}"


def get_steam_page(game_id) -> str:
    """Return steam page by given game id."""
    return f"https://store.steampowered.com/app/{game_id}"
