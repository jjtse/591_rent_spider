# 591_rent_spider
因591反爬蟲安全機制，無法直接以搜尋API進行爬蟲，需盡可能地去模擬人類操作網頁
先進入首頁取得token，再帶著取得的token至搜尋的url進行爬蟲

## CSRF( Cross Site Request Forgery )跨站請求偽造
陌生人在你不知情的情況下把有你桌號的菜單送給了老闆，所以跨過了本該知情的你（送出的人不同，所以送出 Request 的 Domain ) 也會不同），
CSRF 的本質在於 web server 無條件信任 cookie 而沒有再確認或以其他方式驗證（等於老闆問也不問無條件相信菜單上的桌號，也不看是誰送的），
因此只能保證這個Request 發自某個 User ，卻不能保證請求本身是 User 自願發出的（ 等於菜單上的桌號是你的，但不代表這個菜是你點的 ）。
