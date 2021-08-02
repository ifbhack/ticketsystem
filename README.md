# Simple Ticketing System

A simple ticketing system made with flask and the python discord api.

## Running

A Makefile has been provided to automate the setup of a development environment
(setting up venv, running tests, etc). To simply run the project, enter the
command:

```bash
$ make run
```

This will test the project and then run the flask application in development
mode. More information about make can be found
[here](https://www.gnu.org/software/make/).

## Testing

Tests can be run using the provided Makefile, or by entering:

```bash
$ python -m unittest discover -p "*_test.py" -s "tests/"
```

In the project root.

## Reference Material

Some links that helped extensively in development.

* [Project Structure](https://docs.python-guide.org/writing/structure/)
* [Flask Tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
* [Python and Make](https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects/)
* [unittest](https://docs.python.org/3/library/unittest.html)
* [coverage](https://devguide.python.org/coverage/)

## License

This project is licensed under a MIT-style license, check the license file for
more details - [LICENSE](LICENSE)
