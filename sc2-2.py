from sc2.bot_ai import BotAI #parent ai class that youll inherit from
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2 import maps
from sc2.ids.unit_typeid import UnitTypeId
import random

class RobotBot(BotAI):
    async def on_step(self, iteration:int):
        print(f"{iteration}, n_workers: {self.workers.amount}, n_idle_workers: {self.workers.idle.amount},", \
			f"minerals: {self.minerals}, gas: {self.vespene}, cannons: {self.structures(UnitTypeId.PHOTONCANNON).amount},", \
			f"pylons: {self.structures(UnitTypeId.PYLON).amount}, nexus: {self.structures(UnitTypeId.NEXUS).amount}", \
			f"gateways: {self.structures(UnitTypeId.GATEWAY).amount}, cybernetics cores: {self.structures(UnitTypeId.CYBERNETICSCORE).amount}", \
			f"stargates: {self.structures(UnitTypeId.STARGATE).amount}, voidrays: {self.units(UnitTypeId.VOIDRAY).amount}, supply: {self.supply_used}/{self.supply_cap}")

        
        await self.distribute_workers()
        
        if self.townhalls:
            nexus = self.townhalls.random
            
            if self.structures(UnitTypeId.VOIDRAY).amount<15 and self.can_afford(UnitTypeId.VOIDRAY):
                for sg in self.structures(UnitTypeId.STARGATE).ready.idle:
                    sg.train(UnitTypeId.VOIDRAY)
            
            
            if nexus.is_idle and self.can_afford(UnitTypeId.PROBE) and self.workers.amount<24:
                    nexus.train(UnitTypeId.PROBE)
            elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0:
                if self.can_afford(UnitTypeId.PYLON):
                    await self.build(UnitTypeId.PYLON, near=nexus)
                    
            elif self.structures(UnitTypeId.PYLON).amount<5:
                if self.can_afford(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0:
                    target_pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
                    pos = target_pylon.position.towards(self.enemy_start_locations[0], random.randrange(1,3))
                    await self.build(UnitTypeId.PYLON, near=pos)
            
            elif self.structures(UnitTypeId.ASSIMILATOR).amount <=1:
                vespenes = self.vespene_geyser.closer_than(15, nexus)
                for vespene in vespenes:
                    if self.can_afford(UnitTypeId.ASSIMILATOR) and not self.already_pending(UnitTypeId.ASSIMILATOR):
                        await self.build(UnitTypeId.ASSIMILATOR,vespene)
            
            elif not self.structures(UnitTypeId.FORGE):
                if self.can_afford(UnitTypeId.FORGE) and not self.already_pending(UnitTypeId.FORGE):
                    await self.build(UnitTypeId.FORGE, near=self.structures(UnitTypeId.PYLON).closest_to(nexus))
            elif self.structures(UnitTypeId.FORGE).ready and self.structures(UnitTypeId.PHOTONCANNON).amount < 4:
                if self.can_afford(UnitTypeId.PHOTONCANNON):
                    await self.build(UnitTypeId.PHOTONCANNON, near = nexus)
                    
                    
            buildings = [UnitTypeId.GATEWAY, UnitTypeId.CYBERNETICSCORE, UnitTypeId.STARGATE]
            
            for building in buildings:
                if not self.structures(building) and self.already_pending(building) == 0:
                    if self.can_afford(building):
                        await self.build(building, near=self.structures(UnitTypeId.PYLON).closest_to(nexus))
                    break
                    
            
            
        else:
            if self.can_afford(UnitTypeId.NEXUS):
                await self.expand_now()
                
                
        if self.units(UnitTypeId.VOIDRAY).amount >= 5:
            if self.enemy_units:
                for vr in self.units(UnitTypeId.VOIDRAY).idle:
                    vr.attack(random.choice(self.enemy_units))
            elif self.enemy_structures:
                for vr in self.units(UnitTypeId.VOIDRAY).idle:
                    vr.attack(random.choice(self.enemy_structures))
            else:
                for vr in self.units(UnitTypeId.VOIDRAY).idle:
                    vr.attack(self.enemy_start_locations[0])
        
run_game(
            maps.get("2000AtmospheresAIE"),
            [Bot(Race.Protoss, RobotBot()),
            Computer(Race.Terran, Difficulty.Hard)],
            realtime=False
            
)            