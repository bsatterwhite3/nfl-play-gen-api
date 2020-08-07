import logging
import sys

from flask import Flask, jsonify, current_app, request
from playgen import dataloader, playsampler, filters, handlers


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


app = Flask(__name__)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.pbp_data = dataloader.load_pbp_data()
app.sampler = playsampler.PlaySampler(app.pbp_data)


@app.route("/plays", methods=["GET"])
def plays():
    app.logger.info("Received GET request for /plays endpoint")
    response, status_code = handlers.get_plays(current_app.pbp_data, request.args)
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(debug=True)
