# Chattervox Examples

A collection of example applications and use cases for the [Chattervox protocol](https://github.com/brannondorsey/chattervox). Created for the _Trust in Waves_ workshop at [WOPR Summit](https://www.woprsummit.org/workshops/) (March 2019).

Examples include:

- Low-Fi Time Server: Broadcast a timestamp beacon at regular intervals 
- `weather/`: [A weather broadcast station](#weather-broadcast-station)
- `news-headlines/`: [Broadcast breaking news headlines](#news-headlines)

## Low-fi Time Server

Modern MacOS and Linux distributions come with the `date` command installed. In this example, we'll use the watch command to trigger `date` at a regular interval. We'll then pipe the output from these two commands to `chattervox send` to create a poor man's network time server over packet radio.

Running the `date` command by itself will output:

```bash
date
Mon Feb  4 21:01:52 EST 2019
```

To broadcast a timestamp in this format once per-minute via Chattervox, run:

```bash
watch -n 60 date | chattervox send
```

If you'd prefer to broadcast an unformatted unix timestamp (e.g. `1549332349`) once every ten seconds, try this:

```bash
watch -n 10 "date '+%s'" | chattervox send
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

We can achieve this by appending every news headline we've ever seen to a file, and then use this file to filter out headlines we've already seen each time we run `news/get_headlines.py`. We'll use the `--exclude` command-line argument in combination with the `tee` command to write our output to both `stdout` and append it to the file we load with `--exclude`. We'll wrap this all up in a `watch` command and pipe the input to `chattervox send` to broadcast any new headlines every two minutes. 

```bash
# Get the current headlines, filter out anything we've already seen before (news/exclude.txt), and broadcast new headlines via chattervox send
watch -n 120 "./news/get_headlines.py --key $API_KEY --category general --country us --exclude news/exclude.txt | tee -a news/exclude.txt" | chattervox send
```

<!-- ## Zork

### Download and Install

```bash
# Debian install
sudo apt-get install frotz
mkdir zork1 && cd zork1
curl http://www.infocom-if.org/downloads/zork1.zip > zork1.zip
unzip zork1.zip && rm zork1.zip
```

```bash
# in one terminal
mkfifo /tmp/pipe
frotz zork_files/DATA/ZORK1.DAT < /tmp/pipe

# in another terminal
echo "open mailbox" > /tmp/pipe
``` -->

