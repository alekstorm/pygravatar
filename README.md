# PyGravatar #

PyGravatar is a set of Python bindings for the Gravatar API.

## Getting Started ##

To install, run `pip install py-gravatar`. To verify that the library is working and can connect to the server, run:

```python
>>> import gravatar
>>> user = gravatar.User(<email>, password=<password>) # substitute the email address and password of a Gravatar account
>>> user.test()
1315290974 # however many seconds have passed since 1970
```

## Documentation ##

Full API documentation is available [here](http://alekstorm.github.com/pygravatar/sphinx).
For more information, see the [home page](http://alekstorm.github.com/pygravatar).
