webpackJsonp([8],{76:function(n,exports,e){function o(){$("#username").focus(),$("#home-header").show(),$(".inner-wrapper").show()}e(42),e(77);var $=e(8);$(document).ready(function(){o(),$(document).on("keyup","#username",function(n){13==n.keyCode&&$("#password").select()}),$(document).on("keyup","#password",function(n){13==n.keyCode&&$("#login").click()}),$(document).on("click","#login",function(){var n=$(this),e=n.closest("#login-container"),o={username:e.find("#username").val(),password:e.find("#password").val()};$.ajax({headers:{"X-CSRFToken":n.siblings('input[name="csrfmiddlewaretoken"]').attr("value")},url:globals.base_url+"/account/login/",data:o,dataType:"json",type:"POST",success:function(n){n.success&&window.location.replace(globals.base_url+"/dashboard")},error:function(n){$(".error").show()}})})})},77:function(n,exports){}},[76]);