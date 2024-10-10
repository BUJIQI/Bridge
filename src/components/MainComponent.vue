<template>
    <div>
        <h2>你所属的是第{{ userInfo?.group }}组第{{ userInfo?.number }}企业，仅有{{ userInfo?.rival }}位竞争对手，目前处于创业决策仿真的第{{ userInfo?.cycle }}周期。</h2>
    </div>
</template>

<script>
import { useUserStore } from '@/store/user';

export default {
    setup() {
        const userStore = useUserStore();
        const userInfo = userStore.userInfo;

        return {
            userInfo,
        };
    },
};
</script>
