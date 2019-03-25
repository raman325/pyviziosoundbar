> This code is deprecated as [pyvizio](https://github.com/vkorn/pyvizio) has been updated to add sound bar support. Please use the latest pyvizio packages instead of this one.

## Description

Simple cli and API implementation for Vizio SmartCast SoundBars. Mainly created for 
integration with [HASS](http://home-assistant.io).

## Installation
### PyPi
```
pip3 install pyviziosoundbar
```

### GitHub Code
Either through pip

```
pip3 install git+https://github.com/raman325/pyviziosoundbar.git@master
```

or checkout repo and run 

```
pip3 install -I .
```

## CLI Usage

To avoid repeating IP param, you can add it to environment variables as `VIZIO_SOUNDBAR_IP`

### Pairing

First, find your device (yeah, I'm too lazy to add another cli group)
```
pyviziosoundbar --ip=0 discover
```

and note it's IP address.

### Turning on/off

```
pyviziosoundbar --ip={ip} power {on|off|toggle}
```

To get current power state simply call

```
pyviziosoundbar --ip={ip} power
``` 

### Volume operations

You could change volume

```
pyviziosoundbar --ip={ip} volume {up|down} amount
```

and get current level (0-100)

```
pyviziosoundbar --ip={ip} volume-current
```

In addition mute command is available

```
pyviziosoundbar --ip={ip} mute {on|off|toggle}
```

### Input sources

You can get current source 

```
pyviziosoundbar --ip={ip} input-current
```

List all sources

```
pyviziosoundbar --ip={ip} input-list
```

And using `Name` column from this list switch input

```
pyviziosoundbar --ip={ip} input-set {name}
```

### Control Media

Play media 

```
pyviziosoundbar --ip={ip} play
```

Pause media

```
pyviziosoundbar --ip={ip} pause
```

## Contribution
- Thanks to @vkorn whose [pyvizio](https://github.com/vkorn/pyvizio) I used as a base. Most of the code is theirs, including most of this documentation
- Thanks for great research uploaded [here](https://github.com/exiva/Vizio_SmartCast_API) and 
absolutely awesome SSDP discovery [snippet](https://gist.github.com/dankrause/6000248)
