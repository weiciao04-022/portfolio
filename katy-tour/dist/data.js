const stories = [
 {title:'年輕失智也失去生活：未能實現的工作權',slug:'dementia-work-YOD',type:'feature',date:'2026.03.26',topic:'勞動・照護',art:'dementia',summary:'當失智不只發生在老年，仍想工作的人，如何在照護與社會參與之間找到自己的位置？',role:'共同署名報導；專題期間參與議題提案、報導面向規劃及實地採訪。',method:'以人物經歷切入，結合照護與工作權的議題研究。'},
 {title:'動漫角色進入咖啡廳　揭露女僕的職場壓力',slug:'maid-cafe-culture',type:'feature',date:'2026.04.16',topic:'文化・勞動',art:'cafe',summary:'走進看似夢幻的互動空間，看見角色扮演背後的情緒勞動、工作界線與職場壓力。',role:'共同署名報導；參與專題規劃及實地採訪，文內照片署名黃暐喬、陳雙。',method:'訪談工作者與經營者，觀察店內互動與工作情境。'},
 {title:'當美被社群媒體形塑　Z世代的體態焦慮與自我追尋',slug:'social-genz-SPA',type:'interactive',topic:'數位・身體',art:'body',summary:'從社群影像與個人經驗出發，用數位敘事理解理想體態、社會比較與自我認同。',role:'數位敘事作品參與 UI／UX 設計與互動程式開發；個別細項待補充。',method:'將專題內容轉化為網頁互動，結合視覺資訊與閱讀動線。'},
 {title:'AI技術重現逝者生命　臺灣數位永生如何發展',slug:'ai-digitalimmortality-developing',type:'feature',date:'2026.05.07',topic:'科技・倫理',art:'digital',summary:'當科技讓離開的人再次出現，數位永生如何回應思念，又帶來哪些倫理與發展難題？',role:'共同署名報導；專題期間參與議題提案、報導面向規劃及實地採訪。',method:'梳理技術應用，從產業與倫理角度探討數位永生。'},
 {title:'年輕失智也失去生活：未能實現的工作權',slug:'dementia-work-YOD-convergencemedia',type:'interactive',topic:'數位・照護',art:'dementia',summary:'透過融媒體敘事，讓年輕型失智者的工作處境與生命經驗被更多讀者看見。',role:'數位敘事作品參與 UI／UX 設計與互動程式開發；個別細項待補充。',method:'以數位介面呈現專題脈絡與人物故事。'},
 {title:'浸大學生會疑因悼大火遭解散　學生嘆校園自治將亡',slug:'wongfukcourtfire-democracywall-studentsunion',type:'news',topic:'國際・校園',region:'香港',art:'campus',summary:'從學生會解散事件，關注學生悼念、校園自治與公共表達的空間。',role:'國際與生活版純淨新聞期間，負責選題、採訪、查證與稿件撰寫。',method:'國際新聞議題追蹤；具體採訪方式待補充。'},
 {title:'故宮首攜東大辦《故宮東遊記》　盼縮短台東與故宮距離',slug:'thenationalpalacemuseum-edutainment-gamebasedchallenge',type:'news',topic:'藝文・教育',region:'台東',art:'culture'},
 {title:'科普環島列車首辦市集　走入北車推科學知識生活化',slug:'sciencefair-scientificknowledge-taipeistation',type:'news',topic:'科普・生活',region:'台北',art:'train'},
 {title:'清大創首屆科技萬聖藝術節　領孩童玩樂中學科學',slug:'-halloween-technology-art',type:'news',topic:'科普・教育',region:'新竹',art:'science'},
 {title:'見書店攜大學生致敬臺灣文學　辦市集傳實體書魅力',slug:'reading-bookcave-promotion',type:'news',topic:'文學・閱讀',region:'台北',art:'culture'},
 {title:'臺師大首辦拉丁舞之夜　美食、文化交流展熱情',slug:'latinculture-salsadance-internationalexchange',type:'news',topic:'文化・交流',region:'台北',art:'culture'},
 {title:'東華族語歌唱比賽首結合市集　藉手工藝展原民之美',slug:'ndhu-indigenous-indigenouslanguagesingingcontest',type:'news',topic:'文化・族語',region:'花蓮',art:'culture'},
 {title:'川普對校新條約遭反彈　德大生疑抹滅校園言論自由',slug:'trump-utaustin-campact',type:'news',topic:'國際・校園',region:'美國',art:'campus'},
 {title:'波大反性侵聯盟辦行動週　多形式展校園對話',slug:'-sexualassault-community-weekofaction',type:'news',topic:'國際・校園',region:'美國',art:'campus'},
 {title:'美國轉折點性別用詞惹議　曼大生抗議聲援跨性別者',slug:'transgender-sports-controversy',type:'news',topic:'國際・性別',region:'英國',art:'campus'},
 {title:'康大合作軍火商引倫理爭議　學生組破鏈行動抗議',slug:'armsmanufacturers-studentprotest-uconn',type:'news',topic:'國際・倫理',region:'美國',art:'campus'},
 {title:'維大關閉學習型宿舍　學生為多元族群文化空間發聲',slug:'livinglearningcommunity-black-lgbtq',type:'news',topic:'國際・校園',region:'美國',art:'campus'},
 {title:'當美被社群媒體形塑　Z世代的體態焦慮與自我追尋',slug:'social-genz-socialphysiqueanxiety',type:'feature',date:'2026.06.30',topic:'社群・身體',art:'body',summary:'從不同年輕人的身體經驗，探討社群媒體、理想體態與自我認同交織的生活困境。',role:'共同署名報導；專題期間參與議題提案、報導面向規劃及實地採訪。',method:'採訪多元身體經驗，結合社群影響與相關研究。'},
 {title:'賞鳥博覽會在台首辦　展現台灣多元生態',slug:'eco-sustainable-bird',type:'news',topic:'生態・保育',art:'nature'},
 {title:'野保法修法首例　屏東黑熊案一審無罪',slug:'blackbear-indigenous-conservation',type:'news',topic:'生態・社會',region:'屏東',art:'nature'}
];
const experiences = [
 {date:'2026.09 — 至今',org:'政大大學報',position:'採訪中心主任・生活版',current:true,text:'負責生活版新聞稿件審閱與編輯，協助記者調整報導切角、內容架構及新聞標題，確保稿件品質與新聞價值。'},
 {date:'2025.09 — 2026.06',org:'政大大學報',position:'採訪中心記者・國際與生活版、專題',text:'獨立完成 12 篇純淨新聞（國際與生活版各 6 篇），負責選題、採訪、查證與寫稿；參與 4 篇專題與 2 件數位敘事，負責專題提案、報導規劃及實地採訪，以及 UI／UX 設計與互動程式開發。'},
 {date:'2025.04 — 2026.06',org:'三立新聞台',position:'編輯台工讀生',text:'協助新聞 RO 帶、Sound On 影音剪輯與《54分局》串帶，整理中央氣象署相關新聞素材；監看午間新聞，彙整各台新聞與重大時事。'},
 {date:'2025.07 — 2025.08',org:'三立財經台',position:'採訪中心實習生',text:'支援記者會現場、遞麥與街頭訪問，協助兼顧播報工作的記者採訪；練習撰寫 SOT 新聞稿，熟悉電視新聞採訪及製稿流程。'},
 {date:'2024.08',org:'電通貝立德・電通娛樂',position:'實習生',text:'協助提案資料整理與簡報流程，獨立完成部門月報、季報，支援現場藝人接待，熟悉媒體代理操作流程。'}
];
const skillGroups = [
 {title:'新聞採訪與編輯',text:'人物訪談・新聞寫作・專題報導・SOT 稿件・查證研究・審稿與標題・電視新聞監看'},
 {title:'網頁與互動製作',text:'HTML / CSS / JavaScript · Figma · p5.js · Max/MSP · Blender'},
 {title:'影像與視覺設計',text:'Lightroom Classic · Photoshop · Illustrator · InDesign · Premiere Pro · EDIUS'},
 {title:'資料處理與視覺化',text:'Gephi 網絡分析與視覺化'}
];
