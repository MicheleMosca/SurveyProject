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
                    if ('error' in response) {
                        Swal.fire({
                            position: 'top',
                            icon: 'error',
                            title: response['error'],
                            showConfirmButton: false,
                            timer: 1450
                        }).then((result) => {

                        })
                    }
                    else if('msg' in response){
                        Swal.fire({
                            position: 'top',
                            icon: 'success',
                            title: response['msg'],
                            showConfirmButton: false,
                            timer: 1450
                        }).then((result) => {
                            window.location.replace("/survey/login");
                        })
                    }
                },

                failure: function (error){
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