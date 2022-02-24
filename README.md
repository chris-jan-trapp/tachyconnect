# tachyconnect

This package can be used make Qt applications communicate with [leica](https://leica-geosystems.com/) total stations.
Qt is required to provide threading and signal/ slot infrastructure. 
It provides a message abstraction for the [GSI](https://totalopenstation.readthedocs.io/en/stable/input_formats/if_leica_gsi.html) and [geoCOM](http://webarchiv.ethz.ch/geometh-data/student/eg1/2010/02_deformation/TPS1200_GeoCOM_Manual.pdf) protocols.

## The Concept

Leica total stations use a set of communication protocols.
This package creates an abstraction layer that allows to send a command to the device (e.g. "set reflector height") and connect the response to a Qt slot.
The communication handling lives in its own thread and thus is non blocking. 

## The Players

### Protocols
`geo_com`, `gc_constants` and `GSI_parser` deal with creating and interpreting messages in either protocol.


#### `GSI_parser.py`

This is mostly used to translate measurements that are triggered at the device and transmitted via serial, but is capable to read any successful reply to a GSI command.
The `parse(line)` function is the central element, the rest consists of definitions.
It takes the ascii decoded bytes from the serial port an returns two dicts: 

```python
# We requested the height of the total station and got:
reply = "*88..10+0000000000000000"

print(parse(reply))

>>> ({'precision': 16, 'instrumentZ': 0.0}, {'instrumentZ': 'meter_1mm'})
```

The first carries the actual data, cast to an appropriate type, the second one provides a string that informs us about the unit. 
The keys (except `precision`, which is attached by the parser) are taken from the `dict_units_attributes_digits`, around line 240 in the parser source.
The `precision` entry refers to the number of available digits for each datum.
GSI uses a fixed field width and GSI8 provides eight places for data.
The newer format GSI16 used in the example surprises with sixteen places.
Which dialect is used is indicated by the leading asterisk of the reply.


#### `geo_com.py'

This is legacy code that has been replaced by 'TachyRequest.py` that primarily exists as design notes for the author. 


#### `gc_constants.py`

Here you find names for the constants that are used as return codes (`GRC_...`) and commands (`BMM...`, `COM_...`, `CSV...`...).
You also get a set of dicts that map the return codes to their names and a more verbose message.
For commands you get a dict that maps command names to the numerical codes.


### Abstraction

Messages to and from the total station get a technical implementation which is then wrapped in an abstraction.
The technical implementation handles the details of constructing the actual byte array that is sent over the serial connection and the extraction of results from the reply.
This is done for GSI and geoCom and takes place in `ts_control.py`.

The wrapper deals with the *intent* of a command e.g. "Take a measurement" and separates it from the two dialects. 


#### `TachyRequest.py`

TachyRequest contains classes for abstracted commands. 
Each class represents one action that can be requested and provides the methods `get_gsi_command()` and `get_geocom_command()`.
The commands bear the names of their geoCOM equivalent:

```python
# Switch off device:
class COM_SwitchOffTPS(TachyRequest):
    gsi_command = "b"

```

***NOTE: This is only partially implemented :( ***

This is to be used in conjunction with an implementation map that informs the dispatcher, which dialect is used for each command by the connected total station. 
When implementing a remote shut down button we would instantiate `COM_SwitchOffTPS` and submit it to the dispatcher.
The dispatcher looks up which dialect implements the functionality and generate the relevant message by calling either `get_gsi_command()` or `get_geocom_command()` and append the result to the respective queue.

***END of fiction***

The class name is also used as label, which in turn can be used to link commands to slots.
See the `ReplyHandler` documentation below for more on this.
Each `TachyRequest` has a gsi command string, a geoCOM command string and also `unpacking_keys`, which are required to access the data in GSI replies.
In the example above this would be '`instrumentZ`'.
The constructor takes a timeout in seconds (defaults to 2) and optional parameters, which will be attached to the actual request.


#### `ReplyHandler.py`

This guy was designed to provide a connection between Qt slots and total station replies, along the lines of "When the reply to a `TMC_GetCoordinate` request comes in, fire a `got_coordinate` signal.
It also emits a fall back signal when it encounters replies that have no connected slot. 
⚠️ ***THIS DOES NOT WORK*** because the design of Qt's signal/ slot architecture prohibits the creation of signals at runtime.

***HOWEVER*** We can do the next best thing.
Signals and slots are only really required for communication between treads. 
As long as we stay in the main class of our widget, we can use callables instead of slots.

This slot should be passed to the ctor.
Besides that the following methods are provided:

1. `register_command(self, command_class, slot)`: Takes any class from `TachyRequest` ⬆️ and a callable. When the reply to the request shows up, the result is extracted from the reply and passed to the callable which is then invoked. The association between requests and callables is implemented as a dict so each request can have at most one function to handle its results.
1. `unregister_command(self, command_class)`: Allows to delete the association between a request and an action.
1. `handle(self, request, reply)`: This is called from the dispatcher when a reply is being received on a queue. Note that the queue bundles each reply with the request that triggered it. The ReplyHandler now looks for an associated function to call. If none is found, request and reply are directed to the fallback signal (if provided earlier).

## The Console

The `tachy_console.py` provides you with debugging functionalities and examples for sending and receiving messages.
