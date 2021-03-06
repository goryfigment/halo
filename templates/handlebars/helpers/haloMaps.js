module.exports = function(mapId) {
    mapId = String(mapId);

    var reach = {
        "190": "Boardwalk",
        "191": "Boneyard",
        "192": "Countdown",
        "193": "Powerhouse",
        "194": "Reflection",
        "195": "Spire",
        "196": "Sword Base",
        "197": "Zealot",
        "198": "Anchor 9",
        "199": "Breakpoint",
        "200": "Tempest",
        "201": "Condemned",
        "202": "Highlands",
        "203": "Battle Canyon",
        "204": "Penance",
        "205": "Ridgeline",
        "206": "Solitary",
        "207": "High Noon",
        "208": "Breakneck",
        "209": "Forge World"
    };

    var h1 = {
        "10": "Battle Creek",
        "11": "Sidewinder",
        "12": "Damnation",
        "13": "Rat Race",
        "14": "Prisoner",
        "15": "Hang em High",
        "16": "Chill Out",
        "17": "Derelict",
        "18": "Boarding Action",
        "19": "Chiron TL-34",
        "20": "Blood Gulch",
        "21": "Wizard",
        "22": "Longest",
        "23": "Death Island",
        "24": "Danger Canyon",
        "25": "Infinity",
        "26": "Timberland",
        "27": "Ice Fields",
        "28": "Gephyrophobia"
    };

    var h2a = {
        "155": "Lockdown",
        "156": "Zenith",
        "157": "Stonetown",
        "158": "Bloodline",
        "159": "Warlord",
        "160": "Shrine",
        "161": "Remnant",

        "163": "Awash"
    };

    var h2c = {
        "44": "Lockout",
        "45": "Ascension",
        "46": "Midship",
        "47": "Ivory Tower",
        "48": "Beaver Creek",
        "49": "Burial Mounds",
        "50": "Colossus",
        "51": "Zanzibar",
        "52": "Coagulation",
        "53": "Headlong",
        "54": "Waterworks",
        "55": "Foundation",
        "56": "Containment",
        "57": "Warlock",
        "58": "Sanctuary",
        "59": "Turf",
        "60": "Backwash",
        "61": "Elongation",
        "62": "Gemini",
        "63": "Relic",
        "64": "Terminal",
        "65": "Desolation",
        "66": "Tombstone",
        "67": "District",
        "68": "Uplift"
    };

    var h3 = {
        "79": "Construct",
        "80": "Epilogue",
        "81": "Guardian",
        "82": "High Ground",
        "83": "Isolation",
        "84": "Last Resort",
        "85": "Narrows",
        "86": "Sandtrap",
        "87": "Boundless",
        "88": "The Pit",
        "89": "Valhalla",
        "90": "Foundry",
        "91": "Rat's Nest",
        "92": "Standoff",
        "93": "Avalanche",
        "94": "Blackout",
        "95": "Ghost Town",
        "96": "Cold Storage",
        "97": "Assembly",
        "98": "Orbital",
        "99": "Sandbox",
        "100": "Citadel",
        "101": "Heretic",
        "102": "Longshore"
    };

    var h4 = {
        "114": "Adrift",
        "115": "Abandon",
        "116": "Complex",
        "117": "Exile",
        "118": "Haven",
        "119": "Longbow",
        "120": "Meltdown",
        "121": "Ragnarok",
        "122": "Solace",
        "123": "Vortex",
        "124": "Settler",
        "125": "Relay",
        "126": "Ascent",
        "128": "Wreckage",
        "129": "Harvest",
        "130": "Shatter",
        "131": "Landfall",
        "132": "Monolith",
        "133": "Skyline",
        "134": "Daybreak",
        "135": "Outcast",
        "136": "Perdition",
        "137": "Pitfall",
        "138": "Vertigo"
    };

    if(mapId in reach) {
        return "REACH: " + reach[mapId];
    } else if(mapId in h1) {
        return "H1: " + h1[mapId];
    } else if(mapId in h2a) {
        return "H2A: " + h2a[mapId];
    } else if(mapId in h2c) {
        return "H2C: " + h2c[mapId];
    } else if(mapId in h3) {
        return "H3: " + h3[mapId];
    } else if(mapId in h4) {
        return "H4: " + h4[mapId];
    } else {
        return "UNKNOWN: " + mapId;
    }
};