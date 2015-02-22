# restack

[![Build Status](https://travis-ci.org/lepoetemaudit/restack.svg?branch=master)](https://travis-ci.org/lepoetemaudit/restack)

A python API for working with Restack, the smart API for IoT

*N.B. This is an early WIP and is not currently useful*

## Usage

```python
from restack import Restack, Device

AUTH_TOKEN = "ae0739cbd09309abec093410aebff70934"

if __name__ == '__main__':

    # Create our authorized connection
    restack = Restack(AUTH_TOKEN)

    # Create a new device
    device = Device(conn=restack)
    device.name = "Test"
    device.description = "Test device"

    print(device)
    # Outputs: <Restack:Device id= name='Test'>

    # Save the device and get the updated version with the identifier
    device.save()
    # Outputs: <Restack:Device id=927372c2be0f47c8b152cdbc09736c0d name='Test'>

    # Get devices belonging to this user
    devices = restack.get_devices()

    # Get the first in the list of devices
    device = devices[0]
    device.name = "Temperature Sensor"

    # Update this device
    device.save()

    print(device)
    # Outputs: <Restack:Device id=927372c2be0f47c8b152cdbc09736c0d name='Temperature Sensor'>

    # Delete this device
    device.delete()

    # Get device by id
    device = restack.get_device("597ac68cd5ff4f97834bd8adb4b3eff1")

    # Get all stacks available on this device
    stacks = device.get_stacks()

    # Create a new stack on this device
    stack = device.create_stack(name="new_stack", unit="Tests", symbol="UT", stack_type=Stack.NUMERIC)

    # Add data to this stack
    stack.put_data(random.randint(1, 100))
```




