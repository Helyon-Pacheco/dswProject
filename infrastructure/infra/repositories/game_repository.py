from domain.core.models.game import Game
from infrastructure.infra.repositories.repository import Repository


class GameRepository(Repository[Game]):
    def __init__(self, session, notifier):
        super().__init__(session, notifier, Game)
