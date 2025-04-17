$("#user-message").html(loadingHTML);
$.get(
{
    url: window.location.origin + window.location.pathname + "json/" + "user" + window.location.search,
    success: function (data) {
        renderUserPage(data);
         $("#user-message").hide();
    }
})

function renderUserPage(data)
{
    var labelsDict = {
        country: [],
    }

    var dataDict = {
        country: [],
    }

    var dataList = [];

    for (var country in data.results.group_by_country)

    {
        var row = [];
        row.push("-")
        labelsDict.country.push(country);
        row.push(country);
        dataDict.country.push(data.results.group_by_country[country]);
        row.push(data.results.group_by_country[country].toLocaleString());

        dataList.push(row);
    }

    totals = Mustache.render(templates.userTableTotals, {totals:"Totals", countries:data.totals.countries.toLocaleString(), users:data.totals.users.toLocaleString()});

    table = $("#userCountryTable").DataTable({
        retrieve: true,
        columns: [
            { title: "Totals"},
            { title: "Country" },
            { title: "Users" },
        ],
       "pageLength": 50,
       "lengthMenu": [ [10, 50, 200, -1], [10, 50, 200, "All"] ]
    })

    table.clear();
    table.rows.add(dataList);
    table.draw();

    $("userTableTotals").html(totals);

    userChart = makeUserChart(dataDict, labelsDict);
}

function makeUserChart(dataDict, labelsDict)
{
    var activeLabels = labelsDict.country;
    var activeData = dataDict.country;

    var html = Mustache.render(templates.canvas, {id:"userChart"})
    $("#userChartBox").html(html);
    var userChartElement = $("#userChart");
    var userChart = new Chart(userChartElement, {
        type: "doughnut",
        data: {
            labels: activeLabels,
            datasets: [{
                data: activeData,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                colorschemes: {
                    scheme: "brewer.Paired12"
                }
            },
            tooltips: {
                callbacks: {
                  label: function(tooltipItem, data) {
                    var dataset = data.datasets[tooltipItem.datasetIndex];
                    var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                    var total = meta.total;
                    var currentValue = dataset.data[tooltipItem.index];
                    var percentage = parseFloat((currentValue/total*100).toFixed(1));
                    return currentValue + " (" + percentage + "%)";
                  },
                  title: function(tooltipItem, data) {
                    return data.labels[tooltipItem[0].index];
                  }
                }
              }
        }
    });
    return userChart
}
