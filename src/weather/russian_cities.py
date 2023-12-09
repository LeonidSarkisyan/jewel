def search_cities_from_file(city_substring: str):
    cities = []
    limit = 5
    index = 0
    with open("weather/cities.txt", encoding="utf-8") as file:
        for row in file:
            if index != limit:
                if city_substring.lower() in row.strip().lower():
                    cities.append(row.strip())
                    index += 1
            else:
                break
    return cities


def get_cities(skip: int = 0, limit: int = 5):
    if skip < 0 or limit < 0:
        raise ValueError("Пропуск или лимит не должен быть меньше нуля!")
    cities = []
    index = 0
    with open("weather/cities.txt", encoding="utf-8") as file:
        for row in file:
            if skip == 0:
                if index != limit:
                    cities.append(row.strip())
                    index += 1
                else:
                    break
            else:
                skip -= 1
                continue
    return cities
