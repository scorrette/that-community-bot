# ECE Bot

The ECE discord bot is currently being designed to fit some odds and ends of features the ECE community may want on the discord server.

## Usage

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages to run the bot.

```bash
pip3 install -U discord.py
pip3 install -U python-dotenv
```
Create a `.env` file in the same directory as the code that contains the following information:
```
DISCORD_TOKEN=<discord-bot-token>
DATABASE=<path-to-db-file>
```
Where `<discord-bot-token>` would be replaced with your particular bot token.
Where `<path-to-db-file>` would be replaced with a local path to where you would like the database file to be saved.

Then run `bot.py` using `python3 bot.py`

## Contributing
If you are currently a member of the ECE discord and would like to contribute, please look for any currently open issues or submit a pull request with a feature you would like to have added!