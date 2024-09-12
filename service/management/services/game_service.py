from typing import Optional, List
from uuid import UUID
from domain.core.models.game import Game
from infrastructure.infra.db.models.game_db_model import GameDBModel
from infrastructure.infra.repositories.game_repository import GameRepository


class GameService:
    def __init__(self, game_repository: GameRepository):
        self._game_repository = game_repository

    async def get_game_by_id(self, game_id: UUID) -> Optional[Game]:
        game_db = await self._game_repository.get_by_id(game_id)
        if game_db:
            return Game.from_orm(game_db)
        return None

    async def get_all_games(self) -> List[Game]:
        games_db = await self._game_repository.get_all()
        return [Game.from_orm(game) for game in games_db]

    async def create_game(self, game_data: Game) -> Game:
        game_db = GameDBModel(**game_data.dict())
        await self._game_repository.add(game_db)
        return Game.from_orm(game_db)

    async def update_game(self, game_id: UUID, game_data: Game) -> Optional[Game]:
        game_db = await self._game_repository.get_by_id(game_id)
        if game_db:
            for key, value in game_data.dict(exclude_unset=True).items():
                setattr(game_db, key, value)
            await self._game_repository.update(game_db)
            return Game.from_orm(game_db)
        return None

    async def delete_game(self, game_id: UUID) -> bool:
        game_db = await self._game_repository.get_by_id(game_id)
        if game_db:
            await self._game_repository.delete(game_db)
            return True
        return False
