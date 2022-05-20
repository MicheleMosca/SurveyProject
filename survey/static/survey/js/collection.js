$(document).ready(function (){
    // Submit post on submit
    $('.post-form').on('submit', function (event){

        event.preventDefault();

        const form = $(this);

        const div = form.children('div').get(0);
        div.className = "card border-success mb-3";

        const h5 = form.children('div').children('div').children('h5').get(0);
        h5.className = "card-title text-success";

        $.ajax({
            type: "POST",
            url: "",
            data: form.serialize(),

            success: function (response){
                // handleAlerts('success', 'Answer submitted!')
                Swal.fire({
                  position: 'top',
                  icon: 'success',
                  title: 'Answer Submitted!',
                  showConfirmButton: false,
                  timer: 1250
                })
            },

            failure: function (error){
                // handleAlerts('danger', 'Error!');
                Swal.fire({
                  position: 'top',
                  icon: 'error',
                  title: 'Error!',
                  showConfirmButton: false,
                  timer: 1250
                })
            }
        })
    });
})