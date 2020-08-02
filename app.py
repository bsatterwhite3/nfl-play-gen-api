from flask import Flask, jsonify, current_app
from playgen import dataloader
from playgen import playsampler


app = Flask(__name__)
app.pbp_data = dataloader.load_data()
app.sampler = playsampler.PlaySampler(app.pbp_data)


@app.route("/plays", methods=["GET"])
def plays():
    return jsonify(f"{current_app.pbp_data.size}")


if __name__ == '__main__':
    app.run(debug=True)
