# 專案名稱：婚禮投影片彈幕

透過line official account擷取使用者傳送的訊息，實時在婚禮會場投放的影片上展現彈幕效果 

## 網站連結
[彈幕DEMO網站](https://danmuku.mingbuff.online/)
<iframe width="560" height="315" src="https://www.youtube.com/embed/qHINz0kgIq0?si=NS023XREi0I1sMwG" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## 另外說明
1. **影片內容**：婚禮影片涉及個人隱私，故將我本人錄製的影片當作範例。
2. **新設置網站**：架設AWS EC2主機，並將網站部署於上，同個主機也架設另一個專案。
3. **網站架設**：使用Flask框架，並使用Socketio套件實現即時彈幕效果。
4. **資料庫**：使用MongoDB儲存使用者傳送的訊息。


