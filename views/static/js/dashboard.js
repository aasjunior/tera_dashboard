const mal = parseInt(document.getElementById("mal").value) ?? null;
const bom = parseInt(document.getElementById("bom").value) ?? null;
const sem_resposta = parseInt(document.getElementById("sem_resposta").value) ?? null;

var dataMal = JSON.parse(document.getElementById("dataMal").value) ?? null;
var dataBom = JSON.parse(document.getElementById("dataBom").value) ?? null;
var dataSemResposta = JSON.parse(document.getElementById("dataSemResposta").value) ?? null;
var line_chart;

// Cores para cada label
let colors = {
  Mal: "#023047",
  Bom: "#45C4B0",
  "Sem resposta": "#8195A8",
};

if (document.querySelector(".dashboard")) {
  dailyRecord(mal, bom, sem_resposta);
  annualRecord(dataMal, dataBom, dataSemResposta);
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

function annualRecord(dataMal, dataBom, dataSemResposta) {

  // Obtém o mês atual
  var mesAtual = new Date().getMonth();
  var mesesAno = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
  ];

  // Cria um array com os nomes dos meses do ano
  var meses = [];

  for (var i = mesAtual - 11; i <= mesAtual; i++) {
    var mes = (i < 0 ? 12 + i : i) % 12; // Ajusta o índice para garantir um valor entre 0 e 11
    meses.push(mesesAno[mes].substr(0, 3));
  }

  // Define o intervalo do eixo X para exibir os meses do ano
  var xaxisRange = {
    min: new Date().getFullYear() - 1 + "-" + (mesAtual + 1) + "-01",
    max: new Date().getFullYear() + "-" + (mesAtual + 1) + "-01",
  };

  // Dados iniciais do gráfico
  var initialData = dataMal;
  var initialColor = colors["Mal"];

  var line_options = {
    series: [
      {
        data: initialData,
      },
    ],
    chart: {
      id: "line-chart",
      height: 350,
      type: "line",
      animations: {
        enabled: true,
        easing: "linear",
        dynamicAnimation: {
          speed: 1000,
        },
      },
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
      colors: [initialColor],
    },
    markers: {
      size: 0,
    },
    xaxis: {
      type: "category",
      categories: meses,
    },
    yaxis: {
      max: 200,
    },
    legend: {
      show: false,
    },
  };
  line_chart = new ApexCharts(
    document.querySelector("#g-annual"),
    line_options
  );
  line_chart.render();

}

// Filtrar o gráfico com base na label selecionada
function filterChart(label) {
  var newData, newColor;

  if (label === "Mal") {
    newData = dataMal;
    newColor = colors["Mal"];
  } else if (label === "Bom") {
    newData = dataBom;
    newColor = colors["Bom"];
  } else if (label === "Sem resposta") {
    newData = dataSemResposta;
    newColor = colors["Sem resposta"];
  }

  line_chart.updateOptions({
    stroke: {
      colors: [newColor],
    },
  });
  line_chart.updateSeries([{ data: newData }]);
}
