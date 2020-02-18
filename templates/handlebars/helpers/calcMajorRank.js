module.exports = function(rank) {
    if(rank < 10) { //Rank 9 or lower
        return 'apprentice_g2';
    } else if(rank >= 10 && rank < 20) { //Rank 19 or lower
        return 'lieutenant';
    } else if(rank >= 20 && rank < 30) { //Rank 29 or lower
        return 'captain';
    } else if(rank >= 30 && rank < 35) { //Rank 34 or lower
        return 'major';
    } else if(rank >= 35 && rank < 40) { //Rank 39 or lower
        return 'commander';
    } else if(rank >= 40 && rank < 45) { //Rank 44 or lower
        return 'colonel';
    } else if(rank >= 45 && rank < 50) { //Rank 49 or lower
        return 'brigadier';
    } else if(rank == 50) { //Rank 50
        return 'general';
    }
};