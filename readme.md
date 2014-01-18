Minecraft Log Parser
=====================
MCLP is a simple Python script that can generate statistics about a Minecraft server based on it's `server.log` file.
This was a fun project to just make something. Some parts are really messy, we have an experienced coder and a very inexperienced coder.
There will be some cleaning up, but for now, it's just something that works.

## Current Features
 * Calculates total time played for each player.
 * Shows deaths and deaths burndown
 * Supports displaying userskins when you add them to the folder playerskins (150x150px)
 * Supports displaying monsters when you add their pictures to the folder images
 * Generates a stats.html in the html directory which you can display on a webserver.
 * When you run Dynmap you can config mc_settings. It enables you to chat "!deaths" and get an answer ingame!

I'm open to suggestions. If you have an idea for a statistic that could be generated feel free to suggest it in the issue tracker. If you're feeling extra generous, you could always implement a feature on your own and submit a pull request!

Run:
mclp /path/to/server.log

Then you should see some neat statistics show up!

!The program acts like a daemon, it will keep reading the log. So run it in a screen session or alternative.

## Credits
Original fork from https://github.com/stevenleeg/Minecraft-Log-Parser

## License
Minecraft Log Parser is released under the [MIT License](http://opensource.org/licenses/MIT). Have fun and make awesome things with it!
