from typing import Dict, Union
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np


# Initialize the Flask application
app = Flask(__name__)

TXT_ALL_OPTION = "-- ALL --"

# ? temporary to create the data frame, the most important thing is the name of the columns
def get_filter_dropdown_values():
    row1 = ["Ric", ("Spanish", "English", "French"), "Colombia"]
    row2 = ["Alejo", ("Spanish", "English"), "Colombia"]
    row3 = ["Gary", "English", "US"]
    row4 = ["Luis", ("Spanish", "English"), "Panama"]
    row5 = ["Orlando", ("English", "Philippino"), "The Philippines"]
    row6 = ["Chris", "English", ("US")]

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
    new_column_data = {}
    for key, val in column_data.items():
        val = list(set(val))
        val.sort()
        new_column_data[key] = val

    return df, new_column_data


class Filter:
    def __init__(self, column_dict: Dict):
        self.filtering = False
        self.filter = {}
        self.last = {}
        self.is_filter_status = {}
        self._initial = column_dict
        self.initialize()

    def initialize(self):
        for key, val in self._initial.items():
            self.filter[key] = None
            self.last[key] = val
            self.is_filter_status[key] = 0

    def get_filter(self):
        return self.filter

    def get_last(self):
        return self.last

    def get_status(self):
        return self.is_filter_status

    def is_filter_active(self):
        return self.filtering

    def set_filtering(self, is_filter_active: bool):
        self.filtering = is_filter_active

    def reset(self):
        self.filtering = False
        self.filter = {}
        self.last = {}
        self.is_filter_status = {}
        self.initialize()

    def update_filter(self, key: str, val: Union[str, None]):
        self.filter[key] = val
        if val is not None:
            self.filtering = True

    def update_last(self, columns_dict: Dict):
        for key, value in columns_dict.items():
            self.last[key] = value

    def update_status(self, key: str, val: Union[str, None]):
        self.is_filter_status[key] = val


@app.route("/_dp")
def update_dropdown():

    df, columns = get_filter_dropdown_values()
    output_txt = {"member": "None", "language": "None", "country": "None"}

    call = request.args.get("call", type=str)

    selected_value = request.args.get(str(call), type=str)

    if call == "reset":
        filter_data.reset()

    if selected_value is not None:
        selected_value = selected_value if (selected_value != TXT_ALL_OPTION) else None
        filter_data.update_filter(call, selected_value)

    updated_columns = filter_data.get_last()

    if call != "reset":

        for key, value in filter_data.get_filter().items():
            if value is not None:
                df = df.loc[df[key] == value]

        for key in updated_columns.keys():
            updated_columns[key] = list(set(df[key]))

    if filter_data.is_filter_active():
        for key, val in filter_data.get_filter().items():
            if val is None:
                filter_data.update_status(key, 1)
            else:
                filter_data.update_status(key, -1)

    if call == "print":
        for key, item in filter_data.get_status().items():
            if item == -1:
                output_txt[key] = filter_data.get_filter()[key]

    dp_data_list = {}
    for key, col in updated_columns.items():
        if len(col) > 1 and isinstance(col, list):
            col.sort()
            col.insert(0, TXT_ALL_OPTION)

        filter_element = filter_data.get_filter()[key]
        if filter_element is not None:
            temp_elem = []
            for item in filter_data.get_last()[key]:
                if item != filter_element:
                    temp_elem.append(item)
                    continue
            temp_elem.sort()
            col.extend(temp_elem)
            col.insert(1, TXT_ALL_OPTION)

        dp_data_html = ""
        for entry in col:
            dp_data_html += '<option value="{}">{}</option>'.format(entry, entry)
        dp_data_list[key] = dp_data_html
        filter_element = filter_data.get_filter()[key]

        if col[0] == TXT_ALL_OPTION and col[1:] == columns[key]:
            filter_data.update_status(key, 0)

        if TXT_ALL_OPTION in col:
            col.remove(TXT_ALL_OPTION)

    filter_data.update_last(updated_columns)
    print(50 * "*")
    # print(filter_data.get_filter().values())
    # print(filter_data.get_status().values())
    # print(output_txt)
    print(
        f"call: {call}\ndpData {updated_columns}\nstate: {filter_data.get_status()}\nallConst: {TXT_ALL_OPTION}"
    )
    print(50 * "*")
    return jsonify(
        dpData=dp_data_list,
        printFilter=output_txt,
        state=filter_data.get_status(),
        allConst=TXT_ALL_OPTION,
    )


@app.route("/")
def index():
    all_columns = get_filter_dropdown_values()[1]
    for col in all_columns.values():
        col.insert(0, TXT_ALL_OPTION)
    filter_data.initialize()
    return render_template(
        "index.html",
        all_columns=all_columns,
    )


if __name__ == "__main__":
    filter_data = Filter(get_filter_dropdown_values()[1])
    app.run(debug=True, host="localhost", port=3000)
