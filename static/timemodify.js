
var selectedfilm;
var orari = '<select class="custom-select" name="oldtime">';
orari += '<option selected>Vecchio Orario</option>';
$("select.time-select").change(function(){
    selectedfilm = $(this).children("option:selected").val();
    alert("You have selected the film - " + selectedfilm);

    var lis = {{lista}};
    for(var i=0; i<lis.length; i++){
        if(lis[i]['id'] == selectedfilm){
            for(var j=0; j<lis[i]['orari'].length; j++){
                orari += '<option value="' + lis[i]['orari'][j]['id_orario'] + '">' + lis[i]['orari'][j]['orario'] + '</option>';
            }
        }
    }
    orari += '</select>'
    document.write(orari);
});