webpackJsonp([10],{87:function(e,exports,r){function a(){$("#username").focus(),$("#home-header").show(),$(".inner-wrapper").show()}function s(e){return/\S+@\S+\.\S+/.test(e)}r(40),r(88);var $=r(7);$(document).ready(function(){a(),$(document).on("click","#sign-up-submit",function(){$(".error").hide();var e=$("#username").val(),r=$("#password").val(),a=$("#email").val();if(e.length<=3||e.length>=17){var o=$(".error.username");o.text("Username must be between 4 to 16 characters."),o.show()}r.length<=7&&(o=$(".error.password"),o.text("Password must be 8 characters or more."),o.show()),s(a)||(o=$(".error.email"),o.text("Must be a valid email."),o.show());var t={username:e,email:a,password:r};$.ajax({headers:{"X-CSRFToken":$('input[name="csrfmiddlewaretoken"]').attr("value")},url:globals.base_url+"/account/register/",data:t,dataType:"json",type:"POST",success:function(e){window.location.replace(globals.base_url+"/dashboard")},error:function(e){console.log(JSON.stringify(e.responseJSON));var r=e.responseJSON.error_msg;if("Username must be between 3 to 15 characters."==r){var a=$(".error.username");a.text(r),a.show()}else"Username exists."==r&&(a=$(".error.username"),a.text("Username is not available."),a.show());"Password must be 8 characters or more."==r?(a=$(".error.password"),a.text(r),a.show()):"Invalid password."==r&&(a=$(".error.password"),a.text("Password must contain letter and digit."),a.show()),"Invalid email."==r?(a=$(".error.email"),a.text("Must be a valid email."),a.show()):"Email exists."==r&&(a=$(".error.email"),a.text("Email is not available."),a.show()),"Must have a first name."==r&&(a=$(".error.email"),a.show()),"Must have a last name."==r&&(a=$(".error.email"),a.show())}})})})},88:function(e,exports){}},[87]);