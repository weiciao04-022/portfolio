const $ = s => document.querySelector(s);
const room = $('#room'), video = $('#tour'), still = $('#still'), dialog = $('#content');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const clips = {cabinet:[121,192,252],bookshelf:[253,396,480],newspaper:[481,552,612],laptop:[613,684,744]};
const titles = {cabinet:['MY JOURNEY','學歷與經歷'],bookshelf:['FEATURE STORIES','我的專題報導'],newspaper:['SELECTED REPORTING','我的新聞作品'],laptop:['DIGITAL STORYTELLING','用不同的方式說故事'],notebook:['ABOUT ME','關於我'],violin:['AFTER HOURS','工作之外的我'],phone:['SAY HELLO','保持聯絡']};
let current = null, busy = false, demoPlaying = false, returnFocus = null, cancelPlayback = () => {};
const paragraphs = text => text.split(/(?<=。)\s+/).map(p=>`<p>${p}</p>`).join('');
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
function openObject(id,button) {
  if(busy||dialog.open)return;
  current=id;returnFocus=button;
  // 閱讀立即開啟；完整鏡頭留在房間導覽，避免每次點擊等待。
  room.classList.remove('playing');
  still.src=`assets/room/${clips[id]?id:'home'}.webp`;
  const [label,title]=titles[id];
  dialog.dataset.view=id;
  $('#page').innerHTML=`<p class="eyebrow">${label}</p><h2 id="page-title">${title}</h2>${content(id)}`;
  dialog.showModal();dialog.scrollTop=0;
  button.setAttribute('aria-expanded','true');
}
function closeContent() {
  dialog.close();video.pause();still.src='assets/room/home.webp';room.classList.remove('playing');
  returnFocus?.setAttribute('aria-expanded','false');returnFocus?.focus();current=null;
}
$('#objects').addEventListener('click',e=>{const b=e.target.closest('[data-object]');if(b)openObject(b.dataset.object,b)});
$('#close').addEventListener('click',closeContent);
dialog.addEventListener('cancel',e=>{e.preventDefault();closeContent()});
dialog.addEventListener('click',e=>{
  if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeContent()}
  const tab=e.target.closest('[data-project]');if(tab)selectProject(tab);
});
dialog.addEventListener('keydown',e=>{
  const tab=e.target.closest('[role=tab]');if(!tab)return;
  const vertical=tab.parentElement.getAttribute('aria-orientation')==='vertical';
  const next=vertical?'ArrowDown':'ArrowRight',previous=vertical?'ArrowUp':'ArrowLeft';
  if(![next,previous,'Home','End'].includes(e.key))return;
  e.preventDefault();const tabs=[...tab.parentElement.children],i=tabs.indexOf(tab);
  selectProject(tabs[e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key===next?1:-1)+tabs.length)%tabs.length],true);
});
$('#guide').addEventListener('click',()=>{const show=room.classList.toggle('labels');$('#guide').setAttribute('aria-pressed',show);$('#guide').textContent=show?'隱藏物件名稱':'顯示物件名稱'});
$('#demo').addEventListener('click',async()=>{
  if(demoPlaying){cancelPlayback();return}
  if(busy)return;demoPlaying=true;setBusy(true);$('#demo').textContent='回到房間 ×';
  await play(1,800);demoPlaying=false;room.classList.remove('playing');setBusy(false);$('#demo').textContent='播放房間導覽 ↗';
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&busy&&!dialog.open)cancelPlayback()});
