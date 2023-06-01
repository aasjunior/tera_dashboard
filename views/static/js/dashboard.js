const mal = parseInt(document.getElementById("mal").value) ?? null;
const bom = parseInt(document.getElementById("bom").value) ?? null;
const sem_resposta = parseInt(document.getElementById("sem_resposta").value) ?? null;

if(document.querySelector('.dashboard')){
    dailyRecord(mal, bom, sem_resposta);
}

function dailyRecord(mal, bom, sem_resposta) {
  const options = {
    chart: {
      type: "donut",
      height: "90%",
    },
    series: [mal, bom, sem_resposta],
    colors: ["#023047", "#45C4B0", "#8195A8"],
    labels: ["Humor: Mal", "Humor: Bom", "Sem resposta"],
    legend: {},
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: true,
            name: {
              fontSize: "24px",
              color: "#888",
              offsetY: -5,
            },
            value: {
              fontSize: "24px",
              color: "#111",
              offsetY: 16,
            },
            total: {
              show: true,
              fontSize: "16px",
              color: "#888",
              label: "Total",
              formatter: function (w) {
                return w.globals.seriesTotals.reduce((a, b) => a + b, 0);
              },
            },
          },
          size: "60%",
          strokeWidth: 0,
        },
      },
    },
  };

  const dailyRecord_chart = new ApexCharts(
    document.querySelector("#g-daily"),
    options
  );
  dailyRecord_chart.render();
}
