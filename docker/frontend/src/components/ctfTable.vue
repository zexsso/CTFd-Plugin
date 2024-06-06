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
  appStore.socket.on("new-flag", (data) => {
	console.log(data)
    const scoreboard = transformData(data.scoreboard);

    teams.value = scoreboard;
  });
});
</script>
