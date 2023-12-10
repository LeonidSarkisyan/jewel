from src.gem.images import load_image_and_get_url
from src.gem.search import get_similar_links


def get_links_by_photo(filename: str) -> list[dict[str, str]]:
    url_photo = load_image_and_get_url(filename)
    links = get_similar_links(url_photo)
    return links
