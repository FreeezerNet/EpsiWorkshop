MAX_PRODUCTION = 8115

MAX_STORAGE_RATIO = 0.85

BATTERY_CAPACITY = 16000

SECTOR_CONFIG = {

    "survival": {
        "priority": 1,
        "criticality": 1,
        "maximum": 2000,
        "minimum": 1800
    },

    "server": {
        "priority": 2,
        "criticality": 1,
        "maximum": 840,
        "minimum": 420
    },

    "greenhouse": {
        "priority": 3,
        "criticality": 2,
        "maximum": 1200,
        "minimum": 400
    },

    "lighting": {
        "priority": 4,
        "criticality": 2,
        "maximum": 360,
        "minimum": 18
    },

    "propulsion": {
        "priority": 5,
        "criticality": 3,
        "maximum": 840,
        "minimum": 0
    },

    "leisure": {
        "priority": 6,
        "criticality": 3,
        "maximum": 50,
        "minimum": 0
    }
}