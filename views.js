// 內容呈現與房間播放分開管理；新增作品只需修改 data.js。
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const missing = label => `<span class="placeholder" aria-label="${escapeHTML(label)}：待更新">待更新</span>`;
const provided = value => typeof value === 'string' && value.trim() && !/待更新|待補|待填/.test(value);
const field = (value, label) => provided(value) ? escapeHTML(value) : missing(label);
const workLink = work => provided(work.url) && /^https?:\/\//.test(work.url)
  ? `<a class="read-link" href="${escapeHTML(work.url)}" target="_blank" rel="noopener">查看作品 <span aria-hidden="true">↗</span></a>`
  : `<p class="link-pending">${missing('作品連結')}</p>`;
function contactRow(label, icon, value, destination, scheme) {
  const valid = provided(value) && provided(destination) && (scheme==='mailto:'
    ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(destination)
    : /^\+?[\d ()-]+$/.test(destination));
  const body=`<span class="contact-icon" aria-hidden="true">${icon}</span><span><small>${label}</small>${field(value,label)}</span>`;
  return valid ? `<a class="contact" href="${scheme}${escapeHTML(destination)}">${body}<span aria-hidden="true">↗</span></a>`
    : `<div class="contact">${body}</div>`;
}
function projectPage(work, index, kind) {
  return `<div class="project-page ${kind}" id="project-panel" role="tabpanel" aria-labelledby="tab-${work.id}" tabindex="0">
    <div class="project-cover">${provided(work.image)
      ? `<img src="${escapeHTML(work.image)}" alt="${escapeHTML(provided(work.title)?work.title:'作品')}封面">`
      : `<span class="cover-number" aria-hidden="true">${String(index+1).padStart(2,'0')}</span><span>${missing('作品封面')}</span>`}</div>
    <div class="project-copy"><p class="eyebrow">${kind==='book-page'?'FEATURE STORY':'INTERACTIVE STORY'} / ${String(index+1).padStart(2,'0')}</p>
    <h3>${field(work.title,'作品名稱')}</h3><p>${field(work.summary,'作品簡介')}</p>
    ${workLink(work)}</div>
  </div>`;
}
function projectTabs(items, kind, label) {
  return `<div class="project-tabs" role="tablist" aria-label="${label}" ${kind==='book-page'?'aria-orientation="vertical"':''}>${items.map((work,i)=>
    `<button role="tab" id="tab-${work.id}" aria-controls="project-panel" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-project="${i}">${escapeHTML(work.tab)}</button>`).join('')}</div>`;
}
// The supplied reference uses one continuous editorial page with photo shortcuts.
function featureReader() {
  const items=portfolio.features;
  const montage=items.map(work=>`<button class="feature-jump" data-feature="feature-story-${work.id}" aria-label="前往${escapeHTML(work.title)}">${provided(work.image)?`<img src="${escapeHTML(work.image)}" alt="" decoding="async">`:missing('作品封面')}</button>`).join('');
  const articles=items.map((work,index)=>`<section class="feature-article" id="feature-story-${work.id}" aria-labelledby="feature-title-${work.id}">
    <span class="feature-word word-top" aria-hidden="true">${escapeHTML(work.watermarks?.[0]||'')}</span>
    <span class="feature-word word-bottom" aria-hidden="true">${escapeHTML(work.watermarks?.[1]||'')}</span>
    <h3 tabindex="-1" id="feature-title-${work.id}">${field(work.title,'作品名稱')}</h3>
    <div class="feature-body"><figure>${provided(work.image)?`<img src="${escapeHTML(work.image)}" alt="${escapeHTML(work.title)}封面" width="${work.imageWidth}" height="${work.imageHeight}" loading="lazy" decoding="async">`:missing('作品封面')}</figure>
    <div class="feature-description"><p>${field(work.summary,'作品簡介')}</p>${workLink(work)}</div></div>
  </section>`).join('');
  return `<div class="feature-reader"><nav class="feature-montage" aria-label="專題照片索引">${montage}</nav><div class="feature-stories">${articles}</div></div>`;
}
let featureObserver;
function stopFeatureReveal(){featureObserver?.disconnect()}
function setupFeatureReveal(){
  stopFeatureReveal();
  if(current!=='bookshelf'||reducedMotion.matches||!('IntersectionObserver' in window))return;
  featureObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('is-visible');featureObserver.unobserve(entry.target)}
    });
  },{root:dialog,rootMargin:'-64px 0px -4% 0px',threshold:0.08});
  dialog.querySelectorAll('.feature-article').forEach(story=>{
    story.classList.add('feature-reveal');featureObserver.observe(story);
  });
}
function content(id) {
  if(id==='bookshelf') return featureReader();
  if(id==='laptop') return `<div class="computer"><div class="screen-bar"><span class="screen-light" aria-hidden="true"></span><span>Katy’s digital workspace</span></div>${projectTabs(portfolio.digital,'screen-page','數位敘事作品')}<div id="project-content">${projectPage(portfolio.digital[0],0,'screen-page')}</div><div class="screen-chin" aria-hidden="true">KATY’S ROOM</div></div>`;
  if(id==='newspaper') return `<div class="gazette"><div class="masthead"><span>新聞採訪作品</span><p>${missing('刊頭短句')}</p></div><div class="issue-line"><span>政大大學報 / 新聞採訪選集</span><span>${portfolio.news.length} 篇作品</span></div><div class="news-columns">${portfolio.news.map((work,i)=>`<article class="news-story"><p class="story-no">${String(i+1).padStart(2,'0')} / REPORTING</p><h3>${field(work.title,'作品名稱')}</h3><p class="byline">${escapeHTML(work.media)} · ${field(work.date,'發表日期')}</p><p>${field(work.summary,'採訪導言')}</p><p class="byline">角色：${field(work.role,'此篇採訪／編輯分工')}</p>${workLink(work)}</article>`).join('')}</div></div>`;
  if(id==='phone') return `<div class="contact-note"><span class="letter-mark" aria-hidden="true">K.</span><p>${missing('聯絡短句')}</p>${contactRow('學校 EMAIL','✉',portfolio.contact.email,portfolio.contact.email, 'mailto:')}${contactRow('PHONE','☎',portfolio.contact.phone,portfolio.contact.phoneHref,'tel:')}</div>`;
  if(id==='notebook') return `<div class="about-note"><p class="lead">${escapeHTML(portfolio.about.intro)}</p><h3>核心技能</h3>${skillGroups.map(s=>`<section class="skill"><h4>${escapeHTML(s.title)}</h4><p>${escapeHTML(s.text)}</p></section>`).join('')}<h3>我關注的方向</h3><p>${field(portfolio.about.interests,'想持續關注的議題或創作方向')}</p><details><summary>為什麼想做新聞？</summary>${paragraphs(books.listen.text)}</details></div>`;
  if(id==='violin') return paragraphs(books.life.text);
  return `<article><small>EDUCATION</small><h3>國立政治大學</h3><p>新聞學系 · 雙主修數位內容學士學程</p><time>2023.09 — 2027.06</time><details><summary>更早的學歷</summary><p>私立靜心高級中學｜2020.09–2023.06<br>私立復興實驗高級中學附設中學｜2017.09–2020.06<br>私立復興實驗高級中學附設小學｜2011.09–2017.06</p></details></article>${experiences.map(x=>`<article><time>${x.date}</time><h3>${x.org}</h3><p>${x.position}</p><p>${x.text}</p></article>`).join('')}`;
}
function selectProject(tab, focus=false) {
  const tabs=[...tab.parentElement.querySelectorAll('[role=tab]')];
  tabs.forEach(button=>{const selected=button===tab;button.setAttribute('aria-selected',selected);button.tabIndex=selected?0:-1});
  const index=Number(tab.dataset.project), book=current==='bookshelf';
  $('#project-content').innerHTML=projectPage((book?portfolio.features:portfolio.digital)[index],index,book?'book-page':'screen-page');
  if(focus)tab.focus();
}
