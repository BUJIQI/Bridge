import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        userInfo: null,
    }),
    actions: {
        setUserInfo(info) {
            this.userInfo = info;
        },
    },
});
