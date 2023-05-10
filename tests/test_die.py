import random
import unittest

from gicg_sim.die import DieState, element_names


def create_random_die(low: int = 0, high: int = 10):
    kwargs = dict((en, random.randint(low, high)) for en in element_names)
    return DieState(**kwargs)


class TestDieState(unittest.TestCase):
    def setUp(self):
        self.die_state = DieState()

    def test_omni(self):
        self.die_state.Omni = 5
        self.assertEqual(self.die_state.Omni, 5)

    def test_pyro(self):
        self.die_state.Pyro = 3
        self.assertEqual(self.die_state.Pyro, 3)

    def test_hydro(self):
        self.die_state.Hydro = 2
        self.assertEqual(self.die_state.Hydro, 2)

    def test_anemo(self):
        self.die_state.Anemo = 4
        self.assertEqual(self.die_state.Anemo, 4)

    def test_electro(self):
        self.die_state.Electro = 1
        self.assertEqual(self.die_state.Electro, 1)

    def test_dendro(self):
        self.die_state.Dendro = 0
        self.assertEqual(self.die_state.Dendro, 0)

    def test_cryo(self):
        self.die_state.Cryo = 2
        self.assertEqual(self.die_state.Cryo, 2)

    def test_geo(self):
        self.die_state.Geo = 6
        self.assertEqual(self.die_state.Geo, 6)

    def test_addition(self):
        die_state1 = DieState(Omni=2, Pyro=3, Hydro=1)
        die_state2 = DieState(Omni=1, Pyro=2, Hydro=4)
        result = die_state1 + die_state2
        self.assertEqual(result.Omni, 3)
        self.assertEqual(result.Pyro, 5)
        self.assertEqual(result.Hydro, 5)

    def test_subtraction_1(self):
        die_state1 = DieState(Omni=5, Pyro=3, Hydro=2)
        die_state2 = DieState(Omni=2, Pyro=1, Hydro=1)
        result = die_state1 - die_state2
        self.assertEqual(result.Omni, 3)
        self.assertEqual(result.Pyro, 2)
        self.assertEqual(result.Hydro, 1)

    def test_subtraction_2(self):
        die_state1 = DieState(Omni=5, Pyro=3, Hydro=2)
        die_state2 = DieState(Omni=2, Pyro=1, Hydro=1)
        result = die_state1 - die_state2
        self.assertEqual(result.Omni, 3)
        self.assertEqual(result.Pyro, 2)
        self.assertEqual(result.Hydro, 1)

    def test_subtraction_exception(self):
        DieState(Omni=2, Pyro=3, Hydro=1)
        DieState(Omni=4, Pyro=2, Hydro=3)
        with self.assertRaises(AssertionError):
            pass

    def test_comparison(self):
        die_state1 = create_random_die()

        for en in element_names:
            die_state2 = die_state1.copy()
            value = getattr(die_state2, en)
            setattr(die_state2, en, value + 1)

            self.assertFalse(die_state1 > die_state2)
            self.assertFalse(die_state1 < die_state2)
            self.assertLessEqual(die_state1, die_state2)

        die_state2 = die_state1.copy()
        for i in range(len(die_state2.die_count)):
            die_state2.die_count[i] = die_state2.die_count[i] + 1

        for en in element_names:
            die_state3 = die_state2.copy()
            value = getattr(die_state3, en)
            setattr(die_state3, en, value + 1)

            self.assertFalse(die_state1 > die_state2)
            self.assertLess(die_state1, die_state2)
            self.assertLessEqual(die_state1, die_state2)

    def test_invalid_die_count(self):
        with self.assertRaises(AssertionError):
            self.die_state.Omni = -1


if __name__ == "__main__":
    unittest.main()
