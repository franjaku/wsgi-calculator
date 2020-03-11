import traceback
from functools import reduce
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def divide(*args):
    """
    Returns a STRING with the division of the arguments
    :param args:
    :return:
    """
    nums = [int(num) for num in args]
    return nums[0]/nums[1]


def multiply(*args):
    """
    Returns a STRING with the multiplication of the arguments
    :param args:
    :return str:
    """
    nums = [int(num) for num in args]
    return nums[0] * nums[1]


def subtract(*args):
    """
    Returns a STRING with the subtraction of the arguments
    :param args:
    :return str: subtraction of args
    """
    # try:
    #     inputs = [int(num) for num in args[:]]
    #     return str(inputs[0] + -1*sum(inputs[1:]))
    # except ValueError:
    #     return 'Not possible bud'
    # # ans = int(args[0])
    # # # ans = [arg[0] -= num for num in args[1:]]
    # # for num in args[1:]:
    # #     ans -= int(num)
    nums = [int(num) for num in args]
    return nums[0] - nums[1]


def add(*args):
    """
    Returns a STRING with the sum of the arguments
    :param args:
    :return str: subtraction of args
    """
    # try:
    #     inputs = [int(num) for num in args]
    #     return str(sum(inputs))
    # except ValueError:
    #     return 'Not possible bud'
    nums = [int(num) for num in args]
    return nums[0] + nums[1]


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    :param path:
    :return :
    """
    funcs = {'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide,
             '': 'root'}

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    print(func_name)
    print(args)
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def root():
    body = """
    <h1>Instructions</h1>
    <p>
    You can add, subtract, multiply or divide any amount of numbers as follows.\n\n
    
    /operation/num1/num2/num3\n\n
    
    where operation is one of the options above and numX is any integer. Only positive non-zero\n
    integers are allowed.
    </p>
    <ul>
      <li>http://localhost:8080/add/23/42      => 65</li>
      <li>http://localhost:8080/subtract/23/42 => -19</li>
      <li>http://localhost:8080/multiply/3/5   => 15</li>
      <li>http://localhost:8080/divide/22/11   => 2</li>
    </ul>
    """
    return body


def application(environ, start_response):
    """

    :param environ:
    :param start_response:
    :return:
    """

    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        elif path == '/':
            print('Path in application func: {}'.format(path))
            body = root()
        else:
            func, args = resolve_path(path=path)
            body = str(reduce(func, args))
            # body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "200 OK"
        body = "Warning can't divide by zero!!"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-Length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('127.0.0.1', 8080, application)
    srv.serve_forever()
