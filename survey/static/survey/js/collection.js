const handleAlerts = (type, text) =>{
    const alertBox = document.getElementById('alert-box');
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert"> ${text} </div>`
}

$(document).ready(function (){
    // Submit post on submit
    $('.post-form').on('submit', function (event){

        event.preventDefault();

        const form = $(this);
        $.ajax({
            type: "POST",
            url: "",
            data: form.serialize(),

            success: function (response){
                handleAlerts('success', 'Answer submitted!')
            },

            failure: function (error){
                handleAlerts('danger', 'Error!');
            }
        })
    });
})