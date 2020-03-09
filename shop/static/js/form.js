jQuery(function(){
    jQuery('.main-button').click(function(){
		$('.button-wrapper').addClass('clicked');
		setTimeout(function(){
			$('.layered-content').addClass('active');
		}, 1500);
	});
	$('.close-button').on('click', function(){
		$('.button-wrapper').removeClass('clicked');
		$('.layered-content').removeClass('active');
	});

});

