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

function getStockDetail(tiker) {
    $.ajax({
        url: "/detail",
        type: "GET",
        dataType: "json",
        data: {tiker: tiker},
        success: function (data) {
            document.getElementById('detail').removeAttribute('hidden');
            document.getElementById('company_description').innerText = data['info'][0]['description']
            document.getElementById('country').innerText = data['info'][0]['country']
            document.getElementById('industry').innerText = data['info'][0]['industry']
            document.getElementById('sector').innerText = data['info'][0]['sector']
            document.getElementById('dividents').innerText = data['info'][0]['lastDiv']
            chartDraw(data['historical'])
        }
    });
}


function chartDraw(map) {
    var table = anychart.data.table('date');
    table.addData(map);

    mapping = table.mapAs({x: 'date', value: 'close'});

    var chart = anychart.stock();

    var series = chart.plot(0).area(mapping);

    var scrollerSeries = chart.scroller().area(table.mapAs({'value': 'value'}));

    series.seriesType("column");

    scrollerSeries.seriesType("column");

    document.getElementById('graph')
}