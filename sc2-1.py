from sc2.bot_ai import BotAI #parent ai class that youll inherit from
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps

class RobotBot(BotAI):
    async def on_step(self, iteration:int):
        print(f"The iteration is {iteration}")
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
        
run_game(
            maps.get("2000AtmospheresAIE"),
            [Bot(Race.Protoss, RobotBot()),
            Computer(Race.Zerg, Difficulty.Hard)],
            realtime=False
            
)            