require('./../css/general.css');
require('./../css/dashboard.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');
var $ = require('jquery');

var playerTemplate = require('./../handlebars/admin/players.hbs');
var banTemplate = require('./../handlebars/admin/ban.hbs');

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