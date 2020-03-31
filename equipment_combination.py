from functools import reduce

from equipment_piece import BodyPart, Charm


class EquipmentCombination:
    def __init__(
        self,
        head_piece,
        body_piece,
        arm_piece,
        waist_piece,
        leg_piece,
        charm
    ):
        self._equipment = [
            head_piece,
            body_piece,
            arm_piece,
            waist_piece,
            leg_piece,
            charm,
        ]

    @property
    def equipment(self):
        return {
                k: v for (k,v) in zip([BodyPart.HEAD,
                                       BodyPart.BODY,
                                       BodyPart.ARMS,
                                       BodyPart.WAIST,
                                       BodyPart.LEGS,
                                       BodyPart.CHARM],
                                      self._equipment)
        }

    @property
    def _armour_pieces(self):
        return [
            x for x in self.equipment.values() if not isinstance(x, Charm)
        ]

    @property
    def charm(self):
        return self.equipment[BodyPart.CHARM]
    
    @property
    def total_defence(self):
        return sum([x.defence for x in self._armour_pieces])

    @property
    def total_decoration_slots_by_level(self):
        return _total_decoration_slots_by_level(
            self._armour_pieces
        )

    @property
    def total_skill_levels(self):
        return _total_skill_levels(
            self._armour_pieces,
            self.charm
        )


def _total_decoration_slots_by_level(armour_pieces):
    total_decoration_slots_by_level = {}
    for i in range(1, 5):
        total_decoration_slots_by_level[i] = sum(
            [x.decoration_slots[i] for x in armour_pieces]
        )
    return total_decoration_slots_by_level


def _total_skill_levels(armour_pieces, charm):
    skills = reduce(
        list.__add__, [x.skills for x in armour_pieces]
    ) + charm.skills

    total_skill_levels = {}
    for skill in skills:
        current_level = 0
        if skill.name in total_skill_levels:
            current_level = total_skill_levels[skill.name]
        total_skill_levels[skill.name] = current_level + skill.level
    return total_skill_levels
