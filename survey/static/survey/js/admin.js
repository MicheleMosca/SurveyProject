$(document).ready(function (){
    // Submit post on submit
    $('.post-form').on('submit', function (event){

        event.preventDefault();

        const form = $('.post-form')[0];
        const formData = new FormData(form);
        const input = $(this).children('input').get(1);

        if (formData.get('file').name === '')
        {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Error: File is not selected!',
                showConfirmButton: true
            })
        } else {
            $.ajax({
                type: "POST",
                enctype: 'multipart/form-data',
                url: "",
                data: formData,
                processData: false,
                contentType: false,
                cache: false,

                success: function (response){
                    if ('msg' in response){
                        Swal.fire({
                          position: 'top',
                          icon: 'success',
                          title: response['msg'],
                          showConfirmButton: false,
                          timer: 1250
                        })
                        setInterval('location.reload()', 1250);
                    } else {
                        Swal.fire({
                          position: 'top',
                          icon: 'error',
                          title: response['error'],
                          showConfirmButton: true
                        }).then((result) => {
                            if (result.isConfirmed)
                                input.value = ''
                        })
                    }
                },

                failure: function (error){
                    Swal.fire({
                      position: 'top',
                      icon: 'error',
                      title: error,
                      showConfirmButton: false,
                      timer: 1250
                    })
                }
            })
        }
    });
})