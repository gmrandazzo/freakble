# freakble

A simple tool to send messages into [FreakWAN](https://github.com/antirez/sx1276-micropython-driver/)
over Bluetooth low energy.

**This is still a work in progress and it's not complete.**

## Installation

### Using pipx

The best way to install freakble is using [pipx](https://pypa.github.io/pipx/):
```console
$ pipx install freakble
```

### Using pip

```console
$ python -m pip install freakble
```

### From source

freakble uses [Poetry](https://python-poetry.org) as dependency management and
packaging tool, you need to install it first.

Then:

1. Clone this repository.
2. From the root of the repository run:
   ```console
   $ poetry build
   ```
3. Install using pipx or pip (it's better to use pipx):
   ```console
   $ pipx install dist/freakble-0.1.0-py3-none-any.whl
   ```

## Usage

```console
Usage: freakble [OPTIONS] COMMAND [ARGS]...

  A simple tool to send messages into FreakWAN.

Options:
  --adapter TEXT  ble adapter  [default: (hci0)]
  --help          Show this message and exit.

Commands:
  deep-scan  Scan to find services of a specific device.
  scan       Scan to find BLE devices.
  send       Send one or more messages over BLE to a specific device.
  version    Scan to find services of a specific device.
```

### send

The `send` command is used to send a message to the board. You need to know the
address of the device.

The complete usage is:
```console
Usage: freakble send [OPTIONS] [WORDS]...

  Send one or more words over BLE to a specific device.

Options:
  --loop              send forever the message
  --device TEXT       ble device address  [required]
  --sleep-time FLOAT  sleep between messages sent with --loop  [default: (1
                      sec)]
  --help              Show this message and exit.
```

For example:

```console
$ freakble send --device AA:AA:AA:AA:AA:AA Hello, there!
```

where you have to substitute `AA:AA:AA:AA:AA:AA` with your device's address.

The `--loop` flag will make freakble to send continuosly the message until
`CTRL + C` is pressed. The resend interval is defaults to 1 sec and can be
changed using `--sleep-time`.

```console
$ freakble send --device AA:AA:AA:AA:AA:AA --loop FREAKNET
```

![A photo of a LYLIGO TTGO LoRa v2 1.6 showing the text: you> FREAKNET in multiple lines.](extras/304f4bb6-4f51-4183-95b9-c329b9bf69ab.jpg)

You can use environment variables to set the device address, for example if one
of your device is called `FreakWAN_vuzasu` you can do:

```console
$ export FREAKBLE_SEND_DEVICE=$(freakble scan | grep FreakWAN_vuzasu | cut -d' ' -f1)
$ freakble send "La violenza è l'ultimo rifugio degli incapaci. - Isaac Asimov"
```

## scan

The `scan` command is used to discover BLE devices.

```console
Usage: freakble scan [OPTIONS]

  Scan to find BLE devices.

Options:
  --scan-time FLOAT    scan duration  [default: (5 secs)]
  --service-uuid TEXT  service UUID used to filter  [default: (None)]
  --help               Show this message and exit.
```

For example:
```
$ freakble scan
AB:AB:AB:AB:AB:AB (RSSI=-52): FreakWAN_timatu
AF:AF:AF:AF:AF:AF (RSSI=-57): FreakWAN_vuzasu
```

Please note that the address are *invented*.

## deep-scan

The `deep-scan` command is used to find services of a specific device.

```
Usage: freakble deep-scan [OPTIONS]

  Scan to find services of a specific device.

Options:
  --device TEXT      ble device address  [required]
  --scan-time FLOAT  scan duration  [default: (5 secs)]
  --help             Show this message and exit.

```

## License

freakble is licensed under BSD-3-Clause license.
