import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        userInfo: null,
        selectedHistory: null
    }),
    actions: {
        setUserInfo(info) {
            this.userInfo = info;
        },
        setSelectedHistory(cycle) {
            this.selectedHistory = cycle;
        }
    }
});
