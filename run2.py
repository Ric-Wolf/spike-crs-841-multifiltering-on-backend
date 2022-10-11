from flask import Flask, render_template, request, jsonify
import json

# Initialize the Flask application
app = Flask(__name__)


def get_dropdown_values():

    """
    dummy function, replace with e.g. database call. If data not change, this function is not needed but dictionary
    could be defined globally
    """

    class_entry_relations = {
        "class1": ["val1", "val2"],
        "class2": ["foo", "bar", "xyz"],
        "all_selections": ['val1','val2','foo','bar','xyz']
    }

    return class_entry_relations


@app.route("/_update_dropdown")
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get("selected_class", type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the values in the dropdown as a html string
    html_string_selected = ""

    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route("/_update_dropdown2")
def update_dropdown2():

    # the value of the second dropdown (selected by the user)
    selected_entry = request.args.get("selected_entry", type=str)

    if (selected_entry=='val1' or  selected_entry=='val2'):
        updated_values = 'class1'
    else:
        updated_values = 'class2'
   
    # create the values in the dropdown as a html string
    html_string_selected = '<option value="{}">{}</option>'.format(updated_values,updated_values )

    # for entry in updated_values:
    #     html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route("/_process_data")
def process_data():
    selected_class = request.args.get("selected_class", type=str)
    selected_entry = request.args.get("selected_entry", type=str)

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(
        random_text="you selected {} and {}".format(selected_class, selected_entry)
    )


@app.route("/")
def index():

    """
    Initialize the dropdown menues
    """

    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[
        default_classes[0]
    ]  # aqui hay que mostrar todas las clases

    return render_template(
        "index.html", all_classes=default_classes, all_entries=default_values
    )


if __name__ == "__main__":

    app.run(debug=True, port=8080)
