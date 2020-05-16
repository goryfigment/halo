require('./../css/general.css');
require('./../css/dashboard.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');
var $ = require('jquery');

var playerTemplate = require('./../handlebars/admin/players.hbs');
var banTemplate = require('./../handlebars/admin/ban.hbs');
var matchesTemplate = require('./../handlebars/admin/matches.hbs');
var matchesTableTemplate = require('./../handlebars/admin/matches_table.hbs');

function sendRequest(url, data, request_type, success, error, exception) {
    $.ajax({
        headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').attr('value')},
        url: globals.base_url + url,
        data: data,
        dataType: 'json',
        type: request_type,
        success: function (response) {
            success(response, exception);
        },
        error: function (response) {
            error(response, exception);
        }
    });
}


$(document).ready(function() {
    var players = globals.players;
    $('#player-wrapper').append(playerTemplate({'players': players}));

    globals.players = {};

    for (var i = 0; i < players.length; i++) {
        var currentPlayer = players[i];

        globals.players[currentPlayer['id']] = currentPlayer;
    }
});


//SEARCH//
$(document).on('keyup', '#search-gt-input', function () {
    var $searchInput = $(this);
    var searchValue = $searchInput.val().trim().toLowerCase();
    var $table = $('.table-container tbody');

    //loops through rows
    $table.find('tr').each(function() {
        var $currentRow = $(this);
        var gamertag = $currentRow.find('.gamertag').text().toLowerCase();
        if(gamertag.indexOf(searchValue) != -1) {
            $currentRow.show();
        } else {
            $currentRow.hide();
        }
    })
});
//SEARCH//

// EDIT INVENTORY //
$(document).on('click', 'tbody tr', function () {
    var $this = $(this);
    if(!globals.edit_mode) {
        var $td = $this.find('td');

        for (var i = 0; i < $td.length; i++) {
            var $currentRow = $($td[i]);
            var value = $currentRow.text();
            var column = $currentRow.attr('data-column');
            var input = $currentRow.attr('data-input');

            if(column == undefined) {
                $currentRow.html('<input id="' + input + '"' + 'value="' + value + '" />');
            } else if(column == 'ban') {
                $currentRow.empty();
                $currentRow.append(banTemplate({'ban': value}));
            } else if(column == 'id') {
                globals.id = $currentRow.text();
            }
        }

        var $instructions = $('#instructions');
        $instructions.show();
        $instructions.html("Press '<b>ENTER</b>' to submit or exit EDIT MODE.");
        globals.edit_mode = true;
    }
});

$(document).on('click', '.popup-table input', function (e) {
    e.stopPropagation();
});

$(document).on('change', '#ban-checkbox', function () {
    $('.check-box-label').text($(this).prop('checked'));
});

$(document).on('keyup', function(e) {
    if (e.keyCode == 13 && globals.edit_mode) {

        var data = {
            id: globals.id,
            ban: $('#ban-checkbox').prop('checked'),
            donation: $('#donation').val(),
            twitch: $('#twitch').val(),
            youtube: $('#youtube').val(),
            twitter: $('#twitter').val(),
            mixer: $('#mixer').val(),
            social: $('#social').val(),
            color: $('#color').val(),
            notes: $('#notes').val()
        };

        sendRequest('/edit-player/', data, 'POST', success, error, 'edit');

        function error(response) {
            if(response.status && response.status == 403) {
                $('.error').text(' - Permission Denied').show();
            } else {
                $('.error').text(' - ' + response.responseText).show();
            }
        }

        function success(response) {
            globals.players[response['id']] = response['player'];

            var $playerWrapper = $('#player-wrapper');
            $playerWrapper.empty();
            $playerWrapper.append(playerTemplate({'players': globals.players}));

            globals.edit_mode = false;

            $('#instructions').text(response['success_msg']);
        }
    }
});
// EDIT INVENTORY //

// GET MATCHES //
$(document).on('click', '.popup', function (e) {
    e.stopPropagation();
});

$(document).on('click', '#exit-button', function () {
    $('#overlay').removeClass('active');
    globals.edit_mode = false;
});

$(document).on('keyup',function(e) {
    if (e.keyCode == 27) {
       $('#overlay').removeClass('active');
        globals.edit_mode = false;
    }
});

$(document).on('click', '.history-button', function (e) {
    e.stopPropagation();
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.addClass('active');
    $overlay.append('<i style="font-size:40px" class="fas fa-circle-notch fa-spin"></i>');
    sendRequest('/player-matches/', {'gt': $(this).attr('data-gt'), 'game_variant': '', 'req': 11}, 'GET', playerMatchesSuccess, playerMatchesError);
});

$(document).on('click', '#game-submit', function (e) {
    e.stopPropagation();
    var $tableWrapper = $('#table-wrapper');
    $tableWrapper.empty();
    $tableWrapper.append('<i style="font-size:40px" class="fas fa-circle-notch fa-spin"></i>');
    sendRequest('/game-matches/', {'gt': $(this).attr('data-gt'), 'game_variant': $('#game-variant-input').val(), 'game': $('#game-input').val(), 'req': 11}, 'GET', gameMatchesSuccess, playerMatchesError);
});

function playerMatchesSuccess(response) {
    var $overlay = $('#overlay');
    $overlay.empty();
    $overlay.append(matchesTemplate(response));
}

function gameMatchesSuccess(response) {
    var $tableWrapper = $('#table-wrapper');
    $tableWrapper.empty();
    $tableWrapper.append(matchesTableTemplate(response));
}

function playerMatchesError(response) {
    console.log("Player Matches error!");
}
// GET MATCHES //

//SORTABLE
function replaceAll(str, find, replace) {
    return str.replace(new RegExp(find.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1"), 'g'), replace);
}

function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index);
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB);
    }
}

function getCellValue(row, index){ return $(row).children('td').eq(index).text()}

$(document).on('click', '.sortable', function () {
    var $this = $(this);
    var $sortable = $this.closest('table').find('.sortable');
    for (var s = 0; s < $sortable.length; s++){
        if($sortable[s] != this) {$sortable[s].asc = false;}
        $($sortable[s]).removeClass('ascending').removeClass('descending');
    }
    var table = $this.parents('table').eq(0);
    var rows = table.find('tr:gt(0)').toArray().sort(comparer($this.index()));

    this.asc = !this.asc;
    if (!this.asc){
        rows = rows.reverse();
        $this.addClass('descending');
    } else {
        $this.addClass('ascending');
    }
    for (var i = 0; i < rows.length; i++){table.append(rows[i])}
});
//SORTABLE