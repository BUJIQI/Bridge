<template>
  <div class="panel panel-default mt-3">
    <div class="panel-heading">
      <h3 class="panel-title">基本规则</h3>
    </div>
    <div class="panel-body">
      <p class="welcome-text">欢迎进入《创业决策》人机对抗工作站！</p>

      <h4 class="subtitle highlight">上方导航栏关键栏目为：</h4>
      <ul class="nav-list">
        <li>“决策仿真”链接：本网站主要功能页面，用于决策仿真</li>
        <li>“重要信息”链接：决策基本规则（本页面）、决策名词解释</li>
        <li>“新的一轮”按钮：重新开始新的一轮决策，即从新的第一周期开始</li>
        <li>当前基本信息：组、企业、对手、周期</li>
        <li>“注销”链接：注销账户、退出登录</li>
        <li>“我的资料”按钮：用户可查看个人资料、历史对局信息</li>
      </ul>

      <h4 class="subtitle highlight">“仿真决策”左侧菜单栏推荐点击顺序为：</h4>
      <ol class="decision-list">
        <li>数据报表——市场周期形势：查看当期、往期、历史平均周期形势</li>
        <li>进行决策——输入决策数据：推荐按照给定顺序模块进行决策</li>
        <li>竞争结果报表：提交决策方案后可查看当期结果</li>
        <li>数据报表——企业数据报表：查看当期、历史报告，用于后续决策</li>
        <li>决策评价总表：查看各类指标评价、综合评价，其中综合评价是比赛的综合成绩</li>
      </ol>

      <h4 class="subtitle highlight">“重要信息”左侧菜单栏为：</h4>
      <ul class="info-list">
        <li><strong>决策基本规则：当前页，首次来访务必查看</strong></li>
        <li>决策名词解释：了解各类决策名词的含义，便于做出正确决策</li>
      </ul>

      <h4 class="subtitle highlight">“我的资料”各栏目为：</h4>
      <ul class="profile-list">
        <li>个人信息：展示用户基本信息，可编辑资料、修改密码</li>
        <li>正在进行的对局：展示用户当前正在进行的对局基本信息，点击可跳转至决策页面</li>
        <li>历史对局：展示用户历史对局基本信息，点击可查看对局详情</li>
      </ul>

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

.nav-list,
.decision-list,
.info-list,
.profile-list {
  margin: 10px 0;
  padding-left: 20px;
}

.nav-list li,
.decision-list li,
.info-list li,
.profile-list li {
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