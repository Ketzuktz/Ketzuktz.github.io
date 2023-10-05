from gicg_sim.basic.character import CharacterPrototype


class Character:
    def __init__(self, prototype: CharacterPrototype) -> None:
        self._prototype = prototype
        self.hp: int = self.max_HP
        self.energy: int = self.max_energy
        
        self._skills: list[dict] = self._prototype.skills
        
    @property
    def name(self) -> str:
        return self._prototype.name
    
    @property
    def rarity(self) -> int:
        return self._prototype.rarity
    
    @property
    def element(self) -> str:
        return self._prototype.element
    
    @property
    def weapon(self) -> str:
        return self._prototype.weapon
    
    @property
    def max_HP(self) -> int:
        return self._prototype.max_HP
    
    @property
    def max_energy(self) -> int:
        return self._prototype.max_energy