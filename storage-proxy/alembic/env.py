from app.database import Base, engine
from app import models

def run_migrations_offline():
    # offline mode
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=Base.metadata)
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # online mode
    connectable = engine.connect()
    context.configure(connection=connectable, target_metadata=Base.metadata)
    
    with context.begin_transaction():
        context.run_migrations()
