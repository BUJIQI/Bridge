<template>
  <div class="panel panel-default mt-3">
    <div class="panel-heading">
      <h3 class="panel-title">{{ selectedKey }}</h3>
    </div>
    <div class="panel-body">
      <div v-if="explanation">
        <div v-if="explanation.text" class="explanation-text" v-html="formattedText"></div>
        <ul v-if="explanation.list && explanation.list.length" class="explanation-list">
          <li v-for="(item, index) in explanation.list" :key="index" v-html="item"></li>
        </ul>
        <div v-if="explanation.function" class="explanation-function" v-html="formattedFunction"></div>
        <hr v-if="selectedKey == '生产线投资数'">
        <div v-if="explanation.text2" class="explanation-text" v-html="formattedText2"></div>
        <div v-if="explanation.tableHeader" class="explanation-table">  
          <div  v-if="explanation.tableName" class="header">{{ explanation.tableName }}</div>        
          <table>
            <tbody>
              <tr v-for="(header, index) in explanation.tableHeader" :key="index">
                <td class="highlight">{{ header }}</td>
                <td v-for="(data, index) in explanation.tableData[header]" :key="index">{{ data }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="explanation.image" class="explanation-image">
          <img :src="explanation.image" alt="Explanation Image" />
        </div>
      </div>
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
    const explanation = ref(null);

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
      const mappedKey = keyMapping[noun] || noun;
      if (mappedKey && nounsExplanation.value[mappedKey]) {
        selectedKey.value = mappedKey; 
        selectedValue.value = nounsExplanation.value[mappedKey];
        explanation.value = formatExplanation(selectedValue.value, selectedKey.value);
      } else {
        selectedKey.value = '';
        selectedValue.value = '';
        explanation.value = null;
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

    // 格式化解释内容
    const formatExplanation = (data, selectedKey) => {
      const baseKey = `${selectedKey}文本一`;
      const baseKey2 = `${selectedKey}文本二`;
      const listKey = `${selectedKey}列表`;
      const functionKey = `${selectedKey}函数`;
      const tableNameKey = `${selectedKey}表名`;
      const tableHeaderKey = `${selectedKey}表头`;
      const tableDataKey = `${selectedKey}表数据`;
      const imageKey = `${selectedKey}图片`;

      const formattedData = {
        text: data[baseKey] ? data[baseKey]['文字'] : '',
        emphasis: data[baseKey] ? data[baseKey]['强调'] : '',
        list: data[listKey] ? data[listKey] : [],
        function: data[functionKey] ? data[functionKey] : '',
        text2: data[baseKey2] ? data[baseKey2] : '',
        tableName: data[tableNameKey] ? data[tableNameKey] : '',
        tableHeader: data[tableHeaderKey] ? data[tableHeaderKey] : [],
        tableData: data[tableDataKey] ? data[tableDataKey] : {},
        image: data[imageKey] ? data[imageKey] : ''
      };

      // 将强调内容包含在文字中
      if (formattedData.emphasis) {
        formattedData.text = formattedData.text.replace(formattedData.emphasis, `<span class="text-danger" style="font-weight: bold;">${formattedData.emphasis}</span>`);
      }

      return formattedData;
    };

    // 计算属性，将 \r\n 替换为 <p> 标签
    const formattedText = computed(() => {
      return explanation.value.text.split('\\r\\n').map(line => `<p>${line}</p>`).join('');
    });

    const formattedText2 = computed(() => {
      return explanation.value.text2.split('\\r\\n').map(line => `<p>${line}</p>`).join('');
    });

    const formattedFunction = computed(() => {
      return explanation.value.function.split('\\r\\n').map(line => `<p>${line}</p>`).join('');
    });

    return {
      selectedKey,
      formattedText,
      formattedText2,
      formattedFunction,
      explanation,
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
}

.panel-body {
  padding: 20px;
  border-radius: 8px;
}

.explanation-list {
  margin-bottom: 15px;
  padding-left: 20px;
  color: #333333;
  font-size: 15px;
}

.explanation-list li {
  margin-bottom: 5px;
}

.explanation-function {
  margin-bottom: 15px;
  color: #333333;
  background-color: #ffe6e6;
  padding: 20px;
  border-radius: 4px;
  font-size: 15px;
  width: fit-content;
  line-height: 0.5;
  font-size: 15px;
  font-family: 'Courier New', Courier, monospace;
}

.explanation-table {
  border: 1px solid #ddd;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2); 
  width: fit-content;
  font-size: 15px;
}

.header {
  background-color: #797979;
  color: #fff;
  padding: 10px;
}

.highlight {
  background-color: #f3776c;
  color: #fff;
  border: 1px solid #ddd;
}

td {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

.explanation-image {
  margin-bottom: 15px;
}

hr {
  border-top: 2px dashed rgb(255, 0, 0); 
}
</style>