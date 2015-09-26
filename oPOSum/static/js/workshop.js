var add_workshop_btn = $("#workshop_ticket_add");
if(add_workshop_btn){
    add_workshop_btn.click(function(){
        var modal = $("#mensaje");
        modal.one('show.bs.modal', function(event){
            var mod = $(this);
            var modal_body = mod.find("#mensaje-body");
            var modal_title = mod.find("#mensaje-title");
            modal_title.text("Agregar Reparación");
            var body = "<div id='user_branch'></div>" +
            "<label for='layaway-type'>Ti
        });
    });
}
