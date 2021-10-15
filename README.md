## UNICORN Web Application

`UNICORN` stands for **Unit Conversion**, is a web application created for
resolving the units conversion issues between physics
and engineering realms, specifically, in the accelerator system high-level
controls field.

### Usage
The typical use case should be like:
1. The client (script, opi, etc.) got readings from a device, usually from a IOC,
   say have a variable named current (`I`), with the value of engineering unit of
   `10.0 A`;
2. The client can ask for the unit interpretation within the physics realm, i.e.
   What is the significant representation for the accelerator physicist?
   `UNICORN` helps.

#### Web Interface
Let's say the device talking to is `FE_MEBT:Q_D1057`, which is a quadrupole,
by controlling the current (`I`) the gradient (`G`) changes. The directly way
to do is: firstly locate the function by quick searching, e.g. input 'Q_D1057'
in the search box in Functions page, only remaining two entries;

![](/screenshots/readme-01.png)

Choose correct function, e.g. 'FE_MEBT:Q_D1057_I_to_B2' to convert `I` (current in A) to
`B2` (gradient in T/m),
Click the function name to direct the detail page, on that page, input
`{"x":10}` in the input box and push run button, the output will be shown in
the first two top lines of the function detail page.

![](/screenshots/readme-02.png)
The reverse way could be done by picking another function attached to the same
device.

As one can see, the web application keeps not only the unit conversion functions,
or the scaling laws, but also the data and many other meta properties that
could help us organize all the information.

#### Python Interface
Beside the above way to retrieve the conversion information within the web page,
another essential approach is provided by Python package so-called `unicorn`,
REST APIs are served by `UNICORN` web application, so here is the brief guideline
to make the most in the Python scripting environment:

```python
import unicorn
# admin client to UNICORN service
admin_client = unicorn.AdminClient('http://localhost:5000')
# get all functions
admin_client.get()
# get function by name, return a dict
admin_client.get(name='FE_MEBT:Q_D1057_I_to_B2')

# api client, the base url + '/api/v1.0'
api_client = unicorn.ApiClient('http://localhost:5000/api/v1.0')

# get function execution result, I --> B2
api_client.get('FE_MEBT:Q_D1057_I_to_B2', x=10)
# output: {'result': 1.5043739625926702}

# get result from reverse function, i.e. G --> I
api_client.get('FE_MEBT:Q_D1057_B2_to_I', x=1.5043739625926702)
# output: {'result': 9.999999999999586}
```

### Installation
PPA:
The debian package is available in the following PPA:


### Development
make env
make env_pkg
make run

### Data management
See unicorn.
