import json
import logging
from flask import Flask, render_template, request, g, jsonify

import main

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/', methods=['POST'])
def get_rates():
    print(request)
    try:
        request_data = request.get_json()
        print(request_data)

        if request_data is None:
            raise Exception("missing request json")

        results = main.processData(request_data)
        return jsonify(results), 200

    except Exception as e:
        logging.exception("error!")
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)