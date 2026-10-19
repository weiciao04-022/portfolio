const $ = s => document.querySelector(s);
const room = $('#room'), video = $('#tour'), still = $('#still'), dialog = $('#content');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const clips = {cabinet:[121,192,252],bookshelf:[253,396,480],newspaper:[481,552,612],laptop:[613,684,744]};
const titles = {cabinet:['MY JOURNEY','學歷與經歷'],bookshelf:['A LITTLE ABOUT ME','翻開我的故事'],newspaper:['SELECTED REPORTING','我的新聞作品'],laptop:['DIGITAL STORYTELLING','用不同的方式說故事'],notebook:['NOTES FROM THE FIELD','為什麼想做新聞？'],violin:['AFTER HOURS','工作之外的我'],phone:['SAY HELLO','保持聯絡']};
let current = null, busy = false, demoPlaying = false, returnFocus = null, cancelPlayback = () => {};
const paragraphs = text => text.split(/(?<=。)\s+/).map(p=>`<p>${p}</p>`).join('');
function storyList(type='all') {
  return stories.filter(s=>type==='all'||s.type===type).map(s=>`<a class="story" href="https://unews.nccu.edu.tw/unews/${s.slug}/" target="_blank" rel="noopener"><h3>${s.title}</h3><small>政大大學報 · ${{feature:'專題報導',news:'新聞採訪',interactive:'數位敘事'}[s.type]}<span>閱讀作品 ↗</span></small></a>`).join('');
}
function content(id) {
  if(id==='cabinet') return `<article><small>EDUCATION</small><h3>國立政治大學</h3><p>新聞學系 · 雙主修數位內容學士學程</p><time>2023.09 — 2027.06</time><details><summary>更早的學歷</summary><p>私立靜心高級中學｜2020.09–2023.06<br>私立復興實驗高級中學附設中學｜2017.09–2020.06<br>私立復興實驗高級中學附設小學｜2011.09–2017.06</p></details></article>${experiences.map(x=>`<article><time>${x.date}</time><h3>${x.org}</h3><p>${x.position}</p><p>${x.text}</p></article>`).join('')}`;
  if(id==='bookshelf') return `<div class="tabs" aria-label="選一本書">${['create','listen','life'].map((key,i)=>[key,books[key]]).map(([key,b],i)=>`<button data-book="${key}" aria-pressed="${i===0}">${b.title}</button>`).join('')}</div><div id="book-text">${paragraphs(books.create.text)}</div>`;
  if(id==='newspaper') return `<div class="tabs" aria-label="作品類別"><button data-filter="all" aria-pressed="true">全部</button><button data-filter="feature" aria-pressed="false">專題</button><button data-filter="news" aria-pressed="false">新聞</button></div><div id="stories">${storyList()}</div>`;
  if(id==='laptop') return `${storyList('interactive')}<h3>我的製作工具</h3>${skillGroups.map(s=>`<article><h3>${s.title}</h3><p>${s.text}</p></article>`).join('')}`;
  if(id==='notebook') return paragraphs(books.listen.text);
  if(id==='violin') return paragraphs(books.life.text);
  return `<p>歡迎聊聊採訪、創作，或一個值得被說出來的故事。</p><a class="contact" href="mailto:katyhuang2004@gmail.com"><small>EMAIL</small>katyhuang2004@gmail.com ↗</a><a class="contact" href="mailto:112405118@g.nccu.edu.tw"><small>UNIVERSITY</small>112405118@g.nccu.edu.tw ↗</a><a class="contact" href="tel:+886909070707"><small>PHONE</small>0909 070 707 ↗</a>`;
}
function setBusy(value) { busy=value; document.body.classList.toggle('busy',value); $('#objects').inert=value; $('#demo').disabled=value&&!demoPlaying; }
// One small video contains frames 1–800. Seek only to the clicked object's segment.
function play(start,end) {
  return new Promise(resolve=>{
    let timer, poll, frameCallback, done=false, started=false;
    const finish = ok => {
      if(done)return;done=true;video.pause();clearTimeout(timer);clearInterval(poll);
      if(frameCallback!==undefined)video.cancelVideoFrameCallback(frameCallback);
      video.removeEventListener('seeked',begin);video.removeEventListener('loadedmetadata',seek);video.removeEventListener('error',fail);
      $('#status').textContent='';resolve(ok);
    };
    const fail = () => finish(false);
    cancelPlayback=fail;
    const stop=(end-1)/24;
    const check=()=>{if(video.currentTime>=stop-.018)finish(true)};
    const watch=()=>{check();if(!done)frameCallback=video.requestVideoFrameCallback(watch)};
    function begin(){
      if(started||done)return;started=true;
      room.classList.add('playing');$('#status').textContent='';
      video.play().then(()=>{
        if(done){video.pause();return}
        if(video.requestVideoFrameCallback)frameCallback=video.requestVideoFrameCallback(watch);
        poll=setInterval(check,25);
      }).catch(fail);
    }
    $('#status').textContent='正在靠近…';
    timer=setTimeout(fail,20000+(end-start)/24*1000);
    video.addEventListener('error',fail,{once:true});
    video.addEventListener('seeked',begin,{once:true});
    function seek(){
      video.currentTime=(start-1)/24;
      if(video.readyState>=2&&!video.seeking)begin();
    }
    if(video.readyState>=1)seek();
    else {
      video.addEventListener('loadedmetadata',seek,{once:true});
      video.preload='auto';video.src='assets/room/tour.mp4';video.load();
    }
  });
}
async function openObject(id,button) {
  if(busy||dialog.open)return;
  current=id;returnFocus=button;setBusy(true);
  let animated=false;
  if(clips[id]&&!reducedMotion.matches)animated=await play(clips[id][0],clips[id][1]);
  if(!animated){room.classList.remove('playing');still.src=`assets/room/${clips[id]?id:'home'}.webp`}
  const [label,title]=titles[id];
  $('#page').innerHTML=`<p class="eyebrow">${label}</p><h2 id="page-title">${title}</h2>${content(id)}`;
  dialog.showModal();dialog.scrollTop=0;setBusy(false);
}
async function closeContent() {
  if(busy)return;
  setBusy(true);dialog.close();
  if(clips[current]&&!reducedMotion.matches&&room.classList.contains('playing'))await play(clips[current][1],clips[current][2]);
  still.src='assets/room/home.webp';room.classList.remove('playing');setBusy(false);returnFocus?.focus();current=null;
}
$('#objects').addEventListener('click',e=>{const b=e.target.closest('[data-object]');if(b)openObject(b.dataset.object,b)});
$('#close').addEventListener('click',closeContent);
dialog.addEventListener('cancel',e=>{e.preventDefault();closeContent()});
dialog.addEventListener('click',e=>{
  if(e.target===dialog&&e.offsetX<0){closeContent();return}
  const b=e.target.closest('[data-book],[data-filter]');if(!b)return;
  b.parentElement.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  if(b.dataset.book)$('#book-text').innerHTML=paragraphs(books[b.dataset.book].text);
  else $('#stories').innerHTML=storyList(b.dataset.filter);
});
$('#guide').addEventListener('click',()=>{const show=room.classList.toggle('labels');$('#guide').setAttribute('aria-pressed',show);$('#guide').textContent=show?'隱藏物件名稱':'顯示物件名稱'});
$('#demo').addEventListener('click',async()=>{
  if(demoPlaying){cancelPlayback();return}
  if(busy)return;demoPlaying=true;setBusy(true);$('#demo').textContent='回到房間 ×';
  await play(1,800);demoPlaying=false;room.classList.remove('playing');setBusy(false);$('#demo').textContent='播放房間導覽 ↗';
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&busy&&!dialog.open)cancelPlayback()});
