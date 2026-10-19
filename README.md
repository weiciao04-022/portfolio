# Katy’s Room｜黃暐喬

純 HTML、CSS、原生 JavaScript 的互動房間作品集，不需要安裝套件或建置。
開啟即是房間；點物件看內容，關閉後回到房間。

- 矮櫃：學歷、經歷
- 書架：自我介紹
- 報紙：新聞作品
- 筆電：數位敘事與技能
- 筆記本：為什麼做新聞
- 小提琴：興趣
- 電話：聯絡方式

前 800 張 render 已壓成 `assets/room/tour.mp4`（720p、24fps），首次點擊才載入。
矮櫃、書架、報紙、筆電有完整來回動畫；其餘物件直接開啟內容。
導覽會播放目前的前 800 格（33.33 秒），最後回首頁；Esc 可結束。
手機保留完整房間比例，避免物件點擊位置因裁切錯位。
減少動態效果設定會略過轉場；影片無法播放時自動使用靜態畫面。

## 預覽

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

開啟 http://127.0.0.1:4173/。GitHub Pages 仍可從根目錄發佈。
`data.js` 管理原稿內容；`app.js` 的 `clips` 管理每件物品的動畫起點、內容畫面與回程終點。

## 更新 render

素材處理工具僅用於離線壓縮，網站不需要 Python、Pillow 或 ffmpeg。
準備好 Pillow 與 ffmpeg（或 imageio-ffmpeg）後執行：

```sh
python3 scripts/prepare-room.py /Users/weiciao/Desktop/work/pic 800
```

新增完整片段後，同步更新 `app.js` 的 `clips` 與導覽結束格數。
