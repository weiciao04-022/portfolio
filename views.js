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
// Read the four original features directly, with a short staggered entrance on scroll.
function featureReader(){
  return `<div class="feature-essays">${portfolio.features.map(work=>`<article class="feature-essay">
    <span class="feature-watermark feature-watermark-top" data-reveal="background" aria-hidden="true">${escapeHTML(work.watermarks?.[0]||'')}</span>
    <span class="feature-watermark feature-watermark-bottom" data-reveal="background" aria-hidden="true">${escapeHTML(work.watermarks?.[1]||'')}</span>
    <h3 data-reveal="title">${field(work.title,'作品名稱')}</h3>
    <div class="feature-essay-body"><figure data-reveal="image"><img src="${escapeHTML(work.image)}" alt="${escapeHTML(work.title)}封面" width="${work.imageWidth}" height="${work.imageHeight}" decoding="async"></figure>
    <div class="feature-essay-copy" data-reveal="copy"><p>${field(work.summary,'作品簡介')}</p>${workLink(work)}</div></div>
  </article>`).join('')}</div>`;
}
let featureObserver=null;
function stopFeatureReveal(){
  featureObserver?.disconnect();featureObserver=null;
  $('.feature-essays')?.classList.remove('features-animated');
}
function setupFeatureReveal(){
  if(current==='newspaper')setupNewsReader();
  if(current!=='bookshelf'||reducedMotion.matches||!('IntersectionObserver' in window))return;
  const essays=$('.feature-essays');essays.classList.add('features-animated');
  featureObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('is-visible');featureObserver?.unobserve(entry.target)}
  }),{root:dialog,threshold:.08});
  essays.querySelectorAll('.feature-essay').forEach(article=>featureObserver.observe(article));
}
function content(id) {
  if(id==='bookshelf') return featureReader();
  if(id==='laptop') return `<div class="computer"><div class="screen-bar"><span class="screen-light" aria-hidden="true"></span><span>Katy’s digital workspace</span></div>${projectTabs(portfolio.digital,'screen-page','數位敘事作品')}<div id="project-content">${projectPage(portfolio.digital[0],0,'screen-page')}</div><div class="screen-chin" aria-hidden="true">KATY’S ROOM</div></div>`;
  if(id==='newspaper') return newsReader();
  if(id==='phone') return `<div class="contact-note"><span class="letter-mark" aria-hidden="true">K.</span><p>${missing('聯絡短句')}</p>${contactRow('學校 EMAIL','✉',portfolio.contact.email,portfolio.contact.email, 'mailto:')}${contactRow('PHONE','☎',portfolio.contact.phone,portfolio.contact.phoneHref,'tel:')}</div>`;
  if(id==='notebook') return `<div class="about-note"><p class="lead">${escapeHTML(portfolio.about.intro)}</p><h3>核心技能</h3>${skillGroups.map(s=>`<section class="skill"><h4>${escapeHTML(s.title)}</h4><p>${escapeHTML(s.text)}</p></section>`).join('')}<h3>我關注的方向</h3><p>${field(portfolio.about.interests,'想持續關注的議題或創作方向')}</p><details><summary>為什麼想做新聞？</summary>${paragraphs(books.listen.text)}</details></div>`;
  if(id==='violin') return paragraphs(books.life.text);
  return `<article><small>EDUCATION</small><h3>國立政治大學</h3><p>新聞學系 · 雙主修數位內容學士學程</p><time>2023.09 — 2027.06</time><details><summary>更早的學歷</summary><p>私立靜心高級中學｜2020.09–2023.06<br>私立復興實驗高級中學附設中學｜2017.09–2020.06<br>私立復興實驗高級中學附設小學｜2011.09–2017.06</p></details></article>${experiences.map(x=>`<article><time>${x.date}</time><h3>${x.org}</h3><p>${x.position}</p><p>${x.text}</p></article>`).join('')}`;
}
function selectProject(tab, focus=false) {
  const tabs=[...tab.parentElement.querySelectorAll('[role=tab]')];
  tabs.forEach(button=>{const selected=button===tab;button.setAttribute('aria-selected',selected);button.tabIndex=selected?0:-1});
  const index=Number(tab.dataset.project);
  $('#project-content').innerHTML=projectPage(portfolio.digital[index],index,'screen-page');
  if(focus)tab.focus();
}

// Newspaper navigation stays inside this object; room and project-tab controls are unchanged.
const newsEditions={life:{name:'LIFE',label:'生活版'},international:{name:'INTERNATIONAL',label:'國際版'}};
const newsPendingText='待更新／待確認重刊授權';
function newsOriginalLink(work){
  return `<a class="read-link" href="${escapeHTML(work.url)}" target="_blank" rel="noopener">閱讀原文 <span aria-hidden="true">↗</span></a>`;
}
function newsPhoto(work){
  const photo=work.photo,allowed=photo.permission==='confirmed'&&provided(photo.localPath);
  return `<figure class="news-photo">${allowed?`<img src="${escapeHTML(photo.localPath)}" alt="${escapeHTML(provided(photo.caption)?photo.caption:work.title)}" width="${photo.width}" height="${photo.height}" loading="lazy" decoding="async">`:
    `<div class="news-photo-pending"><span>待更新</span><small>${photo.permission==='confirmed'?'照片待提供':'待確認圖片授權'}</small></div>`}
    <figcaption>${provided(photo.caption)?escapeHTML(photo.caption):`<span>原始圖說：待更新</span><span>${field(photo.credit,'攝影者／圖片來源')}</span>`}</figcaption></figure>`;
}
function newsByline(work){
  return `<div class="news-meta"><time datetime="${escapeHTML(work.date)}">${escapeHTML(work.date)}</time><span>${escapeHTML(work.issue)} · ${escapeHTML(work.publishedSection)}</span><span>${escapeHTML(work.byline)}</span></div>`;
}
function newsBrief(work){
  return work.textPermission==='confirmed'&&provided(work.summary)?`<p class="news-excerpt">${escapeHTML(work.summary)}</p>`:
    `<p class="news-pending">導言：${newsPendingText}</p>`;
}
function newsEdition(edition){
  const info=newsEditions[edition],works=portfolio.news.filter(work=>work.edition===edition);
  const story=work=>`<article class="news-story news-${work.rank}" data-news-open="${work.id}">
      <div class="news-story-label">${work.rank==='lead'?'頭條':work.rank==='secondary'?'次頭條':info.label}</div>
      <h3><button type="button" class="news-headline" data-news-title="${work.id}">${escapeHTML(work.title)}</button></h3>
      ${newsByline(work)}${newsPhoto(work)}${newsBrief(work)}${newsOriginalLink(work)}</article>`;
  return `<div class="news-edition-line"><h4>${info.name}<span>｜${info.label}</span></h4><span>${String(works.length).padStart(2,'0')} 篇作品</span></div>
    <div class="news-grid">${works.slice(0,2).map(story).join('')}<div class="news-lower-grid">${works.slice(2).map(story).join('')}</div></div>`;
}
function newsReader(){
  return `<section class="gazette" aria-label="新聞採訪作品"><header class="news-masthead"><p>KATY’S ROOM / JOURNALISM</p><h3>新聞採訪作品</h3><p>原始刊登媒體｜《政大大學報》</p></header>
    <nav class="news-editions" aria-label="新聞版別"><div role="group" aria-label="選擇版別">${Object.entries(newsEditions).map(([id,info])=>`<button type="button" data-news-edition="${id}" aria-pressed="${id==='life'}">${info.name}<span>${info.label}</span></button>`).join('')}</div><span>新聞採訪選集</span></nav>
    <div class="news-index">${newsEdition('life')}</div><div class="news-reading" hidden></div></section>`;
}
function newsArticle(work){
  const body=work.textPermission==='confirmed'&&Array.isArray(work.body)&&work.body.length
    ?work.body.map(text=>`<p>${escapeHTML(text)}</p>`).join(''):`<p class="news-pending">${newsPendingText}</p>`;
  return `<button type="button" class="news-back" data-news-back>← 返回報紙版面</button><article class="news-article">
    <p class="news-article-section">${newsEditions[work.edition].name}｜${newsEditions[work.edition].label}</p>
    <h3 id="news-reading-title" tabindex="-1">${escapeHTML(work.title)}</h3>${newsByline(work)}${newsPhoto(work)}
    <section class="news-article-text" aria-label="新聞原文"><h4>原文導言</h4>${newsBrief(work)}<h4>新聞正文</h4>${body}</section>
    ${newsOriginalLink(work)}<details class="news-source"><summary>圖片來源與授權</summary><p>${escapeHTML(work.photo.credit||'待更新')}</p><p>圖片：${work.photo.permission==='confirmed'?'已確認使用許可':'待更新／待確認圖片授權'}</p><a href="${escapeHTML(work.url)}" target="_blank" rel="noopener">核對原始圖說與首張正文照片 ↗</a></details></article>`;
}
function setupNewsReader(){
  const root=$('.gazette'),index=root.querySelector('.news-index'),reading=root.querySelector('.news-reading');
  let edition='life',scrollTop=0,selected=null;
  const showEdition=id=>{
    edition=id;index.innerHTML=newsEdition(id);index.hidden=false;reading.hidden=true;reading.innerHTML='';
    root.querySelectorAll('[data-news-edition]').forEach(button=>button.setAttribute('aria-pressed',button.dataset.newsEdition===id));
    dialog.scrollTop=0;
  };
  root.onclick=event=>{
    const section=event.target.closest('[data-news-edition]');
    if(section){showEdition(section.dataset.newsEdition);return}
    if(event.target.closest('[data-news-back]')){
      reading.hidden=true;reading.innerHTML='';index.hidden=false;dialog.scrollTop=scrollTop;
      root.querySelector(`[data-news-title="${selected}"]`)?.focus({preventScroll:true});return;
    }
    if(event.target.closest('a'))return;
    const story=event.target.closest('[data-news-open]');if(!story)return;
    const work=portfolio.news.find(item=>item.id===story.dataset.newsOpen);if(!work)return;
    selected=work.id;scrollTop=dialog.scrollTop;index.hidden=true;reading.innerHTML=newsArticle(work);reading.hidden=false;
    dialog.scrollTop=0;reading.querySelector('h3').focus({preventScroll:true});
  };
  root.querySelector('.news-editions').onkeydown=event=>{
    if(!event.target.closest('[data-news-edition]')||!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();const ids=Object.keys(newsEditions),next=event.key==='Home'?ids[0]:event.key==='End'?ids[1]:ids[1-ids.indexOf(edition)];
    showEdition(next);root.querySelector(`[data-news-edition="${next}"]`).focus({preventScroll:true});
  };
}
