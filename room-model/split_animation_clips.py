import bpy,json
from pathlib import Path
p=Path('/private/tmp/katy-room-animation')
bpy.ops.wm.open_mainfile(filepath=str(p/'Katy_Parisian_Room.blend'))
main=bpy.context.scene;main.name='DEMO • Complete room tour'
plan=json.loads((p/'animation_plan.json').read_text());st={e['step']:e for e in plan['stages']}
clips=[('room_enter','進入房間',1,72,'outside','room'),('cabinet_in','靠近學經歷矮櫃',121,192,'room','cabinet'),('cabinet_out','從矮櫃回房間',192,252,'cabinet','room'),('bookshelf_in','靠近書架',253,301,'room','bookshelf'),('book_open','抽書並打開',301,396,'bookshelf','book_open'),('book_close','關書',396,421,'book_open','book_closed_closeup'),('bookshelf_out','從書架回房間',421,480,'book_closed_closeup','room'),('book_close_and_return','關書並回房間',396,480,'book_open','room')]
for n,key,label in [(7,'newspaper','報紙'),(9,'laptop','筆電'),(11,'notebook','採訪筆記本'),(13,'violin','小提琴'),(15,'phone','電話')]:
 clips.append((key+'_in','靠近'+label,st[n]['start'],st[n]['end'],'room',key))
 clips.append((key+'_out','從'+label+'回房間',st[n]['end'],st[n+1]['end'],key,'room'))
manifest=[]
for index,(id,label,start,end,state_from,state_to) in enumerate(clips,1):
 scene=main.copy();scene.use_fake_user=True;scene.name='CLIP %02d • %s'%(index,id);scene.frame_start=start;scene.frame_end=end
 scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.render.fps=24
 scene.render.image_settings.media_type='VIDEO';scene.render.image_settings.file_format='FFMPEG';scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH';scene.render.ffmpeg.audio_codec='NONE'
 scene.render.filepath='//Katy_Animation_Clips/'+id+'.mp4'
 scene['Clip ID']=id;scene['Clip label']=label;scene['State from']=state_from;scene['State to']=state_to
 scene['Notes']='Render this scene only to export an independent MP4. Shared scene geometry and original timeline frame ranges are intentional.'
 manifest.append({'id':id,'label':label,'scene':scene.name,'start_frame':start,'end_frame':end,'fps':24,'resolution':[1920,1080],'duration_seconds':round((end-start+1)/24,3),'from':state_from,'to':state_to,'file':id+'.mp4'})
# All clips leaving or entering room share exactly the same camera anchor.
cam=main.camera;reference=None
for clip in manifest:
 for state,frame in [(clip['from'],clip['start_frame']),(clip['to'],clip['end_frame'])]:
  if state!='room':continue
  main.frame_set(frame);bpy.context.view_layer.update();pose=(tuple(cam.location),tuple(cam.rotation_quaternion),cam.data.ortho_scale)
  if reference is None:reference=pose
  assert max(abs(a-b) for a,b in zip(pose[0],reference[0]))<1e-5
  assert max(abs(a-b) for a,b in zip(pose[1],reference[1]))<1e-5
  assert abs(pose[2]-reference[2])<1e-5
main.frame_set(1)
if bpy.context.window:bpy.context.window.scene=main
main['Independent clip count']=len(manifest)
main['Website hint']='Object outlines pulse slowly; hover increases glow. Implement in website, not rendered footage.'
bpy.ops.wm.save_as_mainfile(filepath=str(p/'Katy_Parisian_Room.blend'))
(p/'Katy_Animation_Clips.json').write_text(json.dumps({'resolution':[1920,1080],'fps':24,'clips':manifest,'effects':'Website-only slow outline pulse + stronger hover glow','playback':'Preload next clip. Hold final frame. Only play a clip when current state matches its from field.'},ensure_ascii=False,indent=2))
lines=['# 獨立動畫輸出清單','', '完整示範時間軸保留於 DEMO 場景。每個 CLIP 場景可獨立輸出 1920×1080、24 fps、H.264 MP4。','', '各場景使用原時間軸格數，不需要重新從第 1 格開始；輸出的影片會從自己的第一個畫面開始。','', '| ID | 動作 | 格數 | 接點狀態 |','|---|---|---|---|']
for c in manifest:lines.append('| '+c['id']+' | '+c['label']+' | '+str(c['start_frame'])+'–'+str(c['end_frame'])+' | '+c['from']+' → '+c['to']+' |')
lines+=['','在 Blender 右上方場景選單選 CLIP，再按 Ctrl+F12 輸出該段影片。輸出目錄為 blend 同層的 Katy_Animation_Clips。','', '所有回房間的鏡頭皆與進入房間的結尾一致。書架相關片段使用重疊接點格，避免切換時跳動。','', '網頁依點擊播放 *_in；關閉介紹時播放 *_out。書本開啟後可播放 book_close_and_return 一次關書並回房間，或分別播放 book_close 和 bookshelf_out。','', '輪廓慢閃、滑鼠移入加亮留在網頁實作。','', '這次完成場景、動作與輸出設定；所有獨立 1080p MP4 尚未完整渲染。']
(p/'Katy_Independent_Clips.md').write_text('\n'.join(lines))
print('VERIFIED_INDEPENDENT_CLIPS',len(manifest),'1920x1080; identical room anchors; MP4 scene outputs configured')
