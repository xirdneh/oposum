balco.deleteSuccessMessage = function(){
    var $sm = $("p.success_message");
    window.setTimeout(
        function(){
            $sm.hide()
        },
        5000
    );
}
