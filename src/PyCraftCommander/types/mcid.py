from enum import StrEnum
from typing import Literal


class MCID(StrEnum):
    """マインクラフトIDの列挙型です。"""


class V1_21(MCID):
    """v1.21のマインクラフトIDの列挙型です。"""

    # A
    ACACIA_BOAT = "minecraft:acacia_boat"
    ACACIA_BUTTON = "minecraft:acacia_button"
    ACACIA_CHEST_BOAT = "minecraft:acacia_chest_boat"
    ACACIA_DOOR = "minecraft:acacia_door"
    ACACIA_FENCE = "minecraft:acacia_fence"
    ACACIA_FENCE_GATE = "minecraft:acacia_fence_gate"
    ACACIA_HANGING_SIGN = "minecraft:acacia_hanging_sign"
    ACACIA_LEAVES = "minecraft:acacia_leaves"
    ACACIA_LOG = "minecraft:acacia_log"
    ACACIA_PLANKS = "minecraft:acacia_planks"
    ACACIA_PRESSURE_PLATE = "minecraft:acacia_pressure_plate"
    ACACIA_SAPLING = "minecraft:acacia_sapling"
    ACACIA_SIGN = "minecraft:acacia_sign"
    ACACIA_SLAB = "minecraft:acacia_slab"
    ACACIA_STAIRS = "minecraft:acacia_stairs"
    ACACIA_TRAPDOOR = "minecraft:acacia_trapdoor"
    ACACIA_WOOD = "minecraft:acacia_wood"
    ACTIVATOR_RAIL = "minecraft:activator_rail"
    AIR = "minecraft:air"
    ALLAY_SPAWN_EGG = "minecraft:allay_spawn_egg"
    ALLIUM = "minecraft:allium"
    AMETHYST_BLOCK = "minecraft:amethyst_block"
    AMETHYST_CLUSTER = "minecraft:amethyst_cluster"
    AMETHYST_SHARD = "minecraft:amethyst_shard"
    ANCIENT_DEBRIS = "minecraft:ancient_debris"
    ANDESITE = "minecraft:andesite"
    ANDESITE_SLAB = "minecraft:andesite_slab"
    ANDESITE_STAIRS = "minecraft:andesite_stairs"
    ANDESITE_WALL = "minecraft:andesite_wall"
    ANGLER_POTTERY_SHARD = "minecraft:angler_pottery_shard"
    ANVIL = "minecraft:anvil"
    APPLE = "minecraft:apple"
    ARCHER_POTTERY_SHARD = "minecraft:archer_pottery_shard"
    ARMADILLO_SCUTE = "minecraft:armadillo_scute"
    ARMADILLO_SPAWN_EGG = "minecraft:armadillo_spawn_egg"
    ARMOR_STAND = "minecraft:armor_stand"
    ARMS_UP_POTTERY_SHARD = "minecraft:arms_up_pottery_shard"
    ARROW = "minecraft:arrow"
    AXOLOTL_BUCKET = "minecraft:axolotl_bucket"
    AXOLOTL_SPAWN_EGG = "minecraft:axolotl_spawn_egg"
    AZALEA = "minecraft:azalea"
    AZALEA_LEAVES = "minecraft:azalea_leaves"
    AZURE_BLUET = "minecraft:azure_bluet"


MinecraftVersion = Literal["1.21"]


def GET_MCID(MinecraftVersion: MinecraftVersion) -> MCID:
    """マインクラフトIDの列挙型を取得します。

    対応バージョン:
        - 1.21
    """

    if MinecraftVersion == "1.21":
        return V1_21
    else:
        raise ValueError("バージョン非対応です。")
