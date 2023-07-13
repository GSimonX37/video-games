# backloggd.сsv
Data obtained by extracting them from the pages of a web resource **[backloggd.com](https://www.backloggd.com/)** using your own written parser program.

## О веб-ресурсе backloggd.com
"**Backloggd** is a place to keep your personal video game collection. Every game from every platform is here for you to log into your journal. Follow friends along the way to share your reviews and compare ratings. Then use filters to sort through your collection and see what matters to you. Keep a backlog of what you are currently playing and what you want to play, see the numbers change as you continue to log your playthroughs. There's Goodreads for books, Letterboxd for movies, and now Backloggd for games.

All game related metadata comes from the community driven database **[IGDB](https://www.igdb.com/)**. This includes all game, company and platform data you see on the site." - from the site **[backloggd.com](https://www.backloggd.com/)**."

## About the dataset
### Dataset fields
- **name** - video game name;
- **date** - video game release date;
- **developers** - list of video game developers;
- **rating** - video game rating;
- **platforms** - list of gaming platforms for which the game was released;
- **genres** - list of video game genres;
- **category** - video game release category (main game, DLS, mod, addon, expansion, remake, etc.);
- **main** - name of the main video game (if the game is the main one, this field will duplicate the "name" field);
- **reviews** - the number of reviews for this video game;
- **plays** - the number of players who have played this game for all time;
- **playing** - number of players currently playing (as of 06/01/2023);
- **backlogs** - number of users who added this game to backlogs;
- **wishlists** - number of users who added this game to wishlists;
- **description** - video game description.

[Project information](../README.md)