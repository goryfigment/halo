webpackJsonp([2],{18:function(t,exports){},19:function(t,exports,o){var $=o(6);$(document).ready(function(){$(document).on({mouseenter:function(){var t=$(this),o=$("#tip-popup"),n=o.find("#tip-arrow");o.find("#tip-content").html(t.attr("data-title"));var a=t.offset(),e=o.outerWidth()/2,i=t.outerWidth()/2+a.left-e;n.css({left:e-n.outerWidth(!0)/2}),o.finish().css({top:a.top,left:i,"transition-duration":"0ms"}),o.css({display:"block","transition-duration":"350ms",transform:"translate3d(0,"+-(o.outerHeight()+13)+"px, 0)",opacity:1})},mouseleave:function(){var t=$("#tip-popup"),o=parseInt(t.css("top"))-(t.outerHeight()+13);t.css({transform:"","transition-duration":"",top:o}),t.animate({opacity:0,top:o+13+"px"},350,function(){t.css({opacity:0,top:"",left:"",display:"none"})})}},".tippy")})},77:function(t,exports,o){function n(t,o,n,a,e,i){$.ajax({headers:{"X-CSRFToken":$('input[name="csrfmiddlewaretoken"]').attr("value")},url:globals.base_url+t,data:o,dataType:"json",type:n,success:function(t){a(t,i)},error:function(t){e(t,i)}})}function a(t){console.log("Donate Sent")}function e(){console.log("Donate Error")}o(12),o(78),o(13),o(18);var $=o(6);o(8);o(14),o(19),$(document).on("click","#donate-submit",function(t){t.stopPropagation();var o={gamertag:$("#gamertag").val(),twitch:$("#twitch").val(),twitter:$("#twitter").val(),youtube:$("#youtube").val(),message:$("textarea").val(),donate:$("#donate").val()};$("#paypal").submit(),n("/donate-message/",o,"POST",a,e)}),$(document).ready(function(){"true"==globals.t?$("#thank-you-wrapper").show():$("#donate-wrapper").show()})},78:function(t,exports){}},[77]);