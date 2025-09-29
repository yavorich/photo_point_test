from itertools import chain

from apps.accounts.endpoints import handlers as accounts_handlers


handlers = list(
    chain(
        accounts_handlers,
    )
)
