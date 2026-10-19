const $ = s => document.querySelector(s);
const room = $('#room'), video = $('#tour'), still = $('#still'), dialog = $('#content');
const stage = $('#room-stage');
let roomPosition = {left:0,top:0};
function centerRoom(){stage.scrollTo((stage.scrollWidth-stage.clientWidth)/2,(stage.scrollHeight-stage.clientHeight)/2);document.body.classList.toggle('pannable',stage.scrollWidth>stage.clientWidth*1.15)}
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const clips = {cabinet:[121,192,252],bookshelf:[253,396,480],newspaper:[481,552,612],laptop:[613,684,744]};
const titles = {cabinet:['MY JOURNEY','學歷與經歷'],bookshelf:['FEATURE STORIES','我的專題報導'],newspaper:['SELECTED REPORTING','我的新聞作品'],laptop:['DIGITAL STORYTELLING','用不同的方式說故事'],notebook:['ABOUT ME','關於我'],violin:['AFTER HOURS','工作之外的我'],phone:['SAY HELLO','保持聯絡']};
let current = null, busy = false, demoPlaying = false, returnFocus = null, cancelPlayback = () => {};
const paragraphs = text => text.split(/(?<=。)\s+/).map(p=>`<p>${p}</p>`).join('');
function setBusy(value) { busy=value; document.body.classList.toggle('busy',value); $('#objects').inert=value; $('#demo').disabled=value&&!demoPlaying; $('#skip-animation').hidden=!value||demoPlaying; }
// One video contains frames 1–1140. Seek only to the clicked object's segment.
function play(start,end,message='正在靠近…') {
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
    $('#status').textContent=message;
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
      video.preload='auto';video.src='assets/room/tour.mp4?v=frames-1140-1';video.load();
    }
  });
}
async function openObject(id,button) {
  if(busy||dialog.open)return;
  current=id;returnFocus=button;roomPosition={left:stage.scrollLeft,top:stage.scrollTop};centerRoom();setBusy(true);
  let animated=false;
  if(clips[id]&&!reducedMotion.matches)animated=await play(clips[id][0],clips[id][1]);
  if(!animated){
    room.classList.remove('playing');
    still.src=`assets/room/${clips[id]?id:'home'}.webp?v=quality-1080-1`;
  }
  const [label,title]=titles[id];
  dialog.dataset.view=id;
  $('#page').innerHTML=`<p class="eyebrow">${label}</p><h2 id="page-title">${title}</h2>${content(id)}`;
  setBusy(false);dialog.showModal();dialog.scrollTop=0;setupFeatureReveal();
  button.setAttribute('aria-expanded','true');
}
async function closeContent() {
  if(busy)return;
  setBusy(true);stopFeatureReveal();dialog.close();
  if(clips[current]&&!reducedMotion.matches&&room.classList.contains('playing'))
    await play(clips[current][1],clips[current][2],'正在回到房間…');
  video.pause();still.src='assets/room/home.webp?v=quality-1080-1';room.classList.remove('playing');setBusy(false);
  stage.scrollTo(roomPosition.left,roomPosition.top);returnFocus?.setAttribute('aria-expanded','false');returnFocus?.focus({preventScroll:true});current=null;
}
$('#skip-animation').addEventListener('click',()=>cancelPlayback());
$('#objects').addEventListener('click',e=>{const b=e.target.closest('[data-object]');if(b)openObject(b.dataset.object,b)});
$('#close').addEventListener('click',closeContent);
dialog.addEventListener('cancel',e=>{e.preventDefault();closeContent()});
dialog.addEventListener('click',e=>{
  if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeContent()}
  const tab=e.target.closest('[data-project]');if(tab)selectProject(tab);
  const jump=e.target.closest('[data-feature]');
  if(jump){
    const story=document.getElementById(jump.dataset.feature);if(!story)return;
    const top=dialog.scrollTop+story.getBoundingClientRect().top-dialog.getBoundingClientRect().top-64;
    story.querySelector('h3')?.focus({preventScroll:true});dialog.scrollTo({top,behavior:reducedMotion.matches?'instant':'smooth'});
  }
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
  if(busy)return;roomPosition={left:stage.scrollLeft,top:stage.scrollTop};centerRoom();demoPlaying=true;setBusy(true);$('#demo').textContent='回到房間 ×';
  await play(1,1140);demoPlaying=false;room.classList.remove('playing');stage.scrollTo(roomPosition.left,roomPosition.top);setBusy(false);$('#demo').textContent='播放房間導覽 ↗';
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&busy&&!dialog.open)cancelPlayback()});

requestAnimationFrame(centerRoom);
window.addEventListener('resize',centerRoom);
