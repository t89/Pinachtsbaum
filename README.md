# Pinachtsbaum

![Pinachtsbaum Icon](./misc/Icon.png "Pinachtsbaum-Icon")

Get the most out of your [3D Xmas Tree](https://thepihut.com/products/3d-xmas-tree-for-raspberry-pi).

![3D Xmas Tree](https://cdn.shopify.com/s/files/1/0176/3274/products/IMG_0673_1024x1024.JPG?v=1510937356 "Xmas Trees")


## Features:
* Easy, transparent & automatic installation process
* Mappings: Access each LED by the pcb-number, by height, quarter & side
* Simple on / off
* Illuminate with delay, auto-off
* Dim over time, dim from any value to any value, auto-reversible
* Ping a random LED, fill tree in random order
* Blinking: Interval, Speed
* Swirl: Speed, chain length
* Key press listener
* Random, Random for Beat (BPM)
* Increase, decrease brightness
* Ambient Glow
* Advent-Calendar illuminates one LED for each day of December
* Network access using a reworked [Strinder](https://github.com/Beulenyoshi/Strinder) implementation


## Getting Started

### Prerequisites

This repository will provide everything you need to run neat looking effects on your tree in no time. Runs on any raspberry pi and Linux based OS. Just follow the instructions:


### Installing
Depending on the system installed on your Raspberry Pi, it may not have `git` preinstalled. We start by assuring that `git` is available:

```bash
sudo apt-get install git
```

Now we clone this project:
```bash
git clone https://github.com/Beulenyoshi/Pinachtsbaum
```

Run the `install.sh` file:
```bash
bash install.sh
```
(We use `bash` instead of `sh` because we require some bash functionality)

### Run
For a little demo execute the xmas.py file:
```bash
python xmas.py
```

(You may have to run this as root for GPIO access):
```bash
sudo python xmas.py
```

Edit with your favourite editor:
```bash
vim xmas.py
```

### Run via Network

1. Start the server on your Raspberry:
```bash
sudo python Strinder/Server.py
```

2. Clone this project onto your controlling machine
3. Open `Strinder/Client.py` and replace the host ip address with your pi's:
```python
HOST = "192.168.2.107"        # Insert HOST IP / name here
```

4. Now you can send commands to the server like this:
```bash
python Strinder/Client.py "YOUR COMMAND"
```

**Predefined Commands:**

- STOP_SERVER - Stops Server
- BREAK_LOOP - Breaks loops running on background thread within the tree
* ON - Switches every LED on
* OFF - Switches every LED off
* FLUSH - Runs a top-down swirl, leaving the tree off
* AMBIENT_GLOW - Starts ambient glow (Stop using BREAK_LOOP)
* PING - Pings a random LED for 0.2 seconds
* ADVENT - Illuminates one LED for each day of December (Stop using BREAK_LOOP)
* ADD_RANDOM - Illuminate random LED until the tree is filled

You can write your own commands! Take a look inside the `Strinder/Server.py` implementation

## Built With

* [Vim](http://www.vim.org) - Editor / IDE
* [Git](https://git-scm.com) - Version Control
* [Tmux](https://tmux.github.io) - Terminal Multiplexer (Godsend when it comes to ssh-ing into the Pi)

## Authors

* **Thomas Johannesmeyer** - [www.geeky.gent](http://geeky.gent)

## License

This project is licensed under the Beerware License - see the [LICENSE](LICENSE) file for details

## Support

The framework and code is provided as-is, but if you need help or have suggestions, you can contact me anytime at [opensource@geeky.gent](mailto:opensource@geeky.gent?subject=Pinachtsbaum).


## I'd like to hear from you

If you come up with some neat patterns for your tree, feel free to share them with me. :)
