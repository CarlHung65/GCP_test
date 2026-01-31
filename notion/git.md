1. new repo need clone to self disk
git clone <your repo url>

2. 看目前改了哪些檔案

```
git status
```

3. 把變更加入暫存區（add）
   
    1. 全部加入

        ```bash
        git add .
        ```

    2. 只加某個檔案

        ```bash
        git add <file_name>
        ```

4. 建立提交（commit）
```
git commit -m "你的訊息（例如：update README）"
```

5. 推到 GitHub（push）
```
git push
```


6. 檔案操作-更改檔名(如果直接在本機直接改檔名會造成多一個檔案)
```
git mv <舊檔名.ext> <新檔名.ext>
```

7. 檔案操作-刪除檔案
```
git rm <檔名.ext>
```