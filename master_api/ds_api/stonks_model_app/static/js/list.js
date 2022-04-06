$(document).ready(function () {
    $('#table').DataTable({
        data: table,
        dom: '<"search"fl><"top">rt<"bottom"ip><"clear">',
        buttons: [],
        language: {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "infoPostFix": "",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            }
        },
        "iDisplayLength": 25,
        "aLengthMenu": [[10, 20, 50, 100, -1], [10, 20, 50, 100, "все"]],
        columns: [
            {
                data: 'company_name'
            },
            {
                data: 'ticker'
            },
            {
                data: 'price',
                render: function (data, type, row, meta) {
                 return data + "$"
                }
            },

            {
                data: 'absolute_price_change',
                render: function (data, type, row, meta) {
                    var absol = data.toFixed(2) < 0 ? data.toFixed(2) : "+" + data.toFixed(2);
                    var rel = data.toFixed(2) < 0 ? row['relative_price_change'].toFixed(2) : "+" + row['relative_price_change'].toFixed(2);
                    var colour = absol < 0 ? 'red' : 'green'
                    return type === 'display' ?
                        '<span style="color:' + colour + '">' + absol + '$ (' + rel + '%)' + '</span>' :
                        absol + '$ (' + rel + '%)';
                }
            },
        ]


    });

    $('tr').click(function (el) {
        let ticker = el.target.parentNode.childNodes[1].innerText;
        location.href = '/detail/' + ticker;
    })
});

