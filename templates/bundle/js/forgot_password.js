webpackJsonp([9],{84:function(s,exports,e){function o(){$("#username").focus(),$("#home-header").show(),$(".inner-wrapper").show()}e(42),e(85);var $=e(8);$(document).ready(function(){o(),$(document).on("keyup","#username",function(s){13==s.keyCode&&$("#submit").click()}),$(document).on("click","#submit",function(){var s=$(this),e=s.closest("#forgot-password-wrapper"),o={username:e.find("#username").val(),base_url:globals.base_url};$.ajax({headers:{"X-CSRFToken":s.siblings('input[name="csrfmiddlewaretoken"]').attr("value")},url:globals.base_url+"/account/reset_password/",data:o,dataType:"json",type:"POST",success:function(s){s.success&&(e.find("#forgot-password-container").hide(),e.find("#email-sent").show())},error:function(s){$(".error").show()}})}),$(document).on("click","#change-password",function(){var s=$(this),e=s.closest("#forgot-password-wrapper"),o=e.find("#password-1").val(),r=e.find("#password-2").val(),a=$(".error");if(o!=r)return a.text("Passwords do not match."),void a.show();var n=new URL(window.location.href).searchParams.get("code"),t={password1:e.find("#password-1").val(),password2:e.find("#password-2").val(),code:n};$.ajax({headers:{"X-CSRFToken":s.siblings('input[name="csrfmiddlewaretoken"]').attr("value")},url:globals.base_url+"/account/change_password/",data:t,dataType:"json",type:"POST",success:function(s){s.success&&(e.find("#forgot-password-container").hide(),e.find("#success").show())},error:function(s){a.text(s.responseJSON.error_msg),$(".error").show()}})})})},85:function(s,exports){}},[84]);