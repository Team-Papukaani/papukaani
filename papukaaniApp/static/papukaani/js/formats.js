function init(){
    $(".help").each(function(index, element){
        $(element).hide();
    });
}

function toggleElement(id){
    $("#"+id).toggle();
}
