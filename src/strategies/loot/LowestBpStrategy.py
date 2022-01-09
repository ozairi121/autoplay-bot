from typing import List
from src.libs.CrabadaWeb2Client.types import Game, Team
from src.strategies.loot.LootStrategy import LootStrategy
from src.helpers.General import firstOrNone

class LowestBpStrategy(LootStrategy):
    """
    Looting strategy that chooses the mine with the lowest
    defense points
    """

    def query(self, team: Team) -> List[Game]:
        return {
            "can_loot": 1,
            "status": "open",
            "looter_address": team["owner"],
            "limit": 200, # TODO: make it an argument
            "orderBy": 'game_id',
            "order": 'desc',
        }

    def mine(self, team: Team, list: List[Game]) -> Game:
        attackableMines = [ m for m in list if m["defense_point"] < team["battle_point"] ]
        if len(attackableMines) == 0:
            return None
        sortedAttackableMines = sorted(attackableMines, key=lambda m: (m['defense_point'], m['defense_mine_point']))
        return firstOrNone(sortedAttackableMines)