<template>
  <div class="flex justify-center h-[60vh] w-full">
    <DataTable
      :value="teams"
      stripedRows
      paginator
      :rows="10"
      class="w-[80vw] p-10"
    >
      <Column field="place" header="Place"></Column>
      <Column field="name" header="Equipe"></Column>
      <Column field="score" header="Score"></Column>
      <Column field="num_solves" header="Nombre de Challenges Validés"></Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAppStore } from "../stores/appStore";

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
        value: 1,
        date: "2024-06-06T18:25:34.529088Z",
      },
      {
        challenge_id: 2,
        account_id: 23,
        team_id: 23,
        user_id: 25,
        value: 90,
        date: "2024-06-06T18:26:36.362374Z",
      },
      {
        challenge_id: 1,
        account_id: 23,
        team_id: 23,
        user_id: 25,
        value: 10000,
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
        value: 1,
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
        value: 1,
        date: "2024-06-06T18:40:20.591081Z",
      },
    ],
    score: 1,
  },
};

const teams = ref([]);

const transformData = (data) => {
  const transformedData = Object.values(data)
    .map((team, index) => ({
      place: index + 1,
      name: team.name,
      score: team.score,
      num_solves: team.solves.length,
    }))
    .sort((a, b) => b.score - a.score);

  return transformedData;
};

onMounted(() => {
  const scoreboard = transformData(dataG);

  teams.value = scoreboard;

  appStore.socket.emit("scoreboard", (data) => {
    const scoreboard = transformData(data);

    teams.value = scoreboard;
  });

  appStore.socket.on("new-flag", (data) => {
    const scoreboard = transformData(data);

    teams.value = scoreboard;
  });
});
</script>
