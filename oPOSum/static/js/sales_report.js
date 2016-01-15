$('.toggler').click(function(e){
    e.preventDefault();
    var el = $(this);
    var id = el.attr('data-toggle');
    $(id).toggleClass('hidden');
});
