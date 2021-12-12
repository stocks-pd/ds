$(document).ready(function () {
    //переключение вкладок
    $(".jstab > li:not('.selected, .blk')").click(function () {
        var cb = $(this);

        $(".tabs > li").removeClass("selected");
        var cc = cb.attr("class");
        cb.addClass("selected");
        $("form > div").hide();
        $("form > div[id=" + cc + "]").show();
    });
});

function getStockDetail(ticker) {
    $.ajax({
        url: "/detail",
        type: "GET",
        dataType: "json",
        data: {ticker: ticker},
        success: function (data) {
            document.getElementById('detail').removeAttribute('hidden');
            document.getElementById('company_description').innerText = data['info'][0]['description']
            document.getElementById('country').innerText = data['info'][0]['country']
            document.getElementById('industry').innerText = data['info'][0]['industry']
            document.getElementById('sector').innerText = data['info'][0]['sector']
            document.getElementById('dividents').innerText = data['info'][0]['lastDiv']
            graph_data = data['historical'];
            console.log(graph_data)
        }
    });
}

