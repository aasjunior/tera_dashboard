// Cores para cada label
let colors = {
  Mal: "#023047",
  Bom: "#45C4B0",
  Sem_resposta: "#8195A8",
};
var mesesAno = [
  "Janeiro",
  "Fevereiro",
  "Março",
  "Abril",
  "Maio",
  "Junho",
  "Julho",
  "Agosto",
  "Setembro",
  "Outubro",
  "Novembro",
  "Dezembro",
];
var line_chart;
var monthly_chart;

if (document.querySelector(".dashboard")) {
  var mal = parseInt(document.getElementById("mal").value) ?? null;
  var bom = parseInt(document.getElementById("bom").value) ?? null;
  var sem_resposta =
    parseInt(document.getElementById("sem_resposta").value) ?? null;
  var mesAtual = new Date().getMonth() ?? null;
  // var dataMal = JSON.parse(document.getElementById("dataMal").value) ?? null;
  // var dataBom = JSON.parse(document.getElementById("dataBom").value) ?? null;
  // var dataSemResposta = JSON.parse(document.getElementById("dataSemResposta").value) ?? null;

  
  var dataMal = [2, 6, 8, 5, 10, 9, 7, 4, 3, 1, 12];
  var dataBom = [10, 5, 3, 8, 6, 4, 11, 9, 7, 2, 12];
  var dataSemResposta = [4, 2, 1, 6, 3, 5, 2, 4, 1, 6, 5];

  var dataMalMensal =
    JSON.parse(document.getElementById("dataMalMensal").value) ?? null;
  var dataBomMensal =
    JSON.parse(document.getElementById("dataBomMensal").value) ?? null;
  var dataSemRespostaMensal =
    JSON.parse(document.getElementById("dataSemRespostaMensal").value) ?? null;

  dailyRecord(mal, bom, sem_resposta);
  annualRecord(dataMal, dataBom, dataSemResposta);
  // monthlyChart(dataMalMensal, dataBomMensal, dataSemRespostaMensal)
  monthlyChart();
}

if (document.querySelector(".patient-card_dash")) {
  const weight_data =
    parseFloat(document.getElementById("weight_data").value) ?? null;
  const sleep_data =
    parseFloat(document.getElementById("sleep_data").value) ?? null;
  const health_data =
    parseFloat(document.getElementById("health_data").value) ?? null;

  weight_chart(weight_data);
  sleep_chart(sleep_data);
  health_chart(health_data);
}

function dailyRecord(mal, bom, sem_resposta) {
  const options = {
    chart: {
      type: "donut",
      height: "90%",
    },
    series: [mal, bom, sem_resposta],
    colors: [colors["Mal"], colors["Bom"], colors["Sem_resposta"]],
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
      max: 12,
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
    newColor = colors["Sem_resposta"];
  }

  line_chart.updateOptions({
    stroke: {
      colors: [newColor],
    },
  });
  line_chart.updateSeries([{ data: newData }]);
}

// function monthlyChart(dataMalMensal, dataBomMensal, dataSemRespostaMensal) {
//   var selectMes = document.getElementById("lbl_mes");
//   var mesSelecionado = selectMes.value; // Obter o mês selecionado (valor de 1 a 12)

//   var semanasMes = Array.from({ length: 5 }, (_, i) => i + 1); // Considerando 5 semanas em cada mês

//   var dataBomSemanal = dataBomMensal.slice((mesSelecionado - 1) * 5, mesSelecionado * 5);
//   var dataMalSemanal = dataMalMensal.slice((mesSelecionado - 1) * 5, mesSelecionado * 5);
//   var dataSemRespostaSemanal = dataSemRespostaMensal.slice((mesSelecionado - 1) * 5, mesSelecionado * 5);

//   // Define as opções do gráfico de área com ApexCharts
//   var area_options = {
//     series: [
//       {
//         name: "Humor: Bom",
//         data: dataBomSemanal,
//       },
//       {
//         name: "Humor: Mal",
//         data: dataMalSemanal,
//       },
//       {
//         name: "Sem Resposta",
//         data: dataSemRespostaSemanal,
//       },
//     ],
//     chart: {
//       height: 350,
//       type: "area",
//     },
//     dataLabels: {
//       enabled: false,
//     },
//     stroke: {
//       curve: "smooth",
//     },
//     xaxis: {
//       categories: semanasMes.map(function (semanaIndex) {
//         return "Semana " + semanaIndex;
//       }),
//     },
//     tooltip: {
//       x: {
//         format: "dd/MM/yy HH:mm",
//       },
//     },
//     colors: [colors["Mal"], colors["Bom"], colors["Sem_resposta"]],
//   };

//   // Cria um novo gráfico de área com os dados mensais
//   var monthly_chart = new ApexCharts(
//     document.querySelector("#g-monthly"),
//     area_options
//   );
//   monthly_chart.render();
// }
function monthlyChart() {
  var dataMal = [2, 6, 8, 5, 10, 9, 7, 4, 3, 1, 12, 11, 6];
  var dataBom = [10, 5, 3, 8, 6, 4, 11, 9, 7, 2, 12, 1, 6];
  var dataSemResposta = [4, 2, 1, 6, 3, 5, 2, 4, 1, 6, 5, 3, 2];
  var dataTime = generateDateRange("2023-06-01", "2023-06-13");

  var colors = {
    Mal: "#023047",
    Bom: "#45C4B0",
    "Sem Registro": "#8195A8",
  };

  var monthly_options = {
    series: [
      {
        name: "Mal",
        data: dataMal,
      },
      {
        name: "Bom",
        data: dataBom,
      },
      {
        name: "Sem Resposta",
        data: dataSemResposta,
      },
    ],
    chart: {
      height: 350,
      type: "area",
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
    },
    xaxis: {
      type: "datetime",
      categories: dataTime,
    },
    tooltip: {
      x: {
        format: "dd/MM/yy",
      },
    },
    colors: [colors["Mal"], colors["Bom"], colors["Sem Registro"]],
  };

  var monthly_chart = new ApexCharts(
    document.querySelector("#g-monthly"),
    monthly_options
  );
  monthly_chart.render();
}

function generateRandomData(count) {
  var data = [];
  for (var i = 0; i < count; i++) {
    data.push(Math.floor(Math.random() * 100) + 1);
  }
  return data;
}

function generateDateRange(startDate, endDate) {
  var currentDate = new Date(startDate);
  var dates = [];
  while (currentDate <= new Date(endDate)) {
    dates.push(currentDate.toISOString().split("T")[0]);
    currentDate.setDate(currentDate.getDate() + 1);
  }
  return dates;
}

function formatDate(date) {
  var year = date.getFullYear();
  var month = ("0" + (date.getMonth() + 1)).slice(-2);
  var day = ("0" + date.getDate()).slice(-2);
  var hours = ("0" + date.getHours()).slice(-2);
  var minutes = ("0" + date.getMinutes()).slice(-2);
  var seconds = ("0" + date.getSeconds()).slice(-2);
  var milliseconds = ("00" + date.getMilliseconds()).slice(-3);

  return (
    year +
    "-" +
    month +
    "-" +
    day +
    " " +
    hours +
    ":" +
    minutes +
    ":" +
    seconds +
    "." +
    milliseconds
  );
}

function weight_chart(data) {
  var weight_options = {
    series: [data],
    chart: {
      height: 100,
      type: "radialBar",
    },
    colors: ["#71DDB1"],
    plotOptions: {
      radialBar: {
        track: {
          background: "#6C95A0",
        },
        hollow: {
          size: "40%",
        },
        dataLabels: {
          show: false,
        },
      },
    },
  };
  var weight_chart = new ApexCharts(
    document.querySelector("#weight-chart"),
    weight_options
  );
  weight_chart.render();
}

function sleep_chart(data) {
  var sleep_options = {
    series: [data],
    chart: {
      type: "radialBar",
      offsetY: 0,
      width: "240px",
      heigh: "220px",
    },
    colors: ["#71DDB1"],
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 135,
        hollow: {
          size: "50%",
        },
        track: {
          background: "#6C95A0",
        },
        dataLabels: {
          name: {
            show: false,
          },
          value: {
            show: false,
          },
        },
      },
    },
    grid: {
      padding: {
        top: 10,
      },
    },
  };

  var sleep_chart = new ApexCharts(
    document.querySelector("#sleep_chart"),
    sleep_options
  );
  sleep_chart.render();
}

function health_chart(data) {
  var health_options = {
    series: [data],
    chart: {
      height: 100,
      type: "radialBar",
    },
    colors: ["#3FBDF1"],
    plotOptions: {
      radialBar: {
        track: {
          background: "#6C95A0",
        },
        hollow: {
          size: "40%",
        },
        dataLabels: {
          show: false,
        },
      },
    },
  };
  var health_chart = new ApexCharts(
    document.querySelector("#health-chart"),
    health_options
  );
  health_chart.render();
}
