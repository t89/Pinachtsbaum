# Pinachtsbaum

Get the most out of your [3D Xmas Tree](https://thepihut.com/products/3d-xmas-tree-for-raspberry-pi).

![3D Xmas Tree](https://cdn.shopify.com/s/files/1/0176/3274/products/IMG_0673_1024x1024.JPG?v=1510937356 "Xmas Trees")


## Features:
* Easy, transparent & automatic installation process
* Mappings: Access each LED by the pcb-number, bei height, quarter & side
* Simple On / Off
* Illuminate with delay, auto-off
* Dim over time, dim from any value to any value, auto-reversable
* Ping a random LED, fill tree in random order
* Blinking: Interval, Speed
* Swirl: Speed, chain length
* Key press listener
* Random, Random for Beat (BPM)
* Increase, decrease brightness


## Getting Started

### Prerequisites

This repository will provide everything you need to run neat looking effects on your tree in no time. Runs on any raspberry pi and Linux based OS. Just follow the instructions:


### Installing
Depending on the system installed on your Raspberry Pi, it may not have `git` preinstalled. We start by assuring that `git` is available:

```
sudo apt-get install git
```

Now we clone this project:
```
git clone https://github.com/Beulenyoshi/Pinachtsbaum
```

Run the `install.sh` file:
```
bash install.sh
```
(We use `bash` instead of `sh` because we require some bash functionality)

### Run
For a little demo execute the xmas.py file:
```
python xmas.py
```

(You may have to run this as root for GPIO access):
```
sudo python xmas.py
```

Edit with your favourite editor:
```
vim xmas.py
```


## Built With

* [Vim](http://www.vim.org) - Editor / IDE
* [Git](https://git-scm.com) - Version Control
* [Tmux](https://tmux.github.io) - Terminal Multiplexer (Godsend when it comes to ssh-ing into the Pi)

## Authors

* **Thomas Johannesmeyer** - [www.geeky.gent](http://geeky.gent)

## License

This project is licensed under the Beerware License - see the [LICENSE](LICENSE) file for details
