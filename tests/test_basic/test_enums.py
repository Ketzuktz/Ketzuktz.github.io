import gicg_sim
import pytest

class TestEnums:
    def check_two_enums(self, enum1, enum2):
        enum1_keys = {e.name for e in enum1}
        enum2_keys = {e.name for e in enum2}
        
        common_keys = enum1_keys & enum2_keys
        for key in common_keys:
            assert enum1[key].value == enum2[key].value
        
    
    def test_element(self):
        self.check_two_enums(gicg_sim.enums.ElementType, gicg_sim.enums.DieType)
        self.check_two_enums(gicg_sim.enums.ElementType, gicg_sim.enums.CostType)