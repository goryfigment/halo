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

function spliceDict(dict, minKey, maxKey) {
  var newDict = {};
  for(var i in dict) {
    if(i >= minKey && i <= maxKey) {
      newDict[i] = dict[i];
    }
  }
  return newDict;
}


$(document).ready(function() {
    //var players = globals.players;
    $('#player-wrapper').append(verifyTemplate({'xbox': spliceDict(globals.xbox_ranks, 0, 101), 'pc': spliceDict(globals.pc_ranks, 0, 101)}));

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
    var xboxList = globals.xbox_ranks;
    var pcList = globals.pc_ranks;
    var newXboxList = [];
    var newPCList = [];

    for (var key in xboxList) {
        var xboxItem = xboxList[key];
        if(xboxItem['player__gamertag'].toLowerCase().indexOf(searchValue) != -1) {
            newXboxList.push(xboxItem);
        }
    }

    for (var p = 0; p < newXboxList.length; p++) {
        var playerKey = newXboxList[p]['player__id'];
        newPCList.push(pcList[playerKey]);
    }

    var $playerWrapper = $('#player-wrapper');
    $playerWrapper.empty();
    $playerWrapper.append(verifyTemplate({'xbox': newXboxList, 'pc': newPCList}));
});
//SEARCH//

//VERIFY//
$(document).on('change', '.checkbox-input', function () {
    var $this = $(this);
    var $player = $this.closest('.player');
    var key = $this.val();
    var playerId = $player.attr('data-id');
    var value = $this.prop('checked');
    var type = $this.closest('.table-container').attr('data-type');

    var data = {
        id: playerId,
        key: key,
        type: type,
        value: value
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

        if(type == 'xbox') {
            globals.xbox_ranks[playerId][key] = value;
        } else {
            globals.pc_ranks[playerId][key] = value;
        }


    }
});
//VERIFY//