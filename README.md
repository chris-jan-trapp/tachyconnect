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

#### `GSI_parser`

