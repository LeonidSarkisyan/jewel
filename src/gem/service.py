from src.gem.base import get_links_by_photo


class GemService:

    def get_links_by_photo(self, filename: str) -> list[dict[str, str]]:
        links = get_links_by_photo(filename)
        return links


gem_service = GemService()
