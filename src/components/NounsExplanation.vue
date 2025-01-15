<template>
  <div class="panel panel-default mt-3">
    <div class="panel-heading">
      <h3 class="panel-title">{{ selectedKey }}</h3>
    </div>
    <div class="panel-body">
      <span v-html="formattedSelectedValue"></span>
    </div>
  </div>    
</template>

<script>
import axios from '@/api/axios';
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const selectedKey = ref('');
    const selectedValue = ref('');
    const nounsExplanation = ref({});

    // 键名映射对象
    const keyMapping = {
      '附一：投标价格': '附加市场I--投标价格',
      '附二：特殊产品数': '附加市场II--特殊产品数',
      '购买原材料量': '购买原材料、附件量',
      '购买附件量': '购买原材料、附件量',
      '科研人员招收数': '研发人员招收和辞退',
      '科研人员辞退数': '研发人员招收和辞退',
    };

    const fetchData = async () => {
      try {
        const response = await axios.get('/users/import_imformation/', {
          withCredentials: true
        });
        nounsExplanation.value = response.data;
      } catch (error) {
        console.error('Error fetching import information:', error);
      }
    };

    // 监听路由变化，更新显示内容
    const updateContent = () => {
      const noun = route.params.noun;
      console.log('Current noun:', noun); 
      const mappedKey = keyMapping[noun] || noun;
      if (mappedKey && nounsExplanation.value[mappedKey]) {
        selectedKey.value = mappedKey; 
        selectedValue.value = nounsExplanation.value[mappedKey];
      } else {
        selectedKey.value = '';
        selectedValue.value = '';
      }
    };

    onMounted(() => {
      fetchData().then(() => {
        updateContent();
      });
    });

    watch(
      () => route.params.noun,
      () => {
        updateContent();
      }
    );

    // 计算属性，将 \r\n 替换为 <p> 标签
      const formattedSelectedValue = computed(() => {
      return selectedValue.value.split('\r\n').map(line => `<p>${line}</p>`).join('');
    });  


    return {
      selectedKey,
      formattedSelectedValue,
    };
  },
};
</script>

<style scoped>  
.panel {
  margin-top: 20px;
  border-radius: 8px;
}

.panel-heading {
  background-color: #f7f7f9;
  padding: 15px;
  font-size: 1.25rem;
}

.panel-body {
  padding: 20px;
}

.panel-body p {
  margin-bottom: 30px; 
}
</style>