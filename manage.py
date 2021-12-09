import sys

sys.path.append("app")

import code

import manager as mgr
import models


manager = mgr.Manager()


@manager.command
def init_db():
    models.db.drop_all()
    models.db.create_all()
    print("OK")


@manager.command
def orm():
    code.InteractiveConsole(locals=models.__dict__).interact()


if __name__ == "__main__":
    manager.main()