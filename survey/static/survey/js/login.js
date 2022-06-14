$(document).ready(function (){
    // Submit post on submit
    $('.post-form').on('submit', function (event){

        event.preventDefault();

        const form = $(this);
        const usernameField = form.children('div').children('input').get(0);
        const passwordField = form.children('div').next().children('input').get(0);

        if (usernameField.value === ''){
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Username field is empty',
                showConfirmButton: false,
                timer: 1450
            })
        } else if (passwordField.value === ''){
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Password field is empty',
                showConfirmButton: false,
                timer: 1450
            })
        } else {
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
                            usernameField.value = '';
                            passwordField.value = '';
                        })
                    }
                    else if('msg' in response){
                        window.location.replace("/survey/home");
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
        }
    });
})