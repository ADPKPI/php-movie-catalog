import requests
import time
import mysql.connector
from datetime import datetime

# Параметри підключення до бази даних
db_config = {
    'host': '5.11.83.35',
    'user': 'movie_user',
    'password': 'xBURtUG7tqV3_',
    'database': 'movie_catalog'
}

# Ключ API для OMDB
api_key = "8535dfc9"
base_url = "http://www.omdbapi.com/"

# Список ключових слів для пошуку
keywords = [
    "love", "war", "dark", "light", "blood", "city", "dream", "king", "queen", "escape", "lost", "world",
    "night", "day", "heart", "ghost", "death", "life", "fire", "hero", "revenge", "secret", "fear", "last",
    "future", "story", "legend", "mystery", "monster", "island", "road", "storm", "power", "shadow", "rise",
    "end", "new", "game", "battle", "hunt", "destiny", "race", "journey", "ocean", "desert", "jungle",
    "planet", "magic", "silent", "fall", "fight", "earth", "rebellion", "prince", "princess", "curse",
    "child", "time", "midnight", "enemy", "gate", "sword", "throne", "god", "inferno", "beast", "justice",
    "crime", "innocent", "glory", "prison", "echo", "victory", "land", "final", "honor", "sea", "vengeance",
    "spell", "illusion", "gladiator", "nightmare", "labyrinth", "murder", "quest", "awakening", "mirror",
    "heaven", "fury", "ashes", "river", "conquest", "demon", "phoenix", "star", "blade", "sacrifice",
    "conspiracy", "whisper", "fortress", "scar", "artifact", "chase", "fable", "spirit", "mystic", "reborn",
    "destruction", "twilight", "clash", "empire", "guardian", "dominion", "genesis", "prophecy", "symphony",
    "betrayal", "odyssey", "rainbow", "torch", "shield", "strike", "legendary", "samurai", "avatar", "legacy",
    "solitude", "harvest", "echoes", "immortal", "chronicle", "vampire", "dawn", "sunset", "moondust", "phantom",
    "rebellion", "wanderer", "mercy", "zealot", "invincible", "paladin", "avatar", "legacy", "undead", "ancient",
    "warrior", "fairy", "druid", "rift", "abyss", "serenity", "grace", "despair", "savior", "phantasy", "saga",
    "keeper", "illusionist", "forge", "vortex", "brotherhood", "tyrant", "vigilante", "exodus", "haven", "mirage",
    "paradise", "armageddon", "soul", "keeper", "genius", "illusionist", "fortune", "oath", "wanderlust", "zephyr",
    "relic", "eclipse", "bliss", "splendor", "embrace", "salvation", "innocence", "deception", "phantasia", "exile",
    "monsoon", "lament", "purity", "domination", "forever", "harbinger", "clarity", "illusion", "moonlight", "serenity",
    "obsession", "pilgrim", "legend", "valor", "cataclysm", "vengeance", "element", "artifact", "spirit", "patriot",
    "phantom", "rebel", "wildfire", "sanctuary", "scepter", "shackles", "harbinger", "sovereign", "eternal", "uprising",
    "ascent", "whispering", "resurrection", "majesty", "envoy", "dominion", "triumph", "union", "starlight", "conquest",
    "elemental", "devotion", "conundrum", "revival", "cosmos", "vigilance", "legacy", "tempest", "resonance", "wraith",
    "deliverance", "frost", "unity", "seraph", "vengeance", "spectrum", "wisdom", "tranquility", "rift", "euphoria",
    "darkness", "faith", "sanctum", "zeal", "fable", "horizon", "myth", "sacrifice", "serpent", "sorrow", "element",
    "noble", "prism", "celestial", "myriad", "beacon", "glow", "infinity", "reflection", "wanderer", "relic",
    "sanctuary", "arcadia", "overseer", "forbidden", "emerald", "calamity", "rift", "voyage", "salvation", "expedition",
    "whisper", "seer", "illusion", "maze", "eternity", "frost", "vanguard", "haven", "nirvana", "eden", "entity",
    "oracles", "titan", "shadows", "spirits", "alchemy", "havoc", "ashes", "fable", "celestial", "vanquish", "reign",
    "void", "vengeance", "inferno", "rebel", "valor", "phantom", "nightfall", "shroud", "ancestry", "monument",
    "gargoyle", "morningstar", "solstice", "celestia", "ascent", "voyager", "bastion", "reaper", "stormbringer",
    "ether", "glory", "retribution", "chimera", "bravery", "celestial", "vigilance", "apex", "oracle", "strife",
    "overlord", "sanctity", "radiance", "lore", "behemoth", "abyss", "ascendant", "dominion", "regalia", "sentinel",
    "triumph", "majesty", "crusade", "exile", "rift", "fable", "paragon", "cosmic", "legacy", "odyssey", "nexus",
    "retribution", "anomaly", "glimmer", "radiant", "devotion", "twilight", "mirage", "eminence", "eternity",
    "savior", "ember", "fortitude", "equilibrium", "omen", "storm", "summit", "bounty", "echo", "imperium", "lumina",
    "aeon", "aurora", "phoenix", "omen", "valor", "zealot", "conviction", "celestial", "harmony", "oracle",
    "arcane", "abyssal", "genesis", "valor", "essence", "mythic", "omen", "beacon", "oracle", "prophecy", "grace",
    "fable", "arcane", "aurora", "phantasm", "spectral", "ethereal", "sovereign", "shroud", "storm", "frost",
    "apocalypse", "ethos", "crusader", "void", "unity", "bastion", "eternal", "echo", "resolve", "dusk",
    "echo", "grace", "astral", "vengeance", "specter", "rift", "destiny", "oracle", "twilight", "echo", "mythos",
    "element", "monarch", "voyager", "glimmer", "veil", "ethereal", "gale", "crusade", "soul", "aura", "omen",
    "prodigy", "solace", "eternity", "arcanum", "valor", "envoy", "omen", "rising", "synthesis", "arcane", "mantle",
    "virtue", "shard", "celestia", "echo", "veil", "phantasia", "saga", "oracle", "goliath", "shadow", "equilibrium",
    "omen", "vengeance", "ascension", "void", "anomaly", "eden", "radiant", "echo", "dominion", "rift",
    "oracle", "eternal", "bounty", "zephyr", "sentry", "zenith", "haven", "omen", "phalanx", "gale",
    "arcadia", "ember", "glory", "virtue", "beacon", "solstice", "horizon", "echo", "specter", "eden",
    "phoenix", "aegis", "omen", "mythic", "valor", "cosmos", "quasar", "legacy", "ethereal", "sanctum",
    "gale", "celestial", "reign", "strife", "oracle", "light", "fate", "shadow", "solstice", "omen",
    "specter", "chronicle", "inception", "pillar", "zephyr", "solitude", "apex", "veil", "vigilant",
    "mantle", "eclipse", "lament", "synthesis", "saga", "echo", "ethereal", "oracle", "beacon", "ethos",
    "vanguard", "noble", "aegis", "myth", "sanctum", "gale", "prophecy", "allegiance", "element", "fate",
    "sentinel", "virtue", "majesty", "aurora", "goliath", "ethereal", "pillar", "valor", "mantle",
    "phantasia", "genesis", "cosmos", "astral", "chronicle", "fortitude", "eden", "phoenix", "sanctuary",
    "beacon", "epiphany", "valor", "goliath", "horizon", "saga", "ethos", "radiance", "celestial",
    "equinox", "enigma", "anomaly", "sovereign", "rhapsody", "glory", "specter", "elemental", "virtue",
    "seraph", "triumph", "omen", "solstice", "lament", "legacy", "envoy", "mythic", "zephyr", "bounty",
    "virtue", "cosmos", "ethereal", "eternity", "omen", "zenith", "mystic", "sanctum", "oracle", "goliath",
    "astral", "relic", "ember", "echo", "genesis", "cosmos", "strife", "radiance", "glimmer", "ethereal"
]

# Множина унікальних ID фільмів для запобігання дублікатам
unique_movie_ids = set()

# Функція для підключення до бази даних
def connect_db():
    return mysql.connector.connect(**db_config)

# Функція для отримання списку фільмів за ключовим словом
def fetch_movies_by_keyword(keyword):
    url = f"{base_url}?s={keyword}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        movies = response.json().get("Search")
        if movies:
            return movies
    return None

# Функція для збереження даних фільму в базу даних
def save_movie_to_db(movie_data, conn):
    cursor = conn.cursor()

    # Конвертація дати в формат 'YYYY-MM-DD'
    release_date = movie_data["Released"]
    try:
        release_date = datetime.strptime(release_date, "%d %b %Y").strftime("%Y-%m-%d")
    except ValueError:
        release_date = None  # Якщо дата недоступна

    try:
        cursor.execute("""
            INSERT INTO movies (
                title, year, rated, released, runtime, genre, director, writer,
                actors, plot, language, country, awards, poster_url, metascore,
                imdb_rating, imdb_votes, imdb_id, box_office
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            movie_data["Title"], movie_data["Year"], movie_data["Rated"],
            release_date, movie_data["Runtime"], movie_data["Genre"],
            movie_data["Director"], movie_data["Writer"], movie_data["Actors"],
            movie_data["Plot"], movie_data["Language"], movie_data["Country"],
            movie_data["Awards"], movie_data["Poster"],
            int(movie_data["Metascore"]) if movie_data["Metascore"].isdigit() else None,
            float(movie_data["imdbRating"]) if movie_data["imdbRating"] else None,
            movie_data["imdbVotes"], movie_data["imdbID"], movie_data["BoxOffice"]
        ))
        conn.commit()
        print(f"Фільм '{movie_data['Title']}' успішно доданий до бази даних.")
    except mysql.connector.errors.IntegrityError:
        print(f"Фільм '{movie_data['Title']}' вже існує в базі даних.")
    except Exception as e:
        print(f"Помилка під час додавання фільму '{movie_data['Title']}': {e}")
    finally:
        cursor.close()

# Основний процес
conn = connect_db()
for keyword in keywords:
    movies = fetch_movies_by_keyword(keyword)

    if movies:
        for movie in movies:
            imdb_id = movie["imdbID"]
            if imdb_id not in unique_movie_ids:  # Перевірка на унікальність
                unique_movie_ids.add(imdb_id)
                # Отримання детальної інформації про фільм
                detailed_url = f"{base_url}?i={imdb_id}&apikey={api_key}"
                detailed_response = requests.get(detailed_url)
                if detailed_response.status_code == 200:
                    movie_data = detailed_response.json()
                    save_movie_to_db(movie_data, conn)
    else:
        print(f"Не вдалося знайти фільми за ключовим словом: {keyword}")

    time.sleep(0.2)  # Затримка між запитами

conn.close()