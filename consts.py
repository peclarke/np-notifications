from enum import Enum

PIDS = {
    0: "Stars End / Yang",
    1: "conniecakes / Connor",
    2: "Lord Basil / Gareth",
    3: "Cosmo The Monkey / Paul",
    4: "Sentient Specks of Dust / Sam",
    5: "BugChungusGamingTTV / Blake",
    6: "Ulgi / Katya"
}

class StatusCode(Enum):
    DAILY = "An overview of enemy fleets in scanning range"
    ENEMY = "An enemy has been detected in the scan radius"
    FLEET_WATCH = "A fleet you were watching has begun moving"
    FLEET_SHIPS = "A fleet you were watching has passed the threshold of specified ships"