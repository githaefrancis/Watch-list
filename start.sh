#!/bin/bash
export MOVIE_API_KEY='48720892484f348bfcc60f5eeb524a7b'

export SECRET_KEY='\xe5\x08\xcf`\xdan\xe7\xe2\t\x8d\xb7\xfd/N\xdb\x1e{\xfc`\xf2\x15\x1a8\x82'
export FLASK_APP=manage.py 


# flask shell
flask run
# flask test
# export FLASK_ENV=development
#flask db init

#flask db migrate -m 'migrate message'

#flask db upgrade

#db Error target-database-is-not-up-to-date

# $ flask db stamp head  # To set the revision in the database to the head, without performing any migrations. You can change head to the required change you want.
# $ flask db migrate     # To detect automatically all the changes.
# $ flask db upgrade     # To apply all the changes.