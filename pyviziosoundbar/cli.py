import logging
import click
import sys
import pyviziosoundbar

if sys.version_info < (3, 4):
    print("To use this script you need python 3.4 or newer, got %s" %
          sys.version_info)
    sys.exit(1)

_LOGGER = logging.getLogger(__name__)
DEVICE_ID = "pyviziosoundbar"
DEVICE_NAME = "Python Vizio Sound Bar"

pass_soundbar = click.make_pass_decorator(pyviziosoundbar.VizioSoundBar)


@click.group(invoke_without_command=False)
@click.option('--ip', envvar="VIZIO_SOUNDBAR_IP", required=True)
@click.pass_context
def cli(ctx, ip):
    logging.basicConfig(level=logging.INFO)
    ctx.obj = pyviziosoundbar.VizioSoundBar(DEVICE_ID, ip, DEVICE_NAME)

@cli.command()
def discover():
    logging.basicConfig(level=logging.INFO)
    devices = pyviziosoundbar.VizioSoundBar.discovery()
    log_data = "Available devices:" \
               "\nIP\tModel\tFriendly name"
    for dev in devices:
        log_data += "\n{0}\t{1}\t{2}".format(dev.ip, dev.model, dev.name)
    _LOGGER.info(log_data)

@cli.command()
@pass_soundbar
def input_list(viziosoundbar):
    inputs = viziosoundbar.get_inputs()
    if inputs is None:
        return
    log_data = "Available inputs:"
    for v_input in inputs:
        log_data += "\n{0}".format(v_input.name)

    _LOGGER.info(log_data)

@cli.command()
@pass_soundbar
def input_current(viziosoundbar):
    data = viziosoundbar.get_current_input()
    if data is not None:
        _LOGGER.info("Current input: %s", data.meta_name)

@cli.command()
@click.argument("state", required=False)
@pass_soundbar
def power(viziosoundbar, state):
    if state:
        if "on" == state:
            txt = "Turning ON"
            result = viziosoundbar.power_on()
        elif "off" == state:
            txt = "Turning OFF"
            result = viziosoundbar.power_off()
        else:
            txt = "Toggling power"
            result = viziosoundbar.power_toggle()
        _LOGGER.info(txt)
        _LOGGER.info("OK" if result else "ERROR")

    else:
        is_on = viziosoundbar.get_power_state()
        _LOGGER.info("SoundBar is on" if is_on else "SoundBar is off")

@cli.command()
@click.argument("state", required=False)
@click.argument("amount", required=False)
@pass_soundbar
def volume(viziosoundbar, state, amount):
    if not amount:
        amount = 1
    else:
        amount = int(amount)
    if not state:
        state = "up"
    if "up" == state:
        txt = "Increasing volume"
        result = viziosoundbar.vol_up(amount)
    else:
        txt = "Decreasing volume"
        result = viziosoundbar.vol_down(abs(amount))
    _LOGGER.info(txt)
    _LOGGER.info("OK" if result else "ERROR")

@cli.command()
@pass_soundbar
def volume_current(viziosoundbar):
    data = viziosoundbar.get_current_volume()
    if data is not None:
        _LOGGER.info("Current volume: %s", data)

@cli.command()
@click.argument("state", required=False)
@click.argument("num_times", required=False)
@pass_soundbar
def remotekey(viziosoundbar, state, num_times):
    if not num_times:
        num_times = 1
    result = viziosoundbar.remotekey(state, int(num_times))
    _LOGGER.info(state)
    _LOGGER.info("OK" if result else "ERROR")

@cli.command()
@click.argument("state", required=False)
@pass_soundbar
def mute(viziosoundbar, state):
    if "on" == state:
        txt = "Muting"
        result = viziosoundbar.mute_on()
    elif "off" == state:
        txt = "Un-muting"
        result = viziosoundbar.mute_off()
    else:
        txt = "Toggling mute"
        result = viziosoundbar.mute_toggle()
    _LOGGER.info(txt)
    _LOGGER.info("OK" if result else "ERROR")

# @cli.command()
# @pass_soundbar
# def input_next(viziosoundbar):
#     result = viziosoundbar.input_next()
#     _LOGGER.info("Cycling input")
#     _LOGGER.info("OK" if result else "ERROR")

@cli.command(name="input")
@click.argument('name', required=True)
@pass_soundbar
def input_set(viziosoundbar, name):
    result = viziosoundbar.input_switch(name)
    _LOGGER.info("Switching input")
    _LOGGER.info("OK" if result else "ERROR")

@cli.command()
@pass_soundbar
def play(viziosoundbar):
    result = viziosoundbar.play()
    _LOGGER.info("OK" if result else "ERROR")

@cli.command()
@pass_soundbar
def pause(viziosoundbar):
    result = viziosoundbar.pause()
    _LOGGER.info("OK" if result else "ERROR")

# @cli.command()
# @pass_soundbar
# def next(viziosoundbar):
#     result = viziosoundbar.next_track()
#     _LOGGER.info("OK" if result else "ERROR")

# @cli.command()
# @pass_soundbar
# def previous(viziosoundbar):
#     result = viziosoundbar.previous_track()
#     _LOGGER.info("OK" if result else "ERROR")

if __name__ == "__main__":
    cli()
