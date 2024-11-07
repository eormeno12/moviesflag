import json
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
apikey = "apikey"

@lru_cache(maxsize=1000)
def searchfilms(search_text, page=1):
    url = f"https://www.omdbapi.com/?s={search_text}&page={page}&apikey={apikey}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve search results.")
        return None

@lru_cache(maxsize=1000)
def getmoviedetails(imdbID):
    url = f"https://www.omdbapi.com/?i={imdbID}&apikey={apikey}"    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve search results.")
        return None

@lru_cache(maxsize=1000)
def get_country_flag(fullname):

    url = f"https://restcountries.com/v3.1/name/{fullname}?fullText=true"
    response = requests.get(url)
    if response.status_code == 200:
        country_data = response.json()
        if country_data:
            return country_data[0].get("flags", {}).get("svg", None)
    print(f"Failed to retrieve flag for country code: {fullname}")
    return None


def get_movie_details_with_flags(imdbID):
    moviedetails = getmoviedetails(imdbID)
    countriesNames = moviedetails["Country"].split(",")
    countries = []

    for country in countriesNames:
        countrywithflag = {
            "name": country.strip(),
            "flag": get_country_flag(country.strip())
        }
        countries.append(countrywithflag)
    moviewithflags = {
        "title": moviedetails["Title"],
        "year": moviedetails["Year"],
        "countries": countries
    }
    
    return moviewithflags

def merge_data_with_flags(filter, page=1):
    filmssearch = searchfilms(filter, page)
    print(filmssearch)
    if not filmssearch or "Search" not in filmssearch:
        return []
    
    moviesdetailswithflags = []
    
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(get_movie_details_with_flags, movie["imdbID"]): movie 
            for movie in filmssearch["Search"]
        }
        
        for future in futures:
            try:
                moviedetails = future.result()
                moviesdetailswithflags.append(moviedetails)
            except Exception as e:
                print(f"Failed to process movie details: {e}")
                

    return moviesdetailswithflags

@app.route("/")
def index():
    filter = request.args.get("filter", "").upper()
    page = request.args.get("page", 1)
    return render_template("index.html", movies = merge_data_with_flags(filter, page))

@app.route("/api/movies")
def api_movies():
    filter = request.args.get("filter", "")
    page = request.args.get("page", 1)
    return jsonify(merge_data_with_flags(filter, page))

if __name__ == "__main__":
    app.run(debug=True)

