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
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(response['error'], 'text/html');
                        const list = doc.getElementsByTagName('ul')[0];

                        const context = list.children[0].childNodes[1].textContent;

                        Swal.fire({
                            position: 'top',
                            icon: 'error',
                            title: context,
                            showConfirmButton: false,
                            timer: 1850
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
                            window.location.replace("../login");
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