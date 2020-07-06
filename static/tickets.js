
$(document).ready(function boxes(){
    var selectedTickets = [];

    $("td").on("click", function(){
        //Devo fare il controllo se la casella non ha già il posto occupato
        if ($(this).hasClass("booked") || $(this).hasClass("reserved") ||
            $(this).hasClass("columns") || $(this).hasClass("rows")){
            console.log("Questo posto è già occupato");
        }
        else{
            $(this).toggleClass("selected");
        }
    });


    $("#confirm").click(function(){
        var selected = $(".selected");
        for(var i = 0 ; i < selected.length; i++){
            selectedTickets.push(selected[i].id);
        }
        console.log(selectedTickets);
        console.log(JSON.stringify({selectedTickets}));
        //console.log(idOrario);
        $.ajax({
            type: "POST",        
            url: "http://127.0.0.1:5000/buyticket",            
            data: JSON.stringify({selectedTickets}),
            contentType: "application/json"
        }).done(function(data){
            window.location.href = '/buyticket?price='+data;
            console.log(data);
        });       
    });
});