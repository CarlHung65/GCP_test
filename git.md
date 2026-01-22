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
        git add path/to/file
        ```

4. 建立提交（commit）
```
git commit -m "你的訊息（例如：update README）"
```

5. 推到 GitHub（push）
```
git push
```
