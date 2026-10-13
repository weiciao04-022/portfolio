# Katy’s Tour｜黃暐喬個人網站

網站入口位於儲存庫最外層的 `index.html`，可直接開啟，或由 GitHub Pages 發佈。

## 網站檔案

- `index.html`：網站入口與原稿內容
- `style.css`：版面與樣式
- `data.js`：作品、經歷、技能與自我介紹
- `app.js`：作品篩選、詳情、書架互動
- `assets/`：網站素材

網站內容以提供的原稿為準。正式 PDF 履歷與採訪地點尚待提供。

## 本機預覽

```sh
python3 -m http.server 4173
```

開啟 http://localhost:4173/。

## GitHub Pages

在儲存庫 Settings → Pages，將來源設為 Deploy from a branch，選取 `main` 分支與 `/ (root)` 目錄。

舊入口 `katy-tour/dist/index.html` 會轉至最外層入口。後續請編輯最外層網站檔案。
