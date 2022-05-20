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