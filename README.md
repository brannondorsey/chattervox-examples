# Chattervox Examples

A collection of example applications and use cases for the [Chattervox protocol](https://github.com/brannondorsey/chattervox). Created for the _Trust in Waves_ workshop at [WOPR Summit](https://www.woprsummit.org/workshops/) (March 2019).

Examples include:

- [Low-Fi Time Server](#low-fi-time-server): Broadcast a timestamp beacon at regular intervals 
- `weather/`: [A weather broadcast station](#weather-broadcast-station)
- `news-headlines/`: [Broadcast breaking news headlines](#news-headlines)
- [Bash shell](#bash-shell): Use chattervox to control a remote computer via Bash
- [Zork](#zork): Play [the famous text adventure game](https://en.wikipedia.org/wiki/Zork) over packet radio

## Low-fi Time Server

Modern MacOS and Linux distributions come with the `date` command installed. In this example, we'll use the watch command to trigger `date` at a regular interval. We'll then pipe the output from these two commands to `chattervox send` to create a poor man's network time server over packet radio.

Running the `date` command by itself will output:

```bash
date
Mon Feb  4 21:01:52 EST 2019
```

To broadcast a timestamp in this format once per-minute via Chattervox, run:

```bash
watch -n 60 "date | chattervox send"
```

If you'd prefer to broadcast an unformatted unix timestamp (e.g. `1549332349`) once every ten seconds, try this:

```bash
watch -n 10 "date '+%s' | chattervox send"
```

## Weather Broadcast Station

This example uses [OpenWeatherMap.org's](openweathermap.org) free weather API to broadcast real-time weather data for your zip code. `weather/get_weather.py` outputs weather data in the following ASCII format:

```
# temperature, humidity, atmospheric pressure, wind speed and direction, description
48 deg, 84% humidity, 1020 hPa, 3 mph SSW, light rain
```

We can pipe the output of `get_weather.py` to `chattervox send` to broadcast weather information over the radio. We'll use `watch` to run these commands at a regular interval.

```bash
export API_KEY=YYY
# replace this with your zip code, or a zip code of your choice
export ZIP=XXX 
# Broadcast a weather beacon every 30 minutes (1,800 seconds) using chattervox send 
watch -n 1800 "./weather/get_weather.py --zip $ZIP --key $API_KEY | chattervox send"
```

For more information on `get_weather.py`'s usage, run `python3 get_weather.py -h`.

## News Headline Broadcast

This example uses [NewsAPI.org's](https://newsapi.org/) free API to broadcast real-time news headlines from dozens of aggregate news sources. Signing up for a developer account gives you a free API key valid for 1,000 requests a day.

```bash
# replace this with your free NewsAPI.org's key.
export API_KEY=YYY

# get aggregate news headlines by category
./news/get_headlines.py --key $API_KEY --category general --country us
```
```
U.S. Federal District Court Declared Bitcoin As Legal Money - BTCNN
Global warming predicted to melt massive Himalayan glaciers, disrupt food production - USA TODAY
Oceans will change color in less than 100 years, scientists warn - New York Post 
Lobbyist received half a million in Russia-linked deposits around 2016 Trump Tower meeting: report | TheHill - The Hill
Ralph Northam shouldn't resign because of an old photo. He should resign because he's an idiot - Washington Examiner
To protect users’ privacy, iOS 12.2 will limit Web apps’ access to iPhone’s sensors - Ars Technica
Tom Brady and Julian Edelman's Trip to Disney World Is Pretty Super - E! NEWS
Google's capital expenditures doubled in 2018, the fastest growth in at least four years - CNBC
US-South Korea reach agreement over cost of US troops in region - CNN
How Big Beer's Fight Over Corn Syrup Explains American Brewing Today - Mother Jones
The Washington Post went all-in on Brett Kavanaugh but spiked a similar story about a Democrat - Washington Examiner
Alphabet topped revenue targets in Q4 but rising costs spook Wall Street (GOOG, GOOGL) - Markets Insider
```

Top news headlines can be filtered by category including `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`. Headlines can also be filtered by source instead of category like so:

```bash
./news/get_headlines.py --key $API_KEY --source hacker-news
```
```
If Software Is Funded from a Public Source, Its Code Should Be Open Source
Firefox 66 to block automatically playing audible video and audio – Mozilla Hacks - the Web developer blog
'Lambda and serverless is one of the worst forms of proprietary lock-in we've ever seen in the history of humanity'
Matrix at Fosdem 2019
Hacker Tools
Hatari: An Atari ST/STE/TT/Falcon Emulator
Messaging Platform Provider Slack Says It's Filed to Go Public
My Brand New Logo — My Brand New Logo – logo maker | create your own logo
U.S. Federal District Court Declared Bitcoin As Legal Money - BTCNN
A Humility Training Exercise for Technical Interviewers
```

See [here](https://newsapi.org/sources) for a complete list of all 138 news sources.

You'll notice each time you run `news/get_headlines.py` you receive probably receive the same headlines over and over again. While these headlines are updated frequently, they aren't likely going to change within a few minutes. What good is a news broadcast if it just repeats itself over and over again? What we really want to do is broadcast only new news!

We can achieve this by appending every news headline to file, and then use this file to filter out headlines we've already seen each time we run `news/get_headlines.py`. We'll use the `--exclude` command-line argument in combination with the `tee` command to write our output to both `stdout` and append it to the file we load the next time we run the command with `--exclude`. We'll wrap this all up in a `watch` command and prepend a timestamp to each headline with `sed` before using `chattervox send` to broadcast any new headlines every two minutes. 

```bash
# Get the current headlines, filter out anything we've already seen before (news/exclude.txt), prepend a timestamp, and broadcast new headlines via chattervox send
watch -n 120 "./news/get_headlines.py --key $API_KEY --category general --country us --exclude news/exclude.txt | tee -a news/exclude.txt | sed -e \"s/^/$(date): /g\" | chattervox send"
```

## Bash Shell

In this example, we'll use Chattervox's `exec` and `tty` subcommands to launch and interact with a Bash shell. This will allow us to issue bash commands remotely, like `telnet` over packet radio. While it's not encrypted like `ssh`, input to a Bash shell session over chattervox can be restricted to holders of known and trusted key pairs.

### Bash Server

In this example, we'll run a "Bash server" by spawning a Bash process via `chattervox exec`.

```bash
chattervox exec --stderr bash
```

This command does the following:

1. Spawns a Bash shell as a child process of `chattervox`
2. Pipes all received (RX) chattervox messages to Bash's `stdin`
3. Transmits (TX) Bash's `stdout` and `stderr`

`chattervox exec` also reads `stdin` from terminal input in addition to received chattervox messages, so you can type Bash commands like`ls -lha`, `w`, and `ps` directly into the console as well.

```bash
ls -lha
total 44K
drwxrwxr-x  7 braxxox braxxox 4.0K Feb  4 22:24 .
drwxrwxr-x 88 braxxox braxxox 4.0K Feb  4 19:00 ..
drwxrwxr-x  8 braxxox braxxox 4.0K Feb 10 19:45 .git
-rw-rw-r--  1 braxxox braxxox    9 Feb  4 22:00 .gitignore
-rw-rw-r--  1 braxxox braxxox 1.1K Feb  4 22:24 LICENSE
drwxrwxr-x  2 braxxox braxxox 4.0K Feb  4 22:13 news
-rw-rw-r--  1 braxxox braxxox 7.0K Feb 10 19:45 README.md
drwxrwxr-x  2 braxxox braxxox 4.0K Feb  2 17:18 .vscode
drwxrwxr-x  2 braxxox braxxox 4.0K Feb  2 17:31 weather
drwxrwxr-x  3 braxxox braxxox 4.0K Feb  3 15:17 zork

w
 19:47:43 up 1 day,  8:10,  1 user,  load average: 0.52, 0.48, 0.47
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
braxxox  tty7     :0               Sat11   32:07m  9:30   1.75s /sbin/upstart --user

ps
  PID TTY          TIME CMD
 5297 pts/6    00:00:00 bash
18748 pts/6    00:00:00 node
18758 pts/6    00:00:00 bash
18802 pts/6    00:00:00 ps
```

Your personal computer can be a scary place to open an experimental shell like this. If you have docker installed, and would prefer to create a Bash shell inside a temporary docker container, instead of your PC, you can do so like this:

```bash
# download the latest debian image
docker pull debian

# run bash inside a temporary debian docker container
chattervox exec --stderr "docker run --rm -i debian bash"
```

### Bash Client

In order to interface with our "Bash server" over the Chattervox protocol, we'll need to use Chattervox's `tty` subcommand on another computer. For this to work properly, both machines should have eachother's keys saved via `chattervox addkey`.

```
chattervox tty
```

This command acts like a teletype interface; Anything typed to the console is broadcast once a newline character is detected, and anything received is printed to the screen.

> __Note__: If you are expecting to see output from a packet sent to a `chattervox exec` or `chattervox tty` command, but are not, try running both commands with the `--allow-all` flag. Received messages may be unexpectedly filtered if they are coming from an unknown or invalid sender.


## Zork

This example allows you to play Zork I between two computers over packet radio, in true timesharing fashion! Originally written for a DEC PDP-10 in 1977, and then later released by [Infocom](http://infocom-if.org) in 1980, Zork is one of the earliest and most famous text adventure games. We'll use Docker to run the game from a "mainframe" computer and play it via another computer acting as a "dumb terminal".

![Zork I packaging](.images/zork.jpg)

> Infocom's packaging of Zork I

![PDP-10 Image](.images/PDP-10_1090.jpg)

> KL10-DA 1090 CPU and 6 Memory Modules. This mainframe is a member of the PDP-10 family of computers.

### The "Mainframe"

On one computer, we'll download and run zork from a docker container, using `chattervox exec`. This command will launch Zork using the [frotz Z-machine interpreter](https://github.com/DavidGriffith/frotz) using chattervox data packets as its input and output.

```bash
# download the Zork docker image
docker pull brannondorsey/zork

# run Zork I with chattervox exec. This container runs the frotz Infocom emulator
# with the following docker flags:
# --init: helps the frotz process catch signals and reaps child processes
# -i: keep STDIN open even if not attached
# --rm: remove the docker container on exit
# -v: create a ~/.zork_save/ directory on your host system and share it with the 
#     docker container so that zork save files can persist across containers
chattervox exec "docker run --init -i --rm -v $HOME/.zork_saves:/save brannondorsey/zork"
```

The following text should be transmitted by chattervox and printed to the screen.

```
ZORK I: The Great Underground Empire
Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.
ZORK is a registered trademark of Infocom, Inc.
Revision 88 / Serial number 840726

West of House
You are standing in an open field west of a white house, with a boarded front
door.
There is a small mailbox here.

>
```

You can enter commands directly from this terminal, but that's not nearly as fun as actually playing the game from a remote computer.

### The "Dumb Terminal"

We'll communicate with the "mainframe" machine that's running Zork via Chattervox's `tty` subcommand running on another computer. 

```bash
# run this on another computer that's also got a radio and Chattervox installed
chattervox tty
```

The commands you enter in this terminal will now be broadcast to the computer running Zork, and the responses will be sent back and printed to the screen.

```
open mailbox
open mailbox # this repeated input text is normal
Opening the small mailbox reveals a leaflet.


read leaflet
read leaflet
(Taken)
"WELCOME TO ZORK!

ZORK is a game of adventure, danger, and low cunning. In it you will explore
some of the most amazing territory ever seen by mortals. No computer should be
without one!"
```

<!-- ### Alternative Install
hat

```bash
# Debian install
sudo apt-get install frotz
mkdir zork1 && cd zork1
curl http://www.infocom-if.org/downloads/zork1.zip > zork1.zip
unzip zork1.zip && rm zork1.zip


chattervox exec "frotz zork_files/DATA/ZORK1.DAT"
``` -->

