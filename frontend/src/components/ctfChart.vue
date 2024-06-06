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
  import 'chartjs-adapter-date-fns';
  
  const appStore = useAppStore();
  
  let dataG = {
	1: {
	  id: 23,
	  name: "byting",
	  solves: [
		{
		  challenge_id: 3,
		  account_id: 23,
		  team_id: 23,
		  user_id: 25,
		  value: 100,
		  date: "2024-06-06T18:25:34.529088Z",
		},
		{
		  challenge_id: 2,
		  account_id: 23,
		  team_id: 23,
		  user_id: 25,
		  value: 50,
		  date: "2024-06-06T18:26:36.362374Z",
		},
		{
		  challenge_id: 1,
		  account_id: 23,
		  team_id: 23,
		  user_id: 25,
		  value: 100,
		  date: "2024-06-06T18:39:57.262075Z",
		},
	  ],
	  score: 10091,
	},
	2: {
	  id: 25,
	  name: "fgdsgdsg",
	  solves: [
		{
		  challenge_id: 3,
		  account_id: 25,
		  team_id: 25,
		  user_id: 27,
		  value: 100,
		  date: "2024-06-06T18:44:35.764658Z",
		},
		{
		  challenge_id: 2,
		  account_id: 25,
		  team_id: 25,
		  user_id: 27,
		  value: 90,
		  date: "2024-06-06T18:45:42.369208Z",
		},
	  ],
	  score: 91,
	},
	3: {
	  id: 24,
	  name: "ee",
	  solves: [
		{
		  challenge_id: 3,
		  account_id: 24,
		  team_id: 24,
		  user_id: 26,
		  value: 100,
		  date: "2024-06-06T18:40:20.591081Z",
		},
		{
		  challenge_id: 4,
		  account_id: 24,
		  team_id: 24,
		  user_id: 26,
		  value: 200,
		  date: "2024-06-06T19:40:20.591081Z",
		},
	  ],
	  score: 1,
	},
  };
  
  const chartData = ref();
  const chartOptions = ref();
  
  const maxTeam = 10;
  
  // Couleurs prédéfinies
  const colors = [
	"#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", 
	"#9966FF", "#FF9F40", "#E7E9ED", "#71B37C", 
	"#F7464A", "#46BFBD"
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
		  type: 'time',
		  time: {
			unit: 'minute',
			tooltipFormat: 'HH:mm:ss',
			displayFormats: {
			  minute: 'HH:mm:ss'
			}
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
	const chartboard = transformData(dataG);
  
	chartData.value = setChartData(chartboard);
	chartOptions.value = setChartOptions();
  
	appStore.socket.emit("scoreboard", (data) => {
	  const chartboard = transformData(data);
  
	  chartData.value = setChartData(chartboard);
	  chartOptions.value = setChartOptions();
	});
  
	appStore.socket.on("new-flag", (data) => {
	  const chartboard = transformData(data);
  
	  chartData.value = setChartData(chartboard);
	  chartOptions.value = setChartOptions();
	});
  });
  </script>