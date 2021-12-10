# tachyconnect

This package can be used make Qt applications communicate with [leica](https://leica-geosystems.com/) total stations.
It provides a message abstraction for the [GSI](https://totalopenstation.readthedocs.io/en/stable/input_formats/if_leica_gsi.html) and [geoCOM](http://webarchiv.ethz.ch/geometh-data/student/eg1/2010/02_deformation/TPS1200_GeoCOM_Manual.pdf) protocols.

## The Concept

Leica total stations use a set of communication protocols.
This package creates an abstraction layer that allows to send a command to the device (e.g. "set reflector height") and connect the response to a Qt slot.
The communication handling lives in its own thread and thus is non blocking. 

## The Players

### Protocols
`geo_com`, `gc_constants` and `GSI_parser` deal with creating ind interpreting messages in either protocoll.


#### `GSI_parser.py`

This is mostly used to translate measurements that are triggered at the device and transmitted via serial, but is capable to read any sucessful reply to a GSI command.
The `parse(line)` function is the central element, the rest consists of definitions.
It takes the ascii decoded bytes from the serial port an returns two dicts: 

```python
# We requested the height of the total station and got:
reply = "*88..10+0000000000000000"

print(parse(reply))

>>> ({'precision': 16, 'instrumentZ': 0.0}, {'instrumentZ': 'meter_1mm'})
```

The first carries the actual data, cast to an appropriate type, the second one provides a string that informs us about the unit. 
The keys (except 'precision', which is attached py the parser) are taken from the `dict_units_attributes_digits`, around line 240 in the parser source.


#### `geo_com.py'

This is legacy code that has been replaced by 'TachyRequest.py` that primaryly exists as design notes for Christian. 


#### `gc_constants.py`

Here you find names apping for the constants that are used as return codes (`GRC_...`) and commands (`BMM...`, `COM_...`, `CSV...`...).
You also get a set of dicts that map the return codes to their names and a more verbose message.
For commands you get a dict that maps command names to the numerical codes.


### Abstraction

#### `TachyRequest.py`

TachyRequest is the base class from which individual commands are derived. 
Individual commands bear the names of their geoCOM equivalent:

```python
# Switch off device:
class COM_SwitchOffTPS(TachyRequest):
    gsi_command = "b"

```

The same name is used as label, which in turn can be used to link commands to slots.
Each `TachyRequest` has a gsi command string, a geoCOM command string and also `unpacking_keys`, which are required to access the data in GSI replies.
In the example above this would be '`instrumentZ`'.
The constructor takes a timeout in seconds (defaults to 2) and optional parameters, which will be attached to the actual request.


#### `ReplyHandler.py`

This guy provides the connections between Qt slots and total station replies.
It also emits a fall back signal when it encounters replies that have no connected slot. 
This slot should be passed to the ctor.
Besides that the following methods are provided:

1. `register_command(self, label, signal_name=None)`: Takes the label of a `TachyRequest` ⬆️ and an optional name for the signal that will be emitted when the reply to the requst is being received. If no signal name is provided, the label is used instead.
1. `add_connection(self, signal_name, types, slot)`: 
