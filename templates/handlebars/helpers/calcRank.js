module.exports = function(rank, wins) {
    if(rank < 10) { //Rank 9 or lower
        if(wins < 2) {
            return 'recruit';
        } else if(wins == 2) {
            return 'apprentice';
        } else if(wins == 3) {
            return 'apprentice_g2';
        } else if(wins >= 3 && wins < 5) {
            return 'private';
        } else if(wins >= 5 && wins < 7) {
            return 'private_g2';
        } else if(wins >= 10 && wins < 15) {
            return 'corporal';
        } else if(wins >= 15 && wins < 20) {
            return 'corporal_g2';
        } else if(wins >= 20 && wins < 30) {
            return 'sergeant';
        } else if(wins >= 30 && wins < 40) {
            return 'sergeant_g2';
        } else if(wins >= 40 && wins < 50) {
            return 'sergeant_g3';
        } else if(wins >= 50 && wins < 60) {
            return 'gunnery_sergeant';
        } else if(wins >= 60 && wins < 150) {
            return 'gunnery_sergeant_g2';
        } else if(wins >= 150 && wins < 300) {
            return 'gunnery_sergeant_g3';
        } else if(wins >= 300) {
            return 'gunnery_sergeant_g4';
        }
    } else if(rank >= 10 && rank < 20) { //Rank 19 or lower
        if(wins < 85) {
            return 'lieutenant';
        } else if(wins >= 85 && wins < 200) {
            return 'lieutenant_g2';
        } else if(wins >= 200 && wins < 400) {
            return 'lieutenant_g3';
        } else if(wins >= 400) {
            return 'lieutenant_g4';
        }
    } else if(rank >= 20 && rank < 30) { //Rank 29 or lower
        if(wins < 150) {
            return 'captain';
        } else if(wins >= 150 && wins < 300) {
            return 'captain_g2';
        } else if(wins >= 300 && wins < 600) {
            return 'captain_g3';
        } else if(wins >= 600) {
            return 'captain_g4';
        }
    } else if(rank >= 30 && rank < 35) { //Rank 34 or lower
        if(wins < 300) {
            return 'major';
        } else if(wins >= 300 && wins < 600) {
            return 'major_g2';
        } else if(wins >= 600 && wins < 1200) {
            return 'major_g3';
        } else if(wins >= 1200) {
            return 'major_g4';
        }
    } else if(rank >= 35 && rank < 40) { //Rank 39 or lower
        if(wins < 450) {
            return 'commander';
        } else if(wins >= 450 && wins < 900) {
            return 'commander_g2';
        } else if(wins >= 900 && wins < 1800) {
            return 'commander_g3';
        } else if(wins >= 1800) {
            return 'commander_g4';
        }
    } else if(rank >= 40 && rank < 45) { //Rank 44 or lower
        if(wins < 600) {
            return 'colonel';
        } else if(wins >= 600 && wins < 1200) {
            return 'colonel_g2';
        } else if(wins >= 1200 && wins < 2400) {
            return 'colonel_g3';
        } else if(wins >= 2400) {
            return 'colonel_g4';
        }
    } else if(rank >= 45 && rank < 50) { //Rank 49 or lower
        if(wins < 1000) {
            return 'brigadier';
        } else if(wins >= 1000 && wins < 2000) {
            return 'brigadier_g2';
        } else if(wins >= 2000 && wins < 4000) {
            return 'brigadier_g3';
        } else if(wins >= 4000) {
            return 'brigadier_g4';
        }
    } else if(rank == 50) { //Rank 50
        if(wins < 1200) {
            return 'general';
        } else if(wins >= 1200 && wins < 2500) {
            return 'general_g2';
        } else if(wins >= 2500 && wins < 5000) {
            return 'general_g3';
        } else if(wins >= 5000) {
            return 'general_g4';
        }
    }
};