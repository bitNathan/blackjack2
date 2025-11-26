# API Endpoints / Routes
*implemented in controller / routes.py blueprint, which uses service layer to use game logic*

#### POST /games
creates new game
return game.status JSON

#### GET /games/{id}
return game.status JSON

#### POST /games/{id}/action
perform hit or stand
return success or fail

#### POST games/{id}/reset
start new game with same ID
returns game.status

#### DELETE games/{id}

## Later

#### POST /players
creates and returns a player object
persists to database
required to play game
game logic persists winnings / losses to player object without manual call

#### GET /players/{id}
gets player obj ect, stats, and money

#### DELETE /players/{id}
