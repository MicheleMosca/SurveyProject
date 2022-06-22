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
                        const div = document.getElementsByClassName('error-messages')[0];
                        div.insertAdjacentHTML(
                            'afterend',
                            response['error'],
                        );

                        const parser = new DOMParser();
                        const doc = parser.parseFromString(response['error'], 'text/html');
                        const list = doc.getElementsByTagName('ul')[0];

                        for (let i=0; i < list.children.length; i++)
                        {
                            const element = list.children[i].childNodes[0].textContent; // TODO: Aggiungerlo al sito
                            const context = list.children[i].childNodes[1].textContent;
                            console.log(element);
                            console.log(context);
                        }
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