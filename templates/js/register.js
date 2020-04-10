require('./../css/general.css');
require('./../css/register.css');
var $ = require('jquery');

function init() {
    $('#username').focus();
    $('#home-header').show();
    $('.inner-wrapper').show();
}

function checkEmail(email) {
    return /\S+@\S+\.\S+/.test(email);
}

$(document).ready(function() {
    init();

    $(document).on('click', '#sign-up-submit', function () {
        var $errors = $('.error');
        $errors.hide();

        var username = $('#username').val();
        var password = $('#password').val();
        var email = $('#email').val();

        // Check if username is greater than 2 characters or less than 16
        if(username.length <= 3 || username.length >= 17) {
            var $error = $('.error.username');
            $error.text('Username must be between 4 to 16 characters.');
            $error.show();
        }

        // Check if password is 8 characters or more.
        if(password.length <= 7) {
            $error = $('.error.password');
            $error.text('Password must be 8 characters or more.');
            $error.show();
        }

        if(!checkEmail(email)) {
            $error = $('.error.email');
            $error.text('Must be a valid email.');
            $error.show();
        }

        var postData = {
            'username': username,
            'email': email,
            'password': password
        };

        $.ajax({
            headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').attr('value')},
            url: globals.base_url + '/account/register/',
            data: postData,
            dataType: 'json',
            type: "POST",
            success: function (response) {
                window.location.replace(globals.base_url + '/dashboard');
            },
            error: function (response) {
                console.log(JSON.stringify(response.responseJSON));

                var error = response.responseJSON['error_msg'];

                if (error == 'Username must be between 3 to 15 characters.') {
                    var $error = $('.error.username');
                    $error.text(error);
                    $error.show();
                } else if(error == 'Username exists.') {
                    $error = $('.error.username');
                    $error.text('Username is not available.');
                    $error.show();
                }

                if (error == 'Password must be 8 characters or more.') {
                    $error = $('.error.password');
                    $error.text(error);
                    $error.show();

                } else if(error == 'Invalid password.') {
                    $error = $('.error.password');
                    $error.text('Password must contain letter and digit.');
                    $error.show();
                }

                if(error == 'Invalid email.') {
                    $error = $('.error.email');
                    $error.text('Must be a valid email.');
                    $error.show();
                } else if(error == 'Email exists.') {
                    $error = $('.error.email');
                    $error.text('Email is not available.');
                    $error.show();
                }

                if(error == 'Must have a first name.') {
                    $error = $('.error.email');
                    $error.show();
                }

                if(error == 'Must have a last name.') {
                    $error = $('.error.email');
                    $error.show();
                }
            }
        });
    });
});