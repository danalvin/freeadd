(function($){"use strict";if($(window).width()>767){if($('.theiaStickySidebar').length>0){$('.theiaStickySidebar').theiaStickySidebar({additionalMarginTop:30});}}
var header_bottom_height=$('.header-container-bottom').outerHeight();$(window).scroll(function(){var scroll=$(window).scrollTop();if(scroll>70){if($(window).width()>991){$(".header .header-container-bottom").addClass("sticky");$("body").css("margin-top",header_bottom_height);}}
else{if($(window).width()>991){$(".header .header-container-bottom").removeClass("sticky");$("body").css("margin-top",0);}}})
if($(window).width()<=991){var Sidemenu=function(){this.$menuItem=$('.main-nav a');};function init(){var $this=Sidemenu;$('.main-nav a').on('click',function(e){if($(this).parent().hasClass('has-submenu')){e.preventDefault();}
if(!$(this).hasClass('submenu')){$('ul',$(this).parents('ul:first')).slideUp(350);$('a',$(this).parents('ul:first')).removeClass('submenu');$(this).next('ul').slideDown(350);$(this).addClass('submenu');}else if($(this).hasClass('submenu')){$(this).removeClass('submenu');$(this).next('ul').slideUp(350);}});}
init();}
var maxLength=100;$('#review_desc').on('keyup change',function(){var length=$(this).val().length;length=maxLength-length;$('#chars').text(length);});if($('.select').length>0){$('.select').select2({minimumResultsForSearch:-1,width:'100%'});}
if($('.datetimepicker').length>0){$('.datetimepicker').datetimepicker({format:'DD/MM/YYYY',icons:{up:"fas fa-chevron-up",down:"fas fa-chevron-down",next:'fas fa-chevron-right',previous:'fas fa-chevron-left'}});}
if($('.floating').length>0){$('.floating').on('focus blur',function(e){$(this).parents('.form-focus').toggleClass('focused',(e.type==='focus'||this.value.length>0));}).trigger('blur');}
$('body').append('<div class="sidebar-overlay"></div>');$(document).on('click','#mobile_btn',function(){$('main-wrapper').toggleClass('slide-nav');$('.sidebar-overlay').toggleClass('opened');$('html').addClass('menu-opened');return false;});$(document).on('click','.sidebar-overlay',function(){$('html').removeClass('menu-opened');$(this).removeClass('opened');$('main-wrapper').removeClass('slide-nav');});$(document).on('click','#menu_close',function(){$('html').removeClass('menu-opened');$('.sidebar-overlay').removeClass('opened');$('main-wrapper').removeClass('slide-nav');});if($('[data-toggle="tooltip"]').length>0){$('[data-toggle="tooltip"]').tooltip();}
$(".hours-info").on('click','.trash',function(){$(this).closest('.hours-cont').remove();return false;});$(".add-hours").on('click',function(){var hourscontent='<div class="row form-row hours-cont">'+
'<div class="col-12 col-md-10">'+
'<div class="row form-row">'+
'<div class="col-12 col-md-6">'+
'<div class="form-group">'+
'<label>Start Time</label>'+
'<select class="form-control">'+
'<option>-</option>'+
'<option>12.00 am</option>'+
'<option>12.30 am</option>'+
'<option>1.00 am</option>'+
'<option>1.30 am</option>'+
'</select>'+
'</div>'+
'</div>'+
'<div class="col-12 col-md-6">'+
'<div class="form-group">'+
'<label>End Time</label>'+
'<select class="form-control">'+
'<option>-</option>'+
'<option>12.00 am</option>'+
'<option>12.30 am</option>'+
'<option>1.00 am</option>'+
'<option>1.30 am</option>'+
'</select>'+
'</div>'+
'</div>'+
'</div>'+
'</div>'+
'<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>'+
'</div>';$(".hours-info").append(hourscontent);return false;});function resizeInnerDiv(){var height=$(window).height();var header_height=$(".header").height();var footer_height=$(".footer").height();var setheight=height-header_height;var trueheight=setheight-footer_height;$(".content").css("min-height",trueheight);}
if($('.content').length>0){resizeInnerDiv();}
$(window).resize(function(){if($('.content').length>0){resizeInnerDiv();}});if($('.arrival-slider').length>0){$('.arrival-slider').slick({dots:false,infinite:true,speed:500,variableWidth:false,slidesToShow:4,autoplay:false,responsive:[{breakpoint:1024,settings:{slidesToShow:3,slidesToScroll:3}},{breakpoint:768,settings:{slidesToShow:2,slidesToScroll:2}},{breakpoint:480,settings:{slidesToShow:1,slidesToScroll:1}}]});}
if($('.product-slider').length>0){$('.product-slider').slick({dots:false,autoplay:false,infinite:true,variableWidth:false,slidesToShow:4,slidesToScroll:1,swipeToSlide:true,responsive:[{breakpoint:1024,settings:{slidesToShow:3,slidesToScroll:1}},{breakpoint:992,settings:{slidesToShow:3,slidesToScroll:1}},{breakpoint:768,settings:{slidesToShow:2,slidesToScroll:1}},{breakpoint:480,settings:{slidesToShow:1,slidesToScroll:1}}]});}
if($('.selection-slider').length>0){$('.selection-slider').slick({dots:false,infinite:true,speed:500,variableWidth:false,slidesToShow:4,autoplay:false,responsive:[{breakpoint:1024,settings:{slidesToShow:3,slidesToScroll:3}},{breakpoint:768,settings:{slidesToShow:2,slidesToScroll:2}},{breakpoint:480,settings:{slidesToShow:1,slidesToScroll:1}}]});}
if($('.products-slider').length>0){$('.products-slider').slick({slidesToShow:1,slidesToScroll:1,arrows:false,fade:true,asNavFor:'.product-slider-nav'});}
if($('.product-slider-nav').length>0){$('.product-slider-nav').slick({slidesToShow:4,slidesToScroll:1,asNavFor:'.products-slider',dots:false,arrows:false,centerMode:false,variableWidth:false,focusOnSelect:true});}
if($('.relateproduct-slider').length>0){$('.relateproduct-slider').slick({dots:false,autoplay:false,infinite:true,variableWidth:false,slidesToShow:6,slidesToScroll:1,swipeToSlide:true,responsive:[{breakpoint:1024,settings:{slidesToShow:4,slidesToScroll:4}},{breakpoint:992,settings:{slidesToShow:3,slidesToScroll:3}},{breakpoint:767,settings:{slidesToShow:2,slidesToScroll:2}},{breakpoint:480,settings:{slidesToShow:1,slidesToScroll:1}}]});}
if($('.healthcare-banner').length>0){$('.healthcare-banner').slick({dots:false,infinite:true,speed:500,variableWidth:false,slidesToShow:1,autoplay:false,});}
if($(window).width()<1200){if($('.bottom-menu-slider').length>0){$('.bottom-menu-slider').owlCarousel({loop:true,margin:20,nav:true,dots:false,smartSpeed:1500,autoWidth:true,nav:false,responsive:{0:{items:2},767:{items:6}}})}}
if($('.bookingrange').length>0){var start=moment().subtract(6,'days');var end=moment();function booking_range(start,end){$('.bookingrange span').html(start.format('MMMM D, YYYY')+' - '+end.format('MMMM D, YYYY'));}
$('.bookingrange').daterangepicker({startDate:start,endDate:end,ranges:{'Today':[moment(),moment()],'Yesterday':[moment().subtract(1,'days'),moment().subtract(1,'days')],'Last 7 Days':[moment().subtract(6,'days'),moment()],'Last 30 Days':[moment().subtract(29,'days'),moment()],'This Month':[moment().startOf('month'),moment().endOf('month')],'Last Month':[moment().subtract(1,'month').startOf('month'),moment().subtract(1,'month').endOf('month')]}},booking_range);booking_range(start,end);}
var chatAppTarget=$('.chat-window');(function(){if($(window).width()>991)
chatAppTarget.removeClass('chat-slide');$(document).on("click",".chat-window .chat-users-list a.media",function(){if($(window).width()<=991){chatAppTarget.addClass('chat-slide');}
return false;});$(document).on("click","#back_user_list",function(){if($(window).width()<=991){chatAppTarget.removeClass('chat-slide');}
return false;});})();function animateElements(){$('.circle-bar1').each(function(){var elementPos=$(this).offset().top;var topOfWindow=$(window).scrollTop();var percent=$(this).find('.circle-graph1').attr('data-percent');var animate=$(this).data('animate');if(elementPos<topOfWindow+$(window).height()-30&&!animate){$(this).data('animate',true);$(this).find('.circle-graph1').circleProgress({value:percent/100,size:400,thickness:30,fill:{color:'#da3f81'}});}});$('.circle-bar2').each(function(){var elementPos=$(this).offset().top;var topOfWindow=$(window).scrollTop();var percent=$(this).find('.circle-graph2').attr('data-percent');var animate=$(this).data('animate');if(elementPos<topOfWindow+$(window).height()-30&&!animate){$(this).data('animate',true);$(this).find('.circle-graph2').circleProgress({value:percent/100,size:400,thickness:30,fill:{color:'#68dda9'}});}});$('.circle-bar3').each(function(){var elementPos=$(this).offset().top;var topOfWindow=$(window).scrollTop();var percent=$(this).find('.circle-graph3').attr('data-percent');var animate=$(this).data('animate');if(elementPos<topOfWindow+$(window).height()-30&&!animate){$(this).data('animate',true);$(this).find('.circle-graph3').circleProgress({value:percent/100,size:400,thickness:30,fill:{color:'#1b5a90'}});}});}
if($('.circle-bar').length>0){animateElements();}
$(window).scroll(animateElements);$(window).on('load',function(){if($('#loader').length>0){$('#loader').delay(350).fadeOut('slow');$('body').delay(350).css({'overflow':'visible'});}});$(".categories_title").on("click",function(){$(this).toggleClass('active');$('.categories_menu_toggle').slideToggle('medium');});$(".categories_menu_toggle li.hidden").hide();$("#more-btn").on('click',function(e){e.preventDefault();$(".categories_menu_toggle li.hidden").toggle(500);var htmlAfter='<i class="fa fa-minus" aria-hidden="true"></i> Less Categories';var htmlBefore='<i class="fa fa-plus" aria-hidden="true"></i> More Categories';if($(this).html()==htmlBefore){$(this).html(htmlAfter);}else{$(this).html(htmlBefore);}});$('.inc.button').click(function(){var $this=$(this),$input=$this.prev('input'),$parent=$input.closest('div'),newValue=parseInt($input.val())+1;$parent.find('.inc').addClass('a'+newValue);$input.val(newValue);incrementVar+=newValue;});$('.dec.button').click(function(){var $this=$(this),$input=$this.next('input'),$parent=$input.closest('div'),newValue=parseInt($input.val())-1;console.log($parent);$parent.find('.inc').addClass('a'+newValue);$input.val(newValue);incrementVar+=newValue;});$('.custom-container').each(function(){var highestBox=0;$('.prod-widget, .healthcare-widget .card',this).each(function(){if($(this).height()>highestBox){highestBox=$(this).height();}});$('.prod-widget, .healthcare-widget .card',this).height(highestBox);});if($('.owl-carousel.review-slider').length>0){$('.owl-carousel.review-slider').owlCarousel({loop:true,margin:15,dots:false,nav:true,navText:['<i class="fas fa-arrow-left nav-btn prev-slide"></i>','<i class="fas fa-arrow-right nav-btn next-slide"></i>'],responsive:{0:{items:1},500:{items:2},768:{items:3},1000:{items:4},1300:{items:5}}})}
if($('.owl-carousel.popup-owl').length>0){$('.owl-carousel.popup-owl').owlCarousel({loop:true,margin:15,dots:false,nav:true,navText:['<i class="fas fa-arrow-left nav-btn-1 prev-slider"></i>','<i class="fas fa-arrow-right nav-btn-1 next-slider"></i>'],responsive:{0:{items:1},500:{items:1},768:{items:1},1000:{items:1},1300:{items:1}}})}
if($('.owl-carousel.products-search').length>0){$('.owl-carousel.products-search').owlCarousel({loop:true,margin:15,dots:false,nav:false,autoplay:true,autoplayTimeout:3000,responsive:{0:{items:1},500:{items:3},768:{items:4},1000:{items:7},1300:{items:7}}})}
$(document).on("click",".faq-card",function(){$(this).toggleClass('faq-active');});})(jQuery);function readURL(input){if(input.files&&input.files[0]){var reader=new FileReader();reader.onload=function(e){$('#prescription-image').attr('src',e.target.result);}
reader.readAsDataURL(input.files[0]);}}
$(".prescription-upload-btn input").change(function(){readURL(this);$(this).closest('.prescription-btn').next().addClass('show-btn');$(this).closest('.custom-container').addClass('show-pharmacist-confirm');});$(".remove-prescription-image").on("click",function(){$(this).parent().find('#prescription-image').attr("src","#");$(this).parent().removeClass('show-btn');$(this).closest('.custom-container').removeClass('show-pharmacist-confirm');});