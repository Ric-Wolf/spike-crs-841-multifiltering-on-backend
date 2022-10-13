from stat import FILE_ATTRIBUTE_NO_SCRUB_DATA
from typing import Dict
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np


# Initialize the Flask application
app = Flask(__name__)

TXT_ALL_OPTION = "-- ALL --"


def get_filter_dropdown_values():
    row1 = ["Ric", ("Spanish", "English", "French"), "Colombia"]
    row2 = ["Alejo", ("Spanish", "English"), "Colombia"]
    row3 = ["Gary", "English", "US"]
    row4 = ["Luis", ("Spanish", "English"), "Panama"]
    row5 = ["Orlando", ("English", "Philippino"), "The Philippines"]
    row6 = ["Chris", "English", "US"]

    rows = [row1, row2, row3, row4, row5, row6]
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

    df = pd.DataFrame(data=data, columns=["member", "language", "country"])

    column_data = df.to_dict(orient="list")
    new_column_data = []
    for key, val in column_data.items():
        val = list(set(val))
        val.sort()
        new_column_data.append([key, val])

    return df, new_column_data


class Filter:
    def __init__(self):
        self.filter = {}
        self.filtering = False

    def get_filter(self):
        return self.filter

    def is_filter_active(self):
        return self.filtering

    def set_filtering(self, is_filter_active: bool):
        self.filtering = is_filter_active

    def reset(self):
        self.filter = {}

    def update(self, fil_val_dict: Dict):
        for key, val in fil_val_dict.items():
            self.filter[key] = val


filter_data = Filter()


@app.route("/_dp")
def update_dropdown():

    df, columns = get_filter_dropdown_values()
    output_txt = ""
    is_filtered_columns = {}

    to_filter = filter_data.get_filter()

    for col in columns:
        if col[0] not in to_filter.keys():
            filter_data.update({col[0]: None})
        is_filtered_columns[col[0]] = False

    call = request.args.get("call", type=str)
    selected_value = request.args.get(call, type=str)

    if call == "reset":
        filter_data.set_filtering(False)
        output_txt = "Here we display some output based on the selection"
        filter_data.reset()

    if selected_value is not None:
        if selected_value == TXT_ALL_OPTION:
            selected_value = None
        filter_data.update({call: selected_value})

    print(is_filtered_columns)

    # selected_lang = request.args.get_filter("lang", type=str)
    # selected_country = request.args.get_filter("country", type=str)

    updated_columns = columns
    if call not in ("reset"):
        to_filter = filter_data.get_filter()
        output_txt = str(to_filter)
        for key, value in to_filter.items():
            if value is not None:
                df = df.loc[df[key] == value]
                filter_data.set_filtering(True)
        for col in updated_columns:
            col[1] = list(set(df[col[0]]))

    if filter_data.is_filter_active():
        to_filter = filter_data.get_filter()
        for key, val in to_filter.items():
            if val is None:
                is_filtered_columns[key] = True

    if call == "print":
        output_txt = str(updated_columns)

    for col in updated_columns:
        if len(col[1]) > 1:
            col[1].sort()
            col[1].insert(0, TXT_ALL_OPTION)

    dp_data_list = []
    for col in updated_columns:
        dp_data_html = ""
        for entry in col[1]:
            dp_data_html += '<option value="{}">{}</option>'.format(entry, entry)
        dp_data_list.append(dp_data_html)
    return jsonify(dp_data=dp_data_list, print_txt=output_txt)


@app.route("/")
def index():

    """
    Initialize the dropdown menues
    """

    all_columns = get_filter_dropdown_values()[1]
    for col in all_columns:
        col[1].insert(0, TXT_ALL_OPTION)
    return render_template(
        "index.html",
        all_columns=all_columns,
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
