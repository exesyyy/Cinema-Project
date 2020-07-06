$(document).ready(function boxes(){
    var counter = 1;
    var counterN = counter -1;
    var orari = []

    $("#addButton").click(function () {
        var temp = []
        if(counter>5){
            alert("Only 5 times allowed");
            return false;
        }
        if(counter>1){
            temp.push($('#data'+counterN).val());            
            temp.push($('#orario'+counterN).val());
            temp.push($('#selecthall'+counterN).val());
            orari.push(temp);
            //orari[counterN].push($('#selecthall'+counterN).val());
        }
        counterN++;
        console.log(orari);
        console.log(JSON.stringify({orari}));
        var newTextBoxDiv = $(document.createElement('div'))
            .attr("id", 'TextBoxDiv' + counter);
        newTextBoxDiv.after().html('<label>Data : </label>' +
            '<input type="date" name="mydate' + counter +
            '" id="data' + counter + '" value="" required>' +
            '<label>Orario : </label>' +
            '<input type="time" name="mytime' + counter +
            '" id="orario' + counter + '" value="" required>' +
            '<input type="text" id="selecthall' + counter +
            '" name="selectedhall' + counter + '" placeholder="Sala" required>');
        
        newTextBoxDiv.appendTo("#TextBoxesGroup");
        counter++;
    });

    $("#removeButton").click(function () {
        if(counter==1){
        alert("No more times to remove");
            return false;
        }
        counter--;  
        $("#TextBoxDiv" + counter).remove();
        if(counter - orari.length == 0){
            orari.pop();
        }
        counterN--;
        console.log(orari);
    });

    $('#submit').click(function() {
        temp.push($('#data'+counterN).val());            
        temp.push($('#orario'+counterN).val());
        temp.push($('#selecthall'+counterN).val());
        orari.push(temp);
        counterN++;
        console.log(orari);
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/timeinsert",
            data: JSON.stringify({orari}),
            dataType: "application/json"
        });
    });
    
});