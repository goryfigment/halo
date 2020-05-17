module.exports = function(gameId) {
    var gametype = ['Ctf', 'Slayer', 'Oddball', 'King of the Hill', 'Juggernaut', 'Infection', 'Flood', 'Race',
        'Extraction', 'Dominion', 'Regicide', 'Grifball', 'Ricochet', 'Sandbox (FORGE)', 'VIP', 'Territories', 'Assault'];

    return gametype[parseInt(gameId)];
};