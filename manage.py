import os
from app import create_app
from app import create_app,db
from flask_migrate import Migrate
from app.models import User,Role,Review

app=create_app('development')

migrate=Migrate()
migrate.init_app(app,db)


@app.cli.command()
def test():
  """Run the unit tests"""
  import unittest
  tests=unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)


@app.shell_context_processor
def make_shell_context():
  return dict(app=app,db=db,User=User,Role=Role,Review=Review)

if __name__ == '__main__':
  app.run()