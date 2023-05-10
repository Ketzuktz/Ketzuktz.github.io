import random
import unittest

from gicg_sim.die import create_die_state, element_names


class TestDieState(unittest.TestCase):
    def test_create_die_state(self):
        for _ in range(10):
            die_count = dict([(en, 0) for en in element_names])

            die_total = random.randint(8, 20)
            for i in range(die_total):
                en = random.choice(element_names)
                die_count[en] = die_count[en] + 1

            kwargs = dict([(k.lower(), v) for k, v in die_count.items()])
            die_state = create_die_state(**kwargs)

            self.assertEqual(sum(die_state.die_count), die_total)
            for en in element_names:
                self.assertEqual(getattr(die_state, en), die_count[en])


if __name__ == "__main__":
    unittest.main()
