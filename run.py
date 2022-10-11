from typing import Dict
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np


# Initialize the Flask application
app = Flask(__name__)


def get_dropdown_values():
    row1 = ["Ric", ("Spanish", "English", "French"), "Colombia"]
    row2 = ["Alejo", ("Spanish", "English"), "Colombia"]
    row3 = ["Gary", "English", "US"]
    row4 = ["Luis", ("Spanish", "English"), "Panama"]
    row5 = ["Orlando", ("English", "Philippino"), "The Philippines"]

    rows = [row1, row2, row3, row4, row5]
    data = []
    for row in rows:
        if isinstance(row[1], str):
            row[1] = [row[1]]
        if isinstance(row[2], str):
            row[2] = [row[2]]

        for lang in row[1]:
            for country in row[2]:
                data.append([row[0], lang, country])

    data = np.array(data)

    members = list(set(data[:, 0]))
    languages = list(set(data[:, 1]))
    countries = list(set(data[:, 2]))
    members.sort()
    languages.sort()
    countries.sort()
    members.insert(0, "-- all --")
    languages.insert(0, "-- all --")
    countries.insert(0, "-- all --")

    df = pd.DataFrame(data=data, columns=["Member", "Language", "Country"])

    return df, members, languages, countries


class Filter:
    def __init__(self):
        self.member = None
        self.language = None
        self.country = None

    def get(self):
        return {
            "Member": self.member,
            "Language": self.language,
            "Country": self.country,
        }

    def reset(self):
        self.member = None
        self.language = None
        self.country = None

    def update(self, fil_val_dict: Dict):
        for key, val in fil_val_dict.items():
            if key == "Member":
                self.member = val
            if key == "Language":
                self.language = val
            if key == "Country":
                self.country = val


filter_data = Filter()


@app.route("/_dp")
def update_dropdown():
    df, all_members, all_langs, all_countries = get_dropdown_values()

    call = request.args.get("call", type=str)
    member = request.args.get("member", type=str)
    lang = request.args.get("lang", type=str)
    country = request.args.get("country", type=str)

    updated_members = all_members
    updated_languages = all_langs
    updated_countries = all_countries

    if call == "reset":
        filter_data.reset()

    if call == "member":
        filter_data.update({"Member": member})
    elif call == "lang":
        filter_data.update({"Language": lang})
    elif call == "country":
        filter_data.update({"Country": country})

    if call != "reset":
        to_filter = filter_data.get()
        for key, value in to_filter.items():
            if value is not None:
                df = df.loc[df[key] == value]

        updated_members = list(set(df["Member"]))
        updated_languages = list(set(df["Language"]))
        updated_countries = list(set(df["Country"]))

        updated_members.sort()
        updated_languages.sort()
        updated_countries.sort()

        # solo se apendiza a filtros activos y toca revisar si se recibe reset en una call ese filtro se borra
        updated_members.append("--reset--")
        updated_languages.append("--reset--")
        updated_countries.append("--reset--")

    if call == "print":
        print_txt = (
            "Member(s): "
            + str(updated_members)
            + "\nspeak: "
            + str(updated_languages)
            + "\nfrom: "
            + str(updated_countries)
        )
        return jsonify(print_txt=print_txt)
    dp1_data_html = ""
    for entry in updated_members:
        dp1_data_html += '<option value="{}">{}</option>'.format(entry, entry)
    dp2_data_html = ""
    for entry in updated_languages:
        dp2_data_html += '<option value="{}">{}</option>'.format(entry, entry)
    dp3_data_html = ""
    for entry in updated_countries:
        dp3_data_html += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(
        dp1_data=dp1_data_html, dp2_data=dp2_data_html, dp3_data=dp3_data_html
    )


@app.route("/")
def index():

    """
    Initialize the dropdown menues
    """

    all_members, all_langs, all_countries = get_dropdown_values()[1:]

    return render_template(
        "index.html",
        all_members=all_members,
        all_langs=all_langs,
        all_countries=all_countries,
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
