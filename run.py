#! /usr/local/bin/python3


from market_garden import app


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')