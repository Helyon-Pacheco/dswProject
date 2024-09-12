from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from infrastructure.infra.db.session import get_db
from service.management.services.game_service import GameService
from infrastructure.infra.repositories.game_repository import GameRepository
from domain.core.models.game import Game


router = APIRouter()

@router.get("/", response_model=List[Game])
async def get_games(db=Depends(get_db)):
    game_service = GameService(GameRepository(db))
    games = await game_service.get_all_games()
    return games

@router.get("/{game_id}", response_model=Game)
async def get_game_by_id(game_id: UUID, db=Depends(get_db)):
    game_service = GameService(GameRepository(db))
    game = await game_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game

@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_new_game(game: Game, db=Depends(get_db)):
    game_service = GameService(GameRepository(db))
    new_game = await game_service.create_game(game)
    return new_game

@router.put("/{game_id}", response_model=Game)
async def update_game_details(game_id: UUID, game: Game, db=Depends(get_db)):
    game_service = GameService(GameRepository(db))
    updated_game = await game_service.update_game(game_id, game)
    if not updated_game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return updated_game

@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_game(game_id: UUID, db=Depends(get_db)):
    game_service = GameService(GameRepository(db))
    success = await game_service.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
