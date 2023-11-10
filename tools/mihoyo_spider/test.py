import re
import typing

import yaml

from gicg_sim.model.prototype.effect import (DamagePrototype, DamageType,
                                             GetCharacterBuffPrototype,
                                             HealPrototype, SideTargetType,
                                             SideType, TargetType)

TARGET_ALIASES = {
    "自身": "我方出战角色",
    "此角色": "我方出战角色",
    "本角色": "我方出战角色",
    "我方出战角色": "我方出战角色",
    "所有我方角色": "我方所有角色",
}

TARGET_TRANSLATOR = {
    None: (SideTargetType.active, SideType.enemy),
    "我方出战角色": (SideTargetType.active, SideType.self),
    "我方所有角色": (SideTargetType.all, SideType.self),
    "目标角色": (SideTargetType.selected, SideType.undefined),
}

DAMAGE_TYPE_TRANSLATOR = {
    "火": DamageType.pyro,
    "水": DamageType.hydro,
    "风": DamageType.anemo,
    "雷": DamageType.electro,
    "草": DamageType.dendro,
    "冰": DamageType.cryo,
    "岩": DamageType.geo,
    "物理": DamageType.physical,
    "穿透": DamageType.piercing,
}

rules = [
    r'^(?P<is_passive>【被动】)',
    r'^(?P<condition_after_sacrifice>我方其他海乱鬼被击倒时，)',
    r'^(?P<condition_game_init>战斗开始时，)初始附属(?P<buff_init_name>[\u4e00-\u9fa5·]+)。',
    r'^(?P<condition_game_init>战斗开始时，)本角色获得(?P<energy_get>\d+)点充能。',
    r'^(?P<condition_game_init>战斗开始时，)角色处于(?P<status_init_name>[\u4e00-\u9fa5]+)。',
    r'^(?P<condition_card_used>入场时：?)',
    r'^(?P<condition_after_switch>切换到)(?P<equiped_current>装备有此牌的)(?P<switch_target>丽莎)后：',
    r'^(?P<condition_damage_taken>如果造成了)(?P<damage_type>((元素伤害|物理伤害|穿透伤害)、?)+)(?P<condition_reaction>或引发了元素反应)?，',
    r'^(?P<condition_summon_exist>如果已存在)(?P<summon_name>[\u4e00-\u9fa5]+)，',
    r'^(?P<condition_summon_lost>召唤物消失时)：',
    r'^(?P<condition_current_round>本回合中)，',
    r'^(?P<condition_after_operation>我方执行任何行动后)，',
    r'^(?P<condition_on_select_operation>我方选择行动前)，',
    r'^我方出战角色为(?P<condition_active>[\u4e00-\u9fa5]+)时，',
    r'^(?P<condition_no_cards>手牌数量为0)时：',
    r'^(?:我方)?(?P<condition_no_dies>(剩余)?元素骰(数量)?为0)时(?:：|，)',
    r'^(?P<condition_side>我方)(?P<condition_once>下次)?(?P<condition_switch>执行「切换角色」行动|执行行动「切换角色」)时：',
    r'^(?P<condition_side>我方)(?P<condition_after_switch>切换角色后)：',
    r'^(?P<condition_no_energy>如果切换到的角色没有充能)，',
    r'^(?P<play_condition_equiped_any>我方有角色已装备「武器」或「圣遗物」时)，才能打出：',
    r'^(?P<play_condition_active_element>我方出战角色的元素类型为)(?P<element>(?:[\u4e00-\u9fa5]/?)+)时，才能打出：',
    r'^(?P<condition_die_count_ge_8>我方至少剩余8个元素骰)，',
    r'^(?P<condition_enemy_not_end>(?:且)?对方未宣布结束时)，',
    r'^(?P<play_condition>才能打出)：',
    r'^角色所附属的(?P<condition_after_buffloss_name>[\u4e00-\u9fa5]+)效果结束时，重新附属(?P<buff_get_name>[\u4e00-\u9fa5]+)。',
    r'^角色受到(?P<condition_after_damage_type>[\u4e00-\u9fa5]+)元素伤害后，转换为(?P<status_convert_name>[\u4e00-\u9fa5]+)。',
    r'^(?P<skill_caster>此角色|其他我方角色|双方角色|我方|我方角色)(?P<condition_next>下一次)?(?P<condition_skill_used>使用)(?P<skill_type>技能|「元素爆发」|元素爆发|「元素战技」)后(，|：)',
    r'^(?P<skill_caster>此角色|其他我方角色|双方角色|我方|我方角色)(?P<condition_next>下一次)?(?P<condition_before_useskill>使用)(?P<skill_type>技能|「元素爆发」|元素爆发|「元素战技」)(?P<use_talent>或装备「天赋」)时(，|：)',
    r'^(?P<condition_before_specified_useskill>装备有此牌的)(?P<target>[\u4e00-\u9fa5]+)使用(?P<skill_name>[\u4e00-\u9fa5·]+)时，',
    r'^(?P<condition_after_specified_useskill>装备有此牌的)(?P<target>[\u4e00-\u9fa5]+)使用(?P<skill_name>[\u4e00-\u9fa5·]+)后：',
    r'^(?P<condition_after_specified_kill>装备有此牌的)(?P<target>[\u4e00-\u9fa5]+)击倒敌方角色后：',
    r'^(?P<condition_while_specified_live>装备有此牌的)(?P<target>[\u4e00-\u9fa5]+)在场时，',
    r'^(?P<condition_before_useskill_used>我方角色使用本回合使用过的技能)时：',
    r'^(?P<condition_after_token_increase>(当|如果)此牌已累积)(?P<token_count>\d+)个「(?P<token_name>[\u4e00-\u9fa5]+)」时?，',
    r'^(?:我方附属有(?P<buff_name>[\u4e00-\u9fa5]+)的(?P<source_element>雷元素))?(?P<skill_caster>角色)(?P<condition_before_skill_use>，|使用)(?P<skill_type>(?:(?:「元素爆发」|元素爆发|元素战技)和?)+)造成的伤害(?:额外)?\+(?P<damage_add>\d+)。',
    r'^(?P<condition_before_damage>角色造成伤害时)：',
    r'^我方角色每受到(?P<condition_healed_counter>\d+)点治疗，',
    r'^(?P<condition_after_declare_end>本回合中一位牌手先宣布结束时)，',
    r'^我方(?P<condition_once>下一?次)?打出(?P<condtion_before_playcard>(?:「[\u4e00-\u9fa5]+」或?)+)(事件|手|装备)牌时：?',
    r'^我方打出原本元素骰至少为(?P<condition_die_cost_le>\d+)的(?P<condtion_before_playcard>(?:「[\u4e00-\u9fa5]+」或?)+)(事件|手)牌时：',
    r'^(?P<condtion_die_le_cards>如果我方元素骰数量不多于手牌数量)，',
    r'^(?P<condition_phase_roll>投掷阶段：)',
    r'^(?P<condition_phase_roundend>结束阶段：)',
    r'^(?P<combat_action>战斗行动)：',
    r'^(?P<condition_next_turn>下回合)(?P<condition_phase_roundstart>行动阶段开始时：)',
    r'^(?P<condition_is_active>如果此角色是「出战角色」，)',
    r'^(?P<equip_target>[\u4e00-\u9fa5]+)(?P<condition_after_equip>装备此牌后)，',
    r'^(?P<buff_target>在对方场上)，',
    r'^附带(?P<token_init_count>\d+)个「(?P<token_name>[\u4e00-\u9fa5]+)」。',
    r'^(?P<equip>装备此牌)。',
    r'^从牌组中随机抽取(?P<card_draw_count>\d+)张「(?P<card_draw_type>[\u4e00-\u9fa5]+)」事件。',
    r'^(?P<target>未宣布结束的牌手)?抓(?P<card_draw_count>\d+)张牌。',
    r'^抓(?P<card_draw_one>一)张牌',
    r'^(?P<target>此角色|[\u4e00-\u9fa5]+)(?:重新)?附属(?P<buff_get_name>[\u4e00-\u9fa5]+)。',
    r'^切换为(?P<status_convert_name>[\u4e00-\u9fa5]+)，',
    r'^(?P<switch_next_self>自动切换到下一个角色。)',
    r'^将(?P<switch_specified_self>[\u4e00-\u9fa5]+)切换到场上(?:。|，)',
    r'^(?P<switch_target>切换到目标角色)，',
    r'^(?:此牌)?(?:就)?(?P<token_get>补充|累积)(?P<token_get_count>\d+)(?:(?:个「(?P<token_name>[\u4e00-\u9fa5]+)」)|(?:点(?P<token_name_progress>「[\u4e00-\u9fa5]+」)进度))。',
    r'^会(?:额外)?为(?P<target_name>[\u4e00-\u9fa5]+)累积(?P<token_get_count>\d+)点「(?P<token_name>[\u4e00-\u9fa5]+)」。',
    r'^(?:则)?(?P<drop_card>弃置此牌)(：|，)',
    r'^(?P<rebirth>复苏)(?P<target>目标角色|我方所有倒下的角色)，',
    r'^(?:则使该角色)?(?:就)?获得(?P<energy_get>\d+)点充能。',
    r'^(?P<target_equipped>所附属角色)获得(?P<energy_get>\d+)点充能。',
    r'^(?P<fast_switch>将此次切换视为「快速行动」)而非「战斗行动」。?',
    r'^(?P<fast_switch>我方执行的下次「切换角色」行动视为「快速行动」而非「战斗行动」)，',
    r'^(?P<reroll_all>选择任意元素骰重投。)',
    r'^(?P<add_reroll_times>获得额外一次重投机会。)',
    r'^(?P<unplay_card>将一个我方角色所装备的)「(?P<equip_type>[\u4e00-\u9fa5]+)」返回手牌。',
    r'^(?P<transfer_equip>将一个装备在我方角色的)「(?P<equip_type>[\u4e00-\u9fa5]+)」装备牌，转移给另一个(?P<condition_same_equip>武器类型相同的)?我方角色，并重置其效果的「每回合」次数限制。',
    r'^(?:并且|则)?(?:使打出的卡牌)?(?P<reduce_die_cost>少花费)(?P<die_count>\d+)个元素骰(?:。|；)',
    r'^(?P<side>我方)场上每有一个已装备「(?P<tiny_condition_equip>[\u4e00-\u9fa5]+)」的角色，就(?P<reduce_die_cost>额外少花费)(?P<die_count>\d+)个元素骰。',
    r'^消耗所有「(?P<tiny_condition_token>[\u4e00-\u9fa5]+)」，每消耗1个都使造成的伤害\+(?P<convert_token_damage_add>\d+)。',
    r'^(?:然后该角色进行|立刻使用)(?:一次)?(?P<take_action>「普通攻击」|[\u4e00-\u9fa5·\w ]+)。',
    r'^召唤(?P<summon_name>[\u4e00-\u9fa5·]+)(。|；)',
    r'^(?:然后|就先)?造成(?P<direct_damage_count>\d+)点(?P<direct_damage_type>[\u4e00-\u9fa5]+)伤害(，|。|；)',
    r'^并?使(?P<target>目标角色|敌方出战角色)附属(?P<status_get_name>[\u4e00-\u9fa5]+)。',
    r'^并?生成(?P<die_get_count>\d+)点(?P<die_get_type>[\u4e00-\u9fa5]+)元素。',
    r'^生成(?P<die_get_one>一)个(?P<die_get_type>[\u4e00-\u9fa5]+)元素。',
    r'^生成(?P<die_get_count>\d+)个(?P<die_get_type>不同的基础元素|我方下一个后台角色类型的元素)骰子?。',
    r'^并(?P<heal>治疗)(?P<heal_target>此角色|其)(?P<heal_count>\d+)点。',
    r'^(?P<convert_die_all_omni>将我方所有元素骰转换为万能元素)。',
    r'^将所花费的元素骰转换为(?P<die_get_count>\d+)个(?P<die_get_type>[\u4e00-\u9fa5]+)元素。',
    r'^从(?P<energy_transfer_source>最多2个我方后台角色身上)，转移(?P<energy_transfer_count>\d+)点充能到(?P<energy_transfer_target>我方出战角色)。',
    r'^(?P<side>我方)(?P<target>一名充能未满的角色|当前出战角色)获得(?P<energy_get>\d+)点充能。',
    r'^(?:我方)?打出「(?P<condition_before_playcard>[\u4e00-\u9fa5]+)」手牌时：如可能，则支付等同于「\1」总费用数量的「(?P<token_cost>[\u4e00-\u9fa5]+)」，以(?P<token_effect>免费装备此「\1」)。',
    r'^(?:我方)?打出(?P<condition_before_playcards>(?:「([\u4e00-\u9fa5]+)」或?)+)装备时：如果(?P<condition_token_progress_name>「[\u4e00-\u9fa5]+」)进度已达到(?P<token_count>\d+)，',
    r'^(?P<active_first>（出战角色优先）)',
    r'^(?P<limit_per_turn>(\(|（)每回合)(?P<limit_per_turn_count>\d+)次(\)|）)',
    r'^(?P<limit_per_turn>(\(|（)每回合)(?P<limit_once_per_turn>一)次(\)|）)',
    r'^(?:（|\()最多累积(?P<limit_token_count>\d+)(?:点|个)(?:）|\))',
    r'^可用次数：(?P<limit_effect_times>\d+)',
    r'^（整场牌局限制(?P<limit_effect_global>2)次）',
    r'^（牌组包含至少2个「(?P<deckcondition_two_character_region>[\u4e00-\u9fa5]+)」角色，才能加入牌组）',
    r'^（牌组包含至少2个(?P<deckcondition_two_character_element>[\u4e00-\u9fa5]元素)角色，才能加入牌组）',
    r'^（牌组中包含(?P<deckcondition_specified_character>[\u4e00-\u9fa5·]+)，才能加入牌组）',
    # 忽略吧！！
    r'^（角色最多装备1件「圣遗物」(?:）|\))',
    r'^（每回合中，最多通过「料理」复苏1个角色，并且每个角色最多食用1次「料理」\)',
    r'^（整局游戏只能打出一张「秘传」卡牌(?:：|；)这张牌一定在你的起始手牌中）',
    # 特判吧！！
    r'^(?P<Tartaglia_BurstSkill>依据达达利亚当前所处的状态，进行不同的攻击：远程状态·魔弹一闪：造成4点水元素伤害，返还2点充能，目标角色附属断流。近战状态·尽灭水光：造成7点水元素伤害。)',
    r'^(?P<FathomlessFlames_Talent>如果装备有此牌的深渊咏者·渊火已触发过火之新生，就立刻弃置此牌，为角色附属渊火加护。装备有此牌的深渊咏者·渊火触发火之新生时：弃置此牌，为角色附属渊火加护。)',
    r'^(?P<Keqing_ElementalSkill>本次星斗归位会为刻晴附属雷元素附魔，但是不会再生成雷楔。（刻晴使用星斗归位时，如果此牌在手中：不会再生成雷楔，而是改为弃置此牌，并为刻晴附属雷元素附魔）)',
    r'^随机召唤(?P<PureWater_Summon>\d+)种纯水幻形。（优先生成不同的类型）',
    r'^召唤一个(?P<summon_name>随机「丘丘人」召唤物)！',
    r'^生成1个(?P<buff_name>随机类型的「愚人众伏兵」)。',
    r'^(?P<attach_all>对我方所有角色附着我方出战角色类型的元素。)',
]

rules_compiled = [re.compile(r) for r in rules]

def match_rules(e):
    output = {}
    
    while True:
        endable = True
        for r in rules_compiled:
            m = r.match(e)
            if m:
                e = e[m.end():]
                output.update(m.groupdict())
                endable = False
        
        if endable:
            break
        
    return output, e


if __name__ == "__main__":
    with open("output_data.d/effects.yml", "r", encoding="utf-8") as f:
        effects: list[str] = yaml.load(f, Loader=yaml.FullLoader)

    for e_ in effects:
        output, e = match_rules(e_)
        
        if len(e) > 0:
            print(output, e)
