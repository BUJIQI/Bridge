<template>
  <div class="panel panel-default mt-3">
    <div class="panel-heading">
      <h3 class="panel-title">重要信息！</h3>
    </div>
    <div class="panel-body">
      <p class="welcome-text">欢迎进入《创业决策》人机对抗工作站！</p>

      <h4 class="subtitle highlight">上方导航栏关键栏目为：</h4>
      <ul class="info-list">
        <li><strong>重要信息（当前页，首次来访务必查看）</strong></li>
        <li>“新的一轮”按钮（重新开始新的一轮决策，即从新的第一周期开始）</li>
        <li>当前基本信息（组、企业、对手、周期）</li>
      </ul>

      <h4 class="subtitle highlight">左侧菜单栏推荐点击顺序为：</h4>
      <ol class="recommend-list">
        <li>数据报表——市场周期形势（查看当期、往期、历史平均周期形势）</li>
        <li>进行决策（推荐按照给定顺序决策，可根据需要进行预算、提交）</li>
        <li>竞争结果报表（提交决策方案后可查看当期结果）</li>
        <li>数据报表——企业数据报表（查看当期、预算、历史报告）</li>
        <li>评价决策总表</li>
      </ol>

      <h4 class="subtitle highlight">其他提醒：</h4>
      <p>按菜单栏推荐顺序循序渐进使用，即可完成一个周期的决策仿真过程。</p>
      <p>完整的决策仿真过程含有<strong>七个周期</strong>，第七周期的评价总分才是一轮决策仿真的最终成绩。</p>
      <p>务必控制好每个周期的决策时间，掌握好时间进度，每个周期决策过程不宜过快或过慢。</p>
      <p>人机对抗决策过程可重复进行，在规定时间内点击“新的一轮”按钮即可重新开始决策。</p>
      <p>重新开始新的一轮，如难易系数表被设置为了随机，则每轮的周期市场形势均会作变化。</p>
      <p><strong>努力把握市场机会，树立竞争意识，扩大企业规模，应对极端变数，善于困境逆袭求胜。</strong></p>
    </div>
  </div>
</template>

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

.welcome-text {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 1.3rem;
  margin-top: 20px;
  font-weight: bold;
  color: #b14040;
}

.info-list,
.recommend-list {
  margin: 10px 0;
  padding-left: 20px;
}

.info-list li,
.recommend-list li {
  margin-bottom: 10px;
  line-height: 1.4;
}

.highlight {
  font-weight: bold;

  background-color: rgba(212, 91, 91, 0.1);
  padding: 5px;
  border-radius: 4px;
}

</style>