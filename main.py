import json
import math
import random


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance



def calculate_bearing(lat1, lon1, lat2, lon2):
    dlon = math.radians(lon2 - lon1)

    y = math.sin(dlon)
    x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dlon)
    bearing = (math.degrees(math.atan2(y, x)) + 360) % 360

    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(bearing / (360. / len(directions))) % len(directions)
    return directions[index]


def main():
    with open("world.json", "r", encoding="utf-8") as file:
        countries_data = json.load(file)

    correct_country = random.choice(countries_data)

    attempts = 0
    max_attempts = 6

    while attempts < max_attempts:
        guess = input(f"GUESS {attempts + 1}/{max_attempts}: ")

        guessed_country = None
        for country in countries_data:
            if guess.lower() in [
                country["country_code"].lower(),
                country["name_jp"].lower(),
                country["name_jps"].lower(),
                country["name_en"].lower(),
                country["name_ens"].lower(),
                country["capital_jp"].lower(),
                country["capital_en"].lower(),
            ]:
                guessed_country = country
                break

        if guessed_country is not None:
            if (
                correct_country["country_code"].lower()
                == guessed_country["country_code"].lower()
            ):
                print(f"ゲームクリア！正解は {correct_country['name_jps']} でした。")
                break
            else:
                distance = calculate_distance(
                    float(correct_country["lat"]),
                    float(correct_country["lon"]),
                    float(guessed_country["lat"]),
                    float(guessed_country["lon"]),
                )
                bearing = calculate_bearing(
                    float(guessed_country["lat"]),
                    float(guessed_country["lon"]),
                    float(correct_country["lat"]),
                    float(correct_country["lon"]),
                )

                print(f"距離: {distance:.2f} km")
                print(f"方角: {bearing}")
                print(f"--------------------")
                attempts += 1
        else:
            print("その国はデータに存在しません。有効な国を入力してください。")

    if attempts == max_attempts:
        print(f"ゲームオーバー！正解は {correct_country['name_jps']} でした。")


if __name__ == "__main__":
    main()
