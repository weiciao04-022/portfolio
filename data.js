const stories = [
 {title:'年輕失智也失去生活：未能實現的工作權',slug:'dementia-work-YOD',type:'feature',art:'dementia'},
 {title:'動漫角色進入咖啡廳　揭露女僕的職場壓力',slug:'maid-cafe-culture',type:'feature',art:'cafe'},
 {title:'當美被社群媒體形塑　Z世代的體態焦慮與自我追尋',slug:'social-genz-SPA',type:'interactive',art:'body'},
 {title:'AI技術重現逝者生命　臺灣數位永生如何發展',slug:'ai-digitalimmortality-developing',type:'feature',art:'digital'},
 {title:'年輕失智也失去生活：未能實現的工作權',slug:'dementia-work-YOD-convergencemedia',type:'interactive',art:'dementia'},
 {title:'浸大學生會疑因悼大火遭解散　學生嘆校園自治將亡',slug:'wongfukcourtfire-democracywall-studentsunion',type:'news',art:'campus'},
 {title:'故宮首攜東大辦《故宮東遊記》　盼縮短台東與故宮距離',slug:'thenationalpalacemuseum-edutainment-gamebasedchallenge',type:'news',art:'culture'},
 {title:'科普環島列車首辦市集　走入北車推科學知識生活化',slug:'sciencefair-scientificknowledge-taipeistation',type:'news',art:'train'},
 {title:'清大創首屆科技萬聖藝術節　領孩童玩樂中學科學',slug:'-halloween-technology-art',type:'news',art:'science'},
 {title:'見書店攜大學生致敬臺灣文學　辦市集傳實體書魅力',slug:'reading-bookcave-promotion',type:'news',art:'culture'},
 {title:'臺師大首辦拉丁舞之夜　美食、文化交流展熱情',slug:'latinculture-salsadance-internationalexchange',type:'news',art:'culture'},
 {title:'東華族語歌唱比賽首結合市集　藉手工藝展原民之美',slug:'ndhu-indigenous-indigenouslanguagesingingcontest',type:'news',art:'culture'},
 {title:'川普對校新條約遭反彈　德大生疑抹滅校園言論自由',slug:'trump-utaustin-campact',type:'news',art:'campus'},
 {title:'波大反性侵聯盟辦行動週　多形式展校園對話',slug:'-sexualassault-community-weekofaction',type:'news',art:'campus'},
 {title:'美國轉折點性別用詞惹議　曼大生抗議聲援跨性別者',slug:'transgender-sports-controversy',type:'news',art:'campus'},
 {title:'康大合作軍火商引倫理爭議　學生組破鏈行動抗議',slug:'armsmanufacturers-studentprotest-uconn',type:'news',art:'campus'},
 {title:'維大關閉學習型宿舍　學生為多元族群文化空間發聲',slug:'livinglearningcommunity-black-lgbtq',type:'news',art:'campus'},
 {title:'當美被社群媒體形塑　Z世代的體態焦慮與自我追尋',slug:'social-genz-socialphysiqueanxiety',type:'feature',art:'body'},
 {title:'賞鳥博覽會在台首辦　展現台灣多元生態',slug:'eco-sustainable-bird',type:'news',art:'nature'},
 {title:'野保法修法首例　屏東黑熊案一審無罪',slug:'blackbear-indigenous-conservation',type:'news',art:'nature'}
];
const experiences = [
 {date:'2026.09-至今',org:'政大大學報',position:'採訪中心主任（生活版）',text:'負責生活版新聞稿件審閱與編輯，協助記者調整報導切角、內容架構及新聞標題，確保稿件品質與新聞價值。'},
 {date:'2025.09-2026.06',org:'政大大學報',position:'採訪中心記者（國際與生活版、專題）',text:'獨立完成12篇純淨新聞報導（國際版及生活版各6篇），負責新聞選題、採訪、查證與稿件撰寫；參與4篇專題報導，主要負責議題提案、報導面向規劃及實地採訪；另參與2件數位敘事作品，主要負責UI／UX設計與互動程式開發。'},
 {date:'2025.04-2026.06',org:'三立新聞台',position:'編輯台工讀生',text:'協助新聞 RO 帶與 Sound On 影音剪輯、節目《54分局》串帶作業，以及中央氣象署相關新聞素材剪輯與解說內容整理；負責監看午間新聞、彙整各大電視新聞台重要時段的新聞內容，並整理重大新聞事件與時事重點。'},
 {date:'2025.07-08',org:'三立財經台',position:'採訪中心實習生',text:'協助記者執行新聞採訪工作，包括記者會現場支援、遞麥、街頭訪問及協助需兼顧播報工作的記者進行採訪；練習撰寫 SOT 新聞稿，熟悉電視新聞採訪流程與新聞稿件製作。'},
 {date:'2024.08',org:'電通貝立德電通娛樂',position:'實習生',text:'協助整理提案資料、參與提案簡報流程，獨立完成部門月報與季報製作，支援現場藝人接待，熟悉媒體代理操作流程。'}
];
const skillGroups = [
 {title:'新聞採訪與編輯 Journalism & Editorial',text:'新聞採訪、人物訪談、街頭訪問；新聞寫作、專題報導、SOT 稿撰寫；新聞編輯、審稿與標題製作；新聞資料蒐集、查證與議題研究；電視新聞監看、新聞素材整理與影音串帶'},
 {title:'網頁與互動製作 Web & Interactive Media',text:'JavaScript、HTML、CSS；p5.js、Max/MSP（Max 8）；Blender（3D 建模與動畫）；Figma（UI／UX 設計與原型製作）'},
 {title:'影像與視覺設計 Visual & Post-production',text:'Adobe Lightroom Classic（攝影後製）；Adobe Photoshop（影像編修）；Adobe Illustrator（平面與向量設計）；Adobe InDesign（排版與出版設計）；Adobe Premiere Pro（影片剪輯）；EDIUS（電視新聞影音剪輯）'},
 {title:'資料處理與視覺化 Data & Visualization',text:'Gephi（網絡分析與視覺化）'}
];
const books = {"listen": {"title": "為什麼想做新聞？", "text": "在跑採訪的過程中，最讓我感激的一件事，是受訪者總願意向我分享自己的親身經歷。對受訪者而言，記者可能只是第一天見面的陌生人，但他們卻願意敞開心房，回答我的問題，甚至分享那些不曾輕易對外人訴說的故事。透過一次次的提問與傾聽，我得以在短暫的相遇中，與原本陌生的人建立深刻的理解。而每次採訪結束後，思考該如何說好一個故事，總是我最期待的環節。我覺得寫報導就像拼拼圖，將採訪中聽見的故事、實際查找的資料，以及現場觀察到的細節，一片片拼湊起來，讓原本零散、模糊的資訊，逐漸形成一幅清晰的圖像。然而，採訪得越多，我反而越覺得自己渺小。每認識一個人、聽見一段不同的人生經歷，就越發現自己原本認識的世界有多麼狹窄。也正因如此，我想成為記者。 我希望透過一次又一次的採訪與報導，不斷蒐集那些自己未曾理解的故事，像拼拼圖一樣，一片一片地拼湊出更遼闊的世界。"}, "create": {"title": "自我介紹", "text": "我是黃暐喬 Katy Huang，今年22歲，目前就讀國立政治大學新聞學系，並且雙主修數位內容學士學程。當時高中考大學時，一直被父母鼓勵進入科技業，他們認為是更有前景的行業，但是我一頭栽進政大傳播，想要證明：如果好好把內容做好，媒體在世界上總有站穩的地方。雙主修數位內容也是父母說著要和Computer Science有一些關係總是好的，但是在數位內容中，我反而開拓了自己內容產出的方法，例如運用互動裝置設計、3D建模等，可以讓敘事增加除了文字外的想像。於大學報專題時，很榮幸和前Yahoo奇摩總編李怡志教授學習，數位敘事的融媒體新聞產出，也感嘆當時高中想要逃離寫程式，卻也讓程式也融進新聞作品裡。"}, "life": {"title": "工作之外的興趣", "text": "在課業與工作之外，我喜歡和家人、朋友好好相聚。獨處時，我偶爾會拿起小提琴，暫時放下手邊待完成的任務，讓自己從忙碌的生活中抽離。最近也開始學習高爾夫球，透過練習觀察身體的動作與發力方式，逐漸了解如何運用自己的身體。夏天時，我喜歡游泳，讓全身都能徹底放鬆；到了冬天，則喜歡騎腳踏車通勤，也讓思緒自由延伸，從日常獲得新的靈感。"}};
