import { defineStore } from "pinia";
import { ref } from "vue";
import { io } from "socket.io-client";

export const useAppStore = defineStore("app", () => {
  // Vue & PrimeVue
  const router = ref();
  const socket = ref();

    socket.value = io(`${import.meta.env.VITE_SOCKET_URL}`, {
      transports: ["websocket"],
    });

    socket.value.on("connect", () => {
      console.log("Connected to the socket server");
    });

  return {
    router,
    socket,
  };
});
