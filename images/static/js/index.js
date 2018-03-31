new LazyLoad();


// function remove_button(id) {
//
//     swal({
//             title: "你確定要刪除嗎?",
//             text: "你將要刪除這張圖片",
//             type: "warning",
//             showCancelButton: true,
//             confirmButtonClass: "btn-danger",
//             confirmButtonText: "Yes, delete it!",
//             closeOnConfirm: false,
//             showLoaderOnConfirm: true
//         },
//         function () {
//
//             $.ajax({
//                 url: '/api/image/' + id + '/',
//                 method: 'DELETE'
//             }).success(function (data, textStatus, jqXHR) {
//                 location.reload();
//             }).error(function (jqXHR, textStatus, errorThrown) {
//                 console.log(jqXHR)
//             });
//
//         });
// }
