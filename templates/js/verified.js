require('./../css/general.css');
require('./../css/verified.css');
require('./../library/fontawesome/fontawesome.js');
require('./../js/general.js');
var $ = require('jquery');
var verifyTemplate = require('./../handlebars/admin/verified.hbs');

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
    //var players = globals.players;
    $('#player-wrapper').append(verifyTemplate({'xbox': globals.xbox_ranks, 'pc': globals.pc_ranks}));

    //globals.players = {};
    //
    //for (var i = 0; i < players.length; i++) {
    //    var currentPlayer = players[i];
    //
    //    globals.players[currentPlayer['id']] = currentPlayer;
    //}
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

//VERIFY//
$(document).on('change', '.checkbox-input', function () {
    var $this = $(this);
    var $player = $this.closest('.player');

    var data = {
        id: $player.attr('data-id'),
        key: $this.val(),
        type: $this.closest('.table-container').attr('data-type'),
        value: $this.prop('checked')
    };

    sendRequest('/verify-player/', data, 'POST', success, error, 'edit');

    function error(response) {
        if(response.status && response.status == 403) {
            $('.error').text(' - Permission Denied').show();
        } else {
            $('.error').text(' - ' + response.responseText).show();
        }
    }

    function success(response) {
        //globals.players[response['id']] = response['player'];

        //var $playerWrapper = $('#player-wrapper');
        //$playerWrapper.empty();
        //$playerWrapper.append(verifyTemplate({'xbox': globals.xbox_ranks}));
        $('.instructions').text($player.find('.gamertag').text() + ' ' + response['success_msg']);
    }
});
//VERIFY//