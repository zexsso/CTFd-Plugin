<template>
  <div class="flex justify-center h-[40vh] w-full">
    <Chart
      type="line"
      :data="chartData"
      :options="chartOptions"
      class="w-[70vw] p-10"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAppStore } from "../stores/appStore";

// Importer l'adaptateur de date
import "chartjs-adapter-date-fns";

const appStore = useAppStore();

const chartData = ref();
const chartOptions = ref();

const maxTeam = 10;

// Couleurs prédéfinies
const colors = [
  "#FF6384",
  "#36A2EB",
  "#FFCE56",
  "#4BC0C0",
  "#9966FF",
  "#FF9F40",
  "#E7E9ED",
  "#71B37C",
  "#F7464A",
  "#46BFBD",
];

const transformData = (data) => {
  let transformedData = Object.values(data)
    .map((team) => ({
      name: team.name,
      solves: team.solves.map((solve) => ({
        date: new Date(solve.date),
        value: solve.value,
      })),
    }))
    .slice(0, maxTeam);

  return transformedData;
};

const setChartData = (data) => {
  // Générer des labels uniques à partir des dates de toutes les équipes
  const labels = Array.from(
    new Set(
      data.flatMap((team) =>
        team.solves.map((solve) => solve.date.toISOString())
      )
    )
  ).sort();

  const datasets = data.map((team, index) => {
    const cumulativeData = [];
    let cumulativeScore = 0;

    labels.forEach((label) => {
      const dateSolves = team.solves.filter(
        (solve) => solve.date.toISOString() === label
      );

      dateSolves.forEach((solve) => {
        cumulativeScore += solve.value;
      });

      cumulativeData.push(cumulativeScore);
    });

    return {
      label: team.name,
      data: cumulativeData,
      fill: false,
      borderColor: colors[index % colors.length], // Assign a color from the predefined array
    };
  });

  return {
    labels: labels,
    datasets: datasets,
  };
};

const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue("--text-color");
  const textColorSecondary = documentStyle.getPropertyValue(
    "--text-color-secondary"
  );
  const surfaceBorder = documentStyle.getPropertyValue("--surface-border");

  return {
    maintainAspectRatio: false,
    aspectRatio: 0.6,
    plugins: {
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
    scales: {
      x: {
        type: "time",
        time: {
          unit: "minute",
          tooltipFormat: "HH:mm:ss",
          displayFormats: {
            minute: "HH:mm:ss",
          },
        },
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
      y: {
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
    },
  };
};

onMounted(() => {
  chartOptions.value = setChartOptions();

//   appStore.socket.emit("scoreboard", (data) => {
//     const chartboard = transformData(data.scoreboard);

//     chartData.value = setChartData(chartboard);
//   });

  appStore.socket.on("new-flag", (data) => {
    const chartboard = transformData(data.scoreboard);

    chartData.value = setChartData(chartboard);
  });
});
</script>
